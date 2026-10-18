# How to build and check the documentation locally

Start from a repository checkout with Python 3.11+, Node.js 22+, pnpm, and `uv`
installed. Use pnpm 11.11.0 to match the CI setup used for this project.

```sh
uv venv
. .venv/bin/activate
make develop
python -m sphinx -W -b html docs docs/_build/html
python -m http.server 8000 --directory docs/_build/html
```

Open `http://localhost:8000/`. On Windows, activate the environment with
`.venv\Scripts\activate`.

## Add a gallery example

Create a UTF-8 `.mmd` file in `docs/src/examples/`. In `docs/src/examples.md`, add a
source listing and a rendering directive that both read it:

````markdown
## Review flow

```{literalinclude} examples/review.mmd
:language: text
```

```{mermaid} examples/review.mmd
```
````

Use `text` for the source listing so it remains visible as code. A source listing
with language `mermaid` would itself render as a second diagram.

Update the gallery's expected diagram count in `js/tests/index.spec.js`. The
browser checks should fail if a new example produces an error instead of SVG.

## Run the checks

```sh
make lint
make check-types
make test
python -m sphinx -W -b text docs docs/_build/text
```

`make test` runs Python integration tests and Chromium tests against built docs.
Keep port 3000 available for the browser test server. For a docs-only edit,
`make lint-docs` and `make test-js` provide the focused checks.

Rebuild the bundle with `pnpm --dir js build` after editing browser code or
updating Pele. Before changing packaging, also run `make build` and
`make check-dist`.
