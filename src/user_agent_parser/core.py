"""Core parsing logic for User-Agent strings.

This module implements a small, dependency-free parser that extracts
browser, engine, operating system, and device type information from
User-Agent header strings.

The parser uses an ordered list of regular-expression patterns. Ordering
is deliberate: more specific or modern tokens are matched before generic
fallbacks. For example, `Edg/` is matched before `Chrome/` because Edge's
User-Agent contains both tokens.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class UserAgent:
    """Parsed components of a User-Agent string.

    Attributes:
        browser: Browser name, or None if unrecognized.
        browser_version: Version string, or None if unrecognized.
        engine: Rendering engine name, or None if unrecognized.
        engine_version: Engine version, or None if unrecognized.
        operating_system: Operating system name, or None if unrecognized.
        device_type: One of 'desktop', 'mobile', 'tablet', or 'bot', or
            None if the device type cannot be determined.
    """

    browser: str | None
    browser_version: str | None
    engine: str | None
    engine_version: str | None
    operating_system: str | None
    device_type: str | None


# Ordered patterns. Each entry is a tuple of
# (attribute_name, regex, value). The regex is matched with re.search.
# The first matching pattern in each category wins.
_BROWSER_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("browser", re.compile(r"EdgA?/(\d+[\w.]*)"), "Edge"),
    ("browser", re.compile(r"OPR/(\d+[\w.]*)"), "Opera"),
    ("browser", re.compile(r"SamsungBrowser/(\d+[\w.]*)"), "Samsung Internet"),
    ("browser", re.compile(r"(?:Chrome|CriOS)/(\d+[\w.]*)"), "Chrome"),
    ("browser", re.compile(r"Firefox/(\d+[\w.]*)"), "Firefox"),
    ("browser", re.compile(r"Version/(\d+[\w.]*).*Safari/"), "Safari"),
    ("browser", re.compile(r"Version/(\d+[\w.]*).*Mobile/"), "Safari"),
]

_ENGINE_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("engine", re.compile(r"Blink/(\d+[\w.]*)"), "Blink"),
    ("engine", re.compile(r"Gecko/(\d+[\w.]*)"), "Gecko"),
    ("engine", re.compile(r"AppleWebKit/(\d+[\w.]*)"), "WebKit"),
    ("engine", re.compile(r"Trident/(\d+[\w.]*)"), "Trident"),
]

_OS_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("operating_system", re.compile(r"Windows NT 10\.0"), "Windows 10/11"),
    ("operating_system", re.compile(r"Windows NT 6\.3"), "Windows 8.1"),
    ("operating_system", re.compile(r"Windows NT 6\.2"), "Windows 8"),
    ("operating_system", re.compile(r"Windows NT 6\.1"), "Windows 7"),
    ("operating_system", re.compile(r"Windows NT 6\.0"), "Windows Vista"),
    ("operating_system", re.compile(r"Windows NT 5\.1"), "Windows XP"),
    ("operating_system", re.compile(r"Android (\d+[\w.]*)"), "Android"),
    ("operating_system", re.compile(r"iPhone OS (\d+[\w.]*)"), "iOS"),
    ("operating_system", re.compile(r"iPad; CPU OS (\d+[\w.]*)"), "iPadOS"),
    ("operating_system", re.compile(r"Mac OS X (\d+[_\d.]*)"), "macOS"),
    ("operating_system", re.compile(r"CrOS [^\s]+"), "ChromeOS"),
    ("operating_system", re.compile(r"Linux"), "Linux"),
]

_DEVICE_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("device_type", re.compile(r"(?:Googlebot|bingbot|Baiduspider|YandexBot|DuckDuckBot|facebot)", re.IGNORECASE), "bot"),
    ("device_type", re.compile(r"iPad"), "tablet"),
    ("device_type", re.compile(r"Android.*Mobile|iPhone|Windows Phone|BlackBerry|BB10|IEMobile|Opera Mini|Mobile Safari"), "mobile"),
    ("device_type", re.compile(r"Android|Symbian|webOS"), "mobile"),
    ("device_type", re.compile(r"Windows|Macintosh|Linux|CrOS"), "desktop"),
]


def _match_patterns(
    ua_string: str, patterns: list[tuple[str, re.Pattern[str], str]]
) -> tuple[str | None, str | None]:
    """Return (value, version) for the first pattern that matches.

    The regex patterns contain exactly one capturing group for the version
    when a version is expected. Patterns without a capturing group return
    None for version.
    """
    for _, pattern, value in patterns:
        match = pattern.search(ua_string)
        if match:
            try:
                version = match.group(1)
            except IndexError:
                version = None
            return value, version
    return None, None


def parse(user_agent_string: str) -> UserAgent:
    """Parse a User-Agent string into its components.

    Args:
        user_agent_string: The raw User-Agent header value.

    Returns:
        A UserAgent dataclass instance with the extracted components.
        Any component that cannot be determined is set to None.
    """
    if not isinstance(user_agent_string, str):
        raise TypeError("user_agent_string must be a string")

    browser, browser_version = _match_patterns(user_agent_string, _BROWSER_PATTERNS)
    engine, engine_version = _match_patterns(user_agent_string, _ENGINE_PATTERNS)
    os_name, _ = _match_patterns(user_agent_string, _OS_PATTERNS)
    device_type, _ = _match_patterns(user_agent_string, _DEVICE_PATTERNS)

    return UserAgent(
        browser=browser,
        browser_version=browser_version,
        engine=engine,
        engine_version=engine_version,
        operating_system=os_name,
        device_type=device_type,
    )
