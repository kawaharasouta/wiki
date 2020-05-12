====
kvm
====


注意
=======

BIOSでIntel-VT無効になっていても，KVMはQEMUで頑張ってVMを動かすらしいので，
普通にVM動かすだけだと気づかないこと多いから確認しろ．

::

  $ sudo kvm-ok                               ### ダメな例やぞ
    INFO: /dev/kvm does not exist
    HINT:   sudo modprobe kvm_intel
    INFO: Your CPU supports KVM extensions
    INFO: KVM (vmx) is disabled by your BIOS
    HINT: Enter your BIOS setup and enable Virtualization Technology (VT),
          and then hard poweroff/poweron your system
    KVM acceleration can NOT be used

https://momijiame.tumblr.com/post/92845673876/kvm-%E3%81%A8-proccpuinfo-%E3%81%AE%E5%BE%AE%E5%A6%99%E3%81%AA%E9%96%A2%E4%BF%82


package
=========
:: 

  $ sudo apt install qemu-kvm libvirt0 libvirt-bin bridge-utils virtinst libguestfs-tools

これいりそう

::

  $ sudo apt install virtinst         #virt-install

start config
=============
::

  $ sudo systemctl enable libvirt-bin

make image
===========
::

  $ sudo qemu-img create -f qcow2 /var/lib/libvirt/images/ubuntu1804.img 8G

install 
=========

