"""WSGI Messages."""

from his import Message

__all__ = [
    'NoSuchMessage',
    'MessageToggled',
    'MessagePatched',
    'MessageDeleted',
    'EmailAdded',
    'NoSuchEmail',
    'EmailDeleted']


class _TenantToTenantMessage(Message):
    """Abstract base message."""

    DOMAIN = 'tenant2tenant'


class NoSuchMessage(_TenantToTenantMessage):
    """Indicates that the respective message does not exist."""

    STATUS = 404


class MessageToggled(_TenantToTenantMessage):
    """Indicates that the respective message was toggled."""

    STATUS = 200


class MessagePatched(_TenantToTenantMessage):
    """Indicates that the respective message was patched."""

    STATUS = 200


class MessageDeleted(_TenantToTenantMessage):
    """Indicates that the respective message was deleted."""

    STATUS = 200


class EmailAdded(_TenantToTenantMessage):
    """Indicates that the email was added."""

    STATUS = 200


class NoSuchEmail(_TenantToTenantMessage):
    """Indicates that the respective message does not exist."""

    STATUS = 404


class EmailDeleted(_TenantToTenantMessage):
    """Indicates that the respective email was deleted."""

    STATUS = 200
