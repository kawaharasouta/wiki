==========
FPGA関連
==========

今後ずっとFPGAをやっていくかはわかんないけど，今後の役に立ちそうなことはmemoしておこうかな．



開発環境
=========

ボード: DE0-CV (altera(Intel))
開発ソフトウェア: Quartus Prime Lite Edition ver17.0 (https://www.intel.co.jp/content/www/jp/ja/software/programmable/quartus-prime/download.html)
OS: Windows10


環境構築
=========

Quartus Prime install
----------------------



USB-Blasterドライバ install
---------------------------


なんか色々メモっとくゾーン
==========================

命名規則
---------

.. csv-table::
  :header: 項目, 内容
  :widths: 8, 8

  ファイル, 小文字 拡張子は「.v」
  モジュール, 大文字
  入出力信号, 大文字
  パラメータ, 大文字
  内部信号, 小文字
  ローアクティブ信号, 先頭に「n」
  HDLファイルの保存場所, プロジェクトファイルないの「HDL」ディレクトリ
  プロジェクト名と最上位階層名, 大文字で同一にする

ファイルの種類?
----------------

.. csv-table::
  :header: 項目, 内容
  :widths: 4, 4

  ~~~~.v, verilogファイル?
  ~~~~.qsf, ピンアサインファイル(他各種設定ファイル?)
  ~~~~.sdc, 制約ファイル(クロックとか使うのにいる?)
  ~~~~.qpf, プロジェクトファイル




Verilog HDL
===========