serial 
-------
::

  # これだと成功するきっと location が url にしたら通った
  $ virt-install \
  --connect=qemu:///system \
  --name ubuntu1 \
  --vcpus 2 \
  --ram 2048 \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8 \
  --location 'http://jp.archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 

  # よく使われる --cdrom は --extra-args と併用できないのでこれダメ
  $ virt-install --connect=qemu:///system \
  --name ubuntu1 \
  --vcpus 1 \
  --ram 512 \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8 \
  --cdrom /var/lib/libvirt/boot/ubuntu-18.04.2-live-server-amd64.iso \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8'

  #centosの場合 (os-installerが変わるだけだから後でまとめたい
  #centosのCUIインストーラは結構癖ある．メニューから番号選んで叩いて設定すればいいだけ．
  #メモリが足りないとinitramfsが死ぬからちょっと多めにメモリあげる．
  $ virt-install \
  --connect=qemu:///system \
  --name centos7 \
  --vcpus 2 \
  --ram 2048   \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/centos7.img,size=8 \
  --location 'http://ftp.iij.ad.jp/pub/linux/centos/7/os/x86_64/' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 

  # fedora 24までしかなかったけどとりあえず通ったっぽい．
  # 他のミラーサイトみて install tree? installable distribution image? あること探した方がいいかも
  $ sudo virt-install \ 
  --connect=qemu:///system \ 
  --name fedora24 \
  --vcpus 2 --ram 2048 --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/fedora24.img,size=8 \
  --location 'http://ftp.iij.ad.jp/pub/linux/fedora/archive/fedora/linux/releases/24/Server/x86_64/os/' \ 
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8'


  # FreeBSD なんかだめそう1
  http://ftp.iij.ad.jp/pub/FreeBSD/releases/amd64/12.1-RELEASE/
  普通にiso落としてやってみたら
  isoinfo: Unable to find Joliet SVD
  sudo apt iunstall gparted ダメ

  # FreeBSD なんかダメそう2
  https://www.freebsd.org/ja/where.html
  こっから仮想マシンイメージゲットしてきて
  sudo virt-install --import --noreboot --name freebsd1201 --autostart --vcpus 2 --ram 2048 --accelerate --hvm --disk path=/var/lib/libvirt/images/freebsd1201.img --network network=default,model=virtio
  sudo virsh --connect qemu:///system start freebsd1201
  とかってやったらなんかとりあえず動いたの確認できたけどネットワークから見えなくてツムツムした．見えたけどsshd動いてなくて泣いた．

  # shuu先生ありがとうございます．． ちゃんと動いたやつ．
  isoファイルをダウンロードしたあと，マウントして中身を取り出して適当な場所におく．ちゃんとunmountする．
  $ wget https://download.freebsd.org/ftp/releases/amd64/amd64/ISO-IMAGES/12.1/FreeBSD-12.1-RELEASE-amd64-dvd1.iso
  $ mkdir fbsd1201-iso
  $ sudo mount -o loop,ro ./FreeBSD-12.1-RELEASE-amd64-dvd1.iso /mnt/freebsd1201-iso/
  $ sudo cp -av /mnt/freebsd1201-iso/* ./freebsd1201-iso/
  $ sudo umount /mnt/freebsd1201-iso/
  ブートローダのコンソールモードをCOMへ設定する．．らしいよ．．
  $ cd fbsd10-iso/
  $ echo 'console="comconsole"' > boot/loader.conf #ワンチャン権限で怒られます．
  ↑で変更した設定でisoファイルを作る．  
  $ sudo apt install genisoimage
  $ mkisofs -v -b boot/cdboot -no-emul-boot -r -J -V "FREEBSD_INSTALL" -o ~/Headless-FreeBSD.iso ./
  $ sudo qemu-img create -f qcow2 /var/lib/libvirt/images/freebsd.img 15G
  $ sudo virt-install --connect=qemu:///system --name freebsd \
    --vcpus 2 --ram 2048 \
    --serial pty -v \
    --disk=/var/lib/libvirt/images/freebsd.img,format=qcow2,bus=virtio --nographics \
    -c Headless-FreeBSD.iso  --network network=default,model=virtio

  なんかFreeBSDの can't find '/boot/entropy' とかの問題
  https://forums.freebsd.org/threads/installing-9-0-release-mounting-dvd-failed-with-error-19.36579/
  のところに書いてある
  mountroot> cd9660:/dev/cd0
  で解決してしまって．．
  この状態だとホストキーがなくてsshdが動いていないので，
  # ssh-keygen -A     # ホストキーを作る
  # /etc/rc.d/sshd start
  とすると動く．
  ちゃんとここまでやらないと中に入れないただの箱になるからマジ気を付ける．
  あと，あとで別のところにメモするけど，
  known_hostsで衝突があった時,
  ssh-keygen -R [hostname]
  とかってやるとknown_hostsの該当部分消してくれるんだってすごいね．

なんかこのURL指定してインストールする系のやつ，
キックスタートインストールとか行ってRHEL系だけなのか?よくわからんけど．
ubuntuもできたようなできなかったような気がするけどよくわからん．

なんかvirt-installのmanにlocationのURLここだぞって(おそらく)言ってるとこがあったから貼っとく

::
 
  Some distro specific url samples:

   Fedora/Red Hat Based
       http://download.fedoraproject.org/pub/fedora/linux/releases/25/Server/x86_64/os

   Debian
       http://ftp.us.debian.org/debian/dists/stable/main/installer-amd64/

   Ubuntu
       http://us.archive.ubuntu.com/ubuntu/dists/wily/main/installer-amd64/

   Suse
       http://download.opensuse.org/distribution/11.0/repo/oss/

   Mandriva
       ftp://ftp.uwsg.indiana.edu/linux/mandrake/official/2009.0/i586/

   Mageia
       ftp://distrib-coffee.ipsl.jussieu.fr/pub/linux/Mageia/distrib/1

ubuntu2020を(netboot?(locationでURL指定してやるやつ)で) インストールしようとした時，うまく入らなかった．
調べてみたらなんか面白そうな内容だったので別の記事にして書いておくことにする． :ref:`ubuntu2020_on_kvm`
ISOをwgetしてやる方法を↓に書いとく．ちなみに詳細?は↑の場所の記事に一緒に書いておくことにする．
ISOをマウントしてもできるはず(manにはそう書いてある)なんだけど，マウントした場合だとinstall中にmount errorみたいなのが起きてダメだったんだよね．

::

  #isoファイル選ぶから注意 ubuntu2020の場合はこれで行けた
  $ wget http://cdimage.ubuntu.com/ubuntu-legacy-server/releases/20.04/release/ubuntu-20.04-legacy-server-amd64.iso
  $ virt-install \
  --connect=qemu:///system \
  --name ubuntu1 \
  --vcpus 2 \
  --ram 2048 \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8 \
  --location 'path to iso file' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 


ubuntu1604が入らない話
https://www.mckelvaney.co.uk/blog/2019/04/17/ubuntu-16.04-loading-libc-udeb-failed-for-unknown-reasons-aborting/

centos7でメモリが足りなくてinitramfsがエラる話
https://www.centos.org/forums/viewtopic.php?t=67350

locationをどうするかみたいな
https://qiita.com/t_niimura/items/5991c8a2d07b94c06bce

FreeBSD参照先
http://syuu1228.hatenablog.com/entry/20130511/1368267757
http://vega.pgw.jp/~kabe/bsd/fb10-qemu-kvm.html
https://forums.freebsd.org/threads/installing-9-0-release-mounting-dvd-failed-with-error-19.36579/
https://forums.freebsd.org/threads/mount-cdrom.60063/

vnc
-----
::

  $ sudo virt-install \
    --name ubuntu1804 \
    --disk path=/var/lib/libvirt/images/ubuntu1804.qcow2,size=8 \
    --vcpus 2 \
    --ram 512 \
    --os-type linux \
    --graphics vnc,port=5900,listen=0.0.0.0,keymap=us,password=passwd \
    --network bridge:virbr0 \
    --cdrom /var/lib/libvirt/boot/ubuntu-18.04.2-live-server-amd64.iso 

clone
=========

::

  $ sudo virt-clone --original [vm_org] --name [vm_clone] --file /var/lib/libvirt/images/[vm_clone].img   # .imgを作成しておく必要はない
  $ sudo virt-sysprep -d [vm_clone] --enable dhcp-client-state,machine-id,net-hwaddr             # dhcp clientリースだけで良いはずだが一応

and change hostname 


change memory size
===================

::

  #max memory sizeを変更
  $ sudo virsh setmaxmem [domain] 4G

  #起動中にmemory size変更(停止したら戻る)
  $ sudo viesh setmem [domain] 4G

  #停止中のマシンの次回以降のmemory sizeを変更
  $ sudo virsh setmem [domain] 4G --config

  #確認
  $ sudo virsh dominfo [domain] | grep mem

extend disk size
=================

まだ書き終わってない
http://b.ruyaka.com/2014/05/08/kvm-guest-os-increase-disc/
これ見て書く

::

  # 現在の容量確認
  $ sudo qemu-img info [vm].img
  # 拡張
  $ sudo qemu-img resize [vm].img +10G      



rename domain 
===============

::
  
  $ uuidgen           #コピっとく
  $ sudo virsh edit [old domain]
    change name & uuid
  $ sudo virsh undefine [old domain]

file focation
==============
::

  vm images         /var/lib/libvirt/images/
  iso images          /var/lib/libvirt/boot/    ←???
  xml file                /etc/libvirt/qemu/
  network file       /etc/libvirt/qemu/networks/

ブリッジ接続
=============

Linux bridge
-------------

ブリッジ作成してそこに物理インタフェースぶっこむだけ.
インタフェースとブリッジのリンク上げ忘れよくするから注意.
なんか知らないけどグローバルに向けられない．

ovs
-------

macvtap, macvlan
------------------

ゲストのxmlファイルを

::

  <interface type='direct'>
    <mac address='52:54:00:94:9a:a0'/>
    <source dev='eth0' mode='bridge'/>    #devがtapでも動いた
    <model type='virtio'/>
    <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
  </interface>

とかするとブリッジ接続されるが，ホストの物理インタフェース(ここではeth0はvlanの外と見なされてホストとゲストが通信ができない．
そこでmacvlanを使う．
ホストで

::

  $ sudo ip link add dev macvlan0 link eth0 type macvlan mode bridge
  $ sudo ip addr del <address> dev eth0
  $ sudo ip addr add <address> dev macvlan0
  $ sudo ip link set up dev macvlan0
  $ sudo ip route add default via <default route> (dev ~~)

とするとホストとゲストで接続可能になる．
参考: macvlan_

add nic 
==========

e1000

::

  <interface type='bridge'>
    <source bridge='virbr0'/>
    <model type='e1000'/>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x02' function='0x0'/>
  </interface>

virtio

::
  
  <interface type='bridge'>
    <source bridge='virbr0'/>
    <model type='virtio'/>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x02' function='0x0'/>
  </interface>
  

ブリッジがovsの場合

::

  <interface type='bridge'>
    <source bridge='ovs-sw'/>
    <address type='pci' domain='0x0000' bus='0x01' slot='0x02' function='0x0'/>
    <virtualport type='openvswitch'/>
  </interface>

SR-IOV
==========

::

  $ sudo vim /etc/default/grub
  + GRUB_CMDLINE_LINUX="intel_iommu=on"
  $ sudo update-grub2

wakarann

ubuntu image download
=========================

::

  $ wget http://ftp-srv2.kddilabs.jp/Linux/packages/ubuntu/releases-cd/18.04.3/ubuntu-18.04.3-live-server-amd64.iso


vm ip addr
===========

VMのアドレス探すやつだけど，arp-scanじゃなくていいの見つけてしまった．

::

  $ sudo arp-scan -I virbr0 -l | awk '{print $1}' | tail -n 6 | head -n3    #オプションは適当
  $ sudo virsh net-dhcp-leases default | awk '{print $5, $6}'

接続方法とかに関して
=======================

接続方法は多分
- ssh
- console
- virt-manager
- virt-viewer
- vnc
くらいしかないと思う．
そのうちvirt-manager, virt-viewerはGUIで，
vncはお外から見える環境がちゃんと整っていれば．
sshはもちろんsshdが動いてないとで
consoleはちゃんとカーネルパラメータ設定してからじゃないと無理．

reference
===========

domain_xml_format_  

network_xml_format_  

virsh_



.. _macvlan: https://tenforward.hatenablog.com/entry/20111221/1324466720
.. _domain_xml_format: https://libvirt.org/format.html
.. _network_xml_format: https://libvirt.org/formatnetwork.html#examplesBridge
.. _virsh: http://lipix.ciutadella.es/wp-content/uploads/2016/09/kvm_cheatsheet.pdf
