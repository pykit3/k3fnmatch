"""
Enhanced fnmatch with grouping regex and path transformation.

Provides:
- translate(): Enhanced fnmatch.translate() with grouping and ** support
- fnmap(): Transform paths using source and destination patterns

Examples:
    >>> import re
    >>> pattern = translate("**/*.md")
    >>> m = re.match(pattern, "foo/bar/doc.md")
    >>> len(m.groups()) >= 3
    True

    >>> fnmap("foo/bar.md", "**/*.md", "**/*-cn.md")
    'foo/bar-cn.md'
"""

from .pattern import (
    fnmap,
    translate,
)

__all__ = [
    "fnmap",
    "translate",
]


def __getattr__(name: str) -> str:
    # importlib.metadata takes about 20 ms to import, so it is loaded only
    # when __version__ is read
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib.metadata import version

    return version("k3fnmatch")
