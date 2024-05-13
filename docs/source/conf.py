# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tommy'
copyright = '2024, Top models'
author = 'Top models'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "sphinx.ext.napoleon",
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

autosummary_generate = True
napoleon_include_init_with_doc = True

templates_path = ['_templates']
exclude_patterns = []

pygments_style = 'default'
myst_heading_anchors = 3  # Needed for markdown header links

# Removes, from all docs, the copyright footer.
html_show_copyright = False
html_show_sphinx = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
