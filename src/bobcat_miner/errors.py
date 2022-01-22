class BobcatIpAddressNotValidError(Exception):
    """Error thrown when a Bobcat ip address is not valid."""

    pass


class BobcatConnectionError(Exception):
    """Error thrown when unable to connect to bobcat on port 44158 or 80"""

    pass


class BobcatIpAddressNotFoundError(Exception):
    """Error thrown when a Bobcat ip address could not be found in local network."""

    pass
