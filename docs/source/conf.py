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

project = 'memory.fm'
copyright = '2025, Siddhant Sharma'
author = 'Siddhant Sharma'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration', 'sphinx.ext.autodoc', 'sphinx.ext.coverage',
    'sphinx.ext.autosummary', 'myst_parser', 'sphinx_design', 'numpydoc'
]

myst_enable_extensions = ['colon_fence']

templates_path = ['_templates']
exclude_patterns = []

autosummary_generate = True

# numpydoc
#numpydoc_attributes_as_param_list = False
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False

# Napoleon settings
# napoleon_google_docstring = False
# napoleon_numpy_docstring = False
# napoleon_include_init_with_doc = False
# napoleon_include_private_with_doc = False
# napoleon_include_special_with_doc = False
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = False
# napoleon_use_admonition_for_references = False
# napoleon_use_ivar = True
# napoleon_use_param = True
# napoleon_use_rtype = True
# napoleon_use_keyword = True
# napoleon_custom_sections = None


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
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
    "show_nav_level": 1,
    "navbar_center": ["navbar-nav"],
}

html_sidebars = {
    "api": [
        "sidebar-nav-bs",
    ]
}
