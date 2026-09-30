# user-agent-parser

A small, dependency-free Python library that extracts browser, engine, operating system, and device type from User-Agent header strings using ordered regular-expression patterns.

## Usage

```python
from user_agent_parser import parse

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
result = parse(ua)
print(result.browser)            # Chrome
print(result.browser_version)    # 120.0.0.0
print(result.engine)             # Blink
print(result.operating_system)   # Windows 10/11
print(result.device_type)        # desktop
```

The `parse` function returns a `UserAgent` dataclass with the following attributes: `browser`, `browser_version`, `engine`, `engine_version`, `operating_system`, and `device_type`. Any attribute that cannot be determined is `None`.

## Why this library exists

User-Agent strings are notoriously messy and inconsistent. This library aims to cover the most common browser, engine, OS, and device combinations using a small, maintainable set of patterns. It deliberately chooses specificity over exhaustive coverage: patterns are ordered so that more specific tokens (like `Edg/` for Edge) are matched before generic ones (`Chrome/`).

The main trade-off is that unrecognized or very old User-Agents return `None` for some or all fields. The parser is not a comprehensive database and will not attempt to guess from partial matches.

## Edge cases

- Edge's User-Agent contains both `Edg/` and `Chrome/`; the parser matches Edge first.
- The device type is determined by a separate ordered pattern list. Bot detection happens before mobile/tablet detection so that crawlers are not classified as mobile devices.
- macOS version normalization: `Mac OS X 14_2` becomes `macOS` as the OS name; the version is not stored in the dataclass because the API focuses on OS family, not patch level.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

