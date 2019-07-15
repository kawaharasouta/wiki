# -*- coding: utf-8 -*-

import sphinx_rtd_theme
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# -- Project information -----------------------------------------------------
project = u'wiki of khwarizmi'
copyright = 'KAWAHARA souta (@khwarizmi6514)'
author = 'KAWAHARA souta'
version = ''
release = '0.0.0'

# -- General configuration ---------------------------------------------------
extensions = [ 'sphinx.ext.todo', 'sphinx.ext.githubpages' ]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'ja'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = None
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'wiki of khwarizmi'


