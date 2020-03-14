===========
autotools
===========

autoconf, automake, (libtool?) のこと?

よくGNUのソフトウェアはtarボールを展開して ./configure && make && make install とかしてインストールできてしまうが，それのこと．

configure.acとMakefile.amとを書くことによりパッケージの自動生成が可能になる．
複数のプラットフォームでMakefileを共通化できる．
これらGNU Autotoolsを活用すれば，簡単に配布用のフリーソフトウェアパッケージを作ることができる．
AutotoolsはそんなGNU流のフリーソフトウェアパッケージの構築を半自動化するための開発者用のツールである．
最終目的はmake distcheck で [パッケージ名]-[version].tar.gz 形式のパッケージが自動生成できるようになること．
Autotoolsは開発者用のツールであって，パッケージのユーザはそのマシンにAutotoolsをインストールする必要はないし，Autotoolsについて知っている必要もない．

移植性の高いビルドを可能にするビルドツール．
Makefileをそのものを生成する．次のような特徴がある．
- 自動的に依存関係を生成
- 複数のプラットホームをカバーしやすい
- デフォルトでclean, install, distなどの標準的なターゲットが生成される

http://loto.sourceforge.net/feram/Autotools-memo.ja.html

環境構築
===========

::

  $ sudo apt install autoconf automake gcc make



Hello World
============

https://www.miraclelinux.com/tech-blog/reqys8

configure.ac

::

  AC_INIT([prog1], [1.0])
  AM_INIT_AUTOMAKE([foreign])
  AC_PROG_CC
  AC_OUTPUT([Makefile]) 

Makefile.am

::

  bin_PROGRAMS = prog1

prog1.c

::

  #include <stdio.h>
  #include "prog1.h"
  
  int main(void) {
    printf("My name is %s.\n", MY_NAME);
    return 0;
  }

prog1.h

::

  #define MY_NAME "prog1"

command

::

  $ autoreconf -i
  $ ./configure
  $ make

  $ make install
  $ make clean
  $ make distclean  # Makefileなど?の広範囲な生成物．このあと再度configureする必要がある．
  $ make dist       # 配布用のtarボールを生成する．








**autotoolsのための.gitignore**: https://github.com/github/gitignore/blob/master/Autotools.gitignore









