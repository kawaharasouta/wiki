====
kvm
====

※virsh系の操作の多くは sudo いらない(libvirtグループで管理できるのでね)からひとまず目についた分は消して見たけど
一部反映不足あるかもしれないので気づいたらなおそう．

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


ubuntu_kvm_installation_

ダメな例だったらやること

::

  ### とりあえずBIOSで有効にしてくる
  $ lsmod | grep kvm
  kvm と kvm_intel がなかったら
  $ sudo modprobe -r kvm_intel      // kvm も一緒にロードされる


package
=========
:: 

  $ sudo apt install qemu-kvm libvirt0 libvirt-bin bridge-utils virtinst libguestfs-tools

  //! ubuntu2004 (>=1810?) toriaezu
  $ sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst libguestfs-tools

  //! fedora34 toriaezu
  $ sudo dnf install qemu-kvm libvirt virt-install guestfs-tools

  //! rpm distoro (ofcource fedora, centos stream) can groupinstall
  $ sudo dnf groupinstall @virtualiztion

"Getting started with virtualization (on fedora)"
https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-virtualization/


  //! この後一応 libvirtd 起動とか自動起動しとく
  //!!!!!!!!!!!!!!!!!!!!!!!!!!! i'll write about it soon
  $ sudo systemctl enable --now libvirtd

ubuntu2004での変更点とか?
https://wiki.ubuntu.com/FocalFossa/ReleaseNotes/Ja の libvirt のところみる

::

  Ubuntu 18.04 において、単体のモノリシックなパッケージであったlibvirt-binから、以下の3つのメインコンポーネントに分割されました:
  libvirt-daemon-system - 設定とsystemdのサービスファイル群によるデーモンのシステム統合（これは、古いlibvirt-bin最も似ているパッケージです）
  libvirt-clients - virshのようなlibvirtに関連したcliツール群
  libvirt-daemon - サービス群や設定を除いたlibvirtデーモンのみ
  同様に、めったに使用されずサポートが少ないvirtualboxやxenコントロールなどのサブ機能、一般的でないストレージオプションが、さまざまなlibvirt-daemon-driver-*パッケージに分割されました。 これにより、インストール時の専有領域とインストール時の大部分のアクティブコードを削減できます。
  パッケージとプロジェクトには十分な移行時間があったため、libvirt-daemon-system + libvirt-clientsを取り込む空の互換性パッケージであるlibvirt-binがついに削除されました。古い名前を参照しているスクリプトまたはサードパーティのコンポーネントがある場合は、上記のリストを使用して最も新しいパッケージを選択してください。

fedora(というかdebian系以外)だと一般ユーザvirsh listとかとかでちゃんとVMが見えないみたいな話1
=================================================================================================

詳しい話は後ろでやる．ここでは操作だけ．

::

  //! ユーザを libvirt グループに追加
  $ sudo usermod -a -G libvirt $(whoami)

  //! デフォルトの接続ドメインを設定
  $ vi $XDG_CONFIG_HOME/libvirt/libvirt.conf
    + uri_default = "qemu:///system"

start config
=============
::

  $ sudo systemctl enable libvirt-bin

  # ???
  $ sudo systemctl enable libvirtd

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
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8,format=raw \
  --location 'http://jp.archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 

  # よく使われる --cdrom は --extra-args と併用できないのでこれダメ
  $ virt-install --connect=qemu:///system \
  --name ubuntu1 \
  --vcpus 1 \
  --ram 512 \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8,format=raw \
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
  --disk path=/var/lib/libvirt/images/centos7.img,size=8,format=raw \
  --location 'http://ftp.iij.ad.jp/pub/linux/centos/7/os/x86_64/' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 

  /////// centos8のlocationは http://ftp.iij.ad.jp/pub/linux/centos/8/BaseOS/x86_64/os/
  /////// centos8のtextモードのインストールでなんかユーザ作成しても反映されず，グループだけ残ってしまってて厄介だったんだけども

  # fedora 24までしかなかったけどとりあえず通ったっぽい．
  # 他のミラーサイトみて install tree? installable distribution image? あること探した方がいいかも
  $ virt-install \ 
  --connect=qemu:///system \ 
  --name fedora24 \
  --vcpus 2 --ram 2048 --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/fedora24.img,size=8,format=raw \
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
  $ virt-install --import --noreboot --name freebsd1201 --autostart --vcpus 2 --ram 2048 --accelerate --hvm --disk path=/var/lib/libvirt/images/freebsd1201.img --network network=default,model=virtio
  virsh --connect qemu:///system start freebsd1201
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
  $ virt-install --connect=qemu:///system --name freebsd \
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

ubuntu2004を(netboot?(locationでURL指定してやるやつ)で) インストールしようとした時，うまく入らなかった．
調べてみたらなんか面白そうな内容だったので別の記事にして書いておくことにする． 
:ref:`ubuntu2004_on_kvm`
ISOをwgetしてやる方法を↓に書いとく．ちなみに詳細?は↑の場所の記事に一緒に書いておくことにする．
ISOをマウントしてもできるはず(manにはそう書いてある)なんだけど，マウントした場合だとinstall中にmount errorみたいなのが起きてダメだったんだよね．

