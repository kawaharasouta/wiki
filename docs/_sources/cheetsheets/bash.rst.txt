bash
======

add user
---------

::

  $ sudo useradd -m -G users,sudo -s /bin/bash [username]
  $ sudo passwd [username]


change hostname 
----------------

::

  $ sudo vim /etc/cloud/cloud.cfg   #cloud-init が入ってる場合
   - preserve_hostname: fauls
   + preserve_hostname: true
  $ sudo hostnamectl set-hostname [hostname]



shell芸的tips
--------------

::

  awk '{print $1, $3}'        #1,3列目を取得
  awk 'NR==2,NR==5'           #2~5行目を取得


GNU coreutils
--------------

Linux(GNUオペレーティングシステム)の一般的なコマンドツールのパッケージらしい.

コマンドの種類: 


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


aptが途中で死んだ(ctrl-cで殺した)とき
--------------------------------------

::

  $ sudo dpkg --configure -a 
  $ sudo apt --fix-broken install

https://codeday.me/jp/qa/20190808/1401674.html
ダメでした〜〜〜〜〜〜〜〜



こっちで行けそう

::

  $ sudo dpkg -r --force-all [パッケージ名]

https://lb.raspberrypi.org/forums/viewtopic.php?t=200575
