# IFBA Portal Accessibility Evaluation

[![CI](https://github.com/ruliancruz/ifba-a11y/actions/workflows/ci.yml/badge.svg)](https://github.com/ruliancruz/ifba-a11y/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22268515.svg)](https://doi.org/10.5281/zenodo.22268515)

A reproducible, automated evaluation of the accessibility of the institutional
portal of the **Instituto Federal de Educação, Ciência e Tecnologia da Bahia
(IFBA)**, measured against **WCAG 2.2 level AA** with two independent engines, on
a desktop and a mobile viewport.

This repository holds the code. The result data it produces is published separately
as a citable dataset, see [Dataset and provenance](#dataset-and-provenance).

The evaluation is **external**: it runs against a public URL with no privileged
access, no source code and no assertions. It collects measurements, it does not
pass or fail a build.

## What this measures

|                    |                                                                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Reference standard | WCAG 2.2, conformance level AA                                                                                                                                                       |
| Rule tags queried  | `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22a`, `wcag22aa`                                                                                                                    |
| Engines            | [axe-core](https://github.com/dequelabs/axe-core) (Deque Labs) and [IBM Equal Access Checker](https://github.com/IBMa/equal-access) (IBM), both open source and mutually independent |
| Browser            | Chromium, driven by Playwright inside Docker                                                                                                                                         |
| Viewports          | desktop 1280x720, mobile 375x667                                                                                                                                                     |
| Targets            | 8 pages of the portal, see [Targets evaluated](#targets-evaluated)                                                                                                                   |
| Output             | 34 JSON files, roughly 4 MB, one per target, viewport and engine                                                                                                                     |

Two engines are used rather than one because their rule sets overlap only
partially. Running both and reporting the intersection and the difference measures
that divergence instead of inheriting one vendor's blind spots as if they were the
limits of accessibility itself.

## Scope and limitations

These bound what any claim drawn from this repository can mean.

**Automated evaluation covers a minority of WCAG.** Both engines test what a
machine can decide from the rendered DOM. Criteria that depend on human judgment,
such as whether an alternative text is _meaningful_ or whether a heading structure
is _logical_, are either flagged for manual review or not tested at all. The
`incomplete` array in the axe output and the manual-review buckets in the IBM
report are preserved precisely so this limit is visible in the data rather than
hidden by it. A complete audit requires expert manual review and testing with real
users of assistive technology, neither of which this instrument performs.

**No assistive technology is exercised.** No screen reader, magnifier or switch
device takes part. A page can satisfy every automated rule and still be unusable.

**Anonymous, static pages only.** The suite evaluates public pages without
authentication. Authenticated areas of the portal are out of scope, though the
architecture leaves room for them, see
[Applying this to another portal](#applying-this-to-another-portal).

**The headline target is an archived capture, not the live homepage.** The portal
root redirects to an electoral-blackout notice, so the homepage cannot be measured
live in a reproducible way while that redirect stands. The headline dataset is
therefore the last Wayback Machine capture taken before the redirect began, and a
`fidelity.json` record accompanies it stating how faithfully that capture loaded.
Seven live pages are measured alongside it to confirm the toolchain operates
against the portal in service.

**A measurement is dated, not permanent.** Every number describes the portal as it
was at the timestamp recorded in the result file. The live pages are edited
continuously, so a later run will differ, and it should.

## Reproducing the study

There are two distinct things one might want to reproduce, and they do not offer the
same guarantees. **Step 4a** obtains the published dataset, which reproduces the
published tables exactly. **Step 4b** measures the portal as it is today, which does
not. **Step 5** runs the analysis, and is the same either way: the notebook reads
whatever is in `results/` and does not care where it came from.

### 0. Prerequisites

Docker and git. Nothing else, by design: no Node, no Python, no browser and no
package manager is installed on the host, so a clean machine and a working machine
run the same code.

```bash
docker --version
git --version
```

Allow roughly 3 GB of disk for the two images, and network access to
`portal.ifba.edu.br` and `web.archive.org` if you intend to collect.

### 1. Get the code

```bash
git clone https://github.com/ruliancruz/ifba-a11y
cd ifba-a11y
```

To reproduce the published dataset, check out the tag that produced it rather than
the branch tip, since the tip moves:

```bash
git checkout v1.0.0
```

### 2. Build the two images

One multi-stage `Dockerfile` defines two independent images. Collection needs Node
and a browser but no Python. Analysis needs Python but neither Node nor a browser.

```bash
docker build --target collect  -t ifba-a11y-collect  .
docker build --target analysis -t ifba-a11y-analysis .
```

The first build pulls the Playwright base image, which already carries the
browsers, and takes several minutes. Later builds are cached.

### 3. Validate the instrument before trusting it

Every number this suite reports comes from software written for this purpose, so the
software is checked before it is believed. Run the gates listed under
[Tests, coverage and quality gates](#tests-coverage-and-quality-gates). All of them
must pass before a collection or an analysis is worth reading.

### 4a. Take the published dataset

This path touches no network service beyond the download itself and depends on
nothing that can drift. Get the dataset from the DOI below, verify it, and place its
`results/` at the repository root:

```bash
# download and unzip ifba-a11y-results-<version>.zip
cd ifba-a11y-results-<version>
sha256sum -c CHECKSUMS.txt
cp -r results /path/to/ifba-a11y/
```

### 4b. Or re-run the collection against the portal

This path measures the portal as it is now. **It does not reproduce the published
dataset, and it is not expected to.** Seven of the eight targets are live pages on
a portal that is edited continuously, so their content changes independently of
this code. The archived target is stable, being a fixed capture, but the live pages
are not. Read any difference as the portal having changed, unless you have ruled
that out.

```bash
docker run --ipc=host -v "$(pwd)/results":/app/results ifba-a11y-collect
```

The run takes a few minutes. It executes serially, one worker, and paces its
requests, see [Responsible use](#responsible-use). On success `results/` holds 34
files. A partial count means some target failed after its retries, and the
Playwright report says which.

`--ipc=host` is Chromium's recommended flag under Docker and avoids crashes from a
small shared-memory segment.

### 5. Run the analysis

The notebook reads `results/` directly, so this step is identical whether that
directory came from step 4a or from step 4b.

```bash
cd /path/to/ifba-a11y
docker run --rm -v "$(pwd)":/app \
  ifba-a11y-analysis \
  jupyter nbconvert --to notebook --execute analysis/notebook.ipynb
```

The whole repository is mounted, not just `results/`, so that the executed notebook
lands on the host rather than staying inside the container. It writes
`analysis/notebook.nbconvert.ipynb`, the notebook with every table rendered.

If `results/` came from the published dataset, the dataset also ships that same
notebook already executed, under its own `analysis/` directory. Open both and
compare: the numbers should match exactly, and a discrepancy is worth reporting as an
issue. If `results/` came from a fresh collection, expect the live-page numbers to
differ and read the difference as the portal having changed.

To read the tables interactively instead, run Jupyter and open the notebook:

```bash
docker run --rm -it -p 8888:8888 -v "$(pwd)":/app \
  ifba-a11y-analysis \
  jupyter lab --ip=0.0.0.0 --no-browser --allow-root --ServerApp.root_dir=/app
```

Setting `EXPORT = True` in the notebook's configuration cell makes each table also
print a copy-ready markdown version beneath itself, for transcribing a table into
another document from a single source of truth.

### 6. Where the outputs land

| Path                                | Written by         | Contents                                                        |
| ----------------------------------- | ------------------ | --------------------------------------------------------------- |
| `results/`                          | collection         | the result files, see [Result file format](#result-file-format) |
| `reports/html/`                     | collection         | the Playwright HTML report for the run                          |
| `reports/results.json`              | collection         | the same run, machine readable                                  |
| `analysis/notebook.nbconvert.ipynb` | notebook execution | the notebook with tables rendered                               |
| `coverage/`                         | `test:coverage`    | the TypeScript coverage report                                  |

All of these are gitignored build products. Only `results/` is mounted out of the
container by the command in step 4b, so the Playwright reports stay inside the
container unless you mount `reports/` as well.

Files written from inside a container are owned by root on the host. Normalize them
from a container rather than with `sudo`:

```bash
docker run --rm -v "$(pwd)":/app -w /app ifba-a11y-analysis \
  chown -R "$(id -u):$(id -g)" results
```

## Dataset and provenance

**The result files are not in this repository.** They are published as a citable
dataset with its own DOI, under CC BY 4.0, while this code stays under MIT. The
dataset carries its own README describing the execution context of the run that
produced it.

- **Version DOI**, [10.5281/zenodo.22268515](https://doi.org/10.5281/zenodo.22268515):
  resolves to version 1.0.0. This is the one to cite.
- **Concept DOI**, [10.5281/zenodo.22268514](https://doi.org/10.5281/zenodo.22268514):
  resolves to the most recent version.

| Dataset version | Collected  | Produced by  |
| --------------- | ---------- | ------------ |
| 1.0.0           | 2026-09-04 | tag `v1.0.0` |

Each dataset version records which tag of this repository produced it, and every
individual result file repeats its own execution context in a `metadata` object.
A result file is therefore interpretable in isolation, without this repository and
without the directory it was found in.

## Targets evaluated

The collection runs a **manifest** of targets, declared once in
`collection/config.ts` and shared by the collection code and
`playwright.config.ts`.

| Directory                              | Page                                    | Role                                         |
| -------------------------------------- | --------------------------------------- | -------------------------------------------- |
| `archive`                              | archived homepage capture               | headline, reproducible dataset               |
| `live/salvador`                        | Salvador campus homepage                | live check on a template-similar homepage    |
| `live/euclides-da-cunha`               | Euclides da Cunha campus homepage       | template propagation across campus homepages |
| `live/feira-de-santana`                | Feira de Santana campus homepage        | template propagation across campus homepages |
| `live/noticia-institucional`           | an institutional news article           | news template, editorial content             |
| `live/acessoainformacao-institucional` | Acesso à Informação, institutional page | legally mandated transparency page           |
| `live/ingresso-2026`                   | Ingresso 2026 landing page              | high-traffic admissions page                 |
| `live/ingresso-2026-publicacoes`       | Ingresso 2026 publications listing      | high-traffic document listing                |

The archived homepage is the headline because the portal root redirects during the
_Defeso Eleitoral 2026_. The seven live pages serve two purposes: they confirm the
toolchain operates against the portal in service, and they establish whether a
barrier found on the homepage comes from a template reused portal-wide or from one
page's own content, which is what makes a remediation recommendation actionable.

## Result file format

```
results/
  archive/
    desktop/axe.json, ibm.json, fidelity.json
    mobile/axe.json, ibm.json, fidelity.json
  live/<page>/
    desktop/axe.json, ibm.json
    mobile/axe.json, ibm.json
```

Every `axe.json` and `ibm.json` is a **lossless superset**: it keeps what the
engine emitted and adds a normalized view on top, never in place of it.

```jsonc
{
  "metadata": {
    /* self-contained execution context */
  },
  "violations": [
    /* normalized, one shape for both engines */
  ],
  "raw": {
    /* the engine's own output */
  },
}
```

`metadata` carries `timestamp`, `url`, `browser`, `browserVersion`, `viewport`,
`device`, `tool`, `toolVersion`, and `wcagTags` for axe-core. It is assembled by a
single shared function so both engines emit an identical field set.

`violations` is the normalized array. One shape serves both engines, which is what
makes an axe-versus-IBM comparison a table lookup instead of a mess of per-engine
special cases.

| Field         | From axe-core                         | From IBM Equal Access                 |
| ------------- | ------------------------------------- | ------------------------------------- |
| `tool`        | `axe-core`                            | `ibm-equal-access`                    |
| `ruleId`      | `id`                                  | `ruleId`                              |
| `wcag`        | parsed from `tags`, `wcag143`→`1.4.3` | **empty**, see below                  |
| `description` | `description`                         | `message`                             |
| `count`       | `nodes.length`                        | occurrences grouped by `ruleId`       |
| `targets`     | CSS selectors                         | XPath expressions, from `path.dom`    |
| `impact`      | `impact`, `critical` to `minor`       | **absent**, IBM has no severity field |
| `helpUrl`     | `helpUrl`                             | `help`                                |

Two engine asymmetries are surfaced rather than papered over. **`impact` is
axe-only**, because IBM result items carry no severity. **`wcag` is empty for
IBM**, because IBM result items carry no machine-readable criterion. Mapping IBM
rule identifiers to WCAG criteria is curated research knowledge, so it lives in the
analysis package where it can be reviewed, not hardcoded into the collector where
it would silently couple every measurement to a lookup table.

IBM violations are **grouped by `ruleId`** so that both engines yield the same
per-rule shape. Axe is naturally per-rule, one object with a `nodes` array, while
IBM emits a flat per-occurrence list. Per-occurrence detail is never lost, it
remains in `raw`.

`raw` is the engine's own output, kept so that the normalized view above is auditable
and replaceable rather than load-bearing on trust: every field in `violations` can be
re-derived from it, so a reader who disagrees with a normalization choice can work
from the engine's own report instead. The analysis package does read `violations` for
almost everything, which is the point of normalizing at all, and reaches into `raw`
in exactly one place, `aggregate.py`, for IBM's `summary.counts` buckets, the pass,
manual-review and potential-violation counts that bound what automated checking was
able to decide on its own.

For IBM, `raw` is the full report. For axe it is the full result **except `passes`**,
the one deliberate omission: it was around four fifths of each file and is consumed by
nothing. Axe's `incomplete`, the checks it could not decide without a human, is kept.

`fidelity.json`, written only for archived targets, records how faithfully the
capture loaded, as `stylesheets` and `missingAssets`, under a `metadata` object
holding the same execution context as its siblings minus the engine fields, since
fidelity is a property of the page load and not of a rule engine. It is provenance
metadata, not analysis input, and the analysis loader does not read it.

## Architecture

Three layers, separating browser-bound work from pure logic so the pure logic can
be test-driven without a browser at all. The annotation in the tree below is the
point of it: `(pure)` marks a module with no browser and no I/O, unit-tested under
a coverage gate, while `(browser)` and `(fs)` mark the thin shells that are
verified by being run instead.

```
collection/
  config.ts            TARGETS manifest, WCAG tags, viewports, single source of truth
  schema.ts            the result-file contract shared by both engines
  metadata.ts          assembles the metadata object                      (pure)
  normalize/axe.ts     axe output -> the common violation shape           (pure)
  normalize/ibm.ts     IBM output -> the common violation shape           (pure)
  navigate.ts          archive and live navigation, retries and pacing    (browser)
  engines/axe.ts       runs axe-core against the loaded page              (browser)
  engines/ibm.ts       runs IBM Equal Access against the loaded page      (browser)
  collect.ts           serializes and writes result files                 (fs)
analysis/
  a11y/schema.py       dataclasses mirroring schema.ts                    (pure)
  a11y/parse.py        parse and validate a result file                   (pure)
  a11y/aggregate.py    panorama, per-rule, per-criterion, priority tables (pure)
  a11y/wcag.py         POUR principle, conformance level, IBM rule lookup (pure)
  a11y/convergence.py  axe versus IBM, by criterion and by rule pair      (pure)
  a11y/validation.py   live versus archived, by rule and by selector      (pure)
  a11y/components.py   classifies selectors into portal components        (pure)
  a11y/load.py         reads the results directory                        (fs)
  notebook.ipynb       loads, tabulates, displays
tests/
  unit/                vitest, the TypeScript pure core
  analysis/            pytest, the Python pure core
  collect.spec.ts      Playwright orchestration, the collection run itself
```

The **collection shell** drives Chromium, navigates to archived or live targets,
invokes the engines, calls the pure core and writes files. It is I/O with no
decisions in it, which is why it is verified by running the collection in Docker
rather than by unit tests, and why it sits outside the coverage gate.

The **analysis layer** repeats the same split one language over, and its pure core
holds no pandas at all. Aggregators return plain Python and the notebook wraps them
in DataFrames purely for display, for the same reason normalization lives in
TypeScript rather than in the notebook: it keeps the tested logic dependency-light
and its tests trivial.

Two choices in the analysis package are worth naming because they are research
decisions, not engineering ones. `wcag.py` owns the knowledge the result files
cannot supply: the WCAG conformance level of each criterion, which is not derivable
from its number, and the IBM rule-to-criterion lookup. An unlisted rule raises
loudly rather than emitting a blank into a reported number. `components.py` owns the
portal-DOM knowledge in the same spirit, classifying the selectors of a violation
into the components they belong to, which is what allows a shared-template barrier
to be told apart from a per-page one.

The notebook renders **tables only, by design**. Every chart it once drew restated
the table immediately above it, so matplotlib is not a dependency of this project.

Both languages share one `tests/` directory. The code carries no comments by
policy: contracts and reasoning are documented here, in this file, and the code is
written to be read without annotation.

## Tests, coverage and quality gates

Both pure cores are built **test-first** and held at **100% coverage**, enforced in
CI. The gate is scoped to the modules that carry executable logic: on the
TypeScript side `collection/metadata.ts` and `collection/normalize/**`, since
`config.ts` is a declarative manifest and `schema.ts` is type declarations, so
neither has anything to cover; on the Python side the whole `a11y` package except
`load.py`. The shells are left outside that threshold deliberately, since they are
I/O with no test-drivable logic, and are exercised by the collection run and the
notebook execution instead.

Every gate runs from the two images built in
[step 2](#2-build-the-two-images), and every one of them must pass:

```bash
docker run --rm ifba-a11y-collect npm test              # unit suite, no browser
docker run --rm ifba-a11y-collect npm run test:coverage # same, with the 100% gate
docker run --rm ifba-a11y-collect npm run lint          # type-aware ESLint
docker run --rm ifba-a11y-collect npx tsc --noEmit      # type check
docker run --rm ifba-a11y-collect npm audit --audit-level=moderate

docker run --rm ifba-a11y-analysis                      # pytest with the 100% gate
docker run --rm ifba-a11y-analysis ruff check .
docker run --rm ifba-a11y-analysis pip-audit
```

Tests are **self-contained**: each carries its own synthetic, typed input inline,
in its Arrange phase, directly above the assertion on its expected output, so a
whole transformation is readable in one place without chasing a fixture across
files. They follow **Arrange-Act-Assert** with blank-line phases and assert once,
on the full expected object, rather than field by field. Asserting the whole shape
locks the _absence_ of fields too, which is how the suite guarantees that IBM
violations never grow an `impact`.

Test inputs are **synthetic, never real portal output**. They assert the shape of
the transformation, not the portal's values, because real values drift as the
portal changes and would make the suite flaky and coupled to one scan.

`.github/workflows/ci.yml` runs two jobs on every push, both installing from the
lockfile or the pinned requirements rather than resolving afresh. The collection job
runs `npm audit`, ESLint, `tsc --noEmit` and vitest with coverage. The analysis job
runs `pip-audit`, `ruff check`, a check that the committed notebook carries no
execution output, and pytest. A lint, type, coverage or advisory failure fails the
build, and so does committing an executed notebook, which keeps the version history
free of embedded result tables. These are the same gates as the commands above, so a
green badge at the top of this file means they passed on the published commit too.
GitHub Dependabot monitors the dependency surface for newly disclosed
vulnerabilities.

## Versions and pinning

Installs are reproduced from a pinned state rather than resolved afresh. On the
Node side `package-lock.json` fixes all 291 direct and transitive packages to an
exact version with an integrity hash, and both the Docker image and CI install with
`npm ci`, which reads only the lockfile and refuses to run if the lockfile and the
manifest disagree. On the Python side there is no lockfile, so `requirements.txt`
pins every direct dependency to an exact patch with `==`.

This matters more here than in most projects: the two engines are the measuring
instrument, and a patch-level change in a rule can move a reported number. Whatever
version does end up running is recorded in the `metadata.toolVersion` of every
result file, so a measurement identifies the tool that produced it even years
later. For the IBM checker that field names the npm package. The rule set it
applied is recorded separately, in `raw.summary.ruleArchive`.

Three constraints are load-bearing and easy to break:

**The Playwright version in `package.json` must match the Docker base image tag in
`Dockerfile` exactly**, currently `1.61.1`. A mismatch produces browser executable
errors at collection time.

**The IBM rule set must be declared explicitly**, currently the `13July2026`
deployment, in `IBM_RULE_ARCHIVE` in `collection/config.ts`. The
`accessibility-checker` package does not carry its rules: it fetches the engine
from a CDN at run time, and the package default resolves to whichever deployment
IBM published most recently. The lockfile pins the package, this id pins the rules.

**Node is pinned to the version the Playwright image ships**, `24.17`, in
`package.json` `engines` and in CI, so development, CI and collection share one
runtime. Bumping Playwright is what moves it.

The analysis image pins **Python 3.14**. Unlike Node, this is chosen freely, since
the analysis image has no browser constraint, so it tracks current stable Python.

## Responsible use

The collection runs against a public service operated by a third party, so it is
built to be unobtrusive. It executes with a **single worker**, never in parallel.
It **paces** its requests to live pages and retries a refused connection a bounded
number of times with backoff, rather than hammering. It performs **no
authentication**, submits **no forms**, and writes nothing to the portal. It reads
rendered pages, exactly as any visitor's browser does.

The evaluation is an **external assessment of a public interface**. It makes no
attempt to access anything a visitor could not, and the findings it produces are
reported as measurements against a published standard, not as security
disclosures.

Anyone pointing this suite at a portal they do not operate should keep those
properties. Raising the worker count or removing the pacing turns a courteous
measurement into a load test.

## Applying this to another portal

The manifest is the only thing that binds this suite to the IFBA portal. Editing
`TARGETS` in `collection/config.ts` retargets it, and everything downstream, both
engines, both viewports, the result schema and the whole analysis package, works
unchanged.

```ts
{
  label: 'homepage',
  url: 'https://example.edu.br/',
  mode: 'live',          // or 'archive', for a Wayback capture URL
  outDir: 'results/homepage',
}
```

Two parts are portal-specific and would need review. `analysis/a11y/components.py`
classifies selectors into the components of _this_ portal's templates, so its
patterns describe the IFBA portal and not another. The IBM rule-to-criterion table
in `analysis/a11y/wcag.py` covers the rules this portal exhibits, and an unlisted
rule raises rather than emitting a blank, which is the intended behaviour: it tells
you to curate the entry instead of quietly reporting nothing.

## How to cite

Cite the **dataset** when you use the measurements, and the **software** when you
use or extend the instrument. `CITATION.cff` in this repository carries the machine
readable form, which GitHub renders as a "Cite this repository" button.

Software:

> Rulian de Jesus Cruz (2026). _ifba-a11y: accessibility evaluation suite for the
> institutional portal of the Instituto Federal de Educação, Ciência e Tecnologia
> da Bahia_ (version 1.0.0) [Computer software].
> <https://github.com/ruliancruz/ifba-a11y>

Dataset:

> Rulian de Jesus Cruz (2026). _Automated WCAG 2.2 AA accessibility evaluation of
> the institutional portal of the Instituto Federal de Educação, Ciência e
> Tecnologia da Bahia: axe-core and IBM Equal Access Checker results on desktop
> and mobile_ (version 1.0.0) [Data set]. Zenodo.
> <https://doi.org/10.5281/zenodo.22268515>

## License

The code in this repository is licensed under the [MIT License](LICENSE).

The published result dataset is licensed separately, under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as data rather than
software. One caveat on its scope: the `raw` payloads embed short fragments of the
portal's own HTML, quoted by the engines to point at each violating element. Those
fragments belong to the IFBA and are reproduced as evidence of the measurement. The
dataset licence covers the dataset as compiled, not the quoted material.
