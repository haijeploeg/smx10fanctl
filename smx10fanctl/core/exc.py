class AppError(Exception):
    """Generic errors."""
    pass

class InvalidIPMISettings(Exception):
    """IPMI settings errors."""
    pass

class UnknownZoneSpecified(Exception):
    """Unkown zone specified error."""
    pass

class NoFullFanProfileFound(Exception):
    """No full fan profile set."""
    pass

class CouldNotSetFanProfile(Exception):
    """Could not set fan profile."""
    pass