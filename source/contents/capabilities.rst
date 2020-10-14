===================
Linux capabilities
===================

root権限を細かく分割して，特定の権限のみを与えるためのもの．
root権限が必要な操作を含む場合，本来ならば当然root権限で実行する必要があるが，
その実行は本来必要でない操作への権限(root権限なのでね)も持ってしまっているため，
もし脆弱性があった場合非常に危険であるが，
これを使うとその問題が避けられる

例

- CAP_DAC_OVERRIDE
  ファイルの read, write, execute パーミッションのチェックをバイパスする。
- CAP_DAC_READ_SEARCH
  ファイルの read とディレクトリの read と execute のパーミッションチェックをバイパスする。
- CAP_KILL
  シグナルを送るときの権限チェックをバイパスする。
- CAP_NET_BIND_SERVICE
  特権ポートにソケットをバインドできる。
- CAP_SYS_TIME
  システムの時刻を設定できる。．

File capabilities
===================

実行ファイルに capabilities を持たせる方法．
注意点として，
この方法だと起動したユーザによらずプロセスがcapabilitiesを持つことになる．


Ambient capabilities
======================

init(=systemd として良いのか?)から起動するようなプロセス(デーモン)に対して
capabilitiesを持たせる方法．



参照
===========

http://matope.hatenablog.com/entry/2014/09/28/031155
https://nojima.hatenablog.com/entry/2016/12/03/000000
https://linuxjm.osdn.jp/html/LDP_man-pages/man7/capabilities.7.html
https://source.android.com/devices/tech/config/ambient

