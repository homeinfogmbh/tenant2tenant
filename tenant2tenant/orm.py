"""Tenant-to-tenant messaging ORM models."""

from datetime import datetime, date

from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField

from mdb import Address, Customer
from peeweeplus import MySQLDatabase, JSONModel

from tenant2tenant import dom   # pylint: disable=E0611
from tenant2tenant.config import CONFIG


__all__ = ['TenantMessage', 'NotificationEmail']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _Tenant2TenantModel(JSONModel):
    """Basic model for this database."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


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
    def from_location(cls, location, message):
        """Creates a new entry for the respective location."""
        return cls.add(location.customer, location.address, message)

    @classmethod
    def for_location(cls, location):
        """Yields released, active records for the respective location."""
        condition = cls.customer == location.customer
        condition &= cls.address == location.address
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


class NotificationEmail(_Tenant2TenantModel):
    """Stores emails for notifications about new messages."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'notification_emails'

    customer = ForeignKeyField(Customer, column_name='customer')
    email = CharField(255)
    subject = CharField(255, null=True)
    html = BooleanField(default=False)

    @classmethod
    def from_json(cls, json, customer, **kwargs):
        """Creates a notification email for the respective customer."""
        record = super().from_json(json, **kwargs)
        record.customer = customer
        return record
