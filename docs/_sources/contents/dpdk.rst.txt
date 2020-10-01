DPDK
=====


setup
------

ビルドツールがmakeからmeson & ninjaに変わっていた(とりあえず確認 2020-09-22 DPDK 20.08.0)

::

  $ sudo apt install meson ninja-build

  とりあえずライブラリのインストールはこれで良さげ?
  $ cd $RTE_SDK
  $ meson build
  $ cd build
  $ ninja
  $ sudo ninja install
  $ sudo ldconfig
  これにより、ビルドサブディレクトリに DPDK がコンパイルされ、結果として得られたライブラリ、ドライバ、ヘッダファイルがシステム上にインストールされます (通常は /usr/local)。DPDK 用のパッケージ設定ファイル libdpdk.pc もインストールされ、コンパイルやアプリケーションとのリンクが容易になります。

  フラグの管理?にpkg-configを使ってるみたい
  $ sudo apt install pkgconf
  これで多分以前まで設定してた環境変数とかがいらなくなる感じ?
  いやこれ別にそう言う話ではない．て言うか以前から使われていて，pkgconfがいないマシンで普通に動いてたんだけどなんだこれ．

  このあと，helloworld動かすときに，なんかmeson.buildを編集する必要があった．
  $ cd examples/helloworld
  $ vim meson.build
  + project('dpdk-app', 'c')

  + dpdk = dependency('libdpdk')
  + sources = files('main.c')
  + executable('dpdk-app', sources, dependencies: dpdk)

  ※めんどいからサンプル丸投げしてるけど，本当ならちゃんと書き直すべき．
  $ meson build
  $ cd build
  $ ninja

  これでとりあえずビルドして実行までできた．

依然としてmakeもできるみたいだが，どうもできないような気がする．．．?
そもそもTOPのMakefileのallターゲットが，meson&ninja使えよっていう文を出力してるだけになってるから
普通に無理じゃね?

https://doc.dpdk.org/guides/linux_gsg/build_dpdk.html#installation-of-dpdk-target-environment-using-make

また，将来は廃止されることが明記されていて，makeを利用した方法は推奨されていない．


以前のsetup
-----------

envs
~~~~
::  

        $ echo "export RTE_SDK=$HOME/dpdk" >> $HOME/.bashrc
        $ echo "export RTE_TARGET=x86_64-native-linuxapp-gcc" >> $HOME/.bashrc


packages
~~~~~~~~
::

        $ sudo apt install -y libpcap-dev python linux-headers-`uname -r` build-essential git libnuma-dev

clone and build DPDK
~~~~~~~~~~~~~~~~~~~~~~~~
::

        $ git clone http://dpdk.org/git/dpdk $RTE_SDK
        $ cd $RTE_SDK
        $ make install T=$RTE_TARGET

setup Hugepages
~~~~~~~~~~~~~~~
::

        $ sudo vim /etc/default/grub
        - GRUB_CMDLINE_LINUX=""
        + GRUB_CMDLINE_LINUX="hugepages=1024"
        $ sudo grub-mkconfig -o /boot/grub/grub.cfg
        $ sudo mkdir -p /mnt/huge
        $ sudo vim /etc/fstab
        + nodev /mnt/huge hugetlbfs defaults 0 0
        $ reboot

helloworld
~~~~~~~~~~
::

        $ cd $RTE_SDK/examples/helloworld
        $ make
        $ sudo ./build/helloworld



bind NIC
~~~~~~~~~
comming soon

useage
~~~~~~
 
skelton with tap
````````````````
::

        $ sudo ./build/basicfwd --vdev=net_tap0,iface=tap0 --vdev=net_tap1,iface=tap1

pktgen
```````

dpdk v16.11

::
        
        $ git clone https://github.com/slankdev/pktgen
        $ sudo ./app/x86_64-native-linuxapp-gcc/pktgen -- -P -m "[1-7].0,[16-23].0,[8-15].1,[24-31].1"

command
++++++++

*再表示*

::

        redisplay
