"""WSGI Messages."""

from his import Message


class _TenantToTenantMessage(Message):
    """Abstract base message."""

    DOMAIN = 'tenant2tenant'


class NoSuchMessage(_TenantToTenantMessage):
    """Indicates that the respective message does not exist."""

    STATUS = 404


class MessageToggled(_TenantToTenantMessage):
    """Indicates that the respective message was toggled."""

    STATUS = 200


class Messagepatched(_TenantToTenantMessage):
    """Indicates that the respective message was patched."""

    STATUS = 200


class MessageDeleted(_TenantToTenantMessage):
    """Indicates that the respective message was deleted."""

    STATUS = 200