**2021/09/04追記**
ubuntu2004でもnetinstallできた．
urlは http://jp.archive.ubuntu.com/ubuntu/dists/focal/main/installer-amd64/

::

  #isoファイル選ぶから注意 ubuntu2004の場合はこれで行けた コマンドコピペ直してないところあるけど使う時に合わせろあとで直す．
  $ wget http://cdimage.ubuntu.com/ubuntu-legacy-server/releases/20.04/release/ubuntu-20.04-legacy-server-amd64.iso
  ####  なんか↑notfoundしたので (20.04がなくて20.04.1だけになってた)
  $ wget http://cdimage.ubuntu.com/ubuntu-legacy-server/releases/20.04/release/ubuntu-20.04.1-legacy-server-amd64.iso
  $ virt-install \
  --connect=qemu:///system \
  --name ubuntu1 \
  --vcpus 2 \
  --ram 2048 \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8,format=raw \
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

  $ virt-install \
    --name ubuntu1804 \
    --disk path=/var/lib/libvirt/images/ubuntu1804.qcow2,size=8,format=raw \
    --vcpus 2 \
    --ram 512 \
    --os-type linux \
    --graphics vnc,port=5900,listen=0.0.0.0,keymap=us,password=passwd \
    --network bridge:virbr0 \
    --cdrom /var/lib/libvirt/boot/ubuntu-18.04.2-live-server-amd64.iso 


imageのみ入手された場合
-------------------------

オプション "--import" を付けることで，imageだけ入手できた場合もvirt-installでlibvirtに取り込んで管理のうえ動作させることができる．
後述されるvirt-builderでイメージを作成した場合もこの方法で取り込むことができる．
以下はコマンド実行例．

locationを設定していない関係上--extra-argsが設定できなく，consoleがつながらない可能性もあるので注意が必要．
(作成したimageにこの辺りの設定がされていなかったらつながらない．)
(ちなみに対象OSにもよるかもしれないが，今のところvirt-builder作るイメージはコンソール接続できている．)

::

  $ virt-install --connect=qemu:///system \
  --name ztemplate-fedora38 \
  --vcpus 2 --ram 2048 --accelerate --import \
  --disk path=/var/lib/libvirt/images/ztemplate-fedora38.img \
  --network network=default,model=virtio \
  --nographics


console接続について
======================

環境というかOSによってインストール後もそのままconsole接続できるやつとできないやつがいる．
ちなみに今確認しできているのだと

::
 
  できる: centos8(あと一応asianux)
  できない: ubuntu2004 ubuntu1804

多分これはextraargsで渡したカーネルオプションがそのまま使われているかインストール後初期化されてるかみたいなそう言う話だとは思う．

さらに，ubuntuではvirt-install時に--locationでnetwork installerから起こさないと--extra-argsが使えないためちゃんとインストールができない．
(要は--cdromでISOイメージを指定する方法だとうまくserialでインストールできないということ)
詳細はわからないが，https://blog.cybozu.io/entry/3792 ここを読むと少しわかるかもしれない．
また，このコンソール系のカーネルオプションの説明は https://www.support.nec.co.jp/View.aspx?id=3150110824 を読むと少しわかるかもしれない．

できない奴らは↓をやっておくと幸せになれる．

::

  $ sudo vim /etc/default/grub
    + GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200n8"        //! 他に追加で書いてあるやつは残しておいたほうがいい．起動時のログをどの程度出すか的な設定がデフォルトで入ってるので．
  $ sudo update-grub2
  $ sudo reboot


clone
=========

virt-sysprep の man より
You do not need to run virt-sysprep as root.  In fact we'd generally recommend that you don't.  The time you might want to run it as root is when you need root in order to access the disk image, but even in this case it would be better to change the permissions on the disk image to be writable as the non-root user running virt-sysprep.
らしいので，下のコマンドsudoなしのがいいけど，上にも書いてあるように，libvirtのディレクトリはだいたいsudoないとたどり着けないので，
そのあたりも考えて手順を作る必要がありそう．

::

  $ virt-clone --original [vm_org] --name [vm_clone] --file /var/lib/libvirt/images/[vm_clone].img    # .imgを作成しておく必要はない
  $ sudo virt-sysprep -d [vm_clone]                   # operations は 指定しないとすべて (というか man には most と書いてあるけど) になるはずなので指定しない．

and change hostname 


clone 用の template を作る場合，先に virt-sysprep しておいて，それを virt-clone するといい．


テスト用VMイメージの簡単な作り方
==================================

virt-builderコマンドでminimalなVMイメージの作成ができる．libguestfsのソフトウェア．
外部と通信を行うのでproxy環境などでは注意が必要．

