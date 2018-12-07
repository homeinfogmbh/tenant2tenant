"""Configuration file parser."""

from configlib import loadcfg


__all__ = ['CONFIG']


CONFIG = loadcfg('tenant2tenant.conf')
