========
DTrace
========


使い方?
========

::
  
  probe_dewcriotion /predicate/ { action }

プローブ
=========

::

  provider:module:function:name


provider
=========


.. csv-table::
  :header: provider, プロバイダ
  :widths: 15, 15
  
  syscall, システムコールトラップテーブル
  vminfo, 仮想メモリ統計
  sysinfo, システム統計
  profile, 任意のサンプリング
  sched, カーネルスケジューリングイベント
  proc, プロセスレベルのイベント
  io, ブロックデバイスのイベント(作成，実行，終了)
  pid, ユーザレベルの動的トレーシング
  tcp, TCPプロトコルのイベント(接続，送信，受信)
  ip, IPプロトコルのイベント
  fbt, カーネルレベルの動的トレーシング

  また，その他の高水準言語


