kvm
====

package
--------
:: 

  $ sudo apt install qemu-kvm libvirt0 libvirt-bin bridge-utils virtinst libguestfs-tools

start config
--------------
::

  $ sudo systemctl enable libvirt-bin

make image
----------
::

  $ sudo qemu-img create -f qcow2 /var/lib/libvirt/images/ubuntu1804.img 8G

install 
--------

serial *cannot install*
~~~~~~~~~~~~~~~~~~~~~~~
::

  $ sudo virt-install \
    --name ubuntu1804 \
    --disk path=/var/lib/libvirt/images/ubuntu1804.qcow2,size=8 \
    --vcpus 2 \
    --ram 512 \
    --os-type linux \
    --graphics none \
    --console pty,target_type=serial \
    --network bridge:virbr0 \
    --cdrom /var/lib/libvirt/boot/ubuntu-18.04.2-live-server-amd64.iso \
    --extra-args 'console=ttyS0,115200n8 serial'

  # これだと成功するきっと location が url にしたら通った
  $ virt-install \
  --connect=qemu:///system \
  --name ubuntu1 \
  --vcpus 1 \
  --ram 512 \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/ubuntu1.img,size=8 \
  --location 'http://jp.archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 

  #これ成功しないやつ多分
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
  --name centos7   \
  --vcpus 2 \
  --ram 2048   \
  --accelerate --hvm \
  --disk path=/var/lib/libvirt/images/centos7.img,size=8 \
  --location 'http://ftp.iij.ad.jp/pub/linux/centos/7/os/x86_64/' \
  --network network=default,model=virtio \
  --nographics --extra-args='console=tty0 console=ttyS0,115200n8' 

ubuntu1604が入らない話
https://www.mckelvaney.co.uk/blog/2019/04/17/ubuntu-16.04-loading-libc-udeb-failed-for-unknown-reasons-aborting/
centos7でメモリが足りなくてinitramfsがエラる話
https://www.centos.org/forums/viewtopic.php?t=67350

vnc
~~~~
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
------

::

  $ sudo virt-clone --original vm_org --name vm_clone --file /var/lib/libvirt/images/vm_clone.img   # .imgを作成しておく必要はない
  $ sudo virt-sysprep -d vm_clone --enable dhcp-client-state,machine-id,net-hwaddr             # dhcp clientリースだけで良いはずだが一応

and change hostname 


change memory size
-------------------

::

  #max memory sizeを変更
  $ sudo virsh setmaxmem [domain] 4G

  #起動中にmemory size変更(停止したら戻る)
  $ sudo viesh setmem [domain] 4G

  #停止中のマシンの次回以降のmemory sizeを変更
  $ sudo virsh setmem [domain] 4G --config

  #確認
  $ sudo virsh dominfo [domain] | grep mem

rename domain 
---------------

::
  
  $ uuidgen           #コピっとく
  $ sudo virsh edit [old domain]
    change name & uuid
  $ sudo virsh undefine [old domain]

file focation
--------------
::

  vm images         /var/lib/libvirt/images/
  iso images          /var/lib/libvirt/boot/    ←???
  xml file                /etc/libvirt/qemu/
  network file       /etc/libvirt/qemu/networks/

ブリッジ接続
------------

Linux bridge
~~~~~~~~~~~~~~

ブリッジ作成してそこに物理インタフェースぶっこむだけ.
インタフェースとブリッジのリンク上げ忘れよくするから注意.
なんか知らないけどグローバルに向けられない．

ovs
~~~~

macvtap, macvlan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ゲストのxmlファイルを

::

  <interface type='direct'>
    <mac address='52:54:00:94:9a:a0'/>
    <source dev='eth0' mode='bridge'/>
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
--------------------

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
--------

::

  $ sudo vim /etc/default/grub
  + GRUB_CMDLINE_LINUX="intel_iommu=on"
  $ sudo update-grub2

wakarann

ubuntu image download
---------------------
::

  $ wget http://ftp-srv2.kddilabs.jp/Linux/packages/ubuntu/releases-cd/18.04.3/ubuntu-18.04.3-live-server-amd64.iso


reference
---------

domain_xml_format_  

network_xml_format_  

virsh_



.. _macvlan: https://tenforward.hatenablog.com/entry/20111221/1324466720
.. _domain_xml_format: https://libvirt.org/format.html
.. _network_xml_format: https://libvirt.org/formatnetwork.html#examplesBridge
.. _virsh: http://lipix.ciutadella.es/wp-content/uploads/2016/09/kvm_cheatsheet.pdf
