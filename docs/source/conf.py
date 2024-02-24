# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


### Project information

project = 'smoothmath'
version = '0.0.1'
release = '0.0.1'
copyright = '2024, Taylor Hummon'
author = 'Taylor Hummon'

### General

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

### HTML output

html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 2,
}

### Autodoc

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented_params'
