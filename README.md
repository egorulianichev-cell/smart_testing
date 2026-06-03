# Smarter Testing Flask repro

Minimal Flask app with pytest checks that each page is accessible, wrapped in CircleCI Smarter Testing. Use this to reproduce the gospotcheck-style failure where passing tests still exit with `no test available` / `Failed rerunning 0 test atoms`.

## Layout

```
app.py                 # Flask routes: /, /about, /health
tests/                 # One pytest file per route (for parallel splitting)
.circleci/
  config.yml           # parallelism: 6, circleci run testsuite
  test-suites.yml      # max-auto-rerun, TIA, dynamic splitting
```

## Local checks

```bash
cd docs/examples/smarter-testing-flask-repro
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Validate the Smarter Testing definition (requires [CircleCI CLI](https://circleci.com/docs/local-cli/) v0.1.32694+):

```bash
circleci run testsuite "flask smarter tests" --doctor
```

## CircleCI repro

1. Copy this directory into its own GitHub repo (or push this folder as the repo root).
2. Connect the project in CircleCI.
3. Push to a **feature branch** (not `main`) so analysis defaults to `none`, matching the gospotcheck job config.
4. Watch parallel containers in the **Run smarter tests** step.

Settings mirrored from the customer job:

| Option | Value |
|--------|-------|
| `parallelism` | 6 |
| `test-impact-analysis` | true |
| `dynamic-test-splitting` | true |
| `max-auto-rerun` | 1 |
| `--analyze-tests` | `none` (feature branch) |

### What to look for

On containers where pytest passes, the step tail may still show:

```
==> Rerunning failed tests...
==> Failed rerunning 0 test atoms
Not updating test impact data, analysis not enabled
no test available
```

That output comes from `circleci run testsuite`, not from pytest. Compare with Honeycomb spans on `testsuite-subcommand` (`error.detail = "no test available"`, auto_rerun strategy).

### Tips to increase repro rate

- Keep `parallelism: 6` with only three test files so some nodes receive fewer or zero atoms after impact selection.
- Run multiple pipelines on the same feature branch so TIA has history but analysis stays disabled.
- Optionally add a failing test on one node to confirm the workflow fails for two independent reasons (real test failure + wrapper failure).

## References

- [Smarter Testing with pytest](https://circleci.com/docs/guides/test/smart-testing/)
- gospotcheck investigation: pipeline `65a45e8a-ba62-403d-9d37-0e4881b2706d`, job `run_impacted_cypress_missions`
