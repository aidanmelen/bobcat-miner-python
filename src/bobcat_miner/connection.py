from multiprocessing import Pool
from functools import partial

try:
    from base import BobcatBase
except:
    from .base import BobcatBase
try:
    from errors import *
except:
    from .errors import *

import backoff
import ipaddress
import requests
import socket


class BobcatConnection(BobcatBase):
    """A class for Bobcat Connection."""

    FIVE_MINUTES = 300

    def __init__(self, ip_address: str = None, logger: str = None) -> None:
        super().__init__(logger)

        if ip_address:
            # An ip address was passed to the constructor and now we need to validate it.
            if not self.validate_ip_address(ip_address):
                raise BobcatIpAddressNotValidError(ip_address)

            if not self.can_connect(ip_address, port=44158) or not self.can_connect(
                ip_address, port=80
            ):
                raise BobcatConnectionError(ip_address)

            self.ip_address = ip_address
        else:
            # The ip address was not passes to the constructor so we need to find one and set it
            self.ip_address = self.find_bobcat_ip_address()

    def validate_ip_address(self, ip_addr: str = None) -> bool:
        """Validate ip address."""
        if not ip_addr:
            ip_addr = self.ip_address

        try:
            _ = ipaddress.ip_address(ip_addr)
            self.logger.debug(f"The ip address is valid ({ip_addr})")
            return True
        except ValueError:
            self.logger.debug(f"The ip address is invalid ({ip_addr})")
            return False

    def has_bobcat_webpage(self, ip_addr: str) -> bool:
        """Check that the ip address is running the bobcat web page."""
        try:
            r = self.__get(f"http://{ip_addr}")
            return "Diagnoser - Bobcatminer Diagnostic Dashboard" in r.text
        except requests.RequestException:
            return False

    def can_connect(
        self, ip_addr: str = None, port: int = 44158, timeout: int = 5, find_mode: bool = False
    ) -> bool:
        """Connect to the Bobcat socket (ip_addr:port)."""
        if not ip_addr:
            ip_addr = self.ip_address

        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_addr, port))
            self.logger.debug(f"Connected to ({ip_addr}:{port})")
        except OSError:
            result = False
            # do not log in 'find mode' where connect is executed 65280 times.
            if not find_mode:
                self.logger.error(f"Failed to connect ({ip_addr}:{port})")
        else:
            result = True
        finally:
            s.close()
            return result

    def find_bobcat_ip_address(
        self, first_ip_addr: str = "192.168.0.0", processes: int = 100
    ) -> str:
        """Scan the local network for the Bobcat miner ip address. If multiple Bobcats are found then the first ip address will be returned."""
        self.logger.debug(
            f"Scanning the local network for the Bobcat ip address ({first_ip_addr}/16). This could take up to 15 minutes"
        )

        cidr_24 = [str(ip_addr) for ip_addr in ipaddress.ip_network(f"{first_ip_addr}/24").hosts()]
        cidr_16 = [str(ip_addr) for ip_addr in ipaddress.ip_network(f"{first_ip_addr}/16").hosts()]

        for hosts in [
            cidr_24,  # first scan hosts in the smaller 24 CIDR.
            list(
                set(cidr_16) - set(cidr_24)
            ),  # then try the larger 16 CIDR hosts if the ip address is still not found.
        ]:
            with Pool(processes=processes) as p:

                # process connections concurrently and return ordered results
                pool_results = p.map(
                    partial(self.can_connect, port=44158, timeout=1, find_mode=True), hosts
                )

                # get the indices of the successful connections from the pool results
                success_indices = [idx for idx, result in enumerate(pool_results) if result]

                # get ip addrs for successful connections
                ip_addrs = [hosts[idx] for idx in success_indices]

                for ip_addr in ip_addrs:
                    if self.has_bobcat_webpage(ip_addr):
                        self.logger.debug(f"Found the Bobcat ip address ({ip_addr})")
                        return ip_addr
        else:
            raise BobcatIpAddressNotFoundError(
                f"Failed to find Bobcat ip address in local network ({first_ip_addr}/16)."
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
