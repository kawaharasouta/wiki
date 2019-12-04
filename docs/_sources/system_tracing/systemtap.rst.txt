===========
systemtap
===========

実行中のカーネルの特定の処理にフックしてデバッグを行ったりするツール．

SystemTapは「STPスクリプト」と呼ばれる独自言語のスクリプトを利用して記述します。
SystemTapのコマンドであるstapコマンドがSTPスクリプトとカーネルのデバッグ情報からC言語のコードを生成して，
それをカーネルモジュールとしてビルド・ロードし，その結果を標準出力や独自のログバッファなどに保存するのです。



install
==============

「SystemTap本体」と「対象カーネルのデバッグ情報」が必要

::

  $ sudo apt install gnupg

  $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C8CAB6595FDFF622            #11371番ポートがデフォルトだけど↓
    or 
  $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C8CAB6595FDFF622   #fwかまされてたりするとき

  $ codename=$(lsb_release -cs)
  $ sudo tee /etc/apt/sources.list.d/ddebs.list << EOF
    deb http://ddebs.ubuntu.com/ ${codename}      main restricted universe multiverse
    #deb http://ddebs.ubuntu.com/ ${codename}-security main restricted universe multiverse
    deb http://ddebs.ubuntu.com/ ${codename}-updates  main restricted universe multiverse
    deb http://ddebs.ubuntu.com/ ${codename}-proposed main restricted universe multiverse
    EOF
  $ sudo apt update
  $ sudo apt install -y linux-image-$(uname -r)-dbgsym


debianパッケージで頑張ってみたけどちょっと無理そうか?
カーネルバージョン色々いじってみたりしたけどなんかうまく行かなかった．
とりあえずデバグ情報つけてビルドする方法でやってみることにする．  
うーんなんか際ビルドの方法もなかなかうまく行かん．．．



本家: https://sourceware.org/systemtap/

参考にしたところ

https://gihyo.jp/admin/serial/01/ubuntu-recipe/0584

https://www.hiroom2.com/2018/04/27/ubuntu-1804-dbgsym-ja/

https://blog.jeffli.me/blog/2014/10/10/install-systemtap-in-ubuntu-14-dot-04/

https://wiki.ubuntu.com/Kernel/Systemtap#Where_to_get_debug_symbols_for_kernel_X.3F

https://blog.csdn.net/richardysteven/article/details/82525909





もうなんかわかんねえからとにかく参考にしたリンク貼っとくぞおら

http://myokota.hatenablog.jp/entry/2015/01/03/235944

https://mmitou.hatenadiary.org/entry/20120721/1342879187

ubuntuデバグ情報
https://wiki.ubuntu.com/Debug%20Symbol%20Packages

centos
https://access.redhat.com/ja/solutions/289453

linux kernel-devel
https://qiita.com/metheglin/items/60261f474ccdfb467574
https://download.parallels.com/desktop/v10/docs/ja_JP/Parallels%20Desktop%20User's%20Guide/33307.ht

https://blog.jeffli.me/blog/2014/10/10/install-systemtap-in-ubuntu-14-dot-04/m

https://blog.csdn.net/richardysteven/article/details/82525909

https://kernhack.hatenablog.com/entry/2015/12/26/165142

https://askubuntu.com/questions/1079874/unknown-sequence-editconfigs-when-trying-to-build-a-kernel

https://www.itread01.com/content/1550387720.html

systemtap arch wiki
https://wiki.archlinux.jp/index.php/SystemTap

https://sourceware.org/systemtap/wiki/SystemtapOnDebian
