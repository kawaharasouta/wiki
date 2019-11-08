===========
systemtap
===========

実行中のカーネルの特定の処理にフックしてデバッグを行ったりするツール．

SystemTapは「STPスクリプト」と呼ばれる独自言語のスクリプトを利用して記述します。
SystemTapのコマンドであるstapコマンドがSTPスクリプトとカーネルのデバッグ情報からC言語のコードを生成して，
それをカーネルモジュールとしてビルド・ロードし，その結果を標準出力や独自のログバッファなどに保存するのです。



install
==============

「SystemTap本体」と「対象カーネルのデバッグ情報」が必要

::

  $ sudo apt install gnupg
  $ codename=$(lsb_release -c | awk  '{print $2}')
  $ sudo tee /etc/apt/sources.list.d/ddebs.list << EOF
    deb http://ddebs.ubuntu.com/ ${codename}      main restricted universe multiverse
    #deb http://ddebs.ubuntu.com/ ${codename}-security main restricted universe multiverse
    deb http://ddebs.ubuntu.com/ ${codename}-updates  main restricted universe multiverse
    deb http://ddebs.ubuntu.com/ ${codename}-proposed main restricted universe multiverse
    EOF
  $ sudo apt update
  $ sudo apt install -y linux-image-$(uname -r)-dbgsym



  
