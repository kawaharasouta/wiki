linuxのRSSに関して
===================

linuxはデフォでどのようにRSSを行なっているか．
-------------------------------------------------

linuxでは，割り込みの区別にirq番号と言うものを使っている．
irqとは，I/O APICを経由するPCIデバイスの割り込みが上がってくる物理的な割り込み線もしくはそこから上がってくる割り込み要求信号のことで，のことで
現在のMSI・MIS-X割り込みでは使われていないが，おそらく歴史的経緯からlinuxで割り込みの区別をするのにirq番号とか言うものが使われている．
デバイスドライバはデバイスの初期化時にこのirq番号をカーネルから取得する．その後割り込みがあった場合にはこのirq番号に割り込みをあげることになる．
この番号は/proc/interruptで確認することができる．ここには各irqから各コアに対して割り込みが行われた数を記録してある．(他にもっといい確認方法ありそう)
各irqにはデバイスドライバが起動時に名前をつけていて，pciバスアドレスだったりドライバ名が入っていたり，NICだとインタフェース名が入っていたりもする．
ここで，一つのデバイスからいくつのirqが生えているかが確認できるが，インタフェースのirqを見て見ると複数のirqを所持していることがわかる．
ただしこの数はデバイスやデバイスドライバ・割り込みの種類にも関係するが，マルチキューNICではほとんどの場合確実に複数のirqを持っている．
さてこのirqであるが，ここから上がってきた割り込みがどのコアによって処理されるかはどのように決まっているのだろうか．
それは /proc/irq/{irq_num}/smp_affinity に設定されている．
試しにこれファイルの中身を見て見ると,

::

  00,00000002

のような内容になっている．これは割り込み先のCPUのビットマスクである．
この場合0x02は0b10であるため，1番コアに割り込みがいくことになる．
この割り込みビットマスクはlinuxでは通常，irqbalanceによってBadNUMAを起こさないようにかつ別のCPUに割り込みが行くようにバランシングされている．
またこのirqはNICに用意された受信キューの数だけ用意され．NICはRSSによってパケットをハッシュ値ごとに別の受信キューのキューイングされる(と思われる)ため，
割り込みが複数のCPUに分散されRSSにより負荷分散ができているということになる．


linuxで明示的にRSSで使うコア数を制限する
-----------------------------------------

RSSの試験の時にコア数を制限して計測をする方法を記載する．

レポート書く時に一緒にかくう〜〜〜〜






reference
----------

 - `irqbalance <https://sfujiwara.hatenablog.com/entry/20121221/1356084456>`_
 - `ビットマスクと割り込み <https://diary.atzm.org/20111027.html>`_
 - `ethtool queueとか <https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/7/html/performance_tuning_guide/sect-red_hat_enterprise_linux-performance_tuning_guide-networking-configuration_tools#sect-Red_Hat_Enterprise_Linux-Performance_Tuning_Guide-Configuration_tools-Configuring_Receive_Side_Scaling_RSS>`_
 - `RSS無効化なんかもう一個 <https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/6/html/performance_tuning_guide/network-rss>`_
 - `モジュールパラメータ1 <https://stackoverflow.com/questions/23730268/ixgbe-setting-the-number-of-rx-tx-queues>`_
 - `モジュールパラメータ2 <https://www.nic.ad.jp/ja/materials/iw/2011/proceedings/s09/s09-01.pdf>`_






