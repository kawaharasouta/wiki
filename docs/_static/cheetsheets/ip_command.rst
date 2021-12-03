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
ついでに nmcli も並べておく
(ちょっとめもりたいのでまあとりあえずいつかかえよ)

.. csv-table::
  :header: 動作, net-tools, iproute, nmcli
  :widths: 15, 15, 15, 15

  arp table表示,              arp -a,                           ip neigh
  ,                           arp -v,                           ip -s neigh
  arp tableエントリ追加,      arp -s 192.168.1.1 1:2:3:4:5:6,   ip neigh add 192.168.1.1 lladdr 1:2:3:4:5:6 dev eth1 
  arp tableエントリ削除,      arp -i eth1 -d 192.168.1.1,       ip neigh del 192.168.1.1 dev eth1
  インタフェースアドレス表示, ifconfig -a,                      ip a
  interface link down,        ifconfig eth0 down,               ip link set down dev eth0
  interface link up,          ifconfig eth0 up,                 ip link set up dev eth0
  interface add addr,         ifconfig eth0 192.168.0.1,        ip addr add 192.168.0.1/24 dev eth0
  set mtu,                    ifconfig eth0 mtu 9000,           ip link set eth0 mtu 9000
  ,                           netstat,                          ss
  ,                           netstat -neopa,                   ss -neopa
  ,                           netstat -g,                       ip maddr
  ip table 表示,              route,                            ip route 
  set default gate way,       route add default gw 192.168.1.1, ip route add default via 192.168.0.1

brctl と iprouteの比較

.. csv-table::
  :header: 動作, brctl, iproute, nmcli
  :widths: 6, 6, 6, 6

  ブリッジ追加,           brctl addbr [bridge],       ip link add [bridge] type bridge,                                                 nmcli con add type bridge ifname [bridge]
  ブリッジ削除,           brctl delbr [bridge],       ip link del [bridge]
  対象のブリッジのIF表示, brctl show [bridge],        ip link show master [bridge] (or bridge link show [bridge] ※ 期待通りに動作しない
  全ブリッジのIF表示,     brctl show,                 bridge link show 
  IF追加,                 brctl addif [bridge] [if],  ip link set dev [if] master [bridge],                                             nmcli con add [bridge(con)] bridge-slave ifname [if] master [bridge(con)]
  IF削除,                 brctl delif [bridge] [if],  ip link set dev [if] nomaster


rxqueueを変更?
-----------------

::

  sudo ip link set dev dum0 numtxqueues 10



references
------------

 - https://access.redhat.com/sites/default/files/attachments/rh_ip_command_cheatsheet_1214_jcs_print_ja4.pdf
 - https://developers.redhat.com/blog/2018/10/22/introduction-to-linux-interfaces-for-virtual-networking/
