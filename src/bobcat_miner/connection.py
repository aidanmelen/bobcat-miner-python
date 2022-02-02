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
import json
import requests
import socket
import time


class BobcatConnection(BobcatBase):
    """A class for Bobcat Connection."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if self._hostname:
            _ = asyncio.run(self.is_a_bobcat(self._hostname))
        else:
            self._hostname = self.find()

    def can_connect(self, port=80, timeout=3) -> bool:
        """Verify network connectivity.

        Args:
            port (int, optional): The socket port. Defaults to port 80.
            timeout (int, optional): The socket timeout. Defaults to 3 minutes.
        """
        try:
            socket.setdefaulttimeout(timeout)  # minutes
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._hostname, port))
        except OSError as err:
            result = False
        else:
            result = True
        finally:
            s.close()
            return result

    async def is_a_bobcat(self, host, search_mode=False) -> (bool, str):
        """Connect to the host and check that it is a Bobcat and or matches the specified animal name.

        Args:
            host (str): The host to check.
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

        try:
            soup = BeautifulSoup(html, "html.parser")

            # The host is not a bobcat if it does not have a bobcat diagnoser page
            if "Diagnoser - Bobcatminer Diagnostic Dashboard" in soup.title:
                self._logger.debug(f"Connected to Bobcat: {host}")

            else:
                if search_mode:
                    return False
                else:
                    raise BobcatConnectionError(f"Connected to the ({host}) but it is not a Bobcat")
        except Exception as err:
            raise BobcatConnectionError(f"Connected to the ({host}) but it is not a Bobcat")

        # The host is not the bobcat if the animal name does not match
        if self._animal:
            try:
                self._miner_data = self.__get("http://" + host + "/miner.json").json()

                if self._trace:
                    self._logger.debug(
                        "Refresh: Miner Data",
                        extra={
                            "description": f"\n```\n{json.dumps(self._miner_data, indent=4)}\n```"
                        },
                    )
                else:
                    self._logger.debug("Refresh: Miner Data")

                bobcat_animal = self._miner_data.get("animal")

            except Exception as err:
                self._logger.exception(err)
                raise BobcatConnectionError(f"Connected to the ({host}) but it is not a Bobcat")

            # normalize from Helium animal name format (e.g. Fancy Awesome Bobcat) to the Bobcat animal name format (e.g. fancy-awesome-bobcat)
            normalized_animal = (
                str(self._animal).strip().strip("'").strip('"').lower().replace(" ", "-")
                if self._animal
                else None
            )

            if normalized_animal == bobcat_animal:
                self._logger.debug(f"Verified Bobcat Animal: {self._animal}")

            else:
                if search_mode:
                    return False
                else:
                    raise BobcatConnectionError(
                        f"Connected to the ({bobcat_animal}) bobcat on host ({host}) but we are looking for ({normalized_animal})"
                    )

        # This is the bobcat we are looking for ✨ 🍰 ✨
        return host

    def find(self) -> None:
        """Find a Bobcat in a network. In the case of multiple bobcats, the first occurrence will be returned.

        All hosts in the network will be searched concurrently. Each host will be checked for HTTP connection, followed by a bobcat diagnoser check, and an animal name check if specified.
        """

        # https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp

        self._logger.debug(
            f"Searching for {'(' + self._animal + ')' if self._animal else 'a bobcat'} in these networks: {', '.join(self._networks)}"
        )

        async def __find(host) -> (str, None):
            """Create concurrent futures for is_a_bobcat and process them as they complete. Return when the bobcat is found and do not wait for other futures to complete."""

            # create concurrent future tasks for "is_a_bobcat()"
            tasks = [
                asyncio.ensure_future(self.is_a_bobcat(host, search_mode=True)) for host in host
            ]

            # process tasks as they complete for truthy host
            for task in asyncio.as_completed(tasks):
                host = await task
                if host:
                    # end the search now that we found the host
                    return host
            else:
                return None

        for network in self._networks:
            # get list of hosts in the network
            hosts = [str(host) for host in ipaddress.ip_network(network, strict=False).hosts()]

            # search for bobcat in hosts
            if hostname := asyncio.run(__find(hosts)):
                return hostname

        else:
            raise BobcatConnectionError(
                f"Unable to find {'the (' + self._animal + ')' if self._animal else 'and connect to a'} bobcat in these networks: {', '.join(self._networks)}"
            )

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=FIVE_MINUTES,
    )
    def __get(self, url: str) -> str:
        """Make GET request for a URL. The request will exponentially backoff on connection errors and timeouts. The backoff timeout is 5 minutes.
        Args:
            url (str): A URL to GET.
        """
        return requests.get(url)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=FIVE_MINUTES,
    )
    def __post(self, url: str) -> str:
        """Make POST request for a URL. The request will exponentially backoff on connection errors and timeouts. The backoff timeout is 5 minutes.
        Args:
            url (str): A URL to POST.
        """
        return requests.post(url, headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
