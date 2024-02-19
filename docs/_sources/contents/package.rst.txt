===============================
パッケージ管理ツールに関して
===============================

ちょっと歴史的な話も入りそうだし，一部technoteに写した方が良いのではないかと言う話がある．

APT及びdebianパッケージ(debian系)
====================================






YUM・DNF及びRPMパッケージ(RedHat系)
=======================================


参考
-------

あとでそれぞれの章に移すかもしれないけど．  

*RPMについて，詳しく書いてあるっぽい*
 - "GURU LABS - CREATING RPMS GUIDE": https://www.gurulabs.com/media/files/courseware-samples/GURULABS-RPM-GUIDE-v1.0.PDF

*パッケージングに関して*
 - "Packaging Tutorial: GNU Hello": https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/
 - "How to create a GNU Hello RPM package/ja": https://fedoraproject.org/wiki/How_to_create_a_GNU_Hello_RPM_package/ja
 - "Creating RPM packages": https://asamalik.fedorapeople.org/tmp-docs-preview/quick-docs/creating-rpm-packages/
 - "RPM Packaging Guide": https://rpm-packaging-guide.github.io/

*後のパッケージングで参考にしたいリンク*
goのビルド(%buildで直コマンドたたくだけだけど)とsystemd service unit追加の例まで含まれている．
 - "Build your own RPM package with a sample Go program": https://developers.redhat.com/articles/2021/05/21/build-your-own-rpm-package-sample-go-program#

*fedora sourcecodeとか*
 - Fedora Pagure: https://pagure.io/
 - Fedora Package Source: https://src.fedoraproject.org/


fedora koji関連
---------------------

*fedora account*
 - https://accounts.fedoraproject.org/

*kojiを利用したfedora向けビルドに関して*
 - "Building in Fedora infrastructure": https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/#_building_in_fedora_infrastructure
 - "Installing Packager Tools"(認証など): https://docs.fedoraproject.org/en-US/package-maintainers/Installing_Packager_Tools/
 - "Using the Koji build system": https://docs.fedoraproject.org/en-US/package-maintainers/Using_the_Koji_Build_System/

