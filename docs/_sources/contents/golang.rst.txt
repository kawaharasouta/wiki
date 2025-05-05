=========
golang
=========


install
=========

ここ見た方がいいかも https://golang.org/doc/install

::
  
  # linux
  $ wget https://dl.google.com/go/go1.13.linux-amd64.tar.gz     // バージョンは随時最新のを↑で確認しろ
  $ sudo tar -C /usr/local -xzf go1.13.linux-amd64.tar.gz
  # mac
  $ brew install go
  
  # if not seted
  $ export PATH=$PATH:/usr/local/go/bin                 # go installしたときに実行ファイルが飛んでくとこにパス通しとけ的なやつですかね? これ普通に$GOPATH/binでいいんじゃねって気がしてきた．
  $ export GOPATH=$HOME/go                              # ワーキングディレクトのパス


※複数バージョンの管理はいろいろあるらしいけど，とりあえず :doc:`inc_c_c++/version_management` みたいな感じにするのが良さげな気がする．

複数バージョン管理 gvm
------------------------

https://github.com/moovweb/gvm

依存パッケージとgvmのインストール

::

  ### AlmaLinux9
  $ sudo dnf install git bison gcc make
  $ bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
  $ source ${HOME}/.gvm/scripts/gvm

Goは1.5からCコンパイラでなくGoでセルフホスト? されるようになったらしく，ビルドにはGoがいる．
つまりブートストラップ用のGoを用意しないといけない．
また当然だが，バージョンアップに伴ってビルドに要求するバージョンも上がったりするので段階的にビルドしないといけないらしい．

ディストリビューションのgolangパッケージ使うのが手軽で早いと思う．

::

  $ sudo dnf install golang
  $ gvm install go1.24
  $ sudo remove golang
  $ gvm use go1.24 --default


※ これ以降の手順だが，なぜかバイナリインストールがうまくいかなかったので試していない．

正直に段階ビルドする手順
https://github.com/moovweb/gvm?tab=readme-ov-file#to-install-go-120

::

  gvm install go1.4 -B
  gvm use go1.4
  export GOROOT_BOOTSTRAP=$GOROOT
  gvm install go1.17.13
  gvm use go1.17.13
  export GOROOT_BOOTSTRAP=$GOROOT
  gvm install go1.20
  gvm use go1.20

またシンプルにバイナリインストールでもいい

::

  $ gvm install go1.24 -B
  

雑な使い方などメモ
===================

Hello, World
--------------

::

  $ go get gopl.io/ch1/helloworld
  $ $GOPATH/bin/helloworld

Examples
-----------

::

  $ go get github.com/veandco/go-sdl2-examples/examples

cmd
-------

**go**

::
  
  $ go run test.go      #即時実行
  $ go build test.go    #コンパイル
  $ go fmt test.go      #フォーマット整形

**godoc**

::

  $ godoc fmt           #パッケージのドキュメントを見る
  $ godoc -http=":3000" #公式と同様のインタフェースでブラウザからドキュメント確認する

go modと開発の始め(進め)方に関して
===================================

依存モジュールの管理ツールで
なんかよくわからんけど，とりあえず開発のときに↓のようにしておくとうまいことやってくれる?
正直よくわからんマジでよくわからんgo getとどう使ったらいいのかとかよくわからんしわからん．

- go mod init で、初期化する
- go buildなどのビルドコマンドで、依存モジュールを自動インストールする
- go list -m all で、現在の依存モジュールを表示する
- go get で、依存モジュールの追加やバージョンアップを行う
- go mod tidy で、使われていない依存モジュールを削除する

https://qiita.com/uchiko/items/64fb3020dd64cf211d4e
https://qiita.com/propella/items/e49bccc88f3cc2407745

参考
======

本家: https://golang.org/
チュートリアル的な: http://golang.jp/go_tutorial  本家の日本語訳で無駄なコンソールないからこっち見た方がいいや． golang.jp自体は古いから情報には注意．
とりあえず日本語の入門記事の一つ: http://gihyo.jp/dev/feature/01/go_4beginners
見ると幸せになれるらしいよ: https://qiita.com/tenntenn/items/0e33a4959250d1a55045
プロジェクトレイアウトの話: https://techdo.mediado.jp/entry/2019/01/18/112503

☆つまづきポイントFAQ(これめっちゃいい感じ): https://future-architect.github.io/articles/20190713/




条件分岐コンパイル
===================

Cとかで #ifdef でやるような条件コンパイルやる方法
参考: https://qiita.com/yamasaki-masahide/items/8e5d59467dcf67d9b0be





SDL2
=====

https://www.libsdl.org/
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


バイナリ処理
===============


あとでメモる

参照: binary_


imported and not used
======================

https://ksakiyama134.hatenadiary.org/entry/20140309/1394378735


リンク
===============


https://medium.com/since-i-want-to-start-blog-that-looks-like-men-do/%E6%98%94%E3%81%AE%E8%87%AA%E5%88%86%E3%81%AB%E9%80%81%E3%82%8Bgolang%E3%81%AE%E5%9F%BA%E7%A4%8E%E7%9A%84%E3%81%AA%E3%81%93%E3%81%A8-%E5%9E%8B%E7%A2%BA%E8%AA%8D-slice-method-1bd2fae694d1



.. _binary: https://qiita.com/Jxck_/items/c64d9ae0e910762eab37







