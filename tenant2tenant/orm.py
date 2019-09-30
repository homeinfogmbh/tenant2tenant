"""Tenant-to-tenant messaging ORM models."""

from datetime import datetime, date, timedelta

from peewee import BigIntegerField
from peewee import BooleanField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField

from mdb import Address, Customer
from notificationlib import get_orm_model
from peeweeplus import MySQLDatabase, JSONModel

from tenant2tenant import dom   # pylint: disable=E0611
from tenant2tenant.config import CONFIG


__all__ = ['Configuration', 'TenantMessage', 'NotificationEmail']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _Tenant2TenantModel(JSONModel):
    """Basic model for this database."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class Configuration(_Tenant2TenantModel):
    """Customer-specific configuration."""

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    auto_release = BooleanField(default=False)
    release_sec = BigIntegerField(default=432000)

    @classmethod
    def for_customer(cls, customer):
        """Returns the configuration for the respective customer."""
        try:
            return cls.get(cls.customer == customer)
        except cls.DoesNotExist:
            return cls()

    @property
    def release_time(self):
        """Returns a timedelta of the specified release time."""
        return timedelta(seconds=self.release_sec)


class TenantMessage(_Tenant2TenantModel):
    """Tenant to tenant messages."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'tenant_message'

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address')
    message = TextField()
    created = DateTimeField(default=datetime.now)
    released = BooleanField(default=False)
    start_date = DateField(null=True, default=None)
    end_date = DateField(null=True, default=None)

    @classmethod
    def add(cls, customer, address, message):
        """Creates a new entry for the respective customer and address."""
        record = cls()
        record.customer = customer
        record.address = address
        record.message = message
        return record

    @classmethod
    def from_deployment(cls, deployment, message):
        """Creates a new entry for the respective deployment."""
        return cls.add(deployment.customer, deployment.address, message)

    @classmethod
    def for_deployment(cls, deployment):
        """Yields released, active records for the respective deployment."""
        condition = cls.customer == deployment.customer
        condition &= cls.address == deployment.address
        condition &= cls.released == 1
        today = date.today()
        condition &= (cls.start_date >> None) | (cls.start_date <= today)
        condition &= (cls.end_date >> None) | (cls.end_date >= today)
        return cls.select().where(condition)

    @property
    def active(self):
        """Determines whether the message is active."""
        today = date.today()
        match_start = self.start_date is None or self.start_date <= today
        match_end = self.end_date is None or self.end_date >= today
        return match_start and match_end

    def to_json(self, address=True, **kwargs):
        """Adds the address to the dictionary."""
        json = super().to_json(**kwargs)

        if address:
            json['address'] = self.address.to_json()

        return json

    def to_dom(self):
        """Returns the tenant message as XML DOM."""
        xml = dom.TenantMessage(self.message)
        xml.created = self.created
        xml.released = self.released
        xml.startDate = self.start_date
        xml.endDate = self.end_date
        return xml


NotificationEmail = get_orm_model(_Tenant2TenantModel)