::

  //! 作成可能なOS一覧
  $ virt-builder --list

  //! コマンド実行例
  $ virt-builder fedora-38 \
  --size 8G --format raw \
  --hostname ztemplate-fedora38 \
  --root-password 'password:root' \
  --ssh-inject root \
  -o /var/lib/libvirt/images/ztemplate-fedora38.img \
  --selinux-relabel


参考情報: 
 - "virt-builder - Build virtual machine images quickly": https://www.libguestfs.org/virt-builder.1.html
 - "virt-builderでUbuntuのVMイメージを作成する": https://qiita.com/masru0714/items/05d262d1ced5c32023f2 
 - "virt-builderによるLinuxインストールの「省略」": https://endy-tech.hatenablog.jp/entry/virt_builder 


delete vm
==============

::
  
  $ virsh undefine [vm]
  $ virsh pool-list
  $ virsh vol-list [pool]
  $ virsh vol-delete [path to vol]

次のようにオプションを指定してundefineすると一緒にボリュームも消してくれていい感じ．
詳しくはmanを参照のこと．

::

  $ virsh undefine --remove-all-storage [vm]



change memory size
===================

::

  #max memory sizeを変更
  $ virsh setmaxmem [domain] 4G

  #起動中にmemory size変更(停止したら戻る)
  $ virsh setmem [domain] 4G

  #停止中のマシンの次回以降のmemory sizeを変更
  $ virsh setmem [domain] 4G --config

  #確認
  $ virsh dominfo [domain] | grep mem

extend disk size
=================

下の方に詳しく書いた．


rename domain 
===============

::
  
  $ uuidgen           #コピっとく
  $ virsh edit [old domain]
    change name & uuid
  $ virsh undefine [old domain]

file location
==============
::

  vm images         /var/lib/libvirt/images/
  iso images          /var/lib/libvirt/boot/
  xml file                /etc/libvirt/qemu/
  network file       /etc/libvirt/qemu/networks/
  autostart file    /etc/libvirt/qemu/autostart/

isoファイルをローカルにダウンロードしてVMのOSインストール時に利用する場合，上にある "/var/lib/libvirt/boot" 配下に置くべし．
この時，RHEL系だとqemu, debian系だとlibvirtユーザー/グループでのアクセス権限がないとインストールに失敗する．
事前に以下のコマンドを実行してパーミッションを設定しておくと良し．

::

 $ sudo chown :libvirt /var/lib/libvirt/boot
 $ sudo chmod g+rws /var/lib/libvirt/boot

参考:  
上記の設定方法について
https://wiki.wut.ee/sysadmin/libvirt
パーミッションについて
https://wiki.archlinux.jp/index.php/%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E3%83%91%E3%83%BC%E3%83%9F%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%A8%E5%B1%9E%E6%80%A7
https://docs.oracle.com/cd/E19455-01/806-2718/secfiles-69/index.html

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

PCI passthrough
=================

BIOSでIOMMU拡張を有効化する．
なんかよくわからんけど「Intel VT-d」「I/O Virtualization Technology」とからへん?

::

  ### ブートオプションでiommuを有効化
  $ sudo vim /etc/default/grub
  - GRUB_CMDLINE_LINUX=
  + GRUB_CMDLINE_LINUX="intel_iommu=on"

  ### iommuグループの確認??  グループ単位でしかpassthroughできないみたいなんだけど，VMに渡すときは普通にアドレスで指定するからよくわからんけど
  $ vim iommu.sh
  #!/bin/bash
  shopt -s nullglob
  for d in /sys/kernel/iommu_groups/*/devices/*; do
      n=${d#*/iommu_groups/*}; n=${n%%/*}
      printf 'IOMMU Group %s ' "$n"
      lspci -nns "${d##*/}"
  done;
  $ bash iommu.sh

  ### 適当に対象のデバイスのアドレスを確認しとく
  ### なんかGPUの場合とかゲストがwindowsの場合とか少し追加でやることあるらしいけど今はNICだけなので後で調べる

  ### 適当に編集する．
  $ virsh edit [vm]
  + <hostdev mode='subsystem' type='pci' managed='yes'>
  +   <source>
  +     <address domain='0x00' bus='0x5e' slot='0x10' function='0x00'/>           // 5e:10.0 の場合
  +   </source>
  + </hostdev>


これで実行したらホストからデバイスが見えなくなってゲストに見えるようになってる．
VMを停止(shutdown)したらデバイスは帰ってきた．

http://kt-hiro.hatenablog.com/entry/20150616/1434434879

https://www.nexia.jp/server/1802/

http://uramocha02.blogspot.com/2017/01/pciiommu.html



SR-IOV (Single Root I/O Virtualization)
==========================================

仕様が書いてある? https://pcisig.com/

利用可能なintel nic: https://www.intel.co.jp/content/www/jp/ja/support/articles/000005722/network-and-io/ethernet-products.html

とりあえずpci-passthroughできる環境にしておく．

