=======
Docker
=======


install (ubuntu)
===================

::

  $ sudo apt update && sudo apt install -y \
    apt-transport-https ca-certificates curl software-properties-common
  $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  $ sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable"
  $ sudo apt update && sudo apt install -y docker-ce
  $ sudo usermod -aG docker $USER   #sudoなしで現ユーザでdockerkコマンドを実行させるため．このあと再起動必要．

公式
https://docs.docker.com/engine/install/ubuntu/
もっとも簡単なdocker公式セットアップ?
https://qiita.com/zembutsu/items/bedb18e1061303e217b8


commands
========

::
  
  $ docker run -it --name [name] ubuntu:18.04 bash        #名前をつける
  $ docker run -p 8080:80 -it ubuntu:18.04 bash           #ホストの8080ポートをコンテナの80ポートにフォアード
  $ docker run --link [container name]:{link name] nginx  #コンテナをリンクさせる例(nginxでリバースプロキシするときにやったので
  $ docker stop $(docker ps -q)                           #起動中のコンテナ全部停止
  $ docker rm $(docker ps -aq)                            #停止中コンテナ全削除
  $ docker rename [old name] [new name]                   #コンテナリネーム

  $ docker inspect [container id]           #コンテナ情報取得
  $ docker build -t khwarizmi/[name] .      #Dockerfileからbuildする(Dockerfileがいるディレクトリに入って)


images
========

elixir(コードを見やすく表示するやつ)のコンテナ
https://hub.docker.com/r/yutarohayakawa/elixir/

::

  $ mkdir ~/projects
  $ docker run --name elixir -p 8090:80 -v ~/projects:/usr/local/elixir/http/projects -d yutarohayakawa/elixir
  $ docker exec elixir ./add_project -r https://github.com/nginx/nginx -n nginx


imageを作成する
=================

AlmaLinuxのminimalイメージを参考にimageを自作する
 https://hub.docker.com/_/almalinux

この手順では，ホストマシンは作りたいAlmaLinuxの同バージョンである必要がある．
ほかのディストリビューションでやる場合には，適当にリポジトリを設定してやればよい．
rpmでないディストリビューションでも，rpmとdnfを使えるようにしてやればよい．

AlmaLinuxのminimalイメージにどんなパッケージが入っているか確認
-----------------------------------------------------------------

::

  $ docker pull almalinux:9.3-minimal
  $ docker run -it almalinux:9.3-minimal /bin/bash
  # rpm -qa --qf "%{NAME}\n" //! gpg-key は除外しておかないといけないのでここで grep -v しといてもいい


これで取得できたパッケージでroot fsを作る

root fs 作成
----------------

::

  //! ディレクトリはなんでもいい
  $ mkdir my-alma-minimal
  //! ↑で確認したパッケージ一覧を突っ込む
  $ sudo dnf --installroot=</full/path/to>/my-alma-minimal --releasever=9 --setopt=install_weak_deps=False install libgcc crypto-policies tzdata pcre2-syntax ncurses-base libreport-filesystem dnf-data almalinux-gpg-keys almalinux-release almalinux-repos setup filesystem basesystem ncurses-libs glibc bash glibc-common glibc-minimal-langpack zlib libgpg-error xz-libs bzip2-libs libzstd libxml2 sqlite-libs libcap libcom_err libffi p11-kit libassuan libgcrypt gmp libattr libacl libsigsegv libsmartcols libtasn1 libunistring libuuid libxcrypt lz4-libs pcre grep popt readline libidn2 mpfr gawk libksba file-libs alternatives p11-kit-trust gdbm-libs json-c keyutils-libs libcap-ng audit-libs libnghttp2 libsepol libstdc++ libverto libyaml lua-libs nettle gnutls npth pcre2 libselinux coreutils-single sed ca-certificates openssl-libs libcurl-minimal curl-minimal cyrus-sasl-lib libarchive rpm-libs rpm libsolv libevent openldap gnupg2 gpgme systemd-libs libblkid libmount glib2 gobject-introspection libpeas libmodulemd librepo libdnf microdnf libusbx rootfiles krb5-libs

  //! もし追加したいものがあったら追加する
  $ sudo dnf --installroot=/home/khwarizmi/mock-minimal --setopt=install_weak_deps=False install epel-release


root fs 作成続きと掃除
-------------------------

::

  $ dnf --installroot=/home/khwarizmi/mock-minimal clean all
  $ sudo rm -rf var/cache/
  $ sudo rm -rf var/log/
  //!!!!!! ほんとは var/lib/dnf も消したいし消していい気がするけど試してない

  //! dev ファイルの作成
  //! この辺は参考リンクみつつ
  //! あと参考のminimalイメージもみつつ
  //! 割と適当でも動くは動くはず
  $ cd </path/to>/my-alma-minimal
  $ sudo rm null
  $ sudo mknod -m 666 null c 1 3
  $ sudo mknod -m 666 zero c 1 5
  $ sudo mknod -m 666 random c 1 8
  $ sudo mknod -m 666 urandom c 1 9
  $ sudo mkdir -m 755 pts
  $ cd pts/
  $ sudo mknod -m 666 ptmx c 5 2
  $ sudo mknod -m 640 0 c 136 0
  $ sudo mknod -m 640 1 c 136 1
  $ sudo mknod -m 640 2 c 136 2
  $ sudo chown root:tty 0
  $ sudo chown root:tty 1
  $ sudo chown root:tty 2
  $ sudo chmod 620 0
  $ sudo chmod 620 1
  $ sudo chmod 620 2
  $ cd ..
  $ sudo mkdir -m 1777 shm
  $ sudo mknod -m 666 tty c 5 0
  $ sudo mknod -m 600 console c 5 1
  $ sudo ln -s pts/ptmx ptmx


動作確認とdocker importまで
-------------------------------

::

  $ sudo chroot /home/khwarizmi/my-alma-minimal /bin/bash
  $ cd my-alma-minimal/
  $ sudo tar -c . | docker import - alma-my-minimal


