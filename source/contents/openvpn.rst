==========
OpenVPN
==========

easy install
=============

::

  $ curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
  $ chmod +x openvpn-install.sh
  $ sudo ./openvpn-install.sh

clientfileは .ovpn で落ちてる．

参照: https://github.com/angristan/openvpn-install

install
========

::

  $ sudo apt install -y openvpn easy-rsa
  $ make-cadir ~/ca
  $ cd ~/ca

  $ vim vars
  - #export KEY_CONFIG=`$EASY_RSA/whichopensslcnf $EASY_RSA`
  + export KEY_CONFIG="$EASY_RSA/openssl-1.0.0.cnf"

  e export KEY_COUNTRY="JP"
  e export KEY_PROVINCE="KN"
  e export KEY_CITY="TOKYO"
  e export KEY_ORG="geregere.work"
  e export KEY_EMAIL="kawahara6514@gmail.com"
  e export KEY_OU="MyOrganizationalUnit"

  $ source vars

なんか突然強いの↑出てきたから書くのやめる．
もしこっちが必要になった時のために一応残しとく

参照: https://wings2fly.jp/yaneura/openvpn/



vpnサーバのローカルネットワークにアクセスするための設定とか
=============================================================

※正直設定ファイル系はどれが本当にいるやつなのかいまいちわからん．．．
※openvpn-startupとか自動で動かんし．．．


ローカルネットワークへの経路を追加しとくやつ．

::

  sudo vim /etc/openvpn/server.conf
  + push "route 192.168.200.0 255.255.255.0"        //アドレスは環境で適当に変えろよ


．．．．
これ以降の設定ファイル系はあとで下に書いてあるリンク見直して書き直すんだ．．．
でも正直どれが必要でどれがいらない子なのかわからなくてめんどくさいのだ．．．



ローカルにいるマシンに対して，vpnネットワークからのアクセスを許す(ファイアウォール的な意味で)のと，
vpnネットワークへのルーティング情報を足しとく．
※ファイアウォールに関しては僕の環境だとしなくてよかったけどとりあえずダメだったらこんなふうにしたら良さげだよね的なのだけ書いてある．※

::
  
  # ファイアウォール設定
  $ sudo iptables -I INPUT -s 10.8.0.0/24 -j ACCEPT
  $ sudo iptables -I OUTPUT -d 10.8.0.0/24 -j ACCEPT
  # ルーティング
  $ sudo ip route add 10.8.0.0/24 via 192.168.200.1 dev [ローカルネットワークのインタフェース]

参考:
https://centossrv.com/openvpn.shtml
https://teratail.com/questions/140736
https://www.4web8.com/1171.html


クライアント
===============

ubuntu
--------

CUI

::

  $ sudo apt install network-manager-openvpn
  $ sudo openvpn --config [path to ovpn file]


GUI

::

  $ sudo apt install network-manager-openvpn-gnome

あとは適当にGUIでやる．

mac
-----

tunnelblickにovpn食わせて雑にやる．





