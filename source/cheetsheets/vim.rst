====
vim 
====

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
