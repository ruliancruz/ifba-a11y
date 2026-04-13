# IFBA Web Accessibility Evaluation

Automated accessibility tests for the main web platforms of [IFBA](https://portal.ifba.edu.br) (Instituto Federal da Bahia), conducted as part of an undergraduate thesis in _Computing Degree_.

The tests evaluate conformance with **WCAG 2.2 AA** using two independent tools:

- [axe-core](https://github.com/dequelabs/axe-core) by Deque Labs
- [IBM Equal Access Checker](https://github.com/IBMa/equal-access)

## Platforms evaluated

| Platform             | URL                        |
| -------------------- | -------------------------- |
| Portal Institucional | <https://portal.ifba.edu.br> |
| SUAP                 | <https://suap.ifba.edu.br>   |
| AVA                  | <https://ava.ifba.edu.br>    |

## Requirements

- [Docker](https://docs.docker.com/get-docker/)

## Running the tests

```bash
docker build -t ifba-a11y .
docker run --ipc=host -v $(pwd)/results:/app/results ifba-a11y
```

Results are saved to the `results/` directory as JSON files, organized by platform and viewport:

```
results/
  portal/
    desktop/axe.json, ibm.json
    mobile/axe.json, ibm.json
  suap/
    desktop/axe.json, ibm.json
    mobile/axe.json, ibm.json
  ava/
    desktop/axe.json, ibm.json
    mobile/axe.json, ibm.json
```

Each file includes a `metadata` object with `timestamp`, `url`, `browser`, `browserVersion`, `viewport`, `device`, `tool`, and `toolVersion`, making results self-documenting and independent of their directory context.

## Running a single platform

```bash
docker run --ipc=host -v $(pwd)/results:/app/results ifba-a11y npx playwright test portal
docker run --ipc=host -v $(pwd)/results:/app/results ifba-a11y npx playwright test suap
docker run --ipc=host -v $(pwd)/results:/app/results ifba-a11y npx playwright test ava
```

## License

[MIT](https://opensource.org/licenses/MIT)
