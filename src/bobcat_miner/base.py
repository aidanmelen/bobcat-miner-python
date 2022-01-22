class BobcatBase:
    """A base class for Bobcat. This ensures the logger is available to all sub classes."""

    def __init__(self, logger: str = None) -> None:
        self.logger = logger
