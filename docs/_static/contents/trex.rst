=====
TRex
=====


iruyatu
========

::
    
  $ sudo apt install python python-pip
  $ sudo apt install linux-headers-`uname -r` build-essential

#ちょいちょいModuleNotFoundError: No module named 'distutils.util'が出るんだけど, 普通に実行できる時もあるしでながら動いてる時もあるしよくわからん. python3でやれってことなのか?

hardware environment
=====================

.. csv-table::
  :widths: 3, 3

  CPU, 3コア以上 
  memory, 2G以上(たぶん)
  インタフェース, 3つ以上(使用していないものが2つ以上)

install
========

::

  $ sudo mkdir -p /opt/trex && cd $_
  $ sudo wget --no-cache https://trex-tgn.cisco.com/trex/release/latest
  $ sudo tar -xzvf latest

hello world
============

利用できるポートの確認

::

  sudo ./dpdk_setup_ports.py -s

configをインタラクティブに作成 
使用するポートやアドレス等の設定
※履歴見たいのあとで付け足すかも

::

  sudo ./dpdk_setup_ports.py -i

これで設定ファイルが/etc/trex_cfg.yamlにできる．

テストトラフィック生成

:: 

 $ sudo ./t-rex-64 -f ./cap2/dns.yaml -d 10 

インタラクティブモードで実行してpingを飛ばしたりして確認とかもしたらよい．

::

  sudo ./t-rex-64 -i

※いつものDPDKのやつで実行した後はネットワークスタックからインタフェースが見えなくなる※


とりあえずトラフィック流す
============================


statless traffic生成
---------------------

stl/ にStateless traffic?用のpythonファイルがあるのでそれ使う．
trex_stl_libとかで書く．scapy使ってると思う．

e.g. stl/my_udp_1pkt.py

::

 from trex_stl_lib.api import *

  class STLS1(object):
  
      def __init__ (self):
          self.fsize  =64;
  
      def create_pkt_base (self):
          return Ether()/IP(src="10.1.0.2",dst="10.2.0.2")
  
      def create_stream (self):
          # Create base packet and pad it to size
          size = self.fsize - 4; # HW will add 4 bytes ethernet FCS
          base_pkt = self.create_pkt_base ()
          pad = max(0, size - len(base_pkt)) * 'x'
          pkt = STLPktBuilder(pkt = base_pkt/pad, vm = [])
  
          return STLStream(packet = pkt, mode = STLTXCont())
  
      def get_streams (self, direction = 0, **kwargs):
          # create 1 stream
          return [ self.create_stream() ]
  
  
  # dynamic load - used for trex console or simulator
  def register():
      return STLS1() 

パケットの確認
----------------

よくわからんけどなんかコマンドでpcapできるからそれ見て確認したらいい．

::

  $ sudo ./stl-sim -f stl/my_udp_1pkt.py -o ~/my_udp_1pkt.pcap

トラフィックを流す
------------------

インタラクティブモードでtrexを動かしておく
※デーモンにしてもいいんだろうけどインタラクティブモードにしとくとリアタイでトラフィック見える

::

  $ sudo ./t-rex-64 -i 

別のコンソールでtrexコンソールなるものを起動．コマンドラインで操作する．

::

  $ sudo ./trex-console

  # 送信例
  trex>start -p 0 -m 100kbps -f stl/my_udp_1pkt.py
  # 停止
  trex>stop
  # tuiモード(pkygen-dpdkみたいになるぜ．コンソールの画面サイズがある程度ないと怒られてエラる．
  trex>tui


command
===========

::

  $ sudo ./t-rex-64 -f <traffic_yaml> -m <rate multiplier>  -d <duration>  -l <latency test rate>  -c <cores> --lm <active port mask>

この使い方するとき，パケットはTCP/UDPパケットじゃないとダメみたい．

::

  ERROR packet 1 is not supported, should be Ethernet/IP(0x0800)/(TCP|UDP) format try to convert it using Wireshark !

って言われた．
https://trex-tgn.cisco.com/trex/doc/trex_manual.html#cml-line


yaml
======



参考
=====

https://trex-tgn.cisco.com/

https://foobaron.hatenablog.com/entry/2019/03/10/cisco-trex-traffic-generator-l3-stateless

