=================
カーネル関連tips
=================


カーネルバージョン変更
========================

::

  変更可能なバージョン確認
  $ sudo apt-cache search linux-image

  上で確認した中から変更したいバージョンを指定
  $ sudo apt install [linux-images-***]


起動時にカーネルモジュールがロードされるようにする
==================================================

::

  カーネルモジュールの正式な置き場?にモジュールをおく
  $ sudo cp [your module] /lib/modules/$(uname -r)/kernel/drivers/

  依存関係更新
  $ sudo depmod -ae

  モジュール名をmodules.confに書き込み
  $ sudo vim /etc/modules-load.d/modules.conf


grubで起動時に選べるカーネルの種類を見る
========================================

::
  
  $ sudo grep menuentry /boot/grub/grub.cfg
    ...
    menuentry 'Ubuntu, with Linux 5.0.0-25-generic' --class ubuntu --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-5.0.0-25-generic-advanced-e99082e4-8470-4019-9dcc-4535f97283ac' {
    menuentry 'Ubuntu, with Linux 5.0.0-25-generic (recovery mode)' --class ubuntu --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-5.0.0-25-generic-recovery-e99082e4-8470-4019-9dcc-4535f97283ac' {
    ...

ちなみにlinux-imageをinstallしたらこれ増える


.. _kernel_up_target:

標準で起動するカーネルを指定
===============================

::

  $ sudo vim /etc/default/grub
    
    #indexで指定する
    GRUB_DEFAULT=0

    #menuの名前で指定する
    GRUB_DEFAULT="Advanced options for Ubuntu>Ubuntu, with Linux 5.0.0-25-generic'


メインメニュー>サブメニュー とかって表記したらいいらしいんだけど，正直よくわからねえ
http://syuu1228.hatenablog.com/entry/20130120/1358690996


dbgsymパッケージリポジトリ導入
==============================

::

  $ sudo apt install gnupg

  $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C8CAB6595FDFF622            #11371番ポートがデフォルトだけど↓
    or
  $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C8CAB6595FDFF622   #fwかまされてたりするとき
  もしくは
  $ wget -O - http://ddebs.ubuntu.com/dbgsym-release-key.asc | sudo apt-key add -

  $ codename=$(lsb_release -cs)
  $ sudo tee /etc/apt/sources.list.d/ddebs.list << EOF
    deb http://ddebs.ubuntu.com/ ${codename}      main restricted universe multiverse
    #deb http://ddebs.ubuntu.com/ ${codename}-security main restricted universe multiverse
    deb http://ddebs.ubuntu.com/ ${codename}-updates  main restricted universe multiverse
    deb http://ddebs.ubuntu.com/ ${codename}-proposed main restricted universe multiverse
    EOF
  $ sudo apt update

ちなみに具体的にはここ
http://ddebs.ubuntu.com/pool/main/l/linux/
迷ったら直に持ってきちゃえばいい

::

  sudo dpkg -i  [debian package]


カーネル再構築
===============

https://wiki.archlinux.jp/index.php/%E3%82%AB%E3%83%BC%E3%83%8D%E3%83%AB/%E3%82%B3%E3%83%B3%E3%83%91%E3%82%A4%E3%83%AB/%E4%BC%9D%E7%B5%B1%E7%9A%84%E3%81%AA%E6%96%B9%E6%B3%95
↑のリンクを参考にした．

カーネルのソースをダウンロードして展開する．
他のバージョンは適当に探せhttps://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/

::

  $ mkdir kernel && cd $_
  $ wget https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/linux-4.15.1.tar.xz
  $ tar -xvJf linux-4.15.1.tar.xz

ビルドする

::

  $ cd linux-4.15.1/
  $ make clean && make mrproper   #色々cleanするみたいな mrproperだけでいいって聞いたこともある

  # とりあえず既存の.configを持ってくる系のmakeターゲットいくつか並べておく
  $ make localmodconfig   #既存の.configのうち
  $ make oldconfig

  # その後の設定 TUI的な感じで設定ができそう
  $ make menuconfig
  # その他の設定のやり方? ここら辺ncursesが必要だったりしそう
  $ make menuconfig     # ncurses コマンドラインインターフェイス
  $ make nconfig        # コマンドラインの新しい ncurses インターフェイス
  $ make xconfig        #  ユーザーフレンドリーなグラフィカルインターフェイス  packagekit-qt4パッケージ必要? 簡単で初心者向けらしい
  $ make gconfig        # GTK+ を使用する

  # いるっぽかったやつ 他もあるかも信ないけどぐぐりゃだいたいでる
  $ sudo apt install libssl-dev bc libelf-dev(make install の時)
  $ make 

  # モジュールをビルド
  $ sudo make module_install

  # なんかこの後下のコマンドしたらよしなにやってくれます
  $ sudo make install 

  # /boot にカーネルをコピー
  $ sudo cp -v /arch/x86_64/boot/bzImage /boot/vmlinux-4.15.1

  # 初期RAMディスク(initrd)を作成 ubuntuだとinitramfs?
  これ正直よくわからない．
  archだとmkinitcpioってコマンド叩いてるけどubuntuにはなくて，他のコマンド(initramfs的な感じのネーミングのがいくつか)
  あったりするんだけどマジでよくわからなくてわからない．でよくわからなくてわからない


この後適当に起動するカーネルを指定したりして
:ref:`kernel_up_target`
再起動するとビルドしたカーネルで動いてます．

参考
====

ソースコード: https://www.kernel.org/

コードリーディング: https://elixir.bootlin.com/linux/latest/source

linux kernel の make target: https://qiita.com/satoru_takeuchi/items/b372303f62b7ca8b128c
