import html
import json
import re
from pathlib import Path

import pytest
from sphinx.errors import ConfigError
from sphinx.testing.util import SphinxTestApp

from sphinx_pele import _options


@pytest.fixture
def build(tmp_path):
    apps = []

    def run(source, *, builder="html", config=None, files=None, suffix="rst"):
        root = tmp_path / str(len(apps))
        root.mkdir()
        (root / "conf.py").write_text('extensions = ["myst_parser", "sphinx_pele"]\n', encoding="utf-8")
        (root / f"index.{suffix}").write_text(source, encoding="utf-8")
        for name, content in (files or {}).items():
            (root / name).write_text(content, encoding="utf-8")
        app = SphinxTestApp(srcdir=root, buildername=builder, confoverrides=config or {}, freshenv=True)
        apps.append(app)
        app.build()
        return app

    yield run
    for app in apps:
        app.cleanup()


def diagrams(app, page="index.html"):
    output = (app.outdir / page).read_text()
    return [json.loads(html.unescape(value)) for value in re.findall(r'data-pele-options="([^"]*)"', output)], output


def test_directive_options_caption_and_source_escaping(build):
    app = build(
        """Diagrams
========

.. mermaid::
   :name: diagram
   :caption: A **caption**
   :alt: A "quoted" label
   :class: custom
   :width: 80%
   :align: center
   :zoom: true
   :options: {fontSize: 20, config: {flowchart: {rankSpacing: 60}}}

   ---
   title: Diagram
   pele:
     fontSize: 18
     cssVariables:
       --pele-accent: '#123456'
   ---
   flowchart LR
       A["</pre><script>alert(1)</script>"] --> B

See :ref:`diagram`.
""",
        config={"pele_options": {"fontSize": 12, "config": {"flowchart": {"nodeSpacing": 30}}}},
    )
    options, output = diagrams(app)
    assert options == [{"fontSize": 20, "zoom": True, "config": {"flowchart": {"nodeSpacing": 30, "rankSpacing": 60}}}]
    assert 'id="diagram"' in output
    assert "<strong>caption</strong>" in output
    assert "custom align-center" in output
    assert 'data-pele-width="80%"' in output
    assert 'aria-label="A &quot;quoted&quot; label"' in output
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in output
    assert "<script>alert(1)</script>" not in output
    assert "--pele-accent" in output
    assert (app.outdir / "_static/sphinx-pele.js").is_file()
    assert (app.outdir / "_static/sphinx-pele.css").is_file()
    assert not app.warning.getvalue()


def test_myst_fences_and_directives(build):
    app = build(
        """# Diagrams

```mermaid
---
config:
  flowchart:
    nodeSpacing: 40
pele:
  zoom: false
---
flowchart LR
    A --> B
```

```{mermaid}
:config: {flowchart: {rankSpacing: 50}}

sequenceDiagram
    A->>B: Hello
```

```{pele}
:zoom:

pie
    "A": 1
```
""",
        suffix="md",
    )
    options, output = diagrams(app)
    assert options == [{"zoom": False}, {"config": {"flowchart": {"rankSpacing": 50}}}, {"zoom": True}]
    assert "nodeSpacing: 40" in output
    assert not app.warning.getvalue()


def test_external_file_dependency_and_incremental_build(build):
    app = build(
        """File
====

.. mermaid:: chart.mmd
""",
        files={"chart.mmd": "flowchart LR\n    A --> B\n"},
    )
    assert any(Path(path).name == "chart.mmd" for path in app.env.dependencies["index"])
    assert "A --&gt; B" in diagrams(app)[1]
    (app.srcdir / "chart.mmd").write_text("flowchart LR\n    A --> Changed\n")
    app.build()
    assert "Changed" in diagrams(app)[1]
    assert not app.warning.getvalue()


@pytest.mark.parametrize("builder,filename", [("text", "index.txt"), ("latex", "projectnamenotset.tex"), ("man", "projectnamenotset.1")])
def test_non_html_builders_keep_source(build, builder, filename):
    app = build(
        """Fallback
========

.. mermaid::

   flowchart LR
       First --> Second
""",
        builder=builder,
    )
    output = (app.outdir / filename).read_text()
    assert "flowchart LR" in output
    assert "First" in output and "Second" in output
    assert not app.warning.getvalue()


@pytest.mark.parametrize(
    "body,warning",
    [
        (".. mermaid:: missing.mmd", "cannot read Mermaid file"),
        (".. mermaid:: file.mmd\n\n   flowchart LR\n       A --> B", "either a filename or inline content"),
        (".. mermaid::", "requires diagram content"),
        (".. mermaid::\n   :options: {fontSize: nope}\n\n   flowchart LR", "fontSize must be a number"),
        (".. mermaid::\n\n   ---\n   pele: []\n   ---\n   flowchart LR", "expected a mapping"),
        (".. mermaid::\n\n   ---\n   pele: {typo: true}\n   ---\n   flowchart LR", "unknown Pele option"),
        (".. mermaid::\n\n   ---\n   pele: [\n   ---\n   flowchart LR", "invalid YAML"),
        (".. mermaid::\n\n   ---\n   pele: {}\n   flowchart LR", "unterminated"),
    ],
)
def test_invalid_input_warns(build, body, warning):
    app = build("Invalid\n=======\n\n" + body + "\n")
    assert warning in app.warning.getvalue()


@pytest.mark.parametrize(
    "options",
    [
        {"typo": True},
        {"responsive": "false"},
        {"fontFamily": 5},
        {"fontSize": True},
        {"padding": float("nan")},
        {"config": []},
        {"zoom": 12},
        {"linkSchemes": "https"},
    ],
)
def test_invalid_options(options):
    with pytest.raises(ValueError):
        _options(options)


def test_invalid_global_configuration(build):
    with pytest.raises(ConfigError, match="unknown Pele option"):
        build("Invalid\n=======\n", config={"pele_options": {"typo": 1}})
