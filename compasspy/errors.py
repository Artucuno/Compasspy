# Library Errors

class UnknownType(Exception):
    """Raised when an unknown __type is used"""
    pass


class APIError(Exception):
    """Raised when API doesn't return JSON"""
    pass


# Errors from the Compass API

class CompassInvalidArgument(Exception):
    """50F4942D7A88B78667690C1239C736E7D1330268"""  # Unsure
    pass


class CompassInvalidCredentials(Exception):
    """5A5530FF244A9D000B4221B4860BE6764BC56DD9"""  # Unsure
    pass


class UnauthorisedError(Exception):
    """
    Raised when the user is not authorised to perform the action
    B375C43CC62EFAFD95259FEED722C5DC3B4F3187
    """
    pass
