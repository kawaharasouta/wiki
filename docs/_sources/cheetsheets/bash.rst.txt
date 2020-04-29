======
bash
======

※このページcommand util的な名前に変えた方がいい気がするんだ．

add user
==========

::

  $ sudo useradd -m -G users,sudo -s /bin/bash [username]
  $ sudo passwd [username]


change hostname 
=================

::

  $ sudo vim /etc/cloud/cloud.cfg   #cloud-init が入ってる場合
   - preserve_hostname: fauls
   + preserve_hostname: true
  $ sudo hostnamectl set-hostname [hostname]



shell芸的tips
=================

::

  awk '{print $1, $3}'        #1,3列目を取得
  awk 'NR==2,NR==5'           #2~5行目を取得


GNU coreutils
==============

Linux(GNUオペレーティングシステム)の一般的なコマンドツールのパッケージらしい.

参考:


コマンドの種類: 

git系 
=======

でっけえのclone
-----------------

ソフトウェアが使いたいだけなら
タグ指定でcloneしちゃう

::

  $ git clone [repo url] -b [tag name]  

とりあえずお手元に引っ張る時
直近でcloneする

::

  git clone --depth 1 [repo url]

https://qiita.com/yasshcy/items/bd96469f4f30c0e57312

リリース物をダウンロード
-------------------------

cloudius-systemsのosvでの例

とりあえず以下のようにするとrelease情報がまとまってjsonみたいな感じで落ちてくる．

::

  $ curl https://api.github.com/repos/cloudius-systems/osv/releases

これは

::

  $


update-alternatives でコマンドを管理するやつ
===============================================

コマンドの日本語リファレンス:
https://manpages.debian.org/wheezy/dpkg/update-alternatives.8.ja.html

Linuxには，同等の役割を持ったソフトウェアが複数あったり，(エディタとか)
様々なバージョンを使い分けたいような場合(コンパイラとか)があったりするが，
そういうのの選択．切り替えとかをやってくれるやつ．


なんかいろんなやり方とかはあとで書く．


仕組みとか?:
https://vinelinux.org/docs/vine6/cui-guide/update-alternatives.html


sudoでcommand not fountする
=============================

sudoers の env_reset オプションが有効になっている場合，
セキュリティ上環境変数が初期化されて secure_path に設定しているパスが使われるので，環境変数 PATH が通らない。

1. env_reset を無効化する

::

  $ sudo visudo
    - Defaults env_reset
    + #Defaults env_reset

2. 環境変数を引き継ぐ

::

  $ sudo visudo
    - Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin
    + #Defaults    secure_path = /sbin:/bin:/usr/sbin:/usr/bin
    + Defaults env_keep += "PATH"

3. secure_pathにパスを設定してしまう

コマンド省略

メモ系
=========

標準エラー出力のリダイレクト例
-------------------------------

::
  
  ip help 2>&1 | less

ファイル内検索
----------------

::

  $ grep -r "xxx" ./

該当ファイル以外を削除
-------------------------

::

  $ ls | grep -v "file name" | xargs rm -rf



マウントとかそういう系のやつ
=============================

fs(ファイルシステム)もマウント状況をみたいやつ
-----------------------------------------------

::

  $ df -aT

USBをマウントするやつ
-----------------------

USBを刺したあとdmesgをみてデバイスファイルの場所を確認．
(怖かったら/dev/sda とか /dev/sdb とかあたりをUSBを抜き差ししながらみてデバイスファイルにあたりをつける)

::

  $ sudo mount -t vfat /dev/[dev file] /media

マウントしたら，状況確認するために↓やってみとくといい．

::

  $ df

  Filesystem     1K-blocks     Used Available Use% Mounted on
  udev             8110576        0   8110576   0% /dev
  tmpfs            1628416     1424   1626992   1% /run
  /dev/sda2      959862832 28869252 882165420   4% /
  tmpfs            8142060        0   8142060   0% /dev/shm
  tmpfs               5120        0      5120   0% /run/lock
  tmpfs            8142060        0   8142060   0% /sys/fs/cgroup
  /dev/loop0         93568    93568         0 100% /snap/core/8689
  /dev/loop1         93568    93568         0 100% /snap/core/8592
  /dev/sda1         523248     4668    518580   1% /boot/efi
  tmpfs            1628412        0   1628412   0% /run/user/1000
  /dev/sdb1       15122312        0  15122312   0% /media

アンマウントは↓

::

  $ sudo umount /dev/[dev file]



フォーマットする
------------------

もしマウントしてたらまずはアンマウントする．
まじでしないとうんちになる．

**ゼロフォーマットする**

::

  $ sudo dd if=/dev/zero of=/dev/[dev file] bs=16M

※ddによる書き込みは多分最後「dd: error writing '/dev/sdc1': No space left on device」って言われるけど
※最後まで書き込んで出てしまうだけ(仕様なのかは知らん)なので多分無視して大丈夫

**USBをFAT32にフォーマットする**

::

  sudo mkdosfs -F32 -nUSB /dev/[dev file]

※fat32のデフォルトのクラスタサイズ

::

  Partition size           Cluster size
  -------------------------------------
  512 MB to 8,191 MB          4 KB
  8,192 MB to 16,383 MB       8 KB
  16,384 MB to 32,767 MB     16 KB
  Larger than 32,768 MB      32 KB

**isoファイルを焼く** (とりあえず例)

::

  sudo dd bs=16M if=/home/khwarizmi/FreeBSD-12.1-RELEASE-amd64-disc1.iso of=/dev/sdb status=progress && sync

あとでやる
https://www.archlinux.site/2018/03/linuxisoubuntulive-usb.html


syncの面白い話: 
https://qiita.com/tboffice/items/9c6092278ccaab88e71e#fnref2
https://booth.pm/ja/items/1564734


apt のPPAの話
===============

参考
https://kazuhira-r.hatenablog.com/entry/2019/03/10/225459


aptが途中で死んだ(ctrl-cで殺した)とき
=======================================

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


いろいろインストールし直したりしてたら入れたはずなのに動かないみたいな時
==========================================================================

コマンドって大体cacheされてるからいろんな方法でインストールし直して繰り返したりしてると
同じコマンド名だけどインストールされるPathが違くて前の場所にcacheされてて思い通りのところを見に行かないみたいなそういうのある．

cache確認

::

  $ type [command]
  [command] is hashed (/usr/bin/[command])    #みたいな感じ

vimのcacheを消す

::

  $ hash -d vim

シェルがビルトインコマンドではないコマンドを実行する場合、環境変数PATHから該当する実行ファイルを探す必要がありますが、
頻繁に使うコマンドは「ハッシュテーブル」と呼ばれる場所に記憶しています。
「hash」はこのハッシュテーブルの表示や削除、追加を行うコマンドになります。
(https://www.atmarkit.co.jp/ait/articles/1703/23/news017.htmlより)

ビルドインコマンドについて
https://open-groove.net/shell/builtin/

Linuxデストリ
===============

http://note.kurodigi.com/linux-version/


起動時にネットワークどうのこうので起動がおそいやつ
===================================================

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
