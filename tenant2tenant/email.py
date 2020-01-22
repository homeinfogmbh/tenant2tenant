"""Emailing of new tenant-to-tenant messages."""

from emaillib import EMail
from functoolsplus import coerce
from notificationlib import get_email_func

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
        subject = subject.format(address=message.address)
        sender = CONFIG['email']['from']
        html = message.message if notification_email.html else None
        plain = None if notification_email.html else message.message
        yield EMail(subject, sender, recipient, plain=plain, html=html)


email = get_email_func(get_emails)  # pylint: disable=C0103
