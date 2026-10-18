# sphinx-pele

Render Mermaid diagrams in Sphinx with bundled Pele assets. HTML readers get
responsive SVG and optional zoom controls; other builders retain Mermaid source.

## Start with a working diagram

The tutorial takes you from an empty directory to a page with a captioned,
zoomable diagram.

```{toctree}
:maxdepth: 1
:caption: Tutorial

src/tutorial
```

## Solve an authoring task

These guides cover existing Sphinx projects, visual customization, migration,
and local checks.

```{toctree}
:maxdepth: 1
:caption: How-to guides

src/usage
src/styling
src/migration
src/troubleshooting
src/development
```

## Look up options and examples

The reference records supported settings and their precedence. The example
pages pair reusable source with output from the bundled renderer.

```{toctree}
:maxdepth: 1
:caption: Reference

src/configuration
src/examples
src/rst-examples
```

## Understand the rendering model

Learn why diagrams render in the browser and what that means for layout,
configuration, and non-HTML output.

```{toctree}
:maxdepth: 1
:caption: Explanation

src/rendering
```
