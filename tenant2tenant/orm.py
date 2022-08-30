"""Tenant-to-tenant messaging ORM models."""

from __future__ import annotations
from datetime import datetime, date, timedelta
from typing import Optional, Union

from peewee import BigIntegerField
from peewee import BooleanField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect

from hwdb import Deployment
from mdb import Address, Company, Customer
from notificationlib import get_email_orm_model
from peeweeplus import EnumField, HTMLTextField, JSONModel, MySQLDatabaseProxy

from tenant2tenant import dom
from tenant2tenant.enumerations import Visibility


__all__ = ['Configuration', 'TenantMessage', 'NotificationEmail']


DATABASE = MySQLDatabaseProxy('tenant2tenant')


class _Tenant2TenantModel(JSONModel):
    """Basic model for this database."""

    class Meta:
        database = DATABASE
        schema = database.database


class Configuration(_Tenant2TenantModel):
    """Customer-specific configuration."""

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE', lazy_load=False
    )
    auto_release = BooleanField(default=False)
    release_sec = BigIntegerField(default=432000)

    @classmethod
    def select(cls, *args, cascade: bool = False) -> ModelSelect:
        """Selects configurations."""
        if not cascade:
            return super().select(*args)

        return super().select(
            cls, Customer, Company, *args
        ).join(Customer).join(Company)

    @classmethod
    def for_customer(cls, customer: Union[Customer, int]) -> Configuration:
        """Returns the configuration for the respective customer."""
        try:
            return cls.select(cascade=True).where(
                cls.customer == customer
            ).get()
        except cls.DoesNotExist:
            return cls(customer=customer)

    @property
    def release_time(self) -> timedelta:
        """Returns a timedelta of the specified release time."""
        return timedelta(seconds=self.release_sec)


class TenantMessage(_Tenant2TenantModel):
    """Tenant to tenant messages."""

    class Meta:
        table_name = 'tenant_message'

    customer = ForeignKeyField(
        Customer, column_name='customer', lazy_load=False
    )
    address = ForeignKeyField(Address, column_name='address', lazy_load=False)
    subject = HTMLTextField(null=True)
    message = HTMLTextField()
    visibility = EnumField(Visibility, default=Visibility.TENEMENT)
    created = DateTimeField(default=datetime.now)
    # Set by customer, not by end-user.
    released = BooleanField(default=False)
    start_date = DateField(null=True, default=None)
    end_date = DateField(null=True, default=None)

    @classmethod
    def add(
            cls,
            customer: Union[Customer, int],
            address: Union[Address, int],
            message: str
    ) -> TenantMessage:
        """Creates a new entry for the respective customer and address."""
        record = cls(customer=customer, address=address, message=message)
        record.save()
        return record

    @classmethod
    def from_deployment(
            cls,
            deployment: Union[Deployment, int],
            message: str
    ) -> TenantMessage:
        """Creates a new entry for the respective deployment."""
        return cls.add(deployment.customer, deployment.address, message)

    @classmethod
    def for_deployment(
            cls,
            deployment: Union[Deployment, int],
            *,
            released: bool = True,
            active_on: Optional[date] = None
    ) -> ModelSelect:
        """Yields released, active records for the respective deployment."""
        condition = cls.customer == deployment.customer
        condition &= cls.address == deployment.address

        if released:
            condition &= cls.released == 1

        if active_on is not None:
            condition &= (
                ((cls.start_date >> None) | (cls.start_date <= active_on))
                & ((cls.end_date >> None) | (cls.end_date >= active_on))
            )

        return cls.select(cascade=True).where(condition)

    @classmethod
    def select(cls, *args, cascade: bool = False) -> ModelSelect:
        """Selects configurations."""
        if not cascade:
            return super().select(*args)

        return super().select(
            cls, Customer, Company, Address, *args
        ).join(Customer).join(Company).join_from(cls, Address)

    @property
    def active(self) -> bool:
        """Determines whether the message is active."""
        today = date.today()
        match_start = self.start_date is None or self.start_date <= today
        match_end = self.end_date is None or self.end_date >= today
        return match_start and match_end

    def to_json(self, address: bool = True, **kwargs) -> dict:
        """Adds the address to the dictionary."""
        json = super().to_json(**kwargs)

        if address:
            json['address'] = self.address.to_json()

        return json

    def to_dom(self) -> dom.TenantMessage:
        """Returns the tenant message as XML DOM."""
        xml = dom.TenantMessage(self.message)
        xml.created = self.created
        xml.released = self.released
        xml.startDate = self.start_date
        xml.endDate = self.end_date
        return xml


NotificationEmail = get_email_orm_model(_Tenant2TenantModel)
