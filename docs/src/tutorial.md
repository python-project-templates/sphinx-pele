# Build your first diagram

This tutorial builds a small Sphinx site with a publishing flowchart, then adds
a caption and zoom controls. You need Python 3.11 or newer, `pip`, Git, Node.js
22+, and pnpm 11.11.0. This tutorial installs the development version from the
repository.

## Create a project

In an empty working directory, create a virtual environment and install the
extension:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install "sphinx-pele @ git+https://github.com/python-project-templates/sphinx-pele.git@main"
mkdir docs
```

On Windows, use `.venv\Scripts\activate` to activate the environment.

Create `docs/conf.py`:

```python
project = "Publishing guide"
extensions = ["sphinx_pele"]
root_doc = "index"
```

Create `docs/index.rst`:

```rst
Publishing guide
================

.. mermaid::

   flowchart LR
       Draft --> Review --> Published
```

## Build and view it

Run:

```sh
python -m sphinx -W -b html docs docs/_build/html
python -m http.server 8000 --directory docs/_build/html
```

Open `http://localhost:8000/`. The page should show three nodes labeled Draft,
Review, and Published, joined from left to right on a wide screen. Keep the server
running while you edit; use a second terminal for the next build.

## Add a caption and controls

Replace the directive in `docs/index.rst` with:

```rst
.. mermaid::
   :caption: Publishing flow
   :name: publishing-flow
   :alt: A draft is reviewed before publication.
   :zoom: true

   flowchart LR
       Draft --> Review --> Published

See :ref:`publishing-flow`.
```

Build again, then reload the browser:

```sh
python -m sphinx -W -b html docs docs/_build/html
```

The diagram now has a caption, a link to the figure, and zoom buttons. Click the
zoom-in button, then reset the view. Resize the browser to see the diagram adapt
to the page width.

## Change the font size

Add this line to `docs/conf.py`:

```python
pele_options = {"fontSize": 20}
```

Rebuild and reload once more. Diagram labels should be larger; the caption keeps
the Sphinx theme's text style.

Your site now contains a rendered diagram with a caption and reader controls.
Continue with [Markdown and file-based diagrams](usage.md), or copy a different
diagram from the [gallery](examples.md).