とりあえずmodprobeし直してやる方法(/etc/modrobe.d/ に構成ファイルおいとくのが本当はいいのだけれどまだ試してないので後で)
そして，X540-t2(と言うかixgbeなのだけれど)の場合．

::

  $ sudo modprobe -r ixgbe
  $ sudo modprobe ixgbe max_vfs=16        // 最大63だと思う
  $ sudo modprobe -r ixgbevf              // ホストにバカほどvfが生えるのでホストでは外しとく

ちなみに，vfの元になってるインタフェースがちゃんとUPしてないとvfはUPしないでnetlink error出る．
ナンバリングはまだよくわからんけどどうもジグザグっぽい?
それから，同じ物理IFのvf同士はlinkはつながってない感じある．


ubuntu image download
=========================

::

  $ wget http://ftp-srv2.kddilabs.jp/Linux/packages/ubuntu/releases-cd/18.04.3/ubuntu-18.04.3-live-server-amd64.iso


vm ip addr
===========

VMのアドレス探すやつだけど，arp-scanじゃなくていいの見つけてしまった．

::

  $ sudo arp-scan -I virbr0 -l | awk '{print $1}' | tail -n 6 | head -n3    #オプションは適当
  $ virsh net-dhcp-leases default | awk '{print $5, $6}'

virt-net の技術(ハック)・ソフトウェア関連の情報
=================================================

まずdnsmasqがDHCPサーバとDNSフォワーディングを担当している．
https://wiki.archlinux.jp/index.php/Dnsmasq
::

  dnsmasq は、DNS サーバー、DHCPv6 と PXE をサポートする DHCP サーバー および TFTP サーバー を提供します。また、dnsmasq は DNS クエリをキャッシュし、過去に訪問したことのあるサイトへの DNS 検索速度を向上させるように設定することができます。

例えばpsでプロセスをみると，libvirtで定義したネットワーク分だけプロセスが立っている
※以下の例ではdnsmasqだけrootで動いているプロセス見えるんだけど，ちょっと微妙．DHCPしてるからなんらかの権限必要でrootのプロセス残っているとか? 分からない．

::

  $ ps aux | grep dnsmasq                              
  libvirt+    1282  0.0  0.0   9308   316 ?        S     2024   3:02 /usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-ro --dhcp-script=/usr/lib/libvirt/libvirt_leaseshelper
  root        1283  0.0  0.0   9280   956 ?        S     2024   1:21 /usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-ro --dhcp-script=/usr/lib/libvirt/libvirt_leaseshelper
  libvirt+  968887  0.0  0.0   9308   344 ?        S     3月16   0:00 /usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/vmenv-intnet2.conf --leasefile-ro --dhcp-script=/usr/lib/libvirt/libvirt_leaseshelper
  libvirt+  991348  0.0  0.0   9308  2332 ?        S     3月16   0:00 /usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/vmenv-intnet.conf --leasefile-ro --dhcp-script=/usr/lib/libvirt/libvirt_leaseshelper
  khwariz+  995562  0.0  0.0  10080  2640 pts/91   S+   00:02   0:00 grep --color=auto dnsmasq

psのログを見て分かるとおりだが，/var/lib/libvirt/dnsmasq配下に設定ファイルが置かれる．たぶんlibvirtで定義したネットワークのxmlからうまく生成される感じなのかな．
conf以外にもファイルあるがどんなものかはよく調べてない．

natはiptables/nftablesが提供している．
とりあえず以下のコマンドとかうっておくと状態が分かるかもしれないが，いまのところあんまよくわかんない．

::

  ### iptables
  # すべてのテーブルとチェーンを表示
  sudo iptables -L -v
  # NATテーブルの確認
  sudo iptables -t nat -L -v
  # libvirt固有のチェーンを確認
  sudo iptables -t nat -L LIBVIRT_PRT -v

  ### nftables
  # すべてのルールを表示
  sudo nft list ruleset
  # 特定のテーブルを表示
  sudo nft list table nat

あとは，接続追跡(conntrack)なるもので情報を見れたりするらしいんだけど，ちょっと動作確認できてない．

::

  sudo modprobe nf_conntrack
  sudo cat /proc/net/nf_conntrack
  sudo conntrack -L


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

autostart setting
==================

::

  $ virsh autostart [vm name]              #enable
  $ virsh autostart --disable [vm name]    #disable
  $ ls -1 /etc/libvirt/qemu/autostart           # 確認
  

S411の環境を作った時のメモやつ
=================================

vpn掘ってVMがローカルに落ちててシームレスに使えるようにするみたいなやつ．


::

  $ sudo vim /etc/networks/interface    # linux bridgeを永続化して立てる
  ...
  ...
  $ sudo ip link set up dev labnet-br
  $ sudo ip addr flush dev eno3         # ローカルに向いてるインタフェースを綺麗にしておく．
  $ sudo ip addr add 192.168.200.3/24 dev labnet-br       #bridgeにアドレス
  $ sudo ip link set dev eno3 master labnet-br            #物理インタフェース差す．これでパケットくる．
  $ sudo virsh edit [vm]        # VMの設定ファイルを書き換えて↑のブリッジにインタフェースをぶっさす．ちなみにここnetworkにした方が絶対いいけどとりあえずbridgeのまま
  ...
  ...
  $ ssh [vm]
  $ sudo ip link set up dev [生やしたif]
  $ sudo ip addr add 192.168.200.101 dev [生やしたif]
  $ sudo ip route add 10.8.0.0/24 via 192.168.200.1 dev [生やしたif]

