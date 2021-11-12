==========
segv対策
==========

gdb
====

コンパイル時にデバッグ情報を付与
---------------------------------

::

  $ gcc -g ***.c

or Makefileに

::

  CFLAGS += -g

とかしておく

ちなみになんだけど -g3 にした方がマクロ見れたりあと多分他にもいいことありそうなのでそっちの方が良さげ．
https://kohchi.hatenablog.com/entry/20141124/1416790642

コアダンプ機能を有効化
----------------------

::

  ulimit -c unlimited

デバッグファイル
----------------

問題のプログラムを実行すると

::

  $ ls
  ...
  core

coreとかいうでっかいファイルができる

コマンド
--------

::

  バックトレース
  (gdb) bt
  
  関数選択
  frame 1
  
  ポインタ検索 
  p (ポインタ)

自分がコンパイルしていないライブラリに潜りたい
-------------------------------------------------

普通はライブラリ関数的なのはnextで潜らずに飛ばしてっちゃうんだけど，
stepしてその中も見たいよみたいな場合．

あとで自分で書き直す．
参考
https://stackoverflow.com/questions/48278881/gdb-complaining-about-missing-raise-c
https://doss.eidos.ic.i.u-tokyo.ac.jp/html/gdb_step_into_libraries.html







memo
----------

fedoraでcore吐かせようとしたら，デフォルトの出力がよくわからんかったのでいじったときの参照URL
https://qiita.com/suzutsuki0220/items/aa84d7e2e8f37e867f3d
