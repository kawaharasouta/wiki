============================
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






