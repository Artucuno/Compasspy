# Library Errors

class UnknownType(Exception):
    """Raised when an unknown __type is used"""
    pass

# Errors from the Compass API

class CompassInvalidArgument(Exception):
    """50F4942D7A88B78667690C1239C736E7D1330268""" # Unsure
    pass

class CompassInvalidCredentials(Exception):
    """5A5530FF244A9D000B4221B4860BE6764BC56DD9""" # Unsure
    pass
