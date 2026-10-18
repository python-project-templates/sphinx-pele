import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
extensions = ["myst_parser", "sphinx_pele"]
project = "sphinx-pele"
root_doc = "index"
exclude_patterns = ["_build", "html"]
html_theme = "alabaster"
pele_options = {"zoom": False}
