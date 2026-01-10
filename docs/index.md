# k3fnmatch

[![Action-CI](https://github.com/pykit3/k3fnmatch/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3fnmatch/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3fnmatch/badge/?version=stable)](https://k3fnmatch.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3fnmatch)](https://pypi.org/project/k3fnmatch)

Enhanced fnmatch with grouping regex and path transformation utilities.

k3fnmatch is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Features

- **Enhanced pattern matching**: Supports `**` for multi-segment paths
- **Grouping regex**: Captures matched segments for extraction
- **Path transformation**: Convert paths using pattern pairs
- **Drop-in enhancement**: Compatible with standard fnmatch patterns

## Installation

```bash
pip install k3fnmatch
```

## Quick Start

### Pattern Matching with translate()

Convert fnmatch patterns to regex with capture groups:

```python
import re
import k3fnmatch

# Match files in any subdirectory
pattern = k3fnmatch.translate("**/*.md")
regex = re.compile(pattern)

# Extract matched segments
match = regex.match("docs/guide/intro.md")
print(match.groups())  # ('docs/guide/', 'intro', '.md')
```

### Path Transformation with fnmap()

Transform paths using source and destination patterns:

```python
import k3fnmatch

# Convert .md to .html
result = k3fnmatch.fnmap(
    "docs/guide/intro.md",
    "**/*.md",
    "**/*.html"
)
print(result)  # "docs/guide/intro.html"

# Add suffix to filenames
result = k3fnmatch.fnmap(
    "src/module.py",
    "*/*.py",
    "*/*-backup.py"
)
print(result)  # "src/module-backup.py"
```

## Pattern Syntax

| Pattern | Meaning | Example |
|---------|---------|---------|
| `*` | Single segment (no `/`) | `*.txt` matches `file.txt` but not `dir/file.txt` |
| `**` | Multi-segment (with `/`) | `**/*.py` matches `a/b/c.py` |
| `?` | Single character | `file?.txt` matches `file1.txt` |
| `[...]` | Character class | `[abc]` matches `a`, `b`, or `c` |
| `[!...]` | Negated class | `[!0-9]` matches non-digits |

## API Reference

::: k3fnmatch.pattern

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
