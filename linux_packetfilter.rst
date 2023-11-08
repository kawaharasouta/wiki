======================
Linux PacketFilter
======================

Linuxのパケットフィルタ手法?(と言っていいのかわかんないけど)のうち，nftables, iptables, tc(qdisc, QoS)あたりの話を書きたい．
iptablesについては書かないかもしれない．firewalldについては書く気ない．

Netfilterのはなしもちゃんと書きたいけどそのうち．


nftables
==============


*参考*
https://knowledge.sakura.ad.jp/22636/
https://wiki.nftables.org/wiki-nftables/index.php/Main_Page

細かい説明は上のページに任せる．



Hello world -ICMP requestをdropしてpingに応答しないようにする-
---------------------------------------------------------------------







tc(qdisc, QoS)
===================


