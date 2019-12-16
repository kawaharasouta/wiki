=============
Open vSwitch
=============


install
=======

::

  $ sudo apt install openvswitch-switch openvswitch-common

command type 
===============

- ovs-vsctl
  Used for configuring the ovs-vswitchd configuration database (known as ovs-db)
- ovs-ofctl
  A command line tool for monitoring and administering OpenFlow switches
- ovs-dpctl
  Used to administer Open vSwitch datapaths
- ovs−appctl
  Used for querying and controlling Open vSwitch daemons

参考: https://komeiy.hatenablog.com/entry/2015/06/26/233746 クソほど有能な資料

operation
===========

::

  $ sudo ovs-vsctl show 
  $ sudo ovs-vsctl add-br [switch]
  $ sudo ovs-vsctl del-br [switch]
  $ sudo ovs-vsctl add-port [switch] [port]
  $ sudo ovs-vsctl del-port [switch] [port]
  # bridgeのリスト
  $ sudo ovs-vstcl list-br

  $ sudo ovs-ofctl show [switch]
  $ sudo ovs-ofctl dump-flows [switch]
  $ sudo ovs-ofctl add-flow [switch] in_port=[port num],action={output:[port num] または all}   #actionは他にも指定方法ありそう
  $ sudo ovs-ofctl del-flow [switch]  # switch指定がなかったら全ルール削除

  # flow確認
  $ sudo ovs-ofctl dump-flows [switch]
  # flow削除
  $ sudo ovs-ofctl del-flows [switch]
  # flow追加
  $ sudo ovs-ofctl show br0        # ポートとか確認
  $ sudo ovs-ofctl add-flow br0 in_port=1,action=output:3     # 特定のフロールール追加
  ## 他の追加の方法は↓にリンク貼っとく


flow追加: http://alexei-karamazov.hatenablog.com/entry/2013/12/20/103346

kvmのVMをovsに接続
===================

::

  <interface type='bridge'>
    <source bridge='[ovs sw name]'/>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x02' function='0x0'/>
    <virtualport type='openvswitch'/>
  </interface>


==================
OvS DPDK
==================

install
========

::

  $ sudo apt install openvswitch-switch-dpdk
  $ sudo update-alternatives --set ovs-vswitchd /usr/lib/openvswitch-switch-dpdk/ovs-vswitchd-dpdk      # dpdk対応verに切り替えてるだけ
  ※/usr/sbin/ovs-vswitchd      #戻す時こっち

requirement 
============

::

  DPDK:
  OVS:
  QEMU:




::

  $ sudo killall ovsdb-server ovs-vswitchd  or $ systemctl restart ovsdb-server ovs-vswitchd
  $ sudo vim /etc/default/grub
    + GRUB_CMDLINE_LINUX_DEFAULT="default_hugepagesz=1G hugepagesz=1G hugepages=16 hugepagesz=2M hugepages=2048 iommu=pt intel_iommu=on isolcpus=1-21,23-43,45-65,67-87"
  $ sudo vim /etc/dpdk/dpdk.conf
    + NR_1G_PAGES=8
  $ sudo vim /etc/libvirt/qemu.conf
    - #user = "root"
    - #group = "root"
    + user = "root"
    + group = "root"
  $ sudo update-grub && sudo reboot
  
  # いるかどうかわからないけど
  $ sudo mkdir -p /mnt/huge
  $ sudo mkdir -p /mnt/huge_2mb
  $ sudo mount -t hugetlbfs none /mnt/huge
  $ sudo mount -t hugetlbfs none /mnt/huge_2mb -o pagesize=2MB
  $ sudo sudo mount -t hugetlbfs none /dev/hugepages

  $ sudo ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true
  $ sudo ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-lcore-mask=0xfffffbffffefffffbffffe
  $ sudo ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-socket-mem="1024,1024"
  $ sudo ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=1E0000000001E

  # VMのインタフェースの場合
  $ sudo mkdir -p /usr/local/openvswitch/       # ソケットを配置しておくディレクトリ
  $ sudo touch /usr/local/openvswitch/dpdkvhostclient0
  $ sudo touch /usr/local/openvswitch/dpdkvhostclient1
  $ sudo ovs-vsctl add-br [bridge name] -- set bridge [bridge name] datapath_type=netdev
  $ sudo ovs-vsctl add-port [bridge name] dpdkvhostclient1 \
    -- set Interface dpdkvhostclient1 type=dpdkvhostuserclient \
       options:vhost-server-path=/usr/local/openvswitch/dpdkvhostclient1
  $ sudo ovs-vsctl add-port [bridge name] dpdkvhostclient2 \
    -- set Interface dpdkvhostclient2 type=dpdkvhostuserclient \
       options:vhost-server-path=/usr/local/openvswitch/dpdkvhostclient2
  $
  $ sudo virsh edit [VM]
    + <currentMemory unit='KiB'>~~~~~~~</currentMemory>
    + <memoryBacking>
    + <hugepages/>
    + </memoryBacking>
    --------------------------------------------------------
    + <cpu mode='host-passthrough'>
    + <numa>
    + <cell id='0' cpus='0' memory='1048576' unit='KiB' memAccess='shared'/>
    + </numa>
    + </cpu>
    --------------------------------------------------------
    + <interface type='vhostuser'>
    +   <source type='unix'
    +     path='/usr/local/openvswitch/dpdkvhostclient0'
    +     mode='server'/>
    +   <model type='virtio'/>
    + </interface>

  # 物理インタフェースの場合
  $ sudo dpdk-devbind -b igb_uio [pci bus]      # ドライバは任意?
  $ sudo ovs-vsctl add-port [bridge name] nic0 -- set Interface nic0 type=dpdk options:dpdk-devargs=[pci bus]
  

確か，VMにそこそこメモリあげないと動かなかった気がするので動かなかったら確認するといい?
curentじゃないのが1G, currentが500Mで動いてたけどどうなんだろう．
というか，なんか1G以上メモリをあげられなかったんだけどこれはなんだ?
他のVMにはあげられてるのでOVS-DPDKが原因なんだろうけどなんなんだろう．


memo
=====

- 最初flowはNORMALが設定されてるけど，ちゃんとflowをそれぞれ設定した方がスループット出る．




参考
https://www.miraclelinux.com/tech-blog/dpdk-open-vswitch-study-7
https://www.miraclelinux.com/tech-blog/zubcuq
https://software.intel.com/en-us/articles/set-up-open-vswitch-with-dpdk-on-ubuntu-server
https://metonymical.hatenablog.com/entry/2019/01/12/144217#fn-bf36e323
https://teratail.com/questions/125716
https://wiki.qemu.org/Documentation/vhost-user-ovs-dpdk
https://github.com/openvswitch/ovs/blob/branch-2.6/INSTALL.DPDK.md

