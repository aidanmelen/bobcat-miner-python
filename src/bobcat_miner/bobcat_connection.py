from bobcat_base import BobcatBase
from multiprocessing import Pool
from functools import partial

import backoff
import ipaddress
import requests
import socket


class BobcatConnection(BobcatBase):
    """A class for Bobcat Connection."""

    FIVE_MINUTES = 300

    def __init__(self, log_level: str = "INFO") -> None:
        super().__init__(log_level)

    def validate_ip_address(self, ip_addr: str) -> bool:
        """Validate ip address."""
        try:
            _ = ipaddress.ip_address(ip_addr)
            self.logger.debug(f"The ip address is valid ({ip_addr})")
            return True
        except ValueError:
            self.logger.debug(f"The ip address is invalid ({ip_addr})")
            return False

    def validate_bobcat(self, ip_addr: str) -> bool:
        """Validate the Bobcat miner."""
        try:
            r = self.get(f"http://{ip_addr}")
            return "Diagnoser - Bobcatminer Diagnostic Dashboard" in r.text
        except requests.RequestException:
            return False

    def connect(
        self, ip_addr: str, port: int = 44158, timeout: int = 5, discovery_mode: bool = False
    ) -> bool:
        """Connect to the Bobcat socket (ip_addr:port)."""
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_addr, port))
            self.logger.debug(f"Connected to the Bobcat ({ip_addr}:{port})")
        except OSError as err:
            result = False
            # do not log in discovery mode where connect is executed 65280 times.
            if not discovery_mode:
                self.logger.error(f"Failed to connect to the Bobcat ({ip_addr}:{port})")
        else:
            result = True
        finally:
            s.close()
            return result

    def discover_bobcat_ip_address(
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
                    partial(self.connect, port=44158, timeout=1, discovery_mode=True), hosts
                )

                # get the indices of the successful connections from the pool results
                success_indices = [idx for idx, result in enumerate(pool_results) if result]

                # get ip addrs for successful connections
                ip_addrs = [hosts[idx] for idx in success_indices]

                for ip_addr in ip_addrs:
                    if self.validate_bobcat(ip_addr):
                        self.logger.debug(f"Found Bobcat ip address ({ip_addr})")
                        return ip_addr
        else:
            raise BobcatIpAddressDiscoveryError(
                f"Failed to find Bobcat ip address in local network ({first_ip_addr}/16)."
            )

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=FIVE_MINUTES,
    )
    def get(self, url: str) -> str:
        """Get response payload for URL. The request will exponentially backoff on connection errors and timeouts. The backoff timeout is 5 minutes."""
        return requests.get(url)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        max_time=FIVE_MINUTES,
    )
    def post(self, url: str) -> str:
        """Requests post call wrapper with exponential backoff."""
        return requests.post(url, headers={"Authorization": "Basic Ym9iY2F0Om1pbmVy"})