disk拡張する時の話
====================

diskとかでよくLVMってあるけど，よくわからなくて何もしないでいたんだけど，
ボリューム増やしたい時に，LVMじゃないとめちゃくちゃめんどくさかったのでとりあえずLVMにしとけよ．

ボリュームの増やし方．
ちゃんと元からLVMになっててそこからimgに容量増やしてVMにちゃんとマウントしてあげるやつ．

::

  // 現状確認 (ゲストで)
  $ sudo fdisk -l
  Disk /dev/sda: 8 GiB, 438086664192 bytes, 855638016 sectors
  Disk model: QEMU HARDDISK
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: dos
  Disk identifier: 0x6c364c8f
  
  Device     Boot   Start      End  Sectors  Size Id Type
  /dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
  /dev/sda2       1052670 16775167 15722498  7.5G  5 Extended
  /dev/sda5       1052672 16775167 15722496  7.5G 8e Linux LVM
  
  
  
  
  Disk /dev/mapper/vgubuntu2004-root: 6.51 GiB, 6975127552 bytes, 13623296 sectors
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  
  
  Disk /dev/mapper/vgubuntu2004-swap_1: 976 MiB, 1023410176 bytes, 1998848 sectors
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  

  // img を拡張
  $ virsh shutdown [vm]
  $ sudo qemu-img resize /var/lib/libvirt/images/[vm].img +400G
  $ virsh start [vm]


  // ゲストからディスク確認 408GiB に変わってる．けどパテは増えてない．
  $ sudo fdisk -l
  Disk /dev/sda: 408 GiB, 438086664192 bytes, 855638016 sectors
  Disk model: QEMU HARDDISK
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: dos
  Disk identifier: 0x6c364c8f
  
  Device     Boot   Start      End  Sectors  Size Id Type
  /dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
  /dev/sda2       1052670 16775167 15722498  7.5G  5 Extended
  /dev/sda5       1052672 16775167 15722496  7.5G 8e Linux LVM
  ..
  ..
  ..
  
  
  // 当然マウントもしてないのでdfしても増えてない
  $ df -hT

  // パテを切る
  $ sudo fdisk /dev/sda
  
  Welcome to fdisk (util-linux 2.34).
  Changes will remain in memory only, until you decide to write them.
  Be careful before using the write command.
  
  
  Command (m for help): p                 ### 表示
  Disk /dev/sda: 408 GiB, 438086664192 bytes, 855638016 sectors
  Disk model: QEMU HARDDISK
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: dos
  Disk identifier: 0x6c364c8f
  
  Device     Boot   Start      End  Sectors  Size Id Type
  /dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
  /dev/sda2       1052670 16775167 15722498  7.5G  5 Extended
  /dev/sda5       1052672 16775167 15722496  7.5G 8e Linux LVM
  
  Command (m for help): n               ### 新しいパテを作る
  Partition type
     p   primary (1 primary, 1 extended, 2 free)
     l   logical (numbered from 5)
  Select (default p): p                 ### primaryらしい
  Partition number (3,4, default 3): 3        ###3だけどかぶってなきゃ何でもいい sda3になるだけ
  First sector (16775168-855638015, default 16775168):                      ###Endみてケツにくっつくようにすればいいけど大体defがちゃんとしてる．
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (16775168-855638015, default 855638015):        ###defがえらい 
  
  Created a new partition 3 of type 'Linux' and of size 400 GiB.

  Command (m for help): t         ### パテタイプ変更
  Partition number (1-3,5, default 5): 3            ### sda3なのでね
  Hex code (type L to list all codes): 8e           ### 8eがLVM．ただこれディストリビューションごとに違いそう．fedora34 だと 30 だった．随時確認しろ．
  
  Changed type of partition 'Linux' to 'Linux LVM'.

  Command (m for help): p           ### 確認
  Disk /dev/sda: 408 GiB, 438086664192 bytes, 855638016 sectors
  Disk model: QEMU HARDDISK
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: dos
  Disk identifier: 0x6c364c8f
  
  Device     Boot    Start       End   Sectors  Size Id Type
  /dev/sda1  *        2048   1050623   1048576  512M  b W95 FAT32
  /dev/sda2        1052670  16775167  15722498  7.5G  5 Extended
  /dev/sda3       16775168 855638015 838862848  400G 8e Linux LVM
  /dev/sda5        1052672  16775167  15722496  7.5G 8e Linux LVM
  
  Partition table entries are not in disk order.
  
  Command (m for help): w           ### 保存して終了
  The partition table has been altered.
  Syncing disks.

  // VM再起動してパテ変更を反映させるらしい
  
  
  *** 物理ボリューム作成→ボリュームグループを拡張→論理ボリュームを拡張 ***
  // 物理ボリュームを追加
  $ sudo pvcreate /dev/sda3
    Physical volume "/dev/sda3" successfully created.
  // 確認
  $ sudo pvdisplay
    --- Physical volume ---
    PV Name               /dev/sda5
    VG Name               vgubuntu2004
    PV Size               <7.50 GiB / not usable 0
    Allocatable           yes
    PE Size               4.00 MiB
    Total PE              1919
    Free PE               12
    Allocated PE          1907
    PV UUID               vu8L0J-Reh0-dOrU-CqhI-qCfR-Ioss-D4kTyK

    "/dev/sda3" is a new physical volume of "400.00 GiB"
    --- NEW Physical volume ---
    PV Name               /dev/sda3
    VG Name
    PV Size               400.00 GiB
    Allocatable           NO
    PE Size               0
    Total PE              0
    Free PE               0
    Allocated PE          0
    PV UUID               6NhpxX-FK6u-h4rQ-HXq0-LdCF-5H3m-HWuCHp

  // ボリュームグループ確認
  $ $ sudo vgdisplay
    --- Volume group ---
    VG Name               vgubuntu2004
    System ID
    Format                lvm2
    Metadata Areas        1
    Metadata Sequence No  3
    VG Access             read/write
    VG Status             resizable
    MAX LV                0
    Cur LV                2
    Open LV               2
    Max PV                0
    Cur PV                1
    Act PV                1
    VG Size               <7.50 GiB
    PE Size               4.00 MiB
    Total PE              1919
    Alloc PE / Size       1907 / <7.45 GiB
    Free  PE / Size       12 / 48.00 MiB
    VG UUID               ob5lrW-GwTB-oAOs-VQU7-pOew-YV8g-1JkTFv

  //ボリュームグループ拡張 sda3を加える
  $ sudo vgextend vgubuntu2004 /dev/sda3
    Volume group "vgubuntu2004" successfully extended
  // VG Size が増えてる
  $ sudo vgdisplay
    --- Volume group ---
    VG Name               vgubuntu2004
    System ID
    Format                lvm2
    Metadata Areas        2
    Metadata Sequence No  4
    VG Access             read/write
    VG Status             resizable
    MAX LV                0
    Cur LV                2
    Open LV               2
    Max PV                0
    Cur PV                2
    Act PV                2
    VG Size               <407.50 GiB
    PE Size               4.00 MiB
    Total PE              104319
    Alloc PE / Size       1907 / <7.45 GiB
    Free  PE / Size       102412 / <400.05 GiB
    VG UUID               ob5lrW-GwTB-oAOs-VQU7-pOew-YV8g-1JkTFv

  // 論理ボリューム確認
  $ sudo lvdisplay
    --- Logical volume ---
    LV Path                /dev/vgubuntu2004/root
    LV Name                root
    VG Name                vgubuntu2004
    LV UUID                VOf5rg-f3ax-yGc5-YEdd-0x08-Qp0O-1FdoAh
    LV Write Access        read/write
    LV Creation host, time ubuntu2004, 2020-06-11 16:58:25 +0900
    LV Status              available
    # open                 1
    LV Size                <6.50 GiB
    Current LE             1663
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:0

    --- Logical volume ---
    LV Path                /dev/vgubuntu2004/swap_1
    LV Name                swap_1
    VG Name                vgubuntu2004
    LV UUID                2hx5B2-QGEw-7dXA-5hKo-EcVW-xE1B-lD0SKR
    LV Write Access        read/write
    LV Creation host, time ubuntu2004, 2020-06-11 16:58:25 +0900
    LV Status              available
    # open                 2
    LV Size                976.00 MiB
    Current LE             244
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:1

  // 論理ボリュームの拡張 なんか全部割り当てろや「-l +100%FREE」ってやればいいらしい
  $ sudo lvextend -l +100%FREE /dev/vgubuntu2004/root
    Size of logical volume vgubuntu2004/root changed from <6.50 GiB (1663 extents) to 406.54 GiB (104075 extents).
    Logical volume vgubuntu2004/root successfully resized.

  //確認したらLV Size が増えてる
  $ sudo lvdisplay
    --- Logical volume ---
    LV Path                /dev/vgubuntu2004/root
    LV Name                root
    VG Name                vgubuntu2004
    LV UUID                VOf5rg-f3ax-yGc5-YEdd-0x08-Qp0O-1FdoAh
    LV Write Access        read/write
    LV Creation host, time ubuntu2004, 2020-06-11 16:58:25 +0900
    LV Status              available
    # open                 1
    LV Size                406.54 GiB
    Current LE             104075
    Segments               3
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:0

    --- Logical volume ---
    LV Path                /dev/vgubuntu2004/swap_1
    LV Name                swap_1
    VG Name                vgubuntu2004
    LV UUID                2hx5B2-QGEw-7dXA-5hKo-EcVW-xE1B-lD0SKR
    LV Write Access        read/write
    LV Creation host, time ubuntu2004, 2020-06-11 16:58:25 +0900
    LV Status              available
    # open                 2
    LV Size                976.00 MiB
    Current LE             244
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:1

  // ファイルシステムの拡張 (少し時間かかる)
  $ sudo resize2fs /dev/vgubuntu2004/root           # ←は ext4 とかの場合らしく，XFS の場合 (fedora34 というか RHEL 系とか) xfs_growfs コマンドにすればいい．引数も一緒．
  resize2fs 1.45.5 (07-Jan-2020)
  Filesystem at /dev/vgubuntu2004/root is mounted on /; on-line resizing required
  old_desc_blocks = 1, new_desc_blocks = 51
  The filesystem on /dev/vgubuntu2004/root is now 106572800 (4k) blocks long.

  // dfとかで確認したらおしまいや



