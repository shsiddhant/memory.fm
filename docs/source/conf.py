# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Paths ---------------------------------------------------------------

import os
import sys
srcpath = os.path.abspath('../../src')
sys.path.insert(0, srcpath)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from memoryfm import __version__
project = 'memory.fm'
copyright = '2025, Siddhant Sharma'
author = 'Siddhant Sharma'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.autosummary',
    'sphinx_design',
    'numpydoc',
]


templates_path = ['_templates']
exclude_patterns = []

autodoc_typehints = "none"
autosummary_generate = True

# -- numpydoc ---

# numpydoc_attributes_as_param_list = False
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
html_css_files = [
    "css/custom.css",
]
html_theme_options = {
    "external_links": [
        {
            "url": "https://pandas.pydata.org/",
            "name": "pandas",
        },
    ],
    "icon_links": [
        {
            "name": "GitLab",
            "url": "https://gitlab.com/sharmasiddhant/memory.fm",
            "icon": "fa-brands fa-gitlab",
        },
    ],
    "show_toc_level": 1,
    "navbar_align": "left",
    "collapse_navigation": True,
    "show_nav_level": 2,
    "navbar_center": ["navbar-nav"],
}
html_sidebars = {
    "index.rst": []
}
