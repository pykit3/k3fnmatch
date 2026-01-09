# TODO: Future Enhancements for k3fnmatch

## Performance Optimizations
- [ ] Cache compiled regex patterns for repeated translate() calls
- [ ] Add LRU cache decorator for translate()
- [ ] Benchmark against pathlib.Path.match() and glob

## Feature Additions
- [ ] Batch matching: `fnmatch_batch(paths, pattern)` for filtering lists
- [ ] Pattern validation: `validate_pattern(pattern)` to check syntax before use
- [ ] Pattern simplification: `simplify_pattern(pattern)` to reduce redundant wildcards
- [ ] Case-insensitive matching option
- [ ] Support for brace expansion: `{a,b,c}` patterns
- [ ] Inverse matching: patterns that exclude paths

## API Enhancements
- [ ] `fnmap_batch()`: Transform multiple paths in one call
- [ ] `pattern_coverage()`: Determine if one pattern covers another
- [ ] `extract_segments()`: Return matched segments as dict/list
- [ ] Support for named capture groups in patterns
- [ ] Custom separator support (not just `/`)

## Testing & Quality
- [ ] Add property-based testing with hypothesis
- [ ] Benchmark suite comparing with fnmatch, pathlib, glob
- [ ] Fuzzing for pattern parsing edge cases
- [ ] Test against real-world path datasets
- [ ] Cross-platform path handling (Windows vs Unix)

## Documentation
- [ ] Add cookbook with common use cases
- [ ] Migration guide from fnmatch/glob
- [ ] Performance comparison documentation
- [ ] Video tutorial or interactive examples

## Compatibility
- [ ] Windows path separator (`\`) handling
- [ ] Integration with pathlib.Path objects
- [ ] Support for Path-like objects as input
- [ ] Compatibility mode for standard fnmatch behavior

## Error Handling
- [ ] Better error messages for invalid patterns
- [ ] Suggestions for common pattern mistakes
- [ ] Warning for patterns that may not work as expected
- [ ] Strict mode that raises on ambiguous patterns

## Developer Experience
- [ ] Type stubs for better IDE support
- [ ] VS Code extension for pattern syntax highlighting
- [ ] Online pattern tester tool
- [ ] Integration with pytest for test file discovery

## Low Priority
- [ ] Regex optimization: minimize capture groups when not needed
- [ ] Pattern AST representation for programmatic manipulation
- [ ] Integration with file watching libraries
- [ ] Support for .gitignore-style patterns
