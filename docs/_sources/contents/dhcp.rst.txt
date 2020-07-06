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
  +   host [hostname] {                             # 固定したいホスト
  +   hardware ethernet xx:xx:xx:xx:xx:xx;
  +   fixed-address xxx.xxx.xxx.xxx;                # 実際に振る値はrengeと被らせないように注意
  + }

  + host [hostname] { 
  +   hardware ethernet xx:xx:xx:xx:xx:xx;          # 自分の対象のインタフェースのアドレス
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


static routes の配布
https://gauvain.pocentek.net/docs/dhcpd-push-routes/
https://qiita.com/kyokuheki/items/ccf770c6475a236d2035


DHCPクライアント
==================

::

  $ sudo vim /etc/netplan/01-netcfg.yaml          # なんかファイル名いろいろあってよくわからん

  network:
    version: 2
    renderer: networkd
    ethernets:
      enp1s2:
        dhcp4: yes

