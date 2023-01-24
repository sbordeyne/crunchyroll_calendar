"""Sphinx configuration."""
project = "Crunchyroll Calendar"
author = "Dogeek <simon.bordeyne@gmail.com>"
copyright = "2023, Dogeek <simon.bordeyne@gmail.com>"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
