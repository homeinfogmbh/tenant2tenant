"""Authenticated and authorized HIS services."""

from datetime import date
from typing import Union

from flask import request
from peewee import Select

from his import CUSTOMER, authenticated, authorized, Application
from hwdb import Deployment
from mdb import Customer
from notificationlib import get_wsgi_funcs
from previewlib import preview, DeploymentPreviewToken
from wsgilib import JSON, JSONMessage, XML

from tenant2tenant.dom import tenant2tenant
from tenant2tenant.orm import Configuration, TenantMessage, NotificationEmail


__all__ = ['APPLICATION']


APPLICATION = Application('Tenant-to-tenant', debug=True)
ALLOWED_PATCH_FIELDS = ('startDate', 'endDate', 'released', 'message')
SKIPPED_PATCH_FIELDS = set(
    key for key, *_ in TenantMessage.get_json_fields()
    if key not in ALLOWED_PATCH_FIELDS
)


def _get_messages(
        customer: Union[Customer, int],
        released: Union[bool, None]
) -> Select:
    """Yields the customer's tenant-to-tenant messages."""

    expression = TenantMessage.customer == customer

    if released is not None:
        expression &= TenantMessage.released == released

    return TenantMessage.select(cascade=True).where(expression)


def _get_released() -> Union[bool, None]:
    """Returns the released flag."""

    released = request.args.get('released')

    if released is None:
        return None

    try:
        released = int(released)
    except ValueError:
        return None

    return bool(released)


def _get_message(ident: int) -> TenantMessage:
    """Returns the respective message."""

    return TenantMessage.select(cascade=True).where(
        (TenantMessage.id == ident)
        & (TenantMessage.customer == CUSTOMER.id)
    ).get()


@APPLICATION.route('/message', methods=['GET'], strict_slashes=False)
@authenticated
@authorized('tenant2tenant')
def list_messages() -> JSON:
    """Lists the tenant-to-tenant messages."""

    return JSON([
        message.to_json() for message in _get_messages(
            CUSTOMER.id, _get_released()
        )
    ])


@APPLICATION.route(
    '/message/<int:ident>',
    methods=['GET'],
    strict_slashes=False
)
@authenticated
@authorized('tenant2tenant')
def get_message(ident: int) -> JSON:
    """Returns the respective message of the customer."""

    return JSON(_get_message(ident).to_json())


@APPLICATION.route(
    '/message/<int:ident>',
    methods=['PUT'],
    strict_slashes=False
)
@authenticated
@authorized('tenant2tenant')
def toggle_message(ident: int) -> JSONMessage:
    """Toggles the respective message."""

    message = _get_message(ident)
    message.released = not message.released
    message.save()
    return JSONMessage(
        'The message has been toggled.',
        released=message.released,
        status=200
    )


@APPLICATION.route(
    '/message/<int:ident>',
    methods=['PATCH'],
    strict_slashes=False
)
@authenticated
@authorized('tenant2tenant')
def patch_message(ident: int) -> JSONMessage:
    """Toggles the respective message."""

    message = _get_message(ident)
    message.patch_json(request.json, skip=SKIPPED_PATCH_FIELDS)
    message.save()
    return JSONMessage('The message has been updated.', status=200)


@APPLICATION.route(
    '/message/<int:ident>',
    methods=['DELETE'],
    strict_slashes=False
)
@authenticated
@authorized('tenant2tenant')
def delete_message(ident: int) -> JSONMessage:
    """Deletes the respective message."""

    message = _get_message(ident)
    message.delete_instance()
    return JSONMessage('The message has been deleted.', status=200)


@APPLICATION.route('/configuration', methods=['GET'], strict_slashes=False)
@authenticated
@authorized('tenant2tenant')
def get_config() -> Union[JSON, JSONMessage]:
    """Returns the configuration of the respective customer."""

    configuration = Configuration.select(cascade=True).where(
        Configuration.customer == CUSTOMER.id).get()
    return JSON(configuration.to_json())


@APPLICATION.route('/configuration', methods=['POST'], strict_slashes=False)
@authenticated
@authorized('tenant2tenant')
def set_config() -> JSONMessage:
    """Sets the configuration for the respective customer."""
    try:
        configuration = Configuration.select(cascade=True).where(
            Configuration.customer == CUSTOMER.id
        ).get()
    except Configuration.DoesNotExist:
        configuration = Configuration.from_json(request.json)
        configuration.customer = CUSTOMER.id
        configuration.save()
    else:
        configuration.patch_json(request.json)
        configuration.save()

    return JSONMessage('Configuration set.', sltatus=200)


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('tenant2tenant', NotificationEmail)


@APPLICATION.route('/preview', methods=['GET'], strict_slashes=False)
@preview(DeploymentPreviewToken)
def preview_deployment(deployment: Union[Deployment, int]) -> XML:
    """Returns a preview of the respective tenant-to-tenant messages."""

    xml = tenant2tenant()

    for message in TenantMessage.for_deployment(
            deployment, released=True, active_on=date.today()
    ):
        xml.message.append(message.to_dom())

    return XML(xml)


APPLICATION.add_routes([
    ('GET', '/email', GET_EMAILS),
    ('POST', '/email', SET_EMAILS)
])


@APPLICATION.errorhandler(Configuration.DoesNotExist)
def handle_missing_configuration(_: Configuration.DoesNotExist) -> JSONMessage:
    """Handles missing configuration."""

    return JSONMessage('The requested configuration does not exist.',
                       status=404)


@APPLICATION.errorhandler(TenantMessage.DoesNotExist)
def handle_missing_message(_: TenantMessage.DoesNotExist) -> JSONMessage:
    """Handles missing tenant messages."""

    return JSONMessage('The requested message does not exist.', status=404)
