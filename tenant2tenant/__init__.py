"""Microservice for tenant-to-tenant messages."""

from tenant2tenant.orm import TenantMessage
from tenant2tenant.wsgi import APPLICATION


__all__ = ['APPLICATION', 'TenantMessage']
