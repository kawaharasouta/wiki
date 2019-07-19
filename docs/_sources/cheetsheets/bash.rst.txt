bash
======

add user
---------
::

  $ sudo useradd -m -G users,sudo -s /bin/bash [username]
  $ sudo passwd [username]





















メモ系
------

標準エラー出力のリダイレクト例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::
  
  ip help 2>&1 | less

ファイル内検索
~~~~~~~~~~~~~~
::

  $ grep -r "xxx" ./

該当ファイル以外を削除
~~~~~~~~~~~~~~~~~~~~~~~
::

  $ ls | grep -v "file name" | xargs rm -rf
