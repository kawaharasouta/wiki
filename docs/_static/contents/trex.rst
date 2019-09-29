=====
TRex
=====


iruyatu
========

::
    
  $ sudo apt install python python python-pipa
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

  $ sudo mkdir -p /opt/trex
  $ cd /opt/trex
  $ sudo wget --no-cache https://trex-tgn.cisco.com/trex/release/latest
  $ sudo tar -xzvf latest

hello world
============

利用できるポートの確認

::

  sudo ./dpdk_setup_ports.py -s

configをインタラクティブに作成 ※履歴見たいのあとで付け足すかも

::

  sudo ./dpdk_setup_ports.py -i


トラフィック生成

:: 

 $ sudo ./t-rex-64 -f ./cap2/dns.yaml -d 10 


※実行した後はネットワークスタックからインタフェースが見えなくなる※


