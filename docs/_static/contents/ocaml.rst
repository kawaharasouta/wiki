=============================
OCamlについてとりあえずメモ
=============================


環境構築
==========

install
----------

**ubuntu**
ocamlとopam って言うのをインストールする．
ocamlはコンパイラ，opamはパッケージとかの管理ツールと思っておけば良さそう．

::

  $ sudo add-apt-repository ppa:avsm/ppa
  $ sudo apt update
  $ sudo apt install opam ocaml gcc make bubblewrap m4 pkg-config

opam環境構築
--------------

::
  
  $ opam init
  いろいろインストールで聞かれるから適当にyしとけ
  $ vim ~/.bashrc
    + eval `opam config env`
  $ source ~/.bashrc

Hello World
-------------

::

  $ vim my_prog.ml
    + let () = print_endline "Hello, World!"
  $ ocamlbuild my_prog.native
  $ ./my_prog.native
    Hello, World!


コンパイラ(ocaml)のバージョン管理
===================================

opamで管理するんだけど，スイッチとかいう概念があってスイッチで複数のバージョンを切り替えたりする．


::

  $ opam switch create 4.07.0     #新しいバージョンをインストール
  $ opam switch                   #スイッチ一覧
    #  switch   compiler                    description
    →  4.07.0   ocaml-base-compiler.4.07.0  4.07.0
       default  ocaml-system.4.05.0         default
  $ ocaml --version
    The OCaml toplevel, version 4.07.0
  $ opam switch default
  $ eval $(opam env)
  $ ocaml --version
    The OCaml toplevel, version 4.05.0


細かいパスがうんたらとかそう言う話
https://camlspotter.gitlab.io/blog/2018-08-08-opam-switch/




