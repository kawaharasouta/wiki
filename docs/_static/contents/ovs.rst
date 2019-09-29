=============
Open vSwitch
=============


install
=======

::

  $ sudo apt install openvswitch-switch openvswitch-common

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
    <source bridge='ovs-sw'/>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x02' function='0x0'/>
    <virtualport type='openvswitch'/>
  </interface>
