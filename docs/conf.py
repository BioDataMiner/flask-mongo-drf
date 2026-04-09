import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'flask-mongo-drf'
copyright = '2026, wangyunkai'
author = 'wangyunkai'
release = '1.0.0'
version = '1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_names = False
napoleon_include_special_members = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'flask': ('https://flask.palletsprojects.com', None),
    'pymongo': ('https://pymongo.readthedocs.io', None),
}
