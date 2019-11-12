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



参考
====

ソースコード: https://www.kernel.org/

コードリーディング: https://elixir.bootlin.com/linux/latest/source

