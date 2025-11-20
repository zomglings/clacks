"""
Custom exceptions for messaging operations.
"""


class ClacksUserNotFoundError(Exception):
    """Raised when a user lookup fails."""

    pass


class ClacksChannelNotFoundError(Exception):
    """Raised when a channel lookup fails."""

    pass


class ClacksMessageNotFoundError(Exception):
    """Raised when a message with specific timestamp is not found."""

    pass
