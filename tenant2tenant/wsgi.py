"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from wsgilib import JSON

from damage_report.messages import NoSuchMessage, MessageToggled, \
    MessageDeleted
from digsigdb import TenantMessage

__all__ = ['APPLICATION']


APPLICATION = Application('Tenant-to-tenant', cors=True, debug=True)


def _get_messages(released=None):
    """Yields the customer's tenant-to-tenant messages."""

    expression = TenantMessage.customer == CUSTOMER.id

    if released is not None:
        expression &= TenantMessage.released == int(released)

    return TenantMessage.select().where(expression)


def _get_released():
    """Returns the released flag."""

    released = request.args.get('released')

    if released is None:
        return None

    try:
        released = int(released)
    except ValueError:
        return None

    return bool(released)


def _get_message(ident):
    """Returns the respective message."""

    try:
        return TenantMessage.get(
            (TenantMessage.id == ident)
            & (TenantMessage.customer == CUSTOMER.id))
    except TenantMessage.DoesNotExist:
        raise NoSuchMessage()


@authenticated
@authorized('tenant2tenant')
def list_messages():
    """Lists the tenant-to-tenant messages."""

    return JSON([message.to_dict() for message in _get_messages(
        _get_released())])


@authenticated
@authorized('tenant2tenant')
def get_message(ident):
    """Returns the respective message of the customer."""

    return JSON(_get_message(ident).to_dict())


@authenticated
@authorized('tenant2tenant')
def toggle_message(ident):
    """Toggles the respective message."""

    message = _get_message(ident)
    message.released = not message.released
    message.save()
    return MessageToggled(released=message.released)


@authenticated
@authorized('tenant2tenant')
def delete_message(ident):
    """Deletes the respective message."""

    message = _get_message(ident)
    message.delete_instance()
    return MessageDeleted()


ROUTES = (
    ('GET', '/', list_messages, 'list_messages'),
    ('GET', '/<int:ident>', get_message, 'get_message'),
    ('PATCH', '/<int:ident>', toggle_message, 'toggle_message'),
    ('DELETE', '/<int:ident>', delete_message, 'delete_message'))
APPLICATION.add_routes(ROUTES)
