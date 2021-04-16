===============================
パッケージ管理ツールに関して
===============================

ちょっと歴史的な話も入りそうだし，一部technoteに写した方が良いのではないかと言う話がある．

APT及びdebianパッケージ(debian系)
====================================






YUM・DNF及びRPMパッケージ(RedHat系)
=======================================


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

neovimのパッケージを自作してリポジトリまで自作する
-----------------------------------------------------

epelからインストールできるneovimはv3.8でバージョンが低いので，v4.4くらいのパッケージを自作してみる．




