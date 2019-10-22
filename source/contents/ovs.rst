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

DPDK:
OVS:
QEMU:




::

  $ sudo mkdir -p /usr/local/openvswitch/       # ソケットを配置しておくディレクトリ
  $ sudo touch /usr/local/openvswitch/dpdkvhostclient0
  $ sudo touch /usr/local/openvswitch/dpdkvhostclient1
  $ sudo ovs-vsctl add-br [bridge name] -- set bridge [bridge name] datapath_type=netdev
  $ sudo ovs-vsctl add-port [bridge name] dpdkvhostclient0 \
    -- set Interface dpdkvhostclient0 type=dpdkvhostuserclient \
       options:vhost-server-path=/usr/local/openvswitch/dpdkvhostclient0
  $ sudo ovs-vsctl add-port [bridge name] dpdkvhostclient1 \
    -- set Interface dpdkvhostclient1 type=dpdkvhostuserclient \
       options:vhost-server-path=/usr/local/openvswitch/dpdkvhostclient1
  $
  $ sudo virsh edit [VM]
    <interface type='vhostuser'>
      <source type='unix'
        path='/usr/local/openvswitch/dpdkvhostclient0'
        mode='server'/>
      <model type='virtio'/>
    </interface>








