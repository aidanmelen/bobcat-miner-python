from __future__ import annotations
from typing import List
from bs4 import BeautifulSoup

try:
    from base import BobcatBase
except:
    from .base import BobcatBase
try:
    from errors import *
except:
    from .errors import *
try:
    from constants import *
except:
    from .constants import *

import aiohttp
import asyncio
import backoff
import ipaddress
import requests
import socket
import time


class BobcatConnection(BobcatBase):
    """A class for Bobcat Connection."""

    def __init__(
        self,
        hostname: str = None,
        animal: str = None,
        networks: List[str] = ["192.168.0.0/24", "10.0.0.0/24"],
        logger: str = None,
    ) -> None:
        super().__init__(logger)

        self.miner_data = {}  # initialize because we need it to validate the bobcat.

        # normalize Helium animal name format (e.g. Fancy Awesome Bobcat)
        # to the Bobcat animal name format (e.g. fancy-awesome-bobcat)
        normalized_animal = (
            str(animal).strip().strip("'").strip('"').lower().replace(" ", "-") if animal else None
        )

        if hostname:
            self.hostname = asyncio.run(self.is_a_bobcat(hostname, normalized_animal))
        else:
            self.hostname = self.search(networks, normalized_animal)

    def can_connect(self, port=80, timeout=3) -> bool:
        """Verify network connectivity.

        Args:
            port (int, optional): The socket port. Defaults to port 80.
            timeout (int, optional): The socket timeout. Defaults to 3 minutes.
        """
        try:
            socket.setdefaulttimeout(timeout)  # minutes
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.hostname, port))
        except OSError as err:
            result = False
        else:
            result = True
        finally:
            s.close()
            return result

    async def is_a_bobcat(self, host, animal=None, search_mode=False) -> (bool, str):
        """Connect to the host and check that it is a Bobcat and or matches the specified animal name.

        Args:
            host (str): The host to check.
            animal (str, optional): The animal name to check if connected to a bobcat. Defaults to None
            search_mode (bool, optional): Running is search mode e.g. return False instead of raising BobcatConnectionError. Defaults to False
        """

        # The host is not the bobcat if we cannot connect
        html = None
        try:
            timeout = aiohttp.ClientTimeout(sock_connect=1, sock_read=5)

            async with aiohttp.ClientSession(timeout=timeout) as session:

                async with session.get(f"http://{host}/") as response:

                    html = await response.text()

        except Exception as err:
            if search_mode:
                return False
            else:
                raise BobcatConnectionError(f"Cannot connect to {host}: {err}")

        soup = BeautifulSoup(html, "html.parser")

        # The host is not a bobcat if it does not have a bobcat diagnoser page
        if "Diagnoser - Bobcatminer Diagnostic Dashboard" in soup.title:
            self.logger.debug(f"Connected to Bobcat: {host}")
        else:
            if search_mode:
                return False
            else:
                raise BobcatConnectionError(f"Connected to the ({host}) but it is not a Bobcat")

        # The host is not the bobcat if the animal name does not match
        if animal:

            try:
                self.logger.debug("Refresh: Miner Data")
                self.miner_data = self.__get("http://" + host + "/miner.json").json()
                bobcat_animal = self.miner_data.get("animal")
            except Exception as err:
                self.logger.exception(err)
                bobcat_animal = None
            finally:
                if animal != bobcat_animal:
                    if search_mode:
                        return False
                    else:
                        raise BobcatConnectionError(
                            f"Connected to the ({bobcat_animal}) bobcat on host ({host}) but we are looking for ({animal})"
                        )

        # This is the bobcat we are looking for ✨ 🍰 ✨
        return host

    def search(self, networks=["192.168.0.0/24", "10.0.0.0/24"], animal=None) -> (str, None):
        """Search for the Bobcat in a network. In the case of multiple bobcats, the first occurrence will be return, and that may nondeterministic.

        All hosts in the network will be searched concurrently. Each host will be checked for HTTP connection, followed by a bobcat diagnoser check, and an animal name check if specified.

        Args:
            network (list, optional): A network to search in CIDR notation. Defaults to ["192.168.0.0/24", "10.0.0.0/24"]
            animal (str, optional): The animal name of the bobcat to search for. The search will only return the bobcat that matches the animal name. Defaults to None
        """

        # https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp

        self.logger.debug(
            f"Searching for {'(' + animal + ')' if animal else 'a bobcat'} in these networks: {', '.join(networks)}"
        )

        async def __search(host, animal) -> (str, None):
            """Create concurrent futures for is_a_bobcat and process them as they complete. Return when the bobcat is found and do not wait for other futures to complete."""

            # create concurrent future tasks for "is_a_bobcat()"
            tasks = [
                asyncio.ensure_future(self.is_a_bobcat(host, animal=animal, search_mode=True))
                for host in host
            ]

            # process tasks as they complete for truthy host
            for task in asyncio.as_completed(tasks):
                host = await task
                if host:
                    # end the search now that we found the host
                    return host
            else:
                return None

        for network in networks:
            # get list of hosts in the network
            hosts = [str(host) for host in ipaddress.ip_network(network, strict=False).hosts()]

            # search for bobcat in hosts
            if result := asyncio.run(__search(hosts, animal)):
                return result

        else:
            raise BobcatConnectionError(
                f"Unable to find {'the (' + animal + ')' if animal else 'and connect to a'} bobcat in these networks: {', '.join(networks)}"
            )

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=FIVE_MINUTES,
    )
    def __get(self, url: str) -> str:
        """Make GET request for a URL. The request will exponentially backoff on connection errors and timeouts. The backoff timeout is 5 minutes."""
        return requests.get(url)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=FIVE_MINUTES,
    )
    def __post(self, url: str) -> str:
        """Make POST request for a URL. The request will exponentially backoff on connection errors and timeouts. The backoff timeout is 5 minutes."""
        return requests.post(url, headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
