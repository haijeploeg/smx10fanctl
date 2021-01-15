class AppError(Exception):
    """Generic errors."""
    pass

class InvalidIPMISettings(Exception):
    """IPMI settings errors."""
    pass

class UnknownZoneSpecified(Exception):
    """Unkown zone specified error."""
    pass