==========
DHCP
==========



DHCPサーバ
=============

install

::

  $ sudo apt install isc-dhcp-server

::

  $ sudo vim /etc/dhcp/dhcpd.conf
  + subnet xxx.xxx.xxx.xxx netmask xxx.xxx.xxx.xxx {  
  +   range xxx.xxx.xxx.xxx xxx.xxx.xxx.xxx;        #範囲
  + }

  + host [hostname] { 
  +   hardware ethernet xx:xx:xx:xx:xx:xx;        #対象のインタフェースのアドレス
  +   fixed-address xxx.xxx.xxx.xxx; 
  + }

  + log-facility local7;                #コメント外すだけの場合多い

  $ sudo vim /etc/default/isc-dhcp-server           # インタフェース指定
  + INTERFACES=”eth0″

syslog(local7)の設定

::

  $ sudo vim /etc/rsyslog.d/50-default.conf
  + local7.* /var/log/dhcpd.log
  $ sudo systemctl restart syslog         # 本当はrsyslogぽい

最後に再起動

::

  $ sudo systemctl restart 




DHCPクライアント
==================
