"""Emailing of new tenant-to-tenant messages."""

from emaillib import EMail
from functoolsplus import coerce
from notificationlib import EMailFacility

from tenant2tenant.config import CONFIG
from tenant2tenant.orm import NotificationEmail


__all__ = ['email']


@coerce(frozenset)
def get_emails(message):
    """Yields notification emails."""

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == message.customer):
        recipient = notification_email.email
        subject = notification_email.subject or CONFIG['email']['subject']
        address = message.address
        subject = subject.format(address.street, address.house_number)
        sender = CONFIG['email']['from']
        html = message.message if notification_email.html else None
        plain = None if notification_email.html else message.message
        yield EMail(subject, sender, recipient, plain=plain, html=html)


EMAIL_FACILITY = EMailFacility(CONFIG['email'], get_emails)
email = EMAIL_FACILITY.email    # pylint: disable=C0103
