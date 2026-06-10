# Maintainer Plan

## Near-term priorities

1. Keep the CLI predictable and safe: dry runs, explicit confirmation, clear queues.
2. Add tested adapters for common office workflows: PDF, Word, Excel, images.
3. Collect real printer compatibility reports from Windows users.

## Good first issues

- Add a `--limit` option for test batches.
- Add saved queue presets.
- Improve printer selection on Windows with optional `pywin32` support.
- Add richer examples for school, warehouse, and office batch jobs.

## Release checklist

1. Run `python -m unittest discover -s tests -v`.
2. Run a CLI smoke test against `examples/sample-docs`.
3. Update `CHANGELOG.md`.
4. Tag with `vMAJOR.MINOR.PATCH`.
