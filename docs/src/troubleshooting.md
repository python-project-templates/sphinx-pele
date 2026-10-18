# How to troubleshoot diagrams

## A directive is unknown

Confirm `extensions` contains `"sphinx_pele"` in the `conf.py` used by your build.
Follow the [installation command](usage.md) in the same Python environment that
runs Sphinx. For
Markdown, install and enable `myst_parser` too:

```sh
python -m pip install myst-parser
python -m sphinx -W -b html docs docs/_build/html
```

## The extensions conflict

If the build says both extensions register `mermaid`, remove
`"sphinxcontrib.mermaid"` from `extensions`. Follow the
[migration guide](migration.md) to move configuration.

## Configuration produces a warning

Read the file and line number attached to `invalid Pele configuration`. Check
that `pele` is a mapping, that option names use the documented camelCase spelling,
and that values have the required types. For example, use `zoom: false` rather
than `zoom: "false"`.

Keep diagram frontmatter inside the Mermaid block. For MyST `{mermaid}`
directives, use `:options:` for renderer options; a plain `mermaid` fence is the
simplest way to preserve diagram YAML frontmatter.

Build with `-W` to make configuration warnings fail the command. Consult the
[reference](configuration.md) for accepted options.

## The page shows a diagram error

Copy the source into a small diagram and reduce it until the error disappears.
Check the diagram type declaration and the line reported by Pele. A successful
Sphinx build does not validate Mermaid syntax.

For large diagrams, review `limit`, `outputLimit`, and `maxEdges` in
`pele_options`. Raise only the limit that the error identifies, then inspect the
rendered page again.

## HTML shows source instead of SVG

Check that JavaScript is enabled. In the browser's network panel, confirm that
`_static/sphinx-pele.js` loads successfully. Deploy the complete HTML output,
including `_static`, and check your site's script policy if the asset loads but
does not execute.

If you are viewing text or LaTeX output, literal source is expected; see
[rendering and output](rendering.md).

## Assets are missing in a source checkout

Build the browser assets from the repository root:

```sh
pnpm --dir js install --frozen-lockfile
pnpm --dir js build
python -m sphinx -W -b html docs docs/_build/html
```

Node.js and pnpm are needed when building from source. An installed wheel already
contains these assets. See [local development](development.md) for the full setup.

## An external Mermaid file cannot be read

Use a UTF-8 file. Resolve relative paths from the document containing the
directive, or use a leading `/` to resolve from Sphinx's source directory. Do not
supply both a filename and inline diagram content in one directive.