参考:
http://b.ruyaka.com/2014/05/08/kvm-guest-os-increase-disc/

https://qiita.com/nouphet/items/fea026c03ca86ec54111

元々LVM環境が用意できてない場合のやつあったけどうまく行かなかったやつ．
https://gist.github.com/koudaiii/bfcaa6941bd99d688ade

nestedしたい時
=================

ホストで

::

  $ cat /sys/module/kvm_intel/parameters/nested
  /// 1 か Y ならOK    0 か N だったら↓
  $ sudo su 
  # cat << EOF > /etc/modprobe.d/kvm-nested.conf       ///名前はなんでもいい
  > options kvm_intel nested=1
  > EOF
  $ sudo modprobe -r kvm_intel

  /// ゲストの設定を書き直す
  $ virsh edit [vm]
  /////// cpu のところに追加する
  + <feature policy='require' name='vmx'/>

ゲストで確認

::

  $ cat /proc/cpuinfo | grep vmx
  ///  なんか出てくればよい


http://bluearth.cocolog-nifty.com/blog/2019/10/post-78eb20.html



レスキューモードで起動
==============================

::

  $ virt-rescue [vm name]      ### ディスクイメージでも可らしい

起き上がった状態だと簡易的な状態? (どこまで起き上がってるかとかはちょっとよくわからんけど) のため，
いろいろマウントしてchrootしてあげるとよい．

