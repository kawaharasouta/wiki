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


*fedora COPR関連*
 - https://copr.fedorainfracloud.org/coprs/
 - "How to Publish your Software on Copr, Fedora’s User Repository": https://docs.fedoraproject.org/en-US/quick-docs/publish-rpm-on-copr/


テストとしてfedora kojiでCentOS Streamのreleaseパッケージを，gitlabのリンクを指定してビルドしてみたが，まだうまくいっていないという例

::

  $ koji build --scratch f38 git+https://gitlab.com/redhat/centos-stream/rpms/centos-release#2e8259a53fcf1fe43b29d07a48e3686e75d6a6fd

まず少なくともここに指定するscmのurlは，どうやら許可された限られたurlしか受け付けなくなっているみたい? 
スクラッチビルドの許可リストは分けたみたいな情報はあった．
https://pagure.io/fedora-infrastructure/issue/9728

gitlabにリポジトリをおいてそこのリンクを指定してkojiコマンドをたたくみたいなのを想定していたけど，少なくともfedoraのkojiを使うならそれは無理そうかな．
  

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






neovimのパッケージを自作してリポジトリまで自作する(一応アーカイブとして残してるけどあとで消す)
--------------------------------------------------------------------------------------------------

epelからインストールできるneovimはv3.8でバージョンが低いので，v4.4くらいのパッケージを自作してみる．

