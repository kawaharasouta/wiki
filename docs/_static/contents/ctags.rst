ctags
============




超Quick Start
-------------------

参考:  
 - "ctagsの使い方": https://people.redhat.com/yamato/talks/reading/slides/1/12ctags-usage.pdf
 - "開発のお供に - タグ・リファレンスツール": http://gotom.jp/~gotom/pub/2001-07-debuan-comiket-01summer/gotom.pdf



雑に次のようなソースコード

input.c

.. code-block:: c

  #include <stdio.h>
  static boolean debug;
  #include DEBUG(X) (debug=X)
  struct point2d {int x, y;};
  typedef struct point2d *pp;
  int distance (pp p0, pp p1) { /* ... */}
  int main (int argc, char** argv) {
    int local;
  /* ... */
    goto_label:
    return 0;
  }

tagsの出力例

::

  $ ctags -o - input.c
  debug input.c /^static boolean debug;$/;" v file:
  distance input.c /^int distance (pp p0, pp p1) { \/* ... *\/}$/;" f
  main input.c /^int main (int argc, char** argv) {$/;" f
  point2d input.c /^struct point2d {int x, y;};$/;" s file:
  pp input.c /^typedef struct point2d *pp;$/;" t typeref:struct:point2d file:x input.c /^struct point2d {int x, y;};$/;" m struct:point2d file:
  y input.c /^struct point2d {int x, y;};$/;" m struct:point2d file:

こんな感じでタグリファレンス?用のデータベースファイルが生成される．
`-o -` で標準出力に出力する．  

通常の使い方では，トップディレクトリで以下のように実行する．

::

  $ ctags -R
  
tagsというファイルが生成されている．  
ここで例えばシンボル名?を指定して次のようにvimを起動する．

::

  $ vi -t debug

するとそのシンボルにカーネルが合ってvimが起動されているはず．

