===============
データベース
===============


SQLite
==========

bomctlをやるに当たって，データベースにsqliteを使っているので少し勉強しなきゃいけなくなった．
そもそもデータベースとかSQLがわかっていないので，sqliteに限らない(例えば一般的なSQLとか)のことも書く気がするけどご愛嬌．
場合によってはbomctlのことも書くかもしれない．


Package install for CLI tool (AlmaLinux9)
--------------------------------------------

::

  $ sudo dnf install sqlite

SQLite CLI
------------

::

  $ sqlite [/path/to/dbfile]
  $ sqlite ~/.cache/bomctl/bomctl.db

SQLiteの特殊コマンド?系
::

  .tables
  .schema                   -- 全テーブルの構造
  .schema テーブル名          -- 特定テーブルの構造
  .quit
  .help

SQL
::

  SELECT カラム名 FROM テーブル名;        -- 基本的な検索
  SELECT COUNT(*) FROM テーブル名;       -- レコード数を数える
  SELECT * FROM テーブル名;              -- 全カラムを表示

  SELECT d.id, m.name FROM documents d LEFT JOIN metadata m ON d.id = m.document_id;
    # JOIN: 複数のテーブルを結合
    # LEFT JOIN: 左側（documents）のすべてのレコードを表示
    # ON d.id = m.document_id: 結合条件（documentsのidとmetadataのdocument_idが一致）

  SELECT * FROM テーブル名 LIMIT 5;  -- 最初の5件だけ表示
  SELECT DISTINCT カラム名 FROM テーブル名;  -- 重複を除いた値一覧

  SELECT * FROM テーブル名 WHERE カラム名 = '値';
  SELECT * FROM テーブル名 WHERE カラム名 IS NULL;  -- 空の値を検索

  SELECT カラム名, COUNT(*) FROM テーブル名 GROUP BY カラム名;  -- グループ別集計
