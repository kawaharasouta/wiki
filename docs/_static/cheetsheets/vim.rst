====
vim 
====

cheetsheetじゃなくてcontentsの方がいい気がしてきた．

vim日本語ドキュメント:
https://vim-jp.org/vimdoc-ja/usr_90.html
vim-jp:
https://vim-jp.org/docs/build_linux.html

ビルド
=======

インストール

::

  $ git clone https://github.com/vim/vim.git -b v8.2.0000
  $ cd vim
  $ ./configure --with-features=huge --enable-fail-if-missing
  $ make && sudo make install

アンインストール

::

  make uninstall

プラグイン(vundle)導入
========================

::

  $ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
  $ vim ~/.vimrc    # head
    + set nocompatible
    + filetype off
    + set rtp+=~/.vim/bundle/Vundle.vim
    + call vundle#begin()
    + 
    + Plugin 'VundleVim/Vundle.vim'
    + ......
    +
    + call vundle#end()
    + filetype plugin indent on
  $ vim +PluginInstall +qall

コマンド
==========

.. csv-table::
  :header: コマンド名, 機能
  :widths: 3, 3

  d, 削除
  c, 変更
  y, コピー

.. csv-table::
  :header: モーション, 機能
  :widths: 3, 3

  w, カーソル位置から空白を含む単語の末尾
  e, カーソル位置から空白を含まない単語の末尾
  $, カーソル位置から行末

tab空白
===========

tab -> 空白

::

  :set expandtab
  :retab

空白 -> tab

::

  :set noexpndtab
  :retab!

========
neovim
========

install
==========

::

  $ sudo apt-get install software-properties-common
  #######################    $ sudo add-apt-repository ppa:neovim-ppa/unstable
  $ sudo add-apt-repository ppa:neovim-ppa/stable
  $ sudo apt-get update
  $ sudo apt-get install neovim
  $ sudo apt install python3-dev python3-pip
  $ pip3 install -U pip3        # いらんかも
  $ pip3 install neovim

  $ sudo apt install xclip xsel
   
