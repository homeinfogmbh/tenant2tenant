"""WSGI Messages."""

from his import HIS_MESSAGE_FACILITY

__all__ = [
    'NO_SUCH_MESSAGE',
    'MESSAGE_TOGGLED',
    'MESSAGE_PATCHED',
    'MESSAGE_DELETED',
    'EMAILS_UPDATED']


TT_DOMAIN = HIS_MESSAGE_FACILITY.domain('tenant2tenant')
TT_MESSAGE = TT_DOMAIN.message
NO_SUCH_MESSAGE = TT_MESSAGE(
    'The requested message does not exist.', status=404)
MESSAGE_TOGGLED = TT_MESSAGE('The message has been toggled.', status=200)
MESSAGE_PATCHED = TT_MESSAGE('The message has been updated.', status=200)
MESSAGE_DELETED = TT_MESSAGE('The message has been deleted.', status=200)
EMAILS_UPDATED = TT_MESSAGE('The emails list has been updated.', status=200)
