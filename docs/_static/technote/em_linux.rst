==============================
組み込みLinux開発の時のメモ
==============================

ポリテク研修でやったこと適当に並べておくのであとでまとめる


ターゲットボードやクロスコンパイルのための準備
================================================

ひとまず用意することとして，ターゲットボードで動作するバイナリを用意するためのコンパイラ等々とターゲットにインストールするカーネルに対応するglibcを用意する．
以下の手順

- この準備のための環境構築
- binutilsをビルド(gccに必要)
- gccをビルド
  ただしここでビルドするのは無駄なオプションを削ぎ落としていて，glibcをビルドするためのものである．後にglibcをビルドしたあとちゃんとしたgccをビルドする．
  何故こうするかと言うと，gccとglibcは相互依存しているが，glibcのgccへの依存は部分的であるためである．
- カーネルヘッダの用意
- glibcのビルド
- gccのビルド


この準備のための環境構築
-----------------------------

おおよそすでにインストールけどいちお

::

  $ sudo apt install m4 gawk libgmp-dev libmpfr-dev libmpc-dev