::

  > mount /dev/mapper/[vm name]_root  /sysroot      パテへのdevへのパスはちょっと適当なので環境でちゃんとやること
  > mount /dev/sda1 /sysroot/boot
  > mount --bind /dev /sysroot/dev
  > mount --bind /dev/pts /sysroot/dev/pts
  > mount --bind /proc /sysroot/proc
  > mount --bind /sys /sysroot/sys
  > chroot /sysroot

この後はある程度よしなにやりたいことができるはず．


http://manpages.ubuntu.com/manpages/bionic/ja/man1/virt-rescue.1.html


仮想マシンに対してSysRqを送る
==============================

任意のキーストロークを仮想マシンに送るには `virsh send-key` が使えるのでそれを活用する．
以下は仮想マシン"sysrq-fedora36"に対してsysrqのヘルプメッセージ出力させる例．

::

  $ virsh send-key sysrq-fedora36 KEY_LEFTALT KEY_SYSRQ KEY_H


キーコードは例えば `man 7 virkeycode-linux` とかから．
--codesetにもよるのであとはmanを見ること．


参考:
 - "KVM virsh send-key example (Control-Alt-Delete and more)": https://rentry.co/x563n
 - "20.26. 指定したゲスト仮想マシンへのキーストロークの組み合わせの送信": https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-editing_a_guest_virtual_machines_configuration_file-sending_keystoke_combinations_to_a_specified_domain


fedora(というかdebian系以外)だと一般ユーザvirsh listとかとかでちゃんとVMが見えないみたいな話2
=================================================================================================

まあ 1 の方である程度察しはつくけど，
まずvirsh listとかとかでちゃんとVMが見えないことの根本的な原因は，コマンドの対象ドメインすなわち

virsh --connect [domain]

のここのdomainが設定されないから．

ここ，まずdebian系では，バイナリ自体が指定がなければ qemu:///system を見るようになっている．
(ビルド時にこうなるようなオプション指定をしているのかそれともコードに改変加えてるのかはしらん)
で，fedoraとかではそうなっていなく，その時は次のような動作になるらしい．

::

  If the URI passed to virConnectOpen* is NULL, then libvirt will use the following logic to determine what URI to use.

  1.  The environment variable LIBVIRT_DEFAULT_URI
  2.  The client configuration file uri_default parameter
  3.  Probe each hypervisor in turn until one that works is found

https://libvirt.org/uri.html#URI_default

というわけです．

参考: https://listman.redhat.com/archives/libvirt-users/2011-April/msg00091.html


libvirt - monolithic & module mode
=====================================

