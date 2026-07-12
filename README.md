# IFBA Web Accessibility Evaluation

Automated accessibility tests for the institutional portal of [IFBA](https://portal.ifba.edu.br) (Instituto Federal da Bahia), conducted as part of an undergraduate thesis in _Computing Degree_.

The tests evaluate conformance with **WCAG 2.2 AA** using two independent tools:

- [axe-core](https://github.com/dequelabs/axe-core) by Deque Labs
- [IBM Equal Access Checker](https://github.com/IBMa/equal-access)

## Platform evaluated

| Platform             | URL                          |
| -------------------- | ---------------------------- |
| Portal Institucional | <https://portal.ifba.edu.br> |

## Requirements

- [Docker](https://docs.docker.com/get-docker/)

## Running the tests

```bash
docker build -t ifba-a11y .
docker run --ipc=host -v $(pwd)/results:/app/results ifba-a11y
```

Results are saved to the `results/` directory as JSON files, organized by viewport:

```
results/
  desktop/axe.json, ibm.json
  mobile/axe.json, ibm.json
```

Each file has three parts:

- `metadata` — `timestamp`, `url`, `browser`, `browserVersion`, `viewport`, `device`, `tool`, and `toolVersion`, making the result self-documenting and independent of its directory context.
- `violations` — a normalized list of violations with a shape shared by both tools (`tool`, `ruleId`, `wcag`, `description`, `count`, `targets`, `impact`, `helpUrl`), for direct comparison and analysis.
- `raw` — the complete, untouched engine output, so no information is lost.

## Development

The evaluation logic (metadata assembly and the two normalizers) is covered by a
unit suite run with [vitest](https://vitest.dev/), and the code is linted with
type-aware [ESLint](https://eslint.org/). Both run inside Docker so no tooling is
installed on the host:

```bash
docker build -t ifba-a11y .
docker run --rm ifba-a11y npm test
docker run --rm ifba-a11y npm run lint
```

## License

[MIT](https://opensource.org/licenses/MIT)
