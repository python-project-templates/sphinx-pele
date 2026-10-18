# Diagram examples

Each example shows its Mermaid source and rendered output. The source listing
and diagram read the same file, so the text is directly reusable in a `mermaid`
fence or directive. These examples exercise the bundled Pele renderer; they do
not imply support for every Mermaid option.

For Sphinx authoring patterns, see [reStructuredText examples](rst-examples.rst)
and [how to add diagrams](usage.md). Styling recipes are in
[how to style diagrams](styling.md).

## Flowchart with frontmatter

Diagram frontmatter supplies a title, layout settings, font size, and a CSS variable.

```{literalinclude} examples/publishing.mmd
:language: text
```

```{mermaid} examples/publishing.mmd
```

## Sequence diagram

A caption, named reference, accessible label, width, and zoom controls are attached by the Sphinx directive.

```{literalinclude} examples/sequence.mmd
:language: text
```

```{mermaid} examples/sequence.mmd
:name: request-flow
:caption: A **request** and response.
:alt: Client requests a page from the server.
:zoom: true
:width: 75%
```

## External file

The same UTF-8 file supplies the source listing and diagram. Sphinx tracks it as a build dependency.

```{literalinclude} publishing.mmd
:language: text
```

```{mermaid} publishing.mmd
:caption: Loaded from a Mermaid document.
```

## Pie chart

A chart with two labeled slices.

```{literalinclude} examples/pie.mmd
:language: text
```

```{mermaid} examples/pie.mmd
```

## Class diagram

Classes, members, and a composition relationship.

```{literalinclude} examples/classes.mmd
:language: text
```

```{mermaid} examples/classes.mmd
```

## Entity relationship diagram

A documentation collection with pages and embedded diagrams.

```{literalinclude} examples/entities.mmd
:language: text
```

```{mermaid} examples/entities.mmd
```

## State diagram

Transitions through a review cycle, including a return to the draft state.

```{literalinclude} examples/states.mmd
:language: text
```

```{mermaid} examples/states.mmd
```

## Gantt chart

Fixed dates and a disabled today marker keep this example stable across builds.

```{literalinclude} examples/gantt.mmd
:language: text
```

```{mermaid} examples/gantt.mmd
```

## User journey

Scores describe how a reader experiences each part of a documentation task.

```{literalinclude} examples/journey.mmd
:language: text
```

```{mermaid} examples/journey.mmd
```

## Git graph

A documentation branch merged back into main.

```{literalinclude} examples/git-history.mmd
:language: text
```

```{mermaid} examples/git-history.mmd
```

## Mind map

A hierarchy of documentation topics.

```{literalinclude} examples/mindmap.mmd
:language: text
```

```{mermaid} examples/mindmap.mmd
```

## Timeline

Milestones grouped by month.

```{literalinclude} examples/timeline.mmd
:language: text
```

```{mermaid} examples/timeline.mmd
```

## Quadrant chart

Work items positioned by effort and reader impact.

```{literalinclude} examples/quadrants.mmd
:language: text
```

```{mermaid} examples/quadrants.mmd
```

## Sankey diagram

Values represent reader traffic between documentation sections.

```{literalinclude} examples/sankey.mmd
:language: text
```

```{mermaid} examples/sankey.mmd
```

## XY chart

Bars show completed examples over four weeks.

```{literalinclude} examples/xy-chart.mmd
:language: text
```

```{mermaid} examples/xy-chart.mmd
```

## Requirement diagram

A test element verifies a rendering requirement.

```{literalinclude} examples/requirements.mmd
:language: text
```

```{mermaid} examples/requirements.mmd
```

The sequence figure can be referenced as {ref}`request-flow`.
