"""Configuration file parser."""

from functools import cache, partial

from configlib import load_config


__all__ = ["get_config"]


get_config = partial(cache(load_config), "tenant2tenant.conf")
