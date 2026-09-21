"""User-Agent string parser.

Extract browser, engine, operating system, and device type from
User-Agent header strings using pattern matching.
"""

from .core import UserAgent, parse

__all__ = ["UserAgent", "parse"]
