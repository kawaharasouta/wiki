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
