"""Common enumerations."""

from enum import Enum


__all__ = ['Visibility']


class Visibility(Enum):
    """Visibility of tenant-to-tenant messages."""

    TENEMENT = 'tenement'
    CUSTOMER = 'customer'
