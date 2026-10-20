# Contributing

1. Fork, create a branch, make your change.
2. Run `python -m unittest discover -s tests -v`; the tests cross-check the paper's numbers.
3. If you change a reported number, update `results/data/results_summary.json` **and** note the reason in your pull request.
4. Add new simulation exports under `results/data/` and new HFSS projects under `hfss/<design>/`.
5. Open a pull request.

Please report inconsistencies in `docs/KNOWN_ISSUES.md` rather than silently changing values.
