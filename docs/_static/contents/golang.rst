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

Examples
=========

::

  $ go get github.com/veandco/go-sdl2-examples/examples

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
とりあえず日本語の入門記事の一つ: http://gihyo.jp/dev/feature/01/go_4beginners
見ると幸せになれるらしいよ: https://qiita.com/tenntenn/items/0e33a4959250d1a55045
プロジェクトレイアウトの話: https://techdo.mediado.jp/entry/2019/01/18/112503




条件分岐コンパイル
===================

Cとかで #ifdef でやるような条件コンパイルやる方法
参考: https://qiita.com/yamasaki-masahide/items/8e5d59467dcf67d9b0be





SDL2
=====

https://wiki.libsdl.org/
https://godoc.org/github.com/veandco/go-sdl2/sdl#pkg-constants
https://github.com/veandco/go-sdl2

install 
---------

::
  
  $ go get -v github.com/veandco/go-sdl2/{sdl,img,mix,ttf}

sample
----------

::

  $ go get github.com/veandco/go-sdl2-examples/examples



struct と interface
======================

なんか構造体のそれっぽいことを書く．





型を確認する
==============

::

  fmt.Printf("%T", v)
  または
  fmt.Println(reflect.TypeOf(v))



function と method 
===================

go言語にはfunctionとmethodとかいう関数の概念があるらしい．

以下の構造体が宣言されていたとする．

::

  type Receiver struct {
    int num
  }

functionの例

::

  func Function(r Receiver) int {
    return r.num
  }
  
methodの例
関数名の前にレシーバ(構造体とか)が入る

::

  func (r Receiver) Method() int {
    return r.num
  }

使い方の違い

::

  r := Receiver {
    num: 10,
  }

  fmt.Printf("Function:\t%d\n", Function(r))
  fmt.Printf("Method:\t%d\n", r.Method())

こんな感じでC++のクラス内のメソッドみたいな感じで使える．
これでオブジェクト思考的なところを担保してるっぽい．


リンク
===============


https://medium.com/since-i-want-to-start-blog-that-looks-like-men-do/%E6%98%94%E3%81%AE%E8%87%AA%E5%88%86%E3%81%AB%E9%80%81%E3%82%8Bgolang%E3%81%AE%E5%9F%BA%E7%A4%8E%E7%9A%84%E3%81%AA%E3%81%93%E3%81%A8-%E5%9E%8B%E7%A2%BA%E8%AA%8D-slice-method-1bd2fae694d1











