"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from his.messages.request import INVALID_CONTENT_TYPE
from notificationlib import get_wsgi_funcs
from previewlib import preview, DeploymentPreviewToken
from wsgilib import ACCEPT, JSON, XML

from tenant2tenant.dom import tenant2tenant     # pylint: disable=E0401,E0611
from tenant2tenant.messages import MESSAGE_TOGGLED
from tenant2tenant.messages import MESSAGE_PATCHED
from tenant2tenant.messages import MESSAGE_DELETED
from tenant2tenant.messages import NO_SUCH_MESSAGE
from tenant2tenant.orm import TenantMessage, NotificationEmail

__all__ = ['APPLICATION']


APPLICATION = Application('Tenant-to-tenant', debug=True)
ALLOWED_PATCH_FIELDS = ('startDate', 'endDate', 'released', 'message')
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
        raise NO_SUCH_MESSAGE


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
def toggle_message(ident):
    """Toggles the respective message."""

    message = _get_message(ident)
    message.released = not message.released
    message.save()
    return MESSAGE_TOGGLED.update(released=message.released)


@authenticated
@authorized('tenant2tenant')
def patch_message(ident):
    """Toggles the respective message."""

    message = _get_message(ident)
    message.patch_json(request.json, skip=SKIPPED_PATCH_FIELDS)
    message.save()
    return MESSAGE_PATCHED


@authenticated
@authorized('tenant2tenant')
def delete_message(ident):
    """Deletes the respective message."""

    message = _get_message(ident)
    message.delete_instance()
    return MESSAGE_DELETED


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('tenant2tenant', NotificationEmail)


@preview(DeploymentPreviewToken)
def deployment_preview(deployment):
    """Returns the tenant-to-tenant preview
    messages for the requested deployment.
    """

    messages = TenantMessage.for_deployment(deployment)

    if  'application/xml' in ACCEPT or '*/*' in ACCEPT:
        xml = tenant2tenant()

        for message in messages:
            xml.message.append(message.to_dom())

        return XML(xml)

    if 'application/json' in ACCEPT:
        return JSON([message.to_json() for message in messages])

    return INVALID_CONTENT_TYPE


APPLICATION.add_routes((
    ('GET', '/message', list_messages, 'list_messages'),
    ('GET', '/message/<int:ident>', get_message, 'get_message'),
    ('PUT', '/message/<int:ident>', toggle_message, 'toggle_message'),
    ('PATCH', '/message/<int:ident>', patch_message, 'patch_message'),
    ('DELETE', '/message/<int:ident>', delete_message, 'delete_message'),
    ('GET', '/email', GET_EMAILS, 'get_emails'),
    ('POST', '/email', SET_EMAILS, 'set_emails'),
    ('GET', '/preview/deployment', deployment_preview)
))
