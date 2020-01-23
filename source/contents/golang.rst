=========
golang
=========


install
=========

ここ見た方がいいかも https://golang.org/doc/install

::
  
  # linux
  $ wget https://dl.google.com/go/go1.13.linux-amd64.tar.gz
  $ sudo tar -C /usr/local -xzf go1.13.linux-amd64.tar.gz
  # mac
  $ brew install go
  
  # if not seted
  $ export PATH=$PATH:/usr/local/go/bin                 # go installしたときに実行ファイルが飛んでくとこにパス通しとけ的なやつですかね? これ普通に$GOPATH/binでいいんじゃねって気がしてきた．
  $ export GOPATH=$HOME/go                              # ワーキングディレクトのパス

Hello, World
==============

::

  $ go get gopl.io/ch1/helloworld
  $ $GOPATH/bin/helloworld

cmd
=======

**go**

::
  
  $ go run test.go      #即時実行
  $ go build test.go    #コンパイル
  $ go fmt test.go      #フォーマット整形

**godoc**

::

  $ godoc fmt           #パッケージのドキュメントを見る
  $ godoc -http=":3000" #公式と同様のインタフェースでブラウザからドキュメント確認する


参考
======

本家: https://golang.org/
チュートリアル的な: http://golang.jp/go_tutorial  本家の日本語約で無駄なコンソールないからこっち見た方がいいや． golang.jp自体は古いから情報には注意．
