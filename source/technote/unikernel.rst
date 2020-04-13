====================
unikernelについて
====================

インストール
https://mirage.io/wiki/install

はろわ
https://mirage.io/wiki/hello-world


mirageOSでHelloWorldする
===========================

環境
-----

OS: ubuntu18.04
kernel: 4.15.0-91-generic
kvm
ocaml: 4.05.0
opam: 2.0.4

手順
------

kvmはkvmのとこみろや

ocamlとopamのインストール

::

  $ sudo add-apt-repository ppa:avsm/ppa
  $ sudo apt update
  $ sudo apt install opam ocaml gcc make bubblewrap m4 pkg-config


opam環境構築
-------------

::

  $ opam init 
    いろいろインストールで聞かれるから適当にyしとけ
  $ vim ~/.bashrc 
    + eval `opam config env`
  $ source ~/.bashrc

mirageパッケージのインストール
-------------------------------

::

  $ opam install mirage
  $ mirage    #確認


mirageAPP
-----------

hello言うやつ
````````````````

::

  $ git clone https://github.com/mirage/mirage-skeleton.git ~/git/mirage-skeleton
  $ cd ~/git/mirage-skeleton
  $ mirage configure -t hvt     # -tはターゲット指定? これでコンパイルに必要なファイルが流れてくる． autotoolsみたいなのりだと思う． Makefileも出てくる
  $ make depend                 # 依存関係のあるパッケージを入れてるらしい
  $ make 
  えらったわ
  Error: This expression has type unit Time.io
         but an expression was expected of type 'a Lwt.t


make configure の ターゲット一覧一応

::

  Target platform to compile the unikernel for. Valid values are:
  xen, qubes, unix, macosx, virtio, hvt, muen, genode.

ちょっと保存用

::

  mirage build
  + ocamlfind ocamlc -c -g -g -bin-annot -safe-string -principal -strict-sequence -package mirage-types-lwt -package mirage-types -package mirage-solo5 -package mirage-runtime -package mirage-logs -package mirage-clock-freestanding -package mirage-bootvar-solo5 -package lwt -package functoria-runtime -package duration -predicates mirage_solo5 -w A-4-41-42-44 -color always -o unikernel.cmo unikernel.ml
  File "unikernel.ml", line 11, characters 8-41:
  Error: This expression has type unit Time.io
         but an expression was expected of type 'a Lwt.t
  Command exited with code 2.
  run ['ocamlbuild' '-use-ocamlfind' '-classic-display' '-quiet' '-tags'
       'predicate(mirage_solo5),warn(A-4-41-42-44),debug,bin_annot,strict_sequence,principal,safe_string,color(always)'
       '-pkgs'
       'duration,functoria-runtime,lwt,mirage-bootvar-solo5,mirage-clock-freestanding,mirage-logs,mirage-runtime,mirage-solo5,mirage-types,mirage-types-lwt'
       '-cflags' '-g' '-lflags'
       '-g,-dontlink,unix,-dontlink,str,-dontlink,num,-dontlink,threads'
       '-tag-line' '<static*.*>: warn(-32-34)' '-Xs'
       '_build-solo5-hvt,_build-ukvm' 'main.native.o']: exited with 10
  run ['dune' 'exec' '--root'
       '/home/khwarizmi/git/mirage-skeleton/tutorial/hello' '--' './config.exe'
       'build']: exited with 1
  Makefile:18: recipe for target 'build' failed
  make: *** [build] Error 1



なんもしないやつ
```````````````````

とりあえずunixappで動かす

::

  $ cd ~/git/mirage-skeleton/tutorial/noop
  $ mirage configure -t unix
  $ make depend
  $ make 
  $ ./noop      # 実行ファイル
  $ echo $?     # リターンコード確認するけど普通に0だからなんか物足りない
    0


static-website-tlsを動かそうとしてみたら
------------------------------------------

make dependでエラー

::

  The following dependencies couldn't be met:
    - mirage-unikernel-https-unix → conduit-mirage < 3.0.0 → ocaml >= 4.07.0
        base of this switch (use `--unlock-base' to force)
    - mirage-unikernel-https-unix → conduit-mirage < 3.0.0 → mirage-kv >= 3.0.0 → ocaml >= 4.06.0
        base of this switch (use `--unlock-base' to force)
    - mirage-unikernel-https-unix → conduit-mirage < 3.0.0 → dns-client → ocaml >= 4.07.0
        base of this switch (use `--unlock-base' to force)

ocamlのバージョン4.07.0にする必要ありそう．



参考
=======

unikernalの情報
https://qiita.com/t-imada/items/ed6a76f5b257f5608ad0

MirageOSのHelloWorldやってみるやつ
https://qiita.com/t-imada/items/6ee299653ac063532b4f
