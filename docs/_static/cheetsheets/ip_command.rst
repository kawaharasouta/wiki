ip command
===========

netns関連いろいろ
-----------------

**ns0というnetnsを作成**

::

  sudo ip netns add ns0

**ns0にネットワークインタフェースeth6を割り当てる**

::

  sudo ip link set netns ns0 dev eth6 

**ne0を削除**

::

  sudo ip netns del ne0

**現在自分がいるnetns名を取得する**

::

  ip netns identify

**netns全削除**

::
  
  sudo ip -all netns delete


**vethの追加**

::

  $ ip link add [veth name] type veth peer name [veth peer name]

net-tools と iprouteの比較

.. csv-table::
  :header: 効果, net-tools, iproute
  :widths: 15, 15, 15

  arp table表示, arp -a, ip neigh
  , arp -v, ip -s neigh
  arp tableエントリ追加, arp -s 192.168.1.1 1:2:3:4:5:6, ip neigh add 192.168.1.1 lladdr 1:2:3:4:5:6 dev eth1 
  arp tableエントリ削除, arp -i eth1 -d 192.168.1.1, ip neigh del 192.168.1.1 dev eth1
  インタフェースアドレス表示, ifconfig -a, ip a
  interface link down, ifconfig eth0 down, ip link set down dev eth0
  interface link up, ifconfig eth0 up, ip link set up dev eth0
  interface add addr, ifconfig eth0 192.168.0.1, ip addr add 192.168.0.1/24 dev eth0
  set mtu, ifconfig eth0 mtu 9000, ip link set eth0 mtu 9000
  , netstat, ss
  , netstat -neopa, ss -neopa
  , netstat -g, ip maddr
  ip table 表示, route, ip route 
  set default gate way, route add default gw 192.168.1.1, ip route add default via 192.168.0.1


references
------------

 - https://access.redhat.com/sites/default/files/attachments/rh_ip_command_cheatsheet_1214_jcs_print_ja4.pdf
 - https://developers.redhat.com/blog/2018/10/22/introduction-to-linux-interfaces-for-virtual-networking/
