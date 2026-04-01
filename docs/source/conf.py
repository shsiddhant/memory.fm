# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Paths ---------------------------------------------------------------

import os
import sys
from memoryfm._version import __version__

srcpath = os.path.abspath("../../src")
sys.path.insert(0, srcpath)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "memory.fm"
copyright = "2025, Siddhant Sharma"
author = "Siddhant Sharma"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.autosummary",
    "sphinx_design",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_sqlalchemy",
]


# Napoleon settings to support Numpy style
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_ivar = True  # This helps attributes look like "Variables"

templates_path = ["_templates"]
exclude_patterns = []

autodoc_typehints = "description"
autosummary_generate = True
# autodoc_typehints_format = "short"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/shsiddhant/memory.fm",
            "icon": "fa-brands fa-github",
        },
        #        {
        #            "name": "GitLab",
        #            "url": "https://gitlab.com/sharmasiddhant/memory.fm",
        #            "icon": "fa-brands fa-gitlab",
        #        },
    ],
    "show_toc_level": 1,
    "navbar_align": "left",
    "collapse_navigation": True,
    "show_nav_level": 3,
    "navbar_center": ["navbar-nav"],
}
html_sidebars = {"index.rst": []}
