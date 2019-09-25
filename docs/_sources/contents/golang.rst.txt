=========
golang
=========


install
=========

::
  
  $ wget https://dl.google.com/go/go1.13.linux-amd64.tar.gz
  $ sudo tar -C /usr/local -xzf go1.13.linux-amd64.tar.gz
  
  #if not seted
  $ export PATH=$PATH:/usr/local/go/bin
  $ export GOPATH=$HOME/go                                          #ワーキングディレクトのパス

Hello, World
==============

::

  $ go get gopl.io/ch1/helloworld
  $ $GOPATH/bin/helloworld
