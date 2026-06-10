# Contributing

Thanks for helping improve Batch Print Kit.

## Development setup

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
```

Please keep the core package dependency-light. If a new dependency is needed, open an issue explaining the file type or printer workflow it enables.

## Pull request checklist

- Add or update tests for behavior changes.
- Keep real printing behind an explicit confirmation path.
- Update README examples when CLI options change.
- Avoid platform-specific behavior in shared logic unless it is covered by tests.
