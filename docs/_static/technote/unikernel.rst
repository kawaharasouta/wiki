====================
unikernelについて
====================

クラウド環境で，シングルプロセスなVMを並列に展開するみたいな用途が結構ある．
SaaSのさらに上みたいなやつとかもあったりする(AWSのlambdaみたいなやつとか)．
その場合，汎用OS使ってVMたてるのって汎用性が無駄だしパフォーマンスが出ない．
そこで，アプリケーションのための小さな専用カーネルを用意してその上でアプリケーションを動かす．



参考

unikernalの情報
https://qiita.com/t-imada/items/ed6a76f5b257f5608ad0


mirageOSでHelloWorldする
===========================

インストール
https://mirage.io/wiki/install

はろわ
https://mirage.io/wiki/hello-world

環境
-----

::

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


とりあえず動くように改良

::

  open Lwt.Infix

  module Hello (Time : Mirage_time.S) = struct

    let start _time =

      (*let rec loop = function
        | 0 -> Lwt.return_unit
        | n ->
          Logs.info (fun f -> f "hello");
          (*Time.sleep_ns (Duration.of_sec 1) >>= fun () ->
          loop (n-1)*)
          Lwt.return_unit
      in
      loop 4*)

      Logs.info (fun f -> f "hello");
      Lwt.return_unit

  end

とりあえずunixAPPとして動かす

::

  $ mirage configure -t unix
  $ make depend
  $ make 
  $ ./hello
    2020-04-14 09:57:51 +00:00: INF [application] hello

kvmで動かす

::

  aaaaaa


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
-------


MirageOSのHelloWorldやってみるやつ
https://qiita.com/t-imada/items/6ee299653ac063532b4f



OSv
=====

やってみる
-----------

::

  $ sudo apt install libvirt0

apps
-------

::

  $ git clone https://github.com/cloudius-systems/osv.git & cd $_
  $ git submodule update --init --recursive
  $ sudo ./scripts/setup.py             ### 必要なパッケージ類とかインストールしてる．
  ////// とりあえずiperfしてみたい
  $ sudo ./scripts/build image=iperf    ### Could not access KVM kernel module: Permission denied にならないユーザならsudoいらない． (usermod -aG kvm <user name>)
  $ sudo ./scripts/run.py -nv       ### 最近buildされたイメージをrunする． -nv はネットワークのための設定でdefaultネットワークインタフェースを生やしてくれるなんともえらいオプション ちなみにtapn(nは環境依存の整数)としてホストから見える
  ctrl A + X で抜ける

ちなみにビルドした後のイメージの場所は /home/khwarizmi/git/osv/build/last/usr.img 

minecraft serverを動かそうとした時のmemo
-------------------------------------------

apps 内のサンプルアプリケーションで，kernelにおくアプリケーションの設定ファイルとかは多分usr.manifestに書かれてる．
必要なサブシステムは多分moduleのところとかにあって，必要なものはmodule.pyにrequireとかってしてあって，それを取りにいくと思う．
こけてるところはca-certificateのところな感じ．
java?のアプリケーションのいくつかも大体同じようなところでブッコケる．

エラーは

::

	///sudoなしだと
  Makefile:8: recipe for target 'module' failed
	make: *** [module] Error 1
	Traceback (most recent call last):
		File "scripts/module.py", line 280, in <module>
			args.func(args)
		File "scripts/module.py", line 233, in build
			make_modules(modules, args)
		File "scripts/module.py", line 124, in make_modules
			raise Exception('make failed for ' + module.name)
	Exception: make failed for ca-certificates
	./scripts/build failed: ( for i in "${args[@]}";
	do
			case $i in
					*=*)
							export "$i"
					;;
			esac;
	done; export fs_type mode OSV_BUILD_PATH; export ARCH=$arch OSV_BASE=$SRC; scripts/module.py $j_arg build -c "$modules" $usrskel_arg $no_required_arg )

  ///sudoありだと
  Adding /usr/lib/jvm/java/jre/lib/security/cacerts...
  terminate called after throwing an instance of 'std::system_error'
    what():  chmod: No such file or directory
  Aborted
  [backtrace]
  0x00000000404be9b3 <???+1078716851>
  0x662068637573206e <???+1970479214>
  qemu-system-x86_64: terminating on signal 2
  Traceback (most recent call last):
    File "/home/khwarizmi/git/osv/scripts/upload_manifest.py", line 170, in <module>
      main()
    File "/home/khwarizmi/git/osv/scripts/upload_manifest.py", line 160, in main
      upload(osv, manifest, depends, upload_port)
    File "/home/khwarizmi/git/osv/scripts/upload_manifest.py", line 107, in upload
      s.recv(1)
  KeyboardInterrupt
  Traceback (most recent call last):
    File "scripts/run.py", line 615, in <module>
      main(cmdargs)
    File "scripts/run.py", line 485, in main
      start_osv(options)
    File "scripts/run.py", line 469, in start_osv
      launchers[options.hypervisor](options)
    File "scripts/run.py", line 282, in start_osv_qemu
      ret = subprocess.call(cmdline, env=qemu_env)
    File "/usr/lib/python3.8/subprocess.py", line 342, in call
      return p.wait(timeout=timeout)
    File "/usr/lib/python3.8/subprocess.py", line 1079, in wait
      return self._wait(timeout=timeout)
    File "/usr/lib/python3.8/subprocess.py", line 1804, in _wait
      (pid, sts) = self._try_wait(0)
    File "/usr/lib/python3.8/subprocess.py", line 1762, in _try_wait
      (pid, sts) = os.waitpid(self.pid, wait_flags)

jreの証明書?のところら辺の設定とかなのかなとは思ってるけどよくわからん．
あとこれ

::
  
  ag /usr/lib/jvm/java/jre/lib/security/cacerts
  openjdk8-from-host/module.py
  39:usr_files.link('/usr/lib/jvm/java/jre/lib/security/cacerts').to('/etc/pki/java/cacerts')

module/openjdk8-from-host/module.pyをちょっと編集してみたりはした．



includeOS
=============

https://github.com/includeos/IncludeOS
https://includeos.readthedocs.io/en/latest/Getting-started.html

location
-------------

デフォルトのプロジェクトpathは /usr/local/includeos だけど↓で設定．

::

  $ echo export INCLUDEOS_PREFIX='$HOME'/includeos >> .bashrc
  $ echo export PATH='$PATH':'$INCLUDEOS_PREFIX'/bin >> $HOME/.bashrc

install
---------

dependency
----------------

- The conan package manager (1.13.1 or newer)    https://docs.conan.io/en/latest/installation.html
- cmake, make, nasm (x86/x86_64 only)
- clang, or alternatively gcc on linux. Prebuilt packages are available for clang 6.0 and gcc 7.3.

::

  $ sudo apt install cmake nasm build-essential


ちょっとconanがわからんかったのでいったんやめとく
