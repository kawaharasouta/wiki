DPDK
=====


setup
-----

envs
~~~~
::  

        $ echo "export RTE_SDK=$HOME/dpdk" >> $HOME/.bashrc
        $ echo "export RTE_TARGET=x86_64-native-linuxapp-gcc" >> $HOME/.bashrc


packages
~~~~~~~~
::

        $ sudo apt install -y libpcap-dev python linux-headers-`uname -r` build-essential git libnuma-dev

clone and build DPDK
~~~~~~~~~~~~~~~~~~~~~~~~
::

        $ git clone http://dpdk.org/git/dpdk $RTE_SDK
        $ cd $RTE_SDK
        $ make install T=$RTE_TARGET

setup Hugepages
~~~~~~~~~~~~~~~
::

        $ sudo vim /etc/default/grub
        - GRUB_CMDLINE_LINUX=""
        + GRUB_CMDLINE_LINUX="hugepages=1024"
        $ sudo grub-mkconfig -o /boot/grub/grub.cfg
        $ sudo mkdir -p /mnt/huge
        $ sudo vim /etc/fstab
        + nodev /mnt/huge hugetlbfs defaults 0 0
        $ reboot

helloworld
~~~~~~~~~~
::

        $ cd $RTE_SDK/examples/helloworld
        $ make
        $ sudo ./build/helloworld

bind NIC
~~~~~~~~~
comming soon

useage
~~~~~~
 
skelton with tap
````````````````
::

        $ sudo ./build/basicfwd --vdev=net_tap0,iface=tap0 --vdev=net_tap1,iface=tap1

pktgen
```````

dpdk v16.11

::
        
        $ git clone https://github.com/slankdev/pktgen
        $ sudo ./app/x86_64-native-linuxapp-gcc/pktgen -- -P -m "[1-7].0,[16-23].0,[8-15].1,[24-31].1"

command
++++++++

*再表示*

::

        redisplay
