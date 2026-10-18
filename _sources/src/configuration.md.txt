# Configuration reference

## Requirements

| Component        | Requirement                                                       |
| ---------------- | ----------------------------------------------------------------- |
| Python           | 3.11 or newer                                                     |
| Sphinx           | 7.4 or newer                                                      |
| MyST             | Optional, for Markdown documents                                  |
| Node.js and pnpm | Needed to build from source; not needed to use an installed wheel |

## Sphinx settings

| Setting              | Default | Meaning                                                             |
| -------------------- | ------- | ------------------------------------------------------------------- |
| `pele_options`       | `{}`    | JSON-compatible Pele mount options, using upstream camelCase names. |
| `pele_css_variables` | `{}`    | CSS custom properties with `--pele-` names and string values.       |

Pele 1.6.0 is bundled in the wheel. HTML documentation uses local JavaScript and
CSS, with no CDN or Node.js runtime requirement. Building the package from source
requires Node.js and pnpm.

(diagram-configuration)=

## Diagram configuration

The `pele` mapping in **diagram** YAML frontmatter accepts the same options as
`pele_options`, plus `cssVariables`. It is not document-level MyST frontmatter.
The source, including Mermaid `title`, `config`, and `%%{init: ...}%%` directives,
is passed to Pele unchanged.

Option precedence, lowest to highest:

1. `pele_options` in `conf.py`.
1. Diagram frontmatter's `pele` mapping.
1. Directive `:options:` mapping.
1. Directive `:zoom:` and `:config:` values.

Nested mappings merge recursively; lists and scalar values replace earlier values.
Mermaid's native frontmatter and initialization directives override defaults in
`options.config` according to Pele's parser. CSS variables merge from Sphinx
settings and diagram `pele.cssVariables`.

## Render options

The extension accepts these JSON-compatible [Pele options](https://pele.run/api):

| Options                                                  | Type                                     |
| -------------------------------------------------------- | ---------------------------------------- |
| `fontFamily`, `fontFamilyMono`, `idPrefix`, `linkRel`    | String                                   |
| `fontSize`, `maxWidth`, `directionBreakpoint`, `padding` | Number                                   |
| `now`                                                    | Numeric Unix timestamp in milliseconds   |
| `limit`, `outputLimit`, `maxEdges`                       | Number                                   |
| `responsive`, `autoDirection`, `links`, `images`         | Boolean                                  |
| `linkSchemes`, `imageSchemes`                            | List of strings                          |
| `config`                                                 | Mermaid configuration mapping            |
| `zoom`                                                   | Boolean, `auto`, or zoom options mapping |

Zoom mappings accept Pele's `always`, `maxScale`, `controls`, and `labels` options.
`labels` is a mapping with `zoomIn`, `zoomOut`, and `reset` strings. The default
`zoom: "auto"` shows controls when a diagram shrinks to fit; `true` always enables
zoom and `false` disables it. The documentation gallery explicitly disables zoom
by default and enables it on selected examples.
Pele supplies defaults for omitted values. Mounting measures the container width;
`:width:` controls the container's available width. `maxWidth` is accepted for API
compatibility but Pele's mount operation uses the measured width.

Function-valued options (`measurer`, `icons`, `sanitize`, `onRender`, `onError`)
are not serialized from Python or YAML. Diagram authors have control over the
exposed rendering options, including links, image URLs, and resource limits;
frontmatter is intended for trusted documentation sources.

Unknown option names, invalid top-level types, and non-JSON values produce build
errors for Sphinx settings or `pele.config` warnings for diagrams. `sphinx-build -W` makes warnings fail the build. Mermaid syntax errors are displayed by Pele
in the browser; they are not validated during the Sphinx build.

## Directives

`mermaid` and `pele` are aliases. Both accept inline Mermaid or one filename,
but not both. Files are UTF-8 and tracked as Sphinx build dependencies. Paths
starting with `/` are relative to Sphinx's source directory.

| Option            | Meaning                                                                                 |
| ----------------- | --------------------------------------------------------------------------------------- |
| `name`            | Sphinx reference target; targets the figure when a caption is present.                  |
| `class`           | Additional container classes.                                                           |
| `caption`         | Figure caption with inline markup.                                                      |
| `alt`             | Accessible container label.                                                             |
| `align`           | `left`, `center`, or `right`.                                                           |
| `width`, `height` | Container dimensions; unitless values mean pixels. Width accepts percentages.           |
| `title`           | Visible heading above the diagram. Native Mermaid frontmatter titles remain in the SVG. |
| `zoom`            | YAML boolean, `auto`, or mapping; an empty option enables zoom.                         |
| `options`         | YAML/JSON mapping of render options.                                                    |
| `config`          | YAML/JSON mapping of default Mermaid settings.                                          |

Ordinary `mermaid` and `pele` code blocks also render as diagrams. This includes
MyST fences, `{code-block}` directives, and reStructuredText `code-block`
directives. No MyST fence registration is needed.

## Themes and builders

The stylesheet reads Furo and PyData theme variables for diagram colors. Other
themes use light defaults. Any [Pele CSS variable](https://pele.run/theming) can
be set through `pele_css_variables`, diagram `cssVariables`, or a custom
stylesheet registered with Sphinx's `html_css_files`. CSS values may refer to
theme variables, so changing theme colors does not require rendering again.

HTML-family builders render SVG in the browser, including responsive layout and
Pele zoom controls. Without JavaScript, escaped Mermaid source remains visible.
Text, LaTeX, man, and other non-HTML builders emit source as a literal block;
PDF/image export is not implemented. Mermaid CLI options, D3 zoom, and
`sphinxcontrib.mermaid`'s class-tree generator are not supported.

## Errors

| Condition                                                   | Result                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------ |
| Invalid `pele_options` or `pele_css_variables` in `conf.py` | Sphinx configuration error.                            |
| Both Mermaid extensions enabled                             | Sphinx configuration error.                            |
| Empty directive, missing file, or invalid directive option  | Document parsing error.                                |
| Invalid diagram frontmatter or `pele` option                | `pele.config` warning; source remains a literal block. |
| Missing packaged browser assets                             | HTML builder initialization error.                     |
| Invalid Mermaid syntax or a rendering limit exceeded        | Browser error display from Pele.                       |

The extension validates the top-level types of renderer options. Nested Mermaid
settings and zoom mapping contents are passed to Pele; they do not receive a
complete schema check in Python. Date-like YAML values must be quoted when used
as strings; `now` accepts a numeric timestamp, not a YAML date.

See [troubleshooting](troubleshooting.md) for recovery steps.
