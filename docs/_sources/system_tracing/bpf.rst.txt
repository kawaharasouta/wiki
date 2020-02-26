=======
BPF
=======

Berkeley Packet Filterの略．現在はパケットフィルタ以外のOS用途で使われる．
eBPFとかに拡張されてる．XDPもこれを用いたもの．















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











リンク
=========

オリジナルのbpfに関する論文
http://www.tcpdump.org/papers/bpf-usenix93.pdf

BPFの日本語超記事
https://www.atmarkit.co.jp/ait/articles/1811/21/news010.html

