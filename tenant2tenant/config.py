"""Configuration file parser."""

from configlib import INIParser


__all__ = ['CONFIG']


CONFIG = INIParser('/etc/tenant2tenant.conf')
