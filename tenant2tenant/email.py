"""Emailing of new tenant-to-tenant messages."""

from emaillib import EMail, Mailer
from functoolsplus import coerce

from tenant2tenant.config import CONFIG
from tenant2tenant.orm import NotificationEmail


__all__ = ['email']


MAILER = Mailer.from_config(CONFIG['email'])


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


def email(message):
    """Sends notifications emails."""

    emails = get_emails(message)

    if emails:  # pylint: disable=W0125
        return MAILER.send(emails)

    return None
