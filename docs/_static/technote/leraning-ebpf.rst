==================
Learning eBPF
==================

入門eBPFを読んでいてのメモなどを書いておくことにする．
(このページは削除する可能性がある．)

本書(の内容限定版?)はisovalentの次のリンクから取得が可能．
https://isovalent.com/books/learning-ebpf/

example code は
https://github.com/lizrice/learning-ebpf


その他の参照先
 - https://gihyo.jp/admin/serial/01/ubuntu-recipe/0690
 - https://github.com/iovisor/bcc/blob/master/docs/reference_guide.mD



環境
==================

本書のexample codeはubuntu2204上での動作が確認されていて環境構築の情報もそのためのものしかない．
fedoraでやりたい．

::

  $ cat /etc/fedora-release
  Fedora release 38 (Thirty Eight)
  $ uname -r
  6.2.9-300.fc38.x86_64

package

::

  $ dnf install clang llvm jq
  $ dnf groupinstall "C Development Tools and Libraries"

  //! libbfd-devに対応するパッケージがわからない．というかもっと言うとlibbfdとbintuilsの関係がよくわからん．今後ちゃんと動くかなど要調査
  $ dnf install elfutils-libelf-devel libpcap-devel binutils-devel
  
  $ dnf install kernel-tools

  $ dnf install bcc-tools
  //! 本当に必要なもの的にいうとpython3-bcc(とその依存)らしいのだが，本書に合わせておく．
  //! ちなみに，python3-bccをweek dependencisにbcc-toolsがあるみたいで，環境にもよると思うが現環境ではどちらを指定してもまったく同じ数種類のパッケージが依存でインストールされる

  //! pipは必要ならあとでいれるからいいやあ


linux-tools-commonとkernel-toolsの根拠 https://wiki.onakasuita.org/pukiwiki/?linux-tools-common
::


  $ dnf repoquery --list kernel-tools | grep -e turbostat -e usb -e perf
  Last metadata expiration check: 0:51:24 ago on Mon 08 Jan 2024 11:50:56 PM JST.
  /usr/bin/turbostat
  /usr/bin/x86_energy_perf_policy
  /usr/share/man/man8/turbostat.8.gz
  /usr/share/man/man8/x86_energy_perf_policy.8.gz
  /usr/bin/turbostat
  /usr/bin/x86_energy_perf_policy
  /usr/share/man/man8/turbostat.8.gz
  /usr/share/man/man8/x86_energy_perf_policy.8.gz

