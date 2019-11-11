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
  
  #indexで指定する
  GRUB_DEFAULT=0

  #menuの名前で指定する
  GRUB_DEFAULT="Ubuntu, with Linux 5.0.0-25-generic'

参考
====

ソースコード: https://www.kernel.org/

コードリーディング: https://elixir.bootlin.com/linux/latest/source

