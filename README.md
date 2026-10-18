# sphinx-pele

Pele mermaid diagrams for Sphinx

[![Build Status](https://github.com/python-project-templates/sphinx-pele/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/sphinx-pele/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/python-project-templates/sphinx-pele/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/sphinx-pele)
[![License](https://img.shields.io/github/license/python-project-templates/sphinx-pele)](https://github.com/python-project-templates/sphinx-pele)
[![PyPI](https://img.shields.io/pypi/v/sphinx-pele.svg)](https://pypi.python.org/pypi/sphinx-pele)

## Usage

Install the development version from the repository, then enable the extension.
Building from source requires Git, Node.js 22+, and pnpm 11.11.0 in addition to
Python 3.11+:

```sh
python -m pip install "sphinx-pele @ git+https://github.com/python-project-templates/sphinx-pele.git@main"
```

```python
# conf.py
extensions = ["sphinx_pele"]
pele_options = {"zoom": "auto"}
```

```rst
.. mermaid::

   flowchart LR
       Mermaid --> Pele --> SVG
```

MyST Markdown `mermaid` fences and external `.mmd` files also work. Replace
`sphinxcontrib.mermaid` in `extensions` when migrating.

## Documentation

Start with the [first-diagram tutorial](docs/src/tutorial.md), or follow
[how to add diagrams](docs/src/usage.md) in an existing Sphinx project.

- [Styling and themes](docs/src/styling.md)
- [Migration from sphinxcontrib-mermaid](docs/src/migration.md)
- [Configuration reference](docs/src/configuration.md)
- [Diagram gallery](docs/src/examples.md) and [reStructuredText examples](docs/src/rst-examples.rst)
- [Troubleshooting](docs/src/troubleshooting.md)
- [Rendering and non-HTML output](docs/src/rendering.md)
- [Local development](docs/src/development.md)

Build the documentation with `python -m sphinx -W -b html docs docs/_build/html`.
See the [documentation homepage](docs/index.md) for the full navigation.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
