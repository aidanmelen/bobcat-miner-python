class BobcatSearchNetworkError(Exception):
    """Error thrown when the bobcat network does not appear to be an IPv4 or IPv6 network."""

    pass


class BobcatNotFoundError(Exception):
    """Error thrown when unable to find a bobcat in the local networks."""

    pass


class BobcatVerificationError(Exception):
    """Error thrown when bobcat verification fails."""

    pass


class BobcatConnectionError(Exception):
    """Error thrown when unable to connect to bobcat."""

    pass
