"""Render Mermaid diagrams with bundled Pele browser assets."""

import html
import json
from pathlib import Path

import yaml
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import ConfigError, ExtensionError
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

__version__ = "0.1.0"

logger = logging.getLogger(__name__)
_ASSETS = Path(__file__).parent / "extension" / "cdn"
_BOOL_OPTIONS = {"responsive", "autoDirection", "links", "images"}
_NUMBER_OPTIONS = {"fontSize", "maxWidth", "directionBreakpoint", "now", "padding", "limit", "outputLimit", "maxEdges"}
_STRING_OPTIONS = {"fontFamily", "fontFamilyMono", "idPrefix", "linkRel"}
_OPTIONS = _BOOL_OPTIONS | _NUMBER_OPTIONS | _STRING_OPTIONS | {"linkSchemes", "imageSchemes", "config", "zoom"}


def _mapping(value):
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError("expected a mapping with string keys")
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError("configuration must contain finite JSON-compatible values") from exc
    return value


def _yaml_mapping(value):
    try:
        return _mapping(yaml.safe_load(value))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc


def _options(value):
    value = _mapping(value)
    for key, item in value.items():
        if key not in _OPTIONS:
            raise ValueError(f"unknown Pele option: {key}")
        if key in _BOOL_OPTIONS and not isinstance(item, bool):
            raise ValueError(f"{key} must be a boolean")
        if key in _NUMBER_OPTIONS and (isinstance(item, bool) or not isinstance(item, (int, float))):
            raise ValueError(f"{key} must be a number")
        if key in _STRING_OPTIONS and not isinstance(item, str):
            raise ValueError(f"{key} must be a string")
        if key in {"linkSchemes", "imageSchemes"} and (not isinstance(item, list) or not all(isinstance(s, str) for s in item)):
            raise ValueError(f"{key} must be a list of strings")
        if key == "config":
            _mapping(item)
        if key == "zoom" and not (isinstance(item, (bool, dict)) or item == "auto"):
            raise ValueError("zoom must be a boolean, 'auto', or a mapping")
    return value


def _css_variables(value):
    value = _mapping(value)
    if not all(key.startswith("--pele-") and isinstance(item, str) for key, item in value.items()):
        raise ValueError("CSS variables must map --pele-* names to strings")
    return value


def _merge(base, override):
    result = dict(base)
    for key, value in override.items():
        result[key] = _merge(result[key], value) if isinstance(result.get(key), dict) and isinstance(value, dict) else value
    return result


def _frontmatter(source):
    lines = source.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    for index, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return _yaml_mapping("\n".join(lines[1:index]) or "{}")
    raise ValueError("unterminated Mermaid frontmatter")


def _zoom(value):
    if not value:
        return True
    try:
        return _options({"zoom": yaml.safe_load(value)})["zoom"]
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid zoom configuration: {exc}") from exc


class MermaidDirective(SphinxDirective):
    has_content = True
    optional_arguments = 1
    option_spec = {  # noqa: RUF012 - Docutils defines directive options on the class.
        "name": directives.unchanged,
        "class": directives.class_option,
        "alt": directives.unchanged,
        "align": lambda value: directives.choice(value, ("left", "center", "right")),
        "caption": directives.unchanged,
        "width": directives.length_or_percentage_or_unitless,
        "height": directives.length_or_unitless,
        "zoom": _zoom,
        "options": lambda value: _options(_yaml_mapping(value)),
        "config": _yaml_mapping,
        "title": directives.unchanged,
    }

    def run(self):
        if self.arguments and self.content:
            raise self.error("mermaid accepts either a filename or inline content, not both")
        if self.arguments:
            if not self.state.document.settings.file_insertion_enabled:
                raise self.error("file insertion is disabled")
            relative, filename = self.env.relfn2path(self.arguments[0])
            self.env.note_dependency(relative)
            try:
                source = Path(filename).read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                raise self.error(f"cannot read Mermaid file {relative}: {exc}") from exc
        else:
            source = "\n".join(self.content)
        if not source.strip():
            raise self.error("mermaid requires diagram content")

        node = nodes.literal_block(source, source, language="mermaid")
        self.set_source_info(node)
        node["classes"] += self.options.get("class", [])
        node["pele_options"] = self.options.get("options", {})
        for key in ("zoom", "config"):
            if key in self.options:
                node["pele_options"] = _merge(node["pele_options"], {key: self.options[key]})
        for key in ("alt", "align", "width", "height", "title"):
            if key in self.options:
                node[key] = self.options[key]

        result = node
        if "caption" in self.options:
            children, messages = self.parse_inline(self.options["caption"])
            result = nodes.figure("", node, nodes.caption("", "", *children), *messages)
            if "align" in self.options:
                result["align"] = self.options["align"]
            self.set_source_info(result)
        self.add_name(result)
        return [result]


