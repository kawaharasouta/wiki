sphinx
=======

ubuntu環境構築
--------------

requirement
```````````

 - python3.6.8?
 - python3-pip

:: 

  $ sudo apt install python3-sphinx
  $ pip3 install sphinx 


html
^^^^^

no more requirement

latexpdf
^^^^^^^^^

::

  sudo apt instal -y texlive-fonts-recommended \
	  texlive-latex-recommended texlive-latex-extra \
	  texlive-lang-japanese latexmk texlive-latex-base python3-sphinx

**conf.py**

::

  language = 'ja'
  latex_docclass = {'manual': 'jsbook'}









build 
------

Makefile example
`````````````````

::

	# Minimal makefile for Sphinx documentation
	#
	
	# You can set these variables from the command line, and also
	# from the environment for the first two.
	SPHINXOPTS    ?=
	SPHINXBUILD   ?= sphinx-build
	SOURCEDIR     = source
	BUILDDIR      = build
	
	# Put it first so that "make" without argument is like "make help".
	help:
	  @$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	
	.PHONY: help Makefile docs
	
	# Catch-all target: route all unknown targets to Sphinx using the new
	# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
	%: Makefile
	  @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	
	docs:
	  @$(SPHINXBUILD) -b html $(SOURCEDIR) "docs" $(SPHINXOPTS) $(0)
	   


make target
````````````

make 打てばターゲット一覧が出る．

::
	
	$ make 


theme (i.e. sphinx_rtd_theme
``````

**install thema**

::

 $ pip3 install sphinx sphinx_rtd_theme 


**edit conf.py**

::

  html_theme = 'sphinx_rtd_theme'

theme_sample_




.. _theme_sample: https://sphinx-themes.org/
