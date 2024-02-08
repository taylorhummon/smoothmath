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
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = []

### HTML output

html_theme = 'alabaster'
html_static_path = ['_static']

### Autodoc

autodoc_class_signature = 'mixed'
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented_params'
autodoc_typehints_format = 'short'
autodoc_type_aliases = {'real_number': 'smoothmath.real_number'}
