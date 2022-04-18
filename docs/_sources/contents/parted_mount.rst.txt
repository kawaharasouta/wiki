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
    + /dev/sdb1 /mnt/part1  ext4  defaults  0 2         ### 最後の 2 はなんかよくわかってないんだけどなんか入れとくほうがいい? 
    + /dev/sdb2 /mnt/part1  ext4  defaults  0 2         ### fsckでファイルシステムをチェックする設定らしい．1 は最優先(ルートfs) で 2 はその次 0 はチェックしない．


その他操作の適当なmemo
=============================================

boot flag を立てて fat32 で mkfs する．

::
  
  $ sudo parted /dev/sdb1 set 1 boot on
  $ sudo mkfs -t vfat -F 32 /dev/sdb1
  

LVM パテ切りから新規作成・追加など
==============================================

/dev/vdb を利用して LV を作成してマウントする．
その後 /dev/vdc を追加して LV を拡張する．
参考: https://qiita.com/ngyuki/items/93da394fd0847ed5155e#lvm

::

  $ sudo apt install lvm2   //! ubuntu はいらん
  $ sudo yum install lvm2

  # parted -l
    Error: /dev/vdb: unrecognised disk label
    Model: Virtio Block Device (virtblk)                                       
    Disk /dev/vdb: 2147MB
    Sector size (logical/physical): 512B/512B
    Partition Table: unknown
    Disk Flags: 

    Error: /dev/vdc: unrecognised disk label
    Model: Virtio Block Device (virtblk)                                       
    Disk /dev/vdc: 2147MB
    Sector size (logical/physical): 512B/512B
    Partition Table: unknown
    Disk Flags:

  # parted -l
  # parted -s /dev/vdb print free

  //! ひとまず MBR にラベルを設定
  # parted /dev/vdb mklabel msdos

  //! パテを切る例えば今回２つ切ることにする サイズは適当
  # parted -s -a optimal /dev/vdb -- mkpart primary 1 -1

  //! lvm ラベルを設定
  # parted -s -a optimal /dev/vdb set 1 lvm on

  //! パテ切りとラベル設定とかはこんな感じでワンライナーでも行けるらしい
  # parted -s -a optimal /dev/vdb -- mklabel msdos mkpart primary 1 -1 set 1 lvm on

LV の作成まで

::

  //! さっき作ったパテを pv(phisical volume) に登録
  # pvcreate /dev/vdb1              //! 複数指定も可
    Physical volume "/dev/vdb1" successfully created.
  # pvdisplay                       //! 追加されているか確認

  //! vg(volume group) 作成
  # vgcreate vg01 /dev/sdb1         //! 複数指定も可．
  # vgdisplay                       //! 作成できているか確認 

  //! lv(logical volume) 作成
  # lvcreate --name lv01 --size 1GB vg01
  # lvdisplay                       //! 作成できているか確認

ここまでやったら /dev/mapper/vg01-lv01 とかみたいなのができているはずなので，フォーマットしてマウントする．

::

  # mkfs -t ext4 /dev/mapper/vg01-lv01
  # mkdir -pv /mnt/vg01-lv01
  # mout -t ext4 /dev/mapper/vg01-lv01 /mnt/vg01-lv01

これで新規作成は完了．

ここから追加手順．まあほとんど変わらんので，新規作成手順ができればできる．
いつか気が向いたら書く．





