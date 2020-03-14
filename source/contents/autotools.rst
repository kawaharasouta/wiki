===========
autotools
===========

https://www.miraclelinux.com/tech-blog/reqys8

移植性の高いビルドを可能にするビルドツール．
Mafileをそのものを生成する．次のような特徴がある．
- 自動的に依存関係を生成
- 複数のプラットホームをカバーしやすい
- デフォルトでclean, install, distなどの標準的なターゲットが生成される

環境構築
===========

::

  $ sudo apt install autoconf automake gcc make



Hello World
============


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







