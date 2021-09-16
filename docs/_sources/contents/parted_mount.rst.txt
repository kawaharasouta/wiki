=====================================
パーティション・マウント関連
=====================================

ひとまずメモ的にパーティション操作やマウント関連について



新しいディスクのパテを切ってマウントするまでの一般的な方法
======================================================================

/dev/sdb に新しいディスクが刺さってる想定でこれのパテを切って /etc/fstab にマウント設定するまで

::
  
  $ sudo parted -l
  $ sudo parted /dev/sdb print free
    
  //! ひとまず MBR にラベルを設定
  $ sudo parted /dev/sdb mklabel msdos

  //! パテを切る例えば今回２つ切ることにする サイズは適当
  $ sudo parted -a cylinder /dev/sdb mkpart primary 1074MB 10GB
  $ sudo parted -a cylinder /dev/sdb mkpart primary 10GB 20GB

  //! パテを確認しとく
  $ sudo parted /dev/sdb print
  $ sudo parted /dev/sdb print free

  //! ひとまず ext4 でフォーマットしておく
  //! 一応 ubuntu だと ext4 が標準なので．cent なら xfs にしとくのが無難．
  $ sudo mkfs -t ext4 /dev/sdb1
  $ sudo mkfs -t ext4 /dev/sdb2

  //! 雑にマウントポイントを作っておく
  $ sudo mkdir -pv /mnt/part1
  $ sudo mkdir -pv /mnt/part2

  //! マウントテスト
  $ sudo mount -t ext4 /dev/sdb1 /mnt/part1
  $ sudo mount -t ext4 /dev/sdb2 /mnt/part2

  //! 適当にチェックしてアンマウント
  $ df -h 
  $ sudo umount /mnt/part1
  $ sudo umount /mnt/part2

  //! /etc/fstab を編集
  $ sudo vim /etc/fstab
    + /dev/sdb1 /mnt/part1  ext4  defaults  0 2         ### 最後の 2 はなんかよくわかってないんだけど
    + /dev/sdb2 /mnt/part1  ext4  defaults  0 2         ### なんか入れとくほうがいい? fsckをする設定らしい．





