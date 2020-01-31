"""Authenticated and authorized HIS services."""

from flask import request

from his import CUSTOMER, authenticated, authorized, Application
from notificationlib import get_wsgi_funcs
from previewlib import preview, DeploymentPreviewToken
from wsgilib import JSON, XML

from tenant2tenant.dom import tenant2tenant
from tenant2tenant.messages import MESSAGE_TOGGLED
from tenant2tenant.messages import MESSAGE_PATCHED
from tenant2tenant.messages import MESSAGE_DELETED
from tenant2tenant.messages import NO_SUCH_MESSAGE
from tenant2tenant.messages import NO_SUCH_CONFIGURATION
from tenant2tenant.messages import CONFIGURATION_SET
from tenant2tenant.orm import Configuration, TenantMessage, NotificationEmail


__all__ = ['APPLICATION']


APPLICATION = Application('Tenant-to-tenant', debug=True)
ALLOWED_PATCH_FIELDS = ('startDate', 'endDate', 'released', 'message')
SKIPPED_PATCH_FIELDS = set(
    key for key, *_ in TenantMessage.get_json_fields()
    if key not in ALLOWED_PATCH_FIELDS)


def _get_messages(customer, released):
    """Yields the customer's tenant-to-tenant messages."""

    expression = TenantMessage.customer == customer

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
        CUSTOMER.id, _get_released())])


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


@authenticated
@authorized('tenant2tenant')
def get_config():
    """Returns the configuration of the respective customer."""
    try:
        configuration = Configuration.get(
            Configuration.customer == CUSTOMER.id)
    except Configuration.DoesNotExist:
        return NO_SUCH_CONFIGURATION

    return JSON(configuration.to_json())


@authenticated
@authorized('tenant2tenant')
def set_config():
    """Sets the configuration for the respective customer."""
    try:
        configuration = Configuration.get(
            Configuration.customer == CUSTOMER.id)
    except Configuration.DoesNotExist:
        configuration = Configuration.from_json(request.json)
        configuration.customer = CUSTOMER.id
        configuration.save()
    else:
        configuration.patch_json(request.json)
        configuration.save()

    return CONFIGURATION_SET


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('tenant2tenant', NotificationEmail)


@preview(DeploymentPreviewToken)
def preview_deployment(deployment):
    """Returns a preview of the respective tenant-to-tenant messages."""

    xml = tenant2tenant()

    for message in TenantMessage.for_deployment(deployment):
        xml.message.append(message.to_dom())

    return XML(xml)


APPLICATION.add_routes((
    ('GET', '/message', list_messages),
    ('GET', '/message/<int:ident>', get_message),
    ('PUT', '/message/<int:ident>', toggle_message),
    ('PATCH', '/message/<int:ident>', patch_message),
    ('DELETE', '/message/<int:ident>', delete_message),
    ('GET', '/configuration', get_config),
    ('POST', '/configuration', set_config),
    ('GET', '/email', GET_EMAILS),
    ('POST', '/email', SET_EMAILS),
    ('GET', '/preview', preview_deployment)
))
