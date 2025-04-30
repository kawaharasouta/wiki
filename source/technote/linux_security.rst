======================================
Linuxのセキュリティモジュールについて
======================================


歴史とかをちょいと書いておく
=====================================

SELinux(Security-Enhanced Linux)はよく聞くセキュリティモジュールであるが，2003年にはすでにLinuxのupstreamにマージされたものである．
Linuxの機能であるためどのディストリでも動かすことが可能なはずではあるが，実はCentOS意外だと導入に段差があったりするらしい．(今はそんなことない?)
周知の通りCentOSではデフォルトで動いている．
ところでubuntuやSUSEではデフォルトでAppArmorというセキュリティモジュールが動くようになっている．他にもいくつものセキュリティモジュールが世の中に存在して，
現在Linuxにマージされているのは AppArmor，Security-Enhanced Linux，SELinux，Smack，TOMOYO，LoadPin?，Yama?
これらは全てモジュールとして実装されており，LSM(Linux Security Modules)の上で動作する．


https://www.redhat.com/ja/topics/linux/what-is-selinux
https://selinuxproject.org/page/Main_Page
https://wiki.archlinux.jp/index.php/AppArmor
https://www.kernel.org/doc/html/v4.15/admin-guide/LSM/index.html
https://ja.wikipedia.org/wiki/Linux_Security_Modules
https://blog.mono0x.net/2011/06/25/


SELinux
===========

全てのファイル及びプロセスにSELinuxコンテキストと呼ばれる情報をラベル付し，それも元にアクセス制御を行うものである．

(一部の)コンテキストの表示の例(-Zオプション)
-------------------------------------------------

::

  $ ls -Z files1 
  -rw-rw-r--  user1 group1 unconfined_u:object_r:user_home_t:s0 file1
  ### ユーザ(unconfined_u)、ロール(object_r)、タイプ(user_home_t)、レベル(s0)
  
  $ ps -Ze | grep nginx
  system_u:system_r:httpd_t:s0       1706 ?        00:00:00 nginx
  system_u:system_r:httpd_t:s0       1707 ?        00:00:00 nginx
  system_u:system_r:httpd_t:s0       1708 ?        00:00:00 nginx

コンテキストの変更操作系
---------------------------




https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-working_with_selinux-selinux_contexts_labeling_files

httpサーバ構築から見るよくあるSELinuxトラブルシューティング
--------------------------------------------------------------

ここ書いてなくてなにを書きたかったのか忘れてしまった...
たぶん2021年4月ごろの例のあれの話...?
とりあえず枠だけおいておくか．





systemdにsshトンネルを掘らせたときのトラブルシューティング
---------------------------------------------------------------

注意
^^^^^^^^^

※この章の情報は実際の対処から半年以上経って記憶をたよりに書いていることに注意．
 おおいに間違っている可能性があるが，大筋はあっているはず．
 細かいところはその時の自分がその時に確認しろ．

概要
^^^^^^^^

sshトンネルを掘るサービスユニットを定義したがうまく動作しなかった．

大きく以下の2つの観点
 - systemdから起動したプロセスはコンテキストはinit_tになっているが，このコンテキストのプロセスからネットワークポートのバインドができない?(のはず)
 - バインドしたいポート8080が未予約であったためバインドできなかった．

対処など
^^^^^^^^^^^^^^

まず，denyされているログはauditかselinuxの拒否メッセージを確認するコマンドで見る．
後者の方が使い勝手は良いけれど，最初あたりをつけるときは前者のほうがいいと思う．
auditのログは /var/log/audit.log
selinuxの拒否メッセージ確認は以下だが，オプションはかなり適当だし，あまり意味分かってない．

::

  ausearch -m AVC,USER_AVC,SELINUX_ERR -ts recent
  audit2allow -a

先ほどの2つの観点に対処するためにカスタムモジュールを作成する．

詳細に入る前にコマンド系

