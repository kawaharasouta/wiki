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

デフォルトでロードされるモジュールをロードされなくする
======================================================

↑と合わせてあとでちゃんとここら辺確認したい．

::

  $ sudo vim /etc/modprobe.d/blacklist.comf
  + blacklist [mod name]
  $ sudo update-initramfs -u
  $ sudo reboot

grubで起動時に選べるカーネルの種類を見る
========================================

※ あとの章で述べているが，grubby でやれという話がある．

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

※ あとの章で述べているが，grubby でやれという話がある．

::

  $ sudo vim /etc/default/grub
    
    #indexで指定する
    GRUB_DEFAULT=0

    #menuの名前で指定する
    GRUB_DEFAULT="Advanced options for Ubuntu>Ubuntu, with Linux 5.0.0-25-generic'


メインメニュー>サブメニュー とかって表記したらいいらしいんだけど，正直よくわからねえ
http://syuu1228.hatenablog.com/entry/20130120/1358690996


grubby での操作
=====================

ちょっとしたカーネル関連の設定変更は grubby でやれという話がさっきから出ている．

::

  //! 起動できるカーネルの種類の確認
  $ sudo grubby --info=ALL

  //! デフォルトで起動するカーネルの確認
  $ sudo grubby --default-kernel
  $ sudo grubby --default-index

  //!
  $ sudo grubby --set-default
  $ sudo grubby --set-default-index=[n]

他にもいろいろありそうだがとりあえずで．

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
↑ なんか過去の僕は mirror.kernel.org から探せといっているようだが，普通に https://www.kernel.org/ からでいいよね．

::

  $ mkdir kernel && cd $_
  $ wget https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/linux-4.15.1.tar.xz
  $ tar -xvJf linux-4.15.1.tar.xz -C /usr/src/kernels     //! カーネルとディストリ基本ぽいののソースは /usr/src 配下においたほうが良いぞという話．

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
  $ make defconfig      # default らしい．わかんなかったら変にいじるよりこれしたほうがいいみたいだけど意外に no change だったりもしたけど．

  # いるっぽかったやつ 他もあるかも信ないけどぐぐりゃだいたいでる
  $ sudo apt install libssl-dev bc libelf-dev(make install の時)
  $ make 

  # モジュールをビルド & インストール (/lib/modules/kernel version>-<config local version> 配下)
  $ sudo make modules_install

  # 下のコマンドしたら，Image のコピー・initramfs の作成配置・systemtap ファイルの配置などなどよしなにやってくれます
  $ sudo make install 


  //!!!! 以下は過去の文章などちょっと memo 的に残しておく
  //!!!! initramfs 作成と systemtap 周りについてはそのうちちゃんとした文章で書きたい．
  # /boot にカーネルをコピー
  $ sudo cp -v /arch/x86_64/boot/bzImage /boot/vmlinuz-4.15.1

  # 初期RAMディスク(initrd)を作成 ubuntuだとinitramfs?
  これ正直よくわからない．
  archだとmkinitcpioってコマンド叩いてるけどubuntuにはなくて，他のコマンド(initramfs的な感じのネーミングのがいくつか)
  あったりするんだけどマジでよくわからなくてわからない．でよくわからなくてわからない


この後適当に起動するカーネルを指定したりして
:ref:`kernel_up_target`
再起動するとビルドしたカーネルで動いてます．


ディストリビューションカーネルのコンフィグを持ってくるプラクティカルな方法
------------------------------------------------------------------------------

.configを用意する際の方法の例として，あるディストリビューションを使っていてそのコンフィグを流用して.configを用意する
ソース持ってきて(/usr/src/kernelに)展開してcdしたあとから

::

  $ make claen && make mrproper

  ### 現在動いているカーネルのコンフィグをそのまま持ってくる
  ### すくなくともfedora38では↓のように/boot配下にコンフィグある．
  ### あとは，linux-headers 入れてから/lib/modules/`uname -r`/build/から持ってくるとかできるはず?
  $ cp /boot/config-6.2.9-300.fc38.x86_64 .config

  ### 用意した.configから，ビルドしたいカーネルまでで追加されたconfigの一覧を見る．
  ### またそれらのhelpも以下のようにして見れる
  $ make listnewconfig
  $ make helpnewconfig

  ### 新しいconfigを設定するために以下のどちらかを実行する．
  ##### すべての新しいconfigを対話的にひとつずつ指定して設定する．
  $ make oldconfig
  ##### すべての新しいconfigをデフォルトの値で設定する．
  $ make olddefconfig


便利なカーネルコンフィグ
=========================

起動中に /proc/config.gz でカーネルコンフィグを確認できるようにする．
---------------------------------------------------------------------

::

  $ grep IKCONFIG .config
  CONFIG_IKCONFIG=y
  CONFIG_IKCONFIG_PROC=y

menuconfigだと

::

  General setup --->
    <*> Kernel .config support
    [*]   Enable access to .config through /proc/config.gz 

**こんなことしなくても/boot/config-`uname -r`とかで見れるんじゃね?**


カーネルブートオプション
==========================

ブートオプションという呼び方があってるのかわからないんだけど，/proc/cmdline で確認できるやつ．

::
  
  $ cat /proc/cdmline
  BOOT_IMAGE=/boot/vmlinuz-4.15.0-101-generic root=UUID=f1f76259-f300-4ddf-9e64-4d770bf4b031 ro default_hugepagesz=1G hugepagesz=1G hugepages=16 hugepagesz=2M hugepages=2048 iommu=pt intel_iommu=on isolcpus=1-21,23-43,45-65,67-87 kgdboc=ttyS0,115200 console=ttyS0,115200

設定
------

※grubの場合は/etc/grub/grub.conf を編集する

grub2の場合

::

  $ vim /etc/default/grub

  $ sudo grub-mkconfig
    or
  $ sudo grub2-mkconfig
    or
  $ uodate-grub
    or
  $ update-grub2

これによって /etc/grub/grub.cfg が自動生成される．

https://ac-as.net/linux-kernel-boot-options/

参考
====

ソースコード: https://www.kernel.org/

コードリーディング: https://elixir.bootlin.com/linux/latest/source

linux kernel の make target: https://qiita.com/satoru_takeuchi/items/b372303f62b7ca8b128c
