====================
Linuxの認証周りの話
====================

PAM
=====

Linuxには認証機能を使うソフトウェアがたくさんあるけど，それぞれのソフトウェアで独自に認証機能を実装してるのはよくないのでモジュールにしたものがある．
それが PAMとかPAM認証 とかってやつ．

/etc/pam.d を見ると，なんかよく見るデーモンの名前のファイルとかがあって，認証にはこいつらを使ってるぽいらしいくさい．
これ以上はよくわからなくなりそうだから触れない．こういうのがあったよっていうメモ．



参照: https://ozuma.hatenablog.jp/entry/20131005/1380942386

passwd変更
-----------

it is based on a dictionary word とかって怒られる時の対処
なんか↓のようにしたら動いた．

::

  $ sudo vim /etc/pam.d/passwd

  + password   sufficient   pam_unix.so nullok md5 shadow
  + password   required     pam_deny.so

参照: https://volvox.hateblo.jp/entry/20130813/1376399307
