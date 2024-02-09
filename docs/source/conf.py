import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

### Project information

project = 'smoothmath'
copyright = '2024, Taylor Hummon'
author = 'Taylor Hummon'

### General

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

### HTML output

html_theme = 'alabaster'
html_static_path = ['_static']

### Autodoc

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented_params'
autodoc_type_aliases = {'RealNumber': 'smoothmath.RealNumber'}
