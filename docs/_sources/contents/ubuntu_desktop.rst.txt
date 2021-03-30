=================
ubuntu desktop
=================

そのうちubuntu(じゃなくてもいいけどlinux類にはしたい)にしようと思ってるからちょいちょいメモする．


そもそもxwindowとかgnomeとかについて
======================================

なんかあとで

GPU(nvidia)のドライバ
========================

とりあえず↓を見てやるとよい．あとでここ書き直す．
http://urusulambda.com/2018/04/14/ubuntu%E3%81%A7nvidia-driver%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%81%9F%E3%82%89nouveau%E6%AD%A2%E3%82%81%E3%82%8D%E3%81%A3%E3%81%A6%E8%A8%80%E3%82%8F%E3%82%8C/

lightdm を disable(自動起動をoff) した場合，is-enabledで見るとstaticとなっていて，もう一度自動起動させようとenableとかreenableとかしても自動起動できなくなる．
ここら辺は依存関係が云々とかの話なんだけど，詳しい話はまた今度調べよう．
結論としては↓のようにすると元に戻る．

::

  $ sudo dpkg-reconfigure lightdm

まあとりあえず，lightdmはこれ自体を起動したりするものじゃなくて依存関係の中でどこかで起動されうるものって感じか．

参考:
https://forum.odroid.com/viewtopic.php?t=34109
https://milestone-of-se.nesuke.com/sv-basic/linux-basic/systemctl/

他のいろんな設定の話
=====================

設定に関していろんなものが詰まったところ

https://sicklylife.jp/ubuntu/2004/settings.html

https://sicklylife.hatenablog.com/entry/2019/01/04/200538