*"Using the koji build system" よりtagとターゲットについて*
(https://docs.fedoraproject.org/en-US/package-maintainers/Using_the_Koji_Build_System/#koji_tags_and_packages_organization)
 - tagはパッケージの集合を表す．tagは継承できる．
 - 普通のビルドシステムのリポジトリがtagに該当するイメージでいいはず?
 - targetは，buildrootとなるtag(ビルド時に参照するリポジトリに該当する)とビルド生成物に付与されるタグの設定．
 - tagやtargetは権限がある人でないとできないようで，個人用のtagやtarget作成も現状は無理っぽい．
 - scratchbuild指定した場合には，指定したtargetのbuildrootを利用してビルドするものの，生成物のtag付与は行わないみたいな感じっぽい．
 - (おそらくscratchじゃなくてproduct?ビルドも権限がないと無理だと思う．)

テストとしてfedora kojiでCentOS Streamのreleaseパッケージを，gitlabのリンクを指定してビルドしてみたが，まだうまくいっていないという例

::

  $ koji build --scratch f38 git+https://gitlab.com/redhat/centos-stream/rpms/centos-release#2e8259a53fcf1fe43b29d07a48e3686e75d6a6fd

まず少なくともここに指定するscmのurlは，どうやら許可された限られたurlしか受け付けなくなっているみたい? 
スクラッチビルドの許可リストは分けたみたいな情報はあった．
https://pagure.io/fedora-infrastructure/issue/9728

gitlabにリポジトリをおいてそこのリンクを指定してkojiコマンドをたたくみたいなのを想定していたけど，少なくともfedoraのkojiを使うならそれは無理そうかな．



fedora COPR関連
-----------------------------

 - https://copr.fedorainfracloud.org/coprs/
 - "How to Publish your Software on Copr, Fedora’s User Repository": https://docs.fedoraproject.org/en-US/quick-docs/publish-rpm-on-copr/
 - fedora COPR User Documentation: https://docs.pagure.org/copr.copr/user_documentation.html
 - fedora COPR Screenshots tutorial: https://docs.pagure.org/copr.copr/screenshots_tutorial.html#screenshots-tutorial

とりあえずUser DocumentationとScreenshots tutorialを見ればなんとなくビルドは仕掛けられる．

::

  ### まずauthentication tokenを.config/coprに作成する．詳細はUser Documentationにある．
  $ sudo dnf install copr-cli
  $ copr-cli build <プロジェクト名> <path to your SRPM>


  

概要
---------



パッケージ開発とかのためのパッケージ
--------------------------------------

::

  $ sudo dnf install @development @rpm-development-tools





ソースコード(SRPM)をダウンロードしてビルドする
--------------------------------------------------

::

  $ dnf download --source [package]
  $ rpm -i [落ちてきたrpm]

ここでホームディレクトリを見ると rpmbuild というディレクトリができていてそこに展開されている．
ここで rpmbuild --showrc | grep topdir してみるとrpmbuildの時のディレクトリ構成みたいなものが見える．
真面目にrpmパッケージの開発を複数するときはこういうのをちゃんと理解してやる必要がありそう．

::

  $ rpmbuild --showrc | grep topdir
  -13: _builddir  %{_topdir}/BUILD
  -13: _buildrootdir      %{_topdir}/BUILDROOT
  -13: _rpmdir    %{_topdir}/RPMS
  -13: _sourcedir %{_topdir}/SOURCES
  -13: _specdir   %{_topdir}/SPECS
  -13: _srcrpmdir %{_topdir}/SRPMS
  -13: _topdir    %{getenv:HOME}/rpmbuild
        -- archivename, no v prefix in the topdir naming inside the archive

  $ ls -1 ~/rpmbuild/
    SEPC     ### specファイルが入ってる
    SOURCE   ### ソースコード・パッチ・デフォルト設定ファイル・READMEなどが入っている．

  ### そのまんまビルドする
  $ sudo dnf builddep ~/rpmbuild/SPECS/[package].spec      ### specファイルから(ビルド時の)依存パッケージをインストール
  $ rpmbuild -ba ~/rpmbuild/SPEC/[package].spec            ### ビルドする
  $ ls ~/rpmbuild/RPMS/                                    ### specファイルに書いてあるサブパッケージも含めてビルドしてできたrpmパッケージが転がってる


パッケージを署名する
----------------------

::

  ### キーペアの作成と設定とか
  $ gpg --gen-key                                         ### 鍵作成．名前とかメールアドレスとか入れる ~/.gnupg ファイルの中にできる
  $ gpg --list-keys                                       ### 鍵が表示される
  $ gpg --export -a '[キーペアの名前]' > ~/rpm-key        ### 公開鍵をexportする
  $ sudo rpm --import ~/rpm-key                           ### 公開鍵をシステムにimportする
  $ sudo rpm -q gpg-pubkey -qf '%{summary}\n'             ### 登録してある公開鍵のlistを取得する BaseOSのキーとかepelのキーとかもあると思う
                                                          ### これとペアの秘密鍵で署名されたパッケージを信頼することになるので注意
  $ echo "%_gpg_name [キーペアの名前]" > ~/.rpmmacros     ### rpmマクロファイルに自身が作成するrpmパッケージに利用するキーペアの名前を設定する

  ### ビルドしたrpmパッケージに署名をする．
  $ rpm --addsign ~/rpmbuild/RPMS/*/*.rpm                 ### 署名する 署名はrpmマクロに登録されている鍵で行われる
  $ rpm --checksig [path to rpm]                          ### 確認

  ### リポジトリの署名検証をONにする．
  $ sudo vim /etc/yum.repos.d/[reponame].repo             ### このレポジトリからインストールする時に署名のチェックがされるようにする
  - gpgcheck=0
  + gpgcheck=1


epel向けパッケージをmockでビルドしてみる例
---------------------------------------------------

mockパッケージをインストールしてuseraddしておく

::

  $ sudo dnf install mock
  $ sudo usermod -a -G mock $USER

swayをepel向け(ベースはAlmaLinux)でビルドしてみる．

swayはfedoraでは提供されているものの，epelでは提供されていない．
swayのビルドには，ベースのAlmaLinuxで提供されているパッケージとepelで現在提供されているパッケージ以外で，以下のパッケージが必要．
また以下のパッケージ同士でも依存関係があるので，ビルドする順番は大事．

 - seatd(libseat)
 - wlroots

kojiからfedora36向けのswayのsource rpmを持ってくる
https://koji.fedoraproject.org/koji/buildinfo?buildID=2088661

このパッケージを取得して以下のコマンドでビルドを試してみる．
コンフィグは/etc/mock配下のalma+epel-9-x86_64を使う．
以下のエラーが出る．

::

 $ mock -r alma+epel-9-x86_64 --rebuild sway-1.7.4.fc36.src.rpm 
 (...)
 Error:
  Problem: nothing provides requested (pkgconfig(wlroots) >= 0.15.0 with pkgconfig(wlroots) < 0.16)
  (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)

pkgconfig(wlroots)がないといわれる．
具体的なfedora上でのパッケージ名はfedora上で下のようにすればわかる．

::
  
  ### fedora38上で実行
  $ dnf provides "pkgconfig(wlroots)"
  Last metadata expiration check: 0:00:01 ago on Wed 14 Feb 2024 06:08:08 PM JST.
  wlroots-devel-0.16.2-1.fc38.i686 : Development files for wlroots
  Repo        : fedora
  Matched from:
  Provide    : pkgconfig(wlroots) = 0.16.2

  wlroots-devel-0.16.2-1.fc38.x86_64 : Development files for wlroots
  Repo        : fedora
  Matched from:
  Provide    : pkgconfig(wlroots) = 0.16.2
  (...)


wlroots-develが足らないらしいので，同様に持ってきてビルドする．
https://koji.fedoraproject.org/koji/buildinfo?buildID=2088613

::

  $ mock -r alma+epel-9-x86_64 --rebuild wlroots-0.15.1-5.fc36.src.rpm
  (...)
  No matching package to install: 'pkgconfig(libseat)'
  No matching package to install: 'pkgconfig(xwayland)'
  Not all dependencies satisfied
  Error: Some packages could not be found.

それぞれfedora上で確認する．
  
::

  ### fedora38上で実行
  $ dnf provides 'pkgconfig(libseat)'
  Last metadata expiration check: 26 days, 10:08:29 ago on Fri 19 Jan 2024 08:13:58 AM JST.
  libseat-devel-0.7.0-3.fc38.i686 : Development files for libseat
  Repo        : fedora
  Matched from:
  Provide    : pkgconfig(libseat) = 0.7.0

  libseat-devel-0.7.0-3.fc38.x86_64 : Development files for libseat
  Repo        : fedora
  Matched from:
  Provide    : pkgconfig(libseat) = 0.7.0
  (...)

  $ dnf provides 'pkgconfig(xwayland)'
  xorg-x11-server-Xwayland-devel-22.1.9-1.fc38.i686 : Development package
  Repo        : fedora
  Matched from:
  Provide    : pkgconfig(xwayland) = 22.1.9

  xorg-x11-server-Xwayland-devel-22.1.9-1.fc38.x86_64 : Development package
  Repo        : fedora
  Matched from:
  Provide    : pkgconfig(xwayland) = 22.1.9


xorg-x11-server-Xwayland-develはAlmaLinuxのdevelリポジトリにある．
configでdevelも参照するようにすればよさそう．

::

  $ dnf list xorg-x11-server-Xwayland-devel
  AlmaLinux 9 - AppStream                                        5.9 kB/s | 4.1 kB     00:00
  AlmaLinux 9 - BaseOS                                           5.7 kB/s | 3.8 kB     00:00
  AlmaLinux 9 - Devel                                            5.9 kB/s | 4.1 kB     00:00
  AlmaLinux 9 - Extras                                           4.6 kB/s | 3.8 kB     00:00
  Available Packages
  xorg-x11-server-Xwayland-devel.x86_64                    22.1.9-2.el9                     devel


というわけで以下のような/etc/mock/alma9-local.cfgを作成する．
今までのconfigをincludeしたうえで，develリポジトリを追加するようにしている．
(今までのconfigで使っているtemplate/almalinux-9.tplでもdevelはenable=0で定義されているけど，末尾に追加しちゃえば問題ないらしい．)

::

  include('alma+epel-9-x86_64.cfg')

  config_opts['root'] = "alma+epel+devel+local-9-{{ target_arch }}"
  config_opts['description'] = 'AlmaLinux 9 + EPEL + devel(for pkgconfig(xwayland)) + local'

  config_opts['dnf.conf'] += """
  [devel]
  name=AlmaLinux $releasever - Devel
  mirrorlist=https://mirrors.almalinux.org/mirrorlist/$releasever/devel
  # baseurl=https://repo.almalinux.org/almalinux/$releasever/devel/$basearch/os/
  gpgcheck=1
  enabled=1
  gpgkey=file:///usr/share/distribution-gpg-keys/alma/RPM-GPG-KEY-AlmaLinux-9
  """

このコンフィグでビルドしてみる．

::

  mock -r alma9-local --rebuild wlroots-0.15.1-5.fc36.src.rpm
  No matching package to install: 'pkgconfig(libseat)'
  Not all dependencies satisfied
  Error: Some packages could not be found.

libseat-develを先にビルドしないといけないので，今までと同様に取ってきてビルドしてみる．
https://koji.fedoraproject.org/koji/buildinfo?buildID=1969776

::

  $ mock -r alma9-local --rebuild seatd-0.7.0-1.fc36.src.rpm

こんどはビルドが成功する．
ビルド生成物の出力先はログに書いてあるので適当に保存しておく．


今後のビルドでは生成物を利用してビルドを行う．
ローカルリポジトリを作成してmockビルド時にそこを参照するようにする．

適当にディレクトリを掘ってそこにビルドしてできたパッケージを入れておく．
そのディレクトリを対象にcreaterepoコマンドを実行してリポジトリ化する．

::

  $ createrepo [対象ディレクトリ]

対象ディレクトリ配下にrepodataというサブディレクトリができていればOK

今作成したローカルリポジトリを参照してmockでビルドを行う．
コンフィグに追加しても良いが，今回はmockコマンドのオプションを使うことにする．
再度wlrootsのビルドを行う．

::

  $ mock -r alma9-local --rebuild wlroots-0.15.1-5.fc36.src.rpm --addrepo=file://[ローカルリポジトリのパス]

これでwlrootsのビルドも完了．
ここで生成されたパッケージをローカルリポジトリに加えて，createrepoしなおす．
そして最後にお目当てのswayのビルドを行う．

::

  $ mock -r alma9-local --rebuild sway-1.7-4.fc36.src.rpm --addrepo=file:///home/khwarizmi/localrepo/

これでビルドは完了．


neovimのパッケージを自作してリポジトリまで自作する(一応アーカイブとして残してるけどあとで消す)
--------------------------------------------------------------------------------------------------

epelからインストールできるneovimはv3.8でバージョンが低いので，v4.4くらいのパッケージを自作してみる．

