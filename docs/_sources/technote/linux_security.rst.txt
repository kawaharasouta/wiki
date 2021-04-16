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