以前いつものように仮想環境を構築していたときに，libvirtd.serviceやlibvirtd.socketが動作していなくてもvirshコマンドが
正常に動作してVMが操作できることに気づいた．

その後調査を進めると，libvirtにはモノリシックモードとモジュールモードが存在するということがわかり，
また例えばfedora38などではlibvirtdのインストール直後はモジュールモードで動作するためにlibvirtd.serviceなどが
動作しない状態であり，もちろんその状態でも正常に操作できるということがわかった．

詳細の説明は以下の記事に任せるが、いずれちゃんと書くかもしれない。

https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/9/html/monitoring_and_managing_system_status_and_performance/assembly_optimizing-libvirt-daemons_optimizing-virtual-machine-performance-in-rhel

http://belbel.or.jp/opensuse-manuals_ja/cha-libvirt-overview.html

さらに，RHEL9ではモノリシックなlibvirtdはdeprecatedになったよう．

https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/9/html/considerations_in_adopting_rhel_9/ref_changes-to-libvirt_assembly_virtualization


仮想化環境構築後にできるグループと，基本的な権限調整について
===============================================================

aaaa


libvirtグループを使わず，polkitを用いて権限調整をする方法
===========================================================


ユーザー "khwarizmi" に対してvirshの操作権限を与える例  

::

  /etc/polkit-1/localauthority/50-local.d/libvirt-user-access.pkla:
  [libvirt Management Access]
  Identity=unix-user:khwarizmi
  Action=org.libvirt.unix.manage
  ResultAny=yes
  ResultInactive=yes
  ResultActive=yes 

参考: https://wiki.libvirt.org/SSHPolicyKitSetup.html


以下，関連してpolkitの活用例

polkitで特定のユーザーに特定のアクションを許可する例
--------------------------------------------------------

Archwikiよりそのまま: https://wiki.archlinux.jp/index.php/Polkit#.E7.89.B9.E5.AE.9A.E3.81.AE.E3.83.A6.E3.83.BC.E3.82.B6.E3.83.BC.E3.81.AB_org.freedesktop.timedate1.set-timezone_.E3.82.A2.E3.82.AF.E3.82.B7.E3.83.A7.E3.83.B3.E3.81.AE.E4.BD.BF.E7.94.A8.E3.82.92.E8.A8.B1.E5.8F.AF.E3.81.99.E3.82.8B

archie という名前のユーザーに org.freedesktop.timedate1.set-timezone アクションの認証なしの使用を許可するには、以下の polkit ルールを root ユーザーを使って作成してください:

::

  /etc/polkit-1/rules.d/49-allow-archie-set-timezone.rules
  polkit.addRule(function(action, subject) {
      if (action.id == "org.freedesktop.timedate1.set-timezone" &&
          subject.user == "archie") {
          return polkit.Result.YES;
      }
  });

org.freedesktop.[コマンド名] みたいな感じにすると別のコマンドでできそうか．

アクションは，pkactionコマンドで確認できるらしい．

::

  $ pkaction --verbose
  //! アクションの詳細を見たい場合
  $ pkaction --verbose --action-id "org.freedesktop.action名"

また，pkactionは/usr/share/polkit-1/actionsのクイックリファレンスらしく，このファイルを実際見に行けばいいっぽい?


**注意**
polkitのアクション名は，d-busのインタフェース名と同じ記法で表現方法もかなり近く，共通する部分も多い．
がしかし，同一ではないようなので注意が必要．

例えば実例として以下らしい?

::

  D-Busインターフェース：
  org.freedesktop.login1.Manager
  
  関連するpolkitアクション：
  org.freedesktop.login1.power-off
  org.freedesktop.login1.reboot
  org.freedesktop.login1.suspend

それぞれ例えば以下のような感じで確認ができるらしい

::

  # D-Busインターフェースの確認
  d-feet （GUIツール）
  busctl list
  
  # polkitアクションの確認
  pkaction --verbose


reference
===========

domain_xml_format_  

network_xml_format_  

virsh_



.. _macvlan: https://tenforward.hatenablog.com/entry/20111221/1324466720
.. _domain_xml_format: https://libvirt.org/format.html
.. _network_xml_format: https://libvirt.org/formatnetwork.html#examplesBridge
.. _virsh: http://lipix.ciutadella.es/wp-content/uploads/2016/09/kvm_cheatsheet.pdf
.. _ubuntu_kvm_installation: https://help.ubuntu.com/community/KVM/Installation



kvmコマンドと言うものがあるらしく
====================================

helloworld
-----------------

Xwindowのあるシステムで↓を実行

::

  $ kvm -monitor stdio

空のVMのウィンドウが立ち上がる．
当然何もないのでbootしないけど．

インストールと起動
-----------------------

::

  ### install
  $ qemu-img create -f qcow2 test.img 4G
  $ sudo kvm -hda test.img -cdrom [path to iso file] -boot d -m 1024

  ### start
  $ sudo kvm -hda test.img -boot c -m 1024

