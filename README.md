# sphinx-pele

Pele mermaid diagrams for Sphinx

[![Build Status](https://github.com/python-project-templates/sphinx-pele/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/sphinx-pele/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/python-project-templates/sphinx-pele/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/sphinx-pele)
[![License](https://img.shields.io/github/license/python-project-templates/sphinx-pele)](https://github.com/python-project-templates/sphinx-pele)
[![PyPI](https://img.shields.io/pypi/v/sphinx-pele.svg)](https://pypi.python.org/pypi/sphinx-pele)

## Usage

Install and enable the extension:

```sh
pip install sphinx-pele
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

See [usage](docs/src/usage.md), [configuration](docs/src/configuration.md), and
[examples](docs/src/examples.md). HTML uses bundled Pele assets. Other builders
retain Mermaid source.

-> [!NOTE]
-> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
