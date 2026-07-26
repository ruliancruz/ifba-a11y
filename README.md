# IFBA Web Accessibility Evaluation

Automated accessibility tests for the institutional portal of [IFBA](https://portal.ifba.edu.br) (Instituto Federal da Bahia), conducted as part of an undergraduate thesis in _Computing Degree_.

The tests evaluate conformance with **WCAG 2.2 AA** using two independent tools:

- [axe-core](https://github.com/dequelabs/axe-core) by Deque Labs
- [IBM Equal Access Checker](https://github.com/IBMa/equal-access)

## Platform evaluated

The suite evaluates a manifest of two targets derived from the IFBA institutional
portal (<https://portal.ifba.edu.br>):

| Target    | Page                                    | Role                                           |
| --------- | --------------------------------------- | ---------------------------------------------- |
| `archive` | Archived homepage (Internet Archive)    | Headline, fully reproducible dataset           |
| `live`    | Salvador campus homepage (`/salvador/`) | Live external-validity check on a similar page |

The portal root currently redirects to an electoral-blackout notice, so the headline
dataset uses the last archived homepage capture taken before the redirect began. The
live Salvador campus homepage, a template-similar page that does not redirect,
confirms the toolchain still operates against the live portal.

## Requirements

- [Docker](https://docs.docker.com/get-docker/)

## Running the tests

```bash
docker build --target collect -t ifba-a11y-collect .
docker run --ipc=host -v $(pwd)/results:/app/results ifba-a11y-collect
```

Results are saved to the `results/` directory as JSON files, organized by target and viewport:

```
results/
  archive/
    desktop/axe.json, ibm.json, fidelity.json
    mobile/axe.json, ibm.json, fidelity.json
  live/
    desktop/axe.json, ibm.json
    mobile/axe.json, ibm.json
```

Archived targets also write a `fidelity.json` recording how faithfully the capture
loaded (stylesheet count and any missing assets), as a capture-provenance record.

Each `axe.json` / `ibm.json` file has three parts:

- `metadata` — `timestamp`, `url`, `browser`, `browserVersion`, `viewport`, `device`, `tool`, `toolVersion`, and `wcagTags` (axe only), making the result self-documenting and independent of its directory context.
- `violations` — a normalized list of violations with a shape shared by both tools (`tool`, `ruleId`, `wcag`, `description`, `count`, `targets`, `impact`, `helpUrl`), for direct comparison and analysis.
- `raw` — the complete, untouched engine output, so no information is lost.

## Analysis

The collected results are analyzed in a [Jupyter](https://jupyter.org/) notebook
(`analysis/notebook.ipynb`) that reads the JSON files directly and reproduces the
violation counts, per-tool tables, the WCAG criterion / principle / conformance-level
and impact breakdowns, the axe-vs-IBM convergence, the desktop-vs-mobile comparison, a
prioritized remediation ranking, and a live-validation section that cross-checks the
live Salvador campus homepage against the archived homepage. All aggregation logic
lives in a small, unit-tested Python package (`analysis/a11y/`); the notebook only
loads the data and renders tables and figures.

Build the analysis image and open the notebook:

```bash
docker build --target analysis -t ifba-a11y-analysis .
docker run --rm -it -p 8888:8888 -v $(pwd):/app \
  ifba-a11y-analysis \
  jupyter lab --ip=0.0.0.0 --no-browser --allow-root --ServerApp.root_dir=/app
```

Open the `http://127.0.0.1:8888/lab?token=…` link it prints, then open
`analysis/notebook.ipynb` and run all cells. Figures are written to
`reports/figures/`. Stop the server with `Ctrl-C`.

To regenerate the tables and figures headlessly, without opening the notebook:

```bash
docker run --rm -v $(pwd)/results:/app/results -v $(pwd)/reports:/app/reports \
  ifba-a11y-analysis jupyter nbconvert --to notebook --execute analysis/notebook.ipynb
```

## Development

The pure logic of both layers is covered by unit suites — TypeScript (metadata
assembly and the two normalizers) with [vitest](https://vitest.dev/) plus
type-aware [ESLint](https://eslint.org/), and Python (the analysis aggregation)
with [pytest](https://pytest.org/) at 100% coverage. Everything runs inside Docker,
so no tooling is installed on the host:

```bash
docker build --target collect  -t ifba-a11y-collect  .
docker build --target analysis -t ifba-a11y-analysis .

docker run --rm ifba-a11y-collect npm test
docker run --rm ifba-a11y-collect npm run lint
docker run --rm ifba-a11y-analysis
```

## License

[MIT](https://opensource.org/licenses/MIT)
