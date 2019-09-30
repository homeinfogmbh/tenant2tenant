"""WSGI Messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_MESSAGE',
    'MESSAGE_TOGGLED',
    'MESSAGE_PATCHED',
    'MESSAGE_DELETED',
    'NO_SUCH_CONFIGURATION',
    'CONFIGURATION_SET'
]


NO_SUCH_MESSAGE = JSONMessage(
    'The requested message does not exist.', status=404)
MESSAGE_TOGGLED = JSONMessage('The message has been toggled.', status=200)
MESSAGE_PATCHED = JSONMessage('The message has been updated.', status=200)
MESSAGE_DELETED = JSONMessage('The message has been deleted.', status=200)
NO_SUCH_CONFIGURATION = JSONMessage('No such configuration.', sltatus=404)
CONFIGURATION_SET = JSONMessage('Configuration set.', sltatus=200)
