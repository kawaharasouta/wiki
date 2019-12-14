=========
BPFとは
=========

Berkeley Packet Filterの略．現在はパケットフィルタ以外のOS用途で使われる．
eBPFとかに拡張されてる．XDPもこれを用いたもの．
多分ここではBPFの話はほとんでしない．eBPFかXDPの話だけすると思う．


install
========

カーネルコンフィグ

https://github.com/iovisor/bcc/blob/master/INSTALL.md#kernel-configuration

ここ見ればいい．
結構最初から設定されてる気がする．


::
  
  $ sudo apt-get install -y \
    bpfcc-tools python3-bpfcc \
    linux-headers-`uname -r`