::

  ### インストールされているモジュール確認
  semodule -l | grep hogehoge
  ### ポートのコンテキスト
  semanage port -l | grep 8080

  ### te(text)からpp(中間ファイル)生成
  checkmodule -M -m -o モジュール名.mod モジュール名.te
  ### pp(ポリシーパッケージ)生成
  semodule_package -o モジュール名.pp -m モジュール名.mod
  ### インストール
  semodule -i モジュール名.pp

  ### selinuxの拒否メッセージから適合するモジュールを作るコマンド
  ### ただし少なくとも自分の環境ではそのままでは動作しなかった
  ### 最初のベースにするのはありだと思うけど
  ausearch -m AVC -ts recent | audit2allow -M モジュール名


カスタムモジュールは3つ作成している．
※冗長な箇所がありそうなので注意．とりあえず確認した時の環境にインストールされていた自作モジュールの内容をダンプしてみている．

1つ目 init_ssh_basic.te 
各行ごとにキャプションをつけてみた

::

  ### モジュール名と版数を宣言
  module init_ssh_basic 1.0;
  
  ### このモジュールが必要とするSELinuxの型・ロール・クラス・権限などの定義
  ### includeとかimportみたいなものだと思っているけどどうなん
  require {
      type init_t;
      type ssh_t;
      type ssh_exec_t;
      role system_r;
      class process { transition sigchld };
      class file { read getattr open execute execute_no_trans entrypoint };
  }
  
  #============= Type transitions =============
  ### systemdプロセス(init_t)がSSH実行ファイル(ssh_exec_t)を実行すると，自動的に新しいプロセスがssh_t型になるという遷移ルール
  type_transition init_t ssh_exec_t:process ssh_t;
  
  #============= init_t ==============
  ### systemd(init_t)にSSH実行ファイル(ssh_exec_t)を読み取り・属性取得・オープン・実行する権限を付与
  allow init_t ssh_exec_t:file { read getattr open execute execute_no_trans };
  ### systemd(init_t)にssh_t型へのプロセス遷移を許可します。
  allow init_t ssh_t:process transition;
  
  #============= ssh_t ==============
  ### SSH(ssh_t)プロセスがsystemd(init_t)に子プロセス終了シグナル(SIGCHLD)を送信できるように許可
  allow ssh_t init_t:process sigchld;
  ### SSH(ssh_t)がSSH実行ファイル(ssh_exec_t)を読み取り・実行・エントリーポイントとして使用できるように許可
  allow ssh_t ssh_exec_t:file { read execute entrypoint };
  
  #============= Role allow =============
  ### system_rロールにssh_t型を関連付けする
  ### systemdから起動されたプロセスはsystem_rロールで実行されるため，この行はssh_t型のプロセスがsystem_rロールで実行できることを保証します
  ### ぶっちゃけよくわかんない
  role system_r types ssh_t;

2つ目 ssh_8080.te

::

  module ssh_8080 1.0;
  
  require {
      type ssh_t;
      type http_cache_port_t;
      class tcp_socket name_bind;
  }
  
  #============= ssh_t ==============
  ### SSH(ssh_t)プロセスがHTTPキャッシュポート(8080, http_cache_port_t)をバインドできるように許可
  allow ssh_t http_cache_port_t:tcp_socket name_bind;

3つ目 ssh_custom_port.te

::

  module ssh_custom_port 1.0;
  
  require {
      type ssh_t;
      type unreserved_port_t;
      class tcp_socket name_bind;
  }
  
  #============= ssh_t ==============
  ### SSH(ssh_t)プロセスが予約されていないポート(unreserved_port_t)をバインドできるようにします。これは8080以外の一般的な非予約ポートを使用するためのルールです。
  allow ssh_t unreserved_port_t:tcp_socket name_bind;


また，メモとして各ポートタイプのポート番号一覧を自分の環境からはっておく．

::

  $ sudo semanage port -l | grep http_cache_port_t
  http_cache_port_t              tcp      8080, 8118, 8123, 10001-10010
  http_cache_port_t              udp      3130

  $ sudo semanage port -l | grep unreserved_port_t
  unreserved_port_t              sctp     1024-65535
  unreserved_port_t              tcp      61000-65535, 1024-32767
  unreserved_port_t              udp      61000-65535, 1024-32767

さらに，自分で特定のポートを特定のタイプに入れることももちろんできる．

::

  sudo semanage port -a -t http_cache_port_t -p tcp 9090


これは書いているときの心境でしかないけれど，unreserved_port_tに許可しただけで大丈夫な気がするんだ．
だって9922とかでも動いているんだもの．

