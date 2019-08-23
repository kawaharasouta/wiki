vim 
====


コマンド
----------

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
--------

tab -> 空白

::

  :set expandtab
  :retab

空白 -> tab

::

  :set noexpndtab
  :retab!
