=======
xen
=======

(↓はたぶん)
xenはホストOS自体も Domain-0 というVMとして管理される．
それから，パテの話はまだよくわかってないのでまた後で．

ubuntu2004でxen環境構築
========================

::

  $ sudo apt install xen-hypervisor
  $ sudo vim /etc/default/grub.d/xen.cfg                  /// (多分だけど) ここである程度システムに対して小さい値を設定しないと，Domain-0に全部メモリ食われるんだと思う
    - #GRUB_CMDLINE_XEN_DEFAULT=
    + GRUB_CMDLINE_XEN_DEFAULT="dom0_mem=512M"
  $ sudo update-grub2
  $ sudo vim /etc/default/xendomains                      /// 終了時にdomUの状態を保持しないように?
    - XENDOMAINS_RESTORE=true
    + XENDOMAINS_RESTORE=false
  ###### 起動するカーネルをxenが組み込まれてるやつに変更する
  $ sudo vim /boot/grub/grub.cfg                          /// ここで設定すべきカーネルを確認する．後でちゃんとリンク貼るけどリンクのところみる．
  $ sudo vim /etc/default/grub                            /// なんかよくわからんけどsubmenu二つネストになってた．
  - GRUB_DEFAULT=0
  + GRUB_DEFAULT="Advanced options for Ubuntu GNU/Linux (with Xen hypervisor)>Xen hypervisor, version 4.11-amd64>Ubuntu GNU/Linux, with Xen 4.11-amd64 and Linux 5.4.0-26-generic"
  ####### ブリッジとかの設定がよくわかってない．

  $ sudo reboot

  $ uname -a                                              /// 起動したカーネルを確認してxenが組み込まれてるかをみておく
  $ sudo apt install libvirt-daemon-system libvirt-clients virtinst 
  $ sudo apt install libvirt-daemon-driver-xen
  $ sudo systemctl restart libvirtd
  $ sudo virsh uri                                        /// xen:///system があるかどうか確認しとく
  $ sudo virsh --connect=xen:///system                    /// 繋がるか確認しとく







参照

- https://www.osarusystem.com/misc/xen_dom0_create.html
- https://think-t.hatenablog.com/entry/20121013/p1









