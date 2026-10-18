# How to migrate from sphinxcontrib-mermaid

## Replace the extension

Follow the [installation instructions](usage.md), then replace `sphinxcontrib.mermaid` with `sphinx_pele` in
`conf.py`:

```python
extensions = ["sphinx_pele"]
```

Keep any other extensions your documentation uses. For MyST Markdown, keep
`myst_parser` enabled. Do not enable both Mermaid extensions: they register the
same directive name.

## Keep the Mermaid source

Start with your existing inline and file-based directives:

```rst
.. mermaid:: diagrams/publishing.mmd
   :caption: Publishing flow
   :name: publishing-flow
```

Ordinary Markdown `mermaid` fences also work. Rebuild HTML and inspect the pages
in a browser. Pele renders the Mermaid source, but layouts and support for
individual Mermaid settings can differ.

## Move configuration

Use this table to replace settings that affect the diagrams:

| Existing setting or feature                           | Action                                                                                                      |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `mermaid_init_config`                                 | Move supported Mermaid defaults into `pele_options["config"]`.                                              |
| Mermaid light/dark theme settings                     | Set Pele CSS variables; see [styling](styling.md).                                                          |
| D3 zoom settings                                      | Use `pele_options = {"zoom": "auto"}` or directive `:zoom:`.                                                |
| Mermaid CDN version or local JS path                  | Remove it; the wheel supplies the pinned Pele bundle.                                                       |
| `mermaid_output_format`, CLI arguments, or PDF export | Keep another rendering/export workflow if you need image files. This extension renders HTML in the browser. |
| Fullscreen, icon packs, or `autoclasstree`            | Review these uses individually; there is no matching extension feature.                                     |

For example:

```python
pele_options = {
    "zoom": "auto",
    "config": {"flowchart": {"nodeSpacing": 40, "rankSpacing": 50}},
}
```

Remove obsolete `mermaid_*` and D3 settings after moving the values you need.
A successful build does not verify whether an unused setting affected the output.

## Check the output you publish

Build with warnings treated as errors:

```sh
python -m sphinx -W -b html docs docs/_build/html
```

Open pages containing each diagram type you use. Check captions, figure links,
fonts, and a narrow viewport. Browser rendering errors do not fail the Sphinx
build, so inspect the rendered diagrams as well as the build log.

If you publish LaTeX or text output, build those formats too. They contain literal
Mermaid source with this extension. See [rendering and output](rendering.md) for
the reason and [troubleshooting](troubleshooting.md) for common failures.
