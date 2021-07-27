==========================
Linux From Scratch メモ
==========================

https://www.linuxfromscratch.org/
http://lfsbookja.osdn.jp/


envs
============

OS: ubuntu2004
kernel: 5.8.0-43-generic
LFS version: 10.1


LFS用パーティションの作成や環境準備
=========================================

LFS用のパーティションを作成する．
ubuntu2004の場合，インストール済みのシステムの上でインストーラーから既存パーティションの変更ができたため，
それによりすでにあるパーティションの一部をLFS用のパーティションとして切り出した．

他の方法として，
- システムを新規インストールしてその際にパーティションを切る
- fdisk等の古来の方法で既存のシステムからパーティションを切り出す? (できるのかよくわからない)
- 新しいディスクを用意してそれにLFS用のパーティションを作成する．
等々がありそう．

またこのパーティション作成の際に今回はext4にフォーマットしてしまっていたが，
これがされない場合は以下のように手動でおこなう．

::

  $ sudo mkfs -v -t ext4 /dev/[dev name]

また，このパーティションを/mnt/lfsにマウントするので

::
  
  $ sudo mkdir -p /mnt/lfs      (マウントポイント先に作っとくの一応かいとく)
  $ sudo mount /dev/[dev name] /mnt/lfs

とかのようにする．
例えば今回の場合は

::

  //! 作成したパーティション
  $ sudo fdisk -l
    ...
    Device            Start      End  Sectors  Size Type
    /dev/nvme0n1p1      256   131327   131072  512M EFI System
    /dev/nvme0n1p2   131328 17221171 17089844 65.2G Linux filesystem
    /dev/nvme0n1p3 17221376 26986751  9765376 37.3G Linux filesystem     ←これ
    ...

  //! 該当パーティションのUUIDを確認
  $ sudo blkid /dev/nvme0n1p3
  UUIDをコピる．

  //! 起動時にこれが /mnt/lfs にマウントされるよう設定
  $ sudo vim /etc/fstab
    + UUID=[ここにUUIDをコピー] /mnt/lfs  ext4  defaults  0 0

とした．

また，swapパーティションは既存のため新たに作成していない．

/mnt/lfs を $LFS としてセットしておく．

::

  $ vim ~/.bashrc
    + export LFS=/mnt/lfs


パッケージとパッチの取得
===============================

まず基本的にhttp://lfsbookja.osdn.jp/10.1-ja/chapter03/introduction.htmlの手順通りに取得する．
この通りにして取得できたなかったものは以下の２つで，後続のURLから取得する
- lfs-bootscripts-20210201.tar.xz: https://www.linuxfromscratch.org/lfs/downloads/stable/lfs-bootscripts-20210201.tar.xz
- expat-2.2.10.tar.xz: https://github.com/libexpat/libexpat/releases/download/R_2_2_10/expat-2.2.10.tar.xz
フットプリントのチェックはちゃんとOKになったので大丈夫そう．




