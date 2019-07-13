# -*- coding: utf-8 -*-

# -- Project information -----------------------------------------------------
project = u'wiki of khwarizmi'
copyright = '2018, Hosei University , NTT Communications'
author = 'KAWAHARA souta'
version = ''
release = '0.0.0'

# -- General configuration ---------------------------------------------------
extensions = [ 'sphinx.ext.todo' ]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'ja'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = None
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'jr-nttcom'

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    'extraclassoptions': 'openany',
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}
latex_docclas = {'manual': 'jsbook'}
latex_documents = [
    (master_doc, 'report.tex', project,
     'Souta Kawahara, Hiroki Shirokura', 'manual'),
]

# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, 'jr-nttcom', project,
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'report', project,
     author, 'report', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_exclude_files = ['search.html']
