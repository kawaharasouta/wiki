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

参考:


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

USBをマウントするやつ
~~~~~~~~~~~~~~~~~~~~~~

USBを刺したあとdmesgをみてデバイスファイルの場所を確認．
(怖かったら/dev/sda とか /dev/sdb とかあたりをUSBを抜き差ししながらみてデバイスファイルにあたりをつける)

::

  sudo mount -t vfat /dev/[デバイスファイル] /media


aptが途中で死んだ(ctrl-cで殺した)とき
--------------------------------------

install するときに依存関係とかで足りないやつがあったときは↓みたいに(1行目いらないかも)
すると依存関係を解決してinstallしてくれるみたい．

::

  $ sudo dpkg --configure -a 
  $ sudo apt --fix-broken install

https://codeday.me/jp/qa/20190808/1401674.html


上でダメだったやつはこれでフットプリント?履歴?みたいなのを削除?すればいい．

::

  $ sudo dpkg -r --force-all [パッケージ名]

https://lb.raspberrypi.org/forums/viewtopic.php?t=200575


Linuxデストリ
---------------

http://note.kurodigi.com/linux-version/


起動時にネットワークどうのこうので起動がおそいやつ
----------------------------------------------------

::

  A start job is running for wait for network to be configured.

とかって言われるやつ．
↓のようにする．

::

  $ systemctl disable systemd-networkd-wait-online.service
  $ systemctl mask systemd-networkd-wait-online.service

他参考:
https://takuya-1st.hatenablog.jp/entry/2017/12/19/211216
https://qiita.com/hnw/items/005b2018efaab5f954a9
