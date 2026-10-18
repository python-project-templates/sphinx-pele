# Rendering and output

Sphinx and Pele run at different times. That distinction explains why a page can
build successfully yet show a diagram error in the browser, and why HTML and
LaTeX contain different output.

## Sphinx preserves the source

During a build, the extension reads Mermaid directives and code blocks. It
combines the Sphinx defaults, diagram frontmatter, and directive options, then
writes escaped source and serialized configuration into the HTML page. External
Mermaid files are registered as dependencies, so editing one causes Sphinx to
rebuild the document that uses it.

The Python extension checks configuration structure and value types. It does
not parse the Mermaid grammar. A misspelled Pele option can therefore generate
a build warning, while a malformed flowchart is reported later by the renderer.

## The browser creates SVG

The wheel contains Pele's JavaScript and the extension's stylesheet. Sphinx
copies those assets into the output's `_static` directory. Once the page loads,
Pele mounts each diagram, measures its container and fonts, and produces SVG.

Rendering in the browser lets diagrams respond to the space readers have.
A narrow page can cause a different layout, and zoom lets a reader inspect a
large diagram. Fonts matter to layout because Pele measures labels before
placing nodes. Colors use CSS variables, so a theme color change can affect
existing SVG without another Sphinx build.

The renderer itself requires no CDN. A diagram containing an external image or
link can still refer to another server; bundling the renderer does not make
those resources local.

## Source remains useful without a browser

Without JavaScript, an HTML page retains a readable source listing. Text, man,
and LaTeX builders also keep the Mermaid source as a literal block. This avoids
discarding the diagram's content when there is no browser to render it.

A PDF produced through the LaTeX builder consequently contains source, not a
rendered diagram. Creating static SVG, PNG, or PDF files would require a separate
rendering step. The current extension does not provide that step.

## Configuration has two layers

Mermaid configuration describes diagram-specific settings such as flowchart
spacing. Pele options describe rendering behavior such as font size, responsive
layout, and zoom. Both can appear in one diagram's frontmatter because they
serve different purposes.

The extension merges its options before passing the original source to Pele.
Pele then applies Mermaid's native frontmatter and initialization directives.
This is why a `config` value inside Mermaid source can override a default supplied
from `conf.py`. The complete order is recorded in the
{ref}`configuration reference <diagram-configuration>`.
