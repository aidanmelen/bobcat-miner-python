from __future__ import annotations
from typing import Tuple

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
            if not asyncio.run(self.verify(self._hostname))[0]:
                raise BobcatVerificationError(
                    f"The bobcat ({self._hostname}) was either not a bobcat or did not match the bobcat animal."
                )
        else:
            self._hostname = self.find()

    def __refresh_miner(self, hostname=None) -> BobcatConnection:
        """Refresh Bobcat miner data.
        Args:
            hostname (str): The hostname to refresh miner data. This will override the class variable for hostname.
        Returns:
            (BobcatConnection): The instance of the BobcatConnection.
        """

        _hostname = hostname if hostname else self._hostname

        self._miner_data = self.__get("http://" + _hostname + "/miner.json").json()

        if self._trace:
            self._logger.debug(
                "Refresh: Miner Data",
                extra={"description": f"{json.dumps(self._miner_data, indent=4)}"},
            )
        else:
            self._logger.debug("Refresh: Miner Data")

        if self._miner_data == {"message": "rate limit exceeded"}:
            time.sleep(30)
            self.__refresh_miner(hostname=_hostname)
        return self

    async def _get_homepage(self, host) -> str:
        """Get the home page for the host.
        Args:
            host (str): The host to check.
        Returns:
            (str): The homepage content for the host.
        """
        try:
            timeout = aiohttp.ClientTimeout(sock_connect=1, sock_read=5)

            async with aiohttp.ClientSession(timeout=timeout) as session:

                async with session.get(f"http://{host}/") as response:

                    return await response.text()

        except Exception as err:
            return None

    def _does_bobcat_match_animal(self, host) -> bool:
        """The host is not the bobcat if the animal name does not match.
        Args:
            host (str): The host to check.
        Returns:
            (bool): Whether or not the bobcat animal matches the search animal.
        """
        self.__refresh_miner(hostname=host)

        bobcat_animal = self._miner_data.get("animal").lower()

        # e.g. normalize "Fancy Awesome Bobcat" to "fancy-awesome-bobcat"
        normalized_animal = (
            str(self._animal).strip().strip("'").strip('"').replace(" ", "-").lower()
        )

        if not (does_bobcat_match_animal := normalized_animal == bobcat_animal):
            self._logger.debug(
                f"Connected to the bobcat ({bobcat_animal}) on host ({host}) but we are looking for bobcat ({normalized_animal})"
            )

        return does_bobcat_match_animal

    async def verify(self, host) -> Tuple[bool, str]:
        """Verify the host is a Bobcat.
        Args:
            host (str): The host to check.
        Returns:
            (Tuple[bool, str]): A tuple containing the verification result and the hostname that was tested.
        """
        is_bobcat_verified = False

        homepage = str(await self._get_homepage(host))

        if (
            has_bobcat_diagnostic_dashboard := "Diagnoser - Bobcatminer Diagnostic Dashboard"
            in homepage
        ):

            self._logger.debug(f"Connected to Bobcat: {host}")

            does_bobcat_match_animal = (
                self._does_bobcat_match_animal(host) if self._animal else True
            )

            is_bobcat_verified = has_bobcat_diagnostic_dashboard and does_bobcat_match_animal

        return is_bobcat_verified, host

    async def _search(self, hosts) -> (str, None):
        """Concurrently search hosts in network and return the host for the first verified bobcat found.
        Args:
            hosts (List[str]): The hosts to search.
        Returns:
            (str, None): The IP address for the host when found otherwise None.
        """

        tasks = [asyncio.ensure_future(self.verify(host)) for host in hosts]

        for task in asyncio.as_completed(tasks):

            is_bobcat_verified, host = await task

            if is_bobcat_verified:
                return host
        else:
            return None

    def find(self) -> str:
        """Find a Bobcat on the local network.
        Returns:
            (str): The hostname for the bobcat found in the local network.
        Raises:
            A BobcatNotFoundError is raised when a bobcat is not found in local networks.
        """

        self._logger.debug(
            f"Searching for {'(' + self._animal + ')' if self._animal else 'a bobcat'} in these networks: {', '.join(self._networks)}"
        )

        for network in self._networks:
            try:
                hosts = [str(host) for host in ipaddress.ip_network(network, strict=False).hosts()]
            except ValueError as err:
                raise BobcatSearchNetworkError(str(err))

            if host := asyncio.run(self._search(hosts)):
                self._logger.debug(f"Found to bobcat: {host}")
                return host

        else:
            raise BobcatNotFoundError(
                f"Unable to find the bobcat{' (' + self._animal + ')' if self._animal else ''} in these networks: {', '.join(self._networks)}"
            )

    def can_connect(self, port=80, timeout=3) -> bool:
        """Verify network connectivity.
        Args:
            port (int, optional): The socket port. Defaults to port 80.
            timeout (int, optional): The socket timeout. Defaults to 3 minutes.
        """
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._hostname, port))
        except OSError as err:
            result = False
        else:
            result = True
        finally:
            s.close()
            return result

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
