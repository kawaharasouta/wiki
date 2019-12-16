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
