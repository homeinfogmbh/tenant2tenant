"""Emailing of new tenant-to-tenant messages."""

from emaillib import EMail, Mailer
from functoolsplus import coerce

from tenant2tenant.config import CONFIG
from tenant2tenant.orm import NotificationEmail


__all__ = ['email']


MAILER = Mailer.from_config(CONFIG['email'])


@coerce(frozenset)
def emails(message):
    """Yields notification emails."""

    for email in NotificationEmail.select().where(
            NotificationEmail.customer == message.customer):
        recipient = email.email
        subject = email.subject or CONFIG['email']['subject']
        address = message.address
        subject = subject.format(address.street, address.house_number)
        sender = CONFIG['email']['from']
        html = message.message if email.html else None
        plain = None if email.html else message.message
        yield EMail(subject, sender, recipient, plain=plain, html=html)


def email(message):
    """Sends notifications emails."""

    return MAILER.send(emails(message))
