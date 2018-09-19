"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from wsgilib import JSON

from tenant2tenant.messages import NoSuchMessage
from tenant2tenant.messages import MessageToggled
from tenant2tenant.messages import MessagePatched
from tenant2tenant.messages import MessageDeleted
from tenant2tenant.messages import EmailAdded
from tenant2tenant.messages import NoSuchEmail
from tenant2tenant.messages import EmailDeleted
from tenant2tenant.orm import TenantMessage, NotificationEmail

__all__ = ['APPLICATION']


APPLICATION = Application('Tenant-to-tenant', cors=True, debug=True)
ALLOWED_PATCH_FIELDS = ('startDate', 'endDate', 'released')
SKIPPED_PATCH_FIELDS = set(
    key for key, *_ in TenantMessage.json_fields()
    if key not in ALLOWED_PATCH_FIELDS)


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

    return JSON([message.to_json() for message in _get_messages(
        _get_released())])


@authenticated
@authorized('tenant2tenant')
def get_message(ident):
    """Returns the respective message of the customer."""

    return JSON(_get_message(ident).to_json())


@authenticated
@authorized('tenant2tenant')
def patch_message(ident):
    """Toggles the respective message."""

    message = _get_message(ident)
    json = request.json

    if not json:
        message.released = not message.released
        message.save()
        return MessageToggled(released=message.released)

    message = message.patch(json, skip=SKIPPED_PATCH_FIELDS)
    message.save()
    return MessagePatched()


@authenticated
@authorized('tenant2tenant')
def delete_message(ident):
    """Deletes the respective message."""

    message = _get_message(ident)
    message.delete_instance()
    return MessageDeleted()


@authenticated
@authorized('tenant2tenant')
def add_email():
    """Deletes the respective message."""

    email = NotificationEmail.from_json(request.json, CUSTOMER.id)
    email.save()
    return EmailAdded(id=email.id)


@authenticated
@authorized('tenant2tenant')
def delete_email(ident):
    """Deletes the respective message."""

    try:
        email = NotificationEmail.get(NotificationEmail.id == ident)
    except NotificationEmail.DoesNotExist:
        return NoSuchEmail()

    email.delete_instance()
    return EmailDeleted()


ROUTES = (
    ('GET', '/message', list_messages, 'list_messages'),
    ('GET', '/message/<int:ident>', get_message, 'get_message'),
    ('PATCH', '/message/<int:ident>', patch_message, 'patch_message'),
    ('DELETE', '/message/<int:ident>', delete_message, 'delete_message'),
    ('POST', '/email/<int:ident>', add_email, 'add_email'),
    ('DELETE', '/email/<int:ident>', delete_email, 'delete_email'))
APPLICATION.add_routes(ROUTES)