def _render_diagrams(app, doctree, docname):
    for node in list(doctree.findall(nodes.literal_block)):
        if node.get("language") not in {"mermaid", "pele"}:
            continue
        source = node.astext()
        try:
            frontmatter = _frontmatter(source)
            local = dict(_mapping(frontmatter.get("pele", {})))
            css = _merge(app.config.pele_css_variables, _css_variables(local.pop("cssVariables", {})))
            options = _merge(app.config.pele_options, _options(local))
            options = _merge(options, node.get("pele_options", {}))
        except ValueError as exc:
            logger.warning("invalid Pele configuration: %s", exc, location=node, type="pele", subtype="config")
            node["language"] = "text"
            continue

        if app.builder.format != "html":
            node["language"] = "text"
            continue

        attrs = {
            "class": " ".join(["sphinx-pele", *node["classes"], *([f"align-{node['align']}"] if "align" in node else [])]),
            "data-pele-options": json.dumps(options, allow_nan=False),
            "data-pele-css": json.dumps(css),
        }
        if node["ids"]:
            attrs["id"] = node["ids"][0]
        for key in ("width", "height", "title"):
            if key in node:
                attrs[f"data-pele-{key}"] = node[key]
        if "alt" in node:
            attrs["aria-label"] = node["alt"]
            attrs["role"] = "group"
        attributes = " ".join(f'{key}="{html.escape(value, quote=True)}"' for key, value in attrs.items())
        markup = f"<div {attributes}><pre>{html.escape(source)}</pre></div>"
        node.replace_self(nodes.raw("", markup, format="html"))


def _validate_config(app, config):
    try:
        _options(config.pele_options)
        _css_variables(config.pele_css_variables)
    except ValueError as exc:
        raise ConfigError(f"invalid Pele configuration: {exc}") from exc
    if "sphinxcontrib.mermaid" in config.extensions:
        raise ConfigError("use sphinx_pele instead of sphinxcontrib.mermaid; both register the mermaid directive")


def _add_assets(app):
    if app.builder.format != "html":
        return
    if not all((_ASSETS / name).is_file() for name in ("sphinx-pele.js", "sphinx-pele.css")):
        raise ExtensionError("Pele assets are missing; run 'pnpm --dir js install' and 'pnpm --dir js build' before building docs")
    app.config.html_static_path = [*app.config.html_static_path, str(_ASSETS)]
    app.add_js_file("sphinx-pele.js", loading_method="defer")
    app.add_css_file("sphinx-pele.css")


def setup(app: Sphinx):
    app.add_config_value("pele_options", {}, "env", types=[dict])
    app.add_config_value("pele_css_variables", {}, "env", types=[dict])
    app.add_directive("mermaid", MermaidDirective)
    app.add_directive("pele", MermaidDirective)
    app.connect("doctree-resolved", _render_diagrams)
    app.connect("config-inited", _validate_config)
    app.connect("builder-inited", _add_assets)
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
