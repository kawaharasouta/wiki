=================
ubuntu desktop
=================

そのうちubuntu(じゃなくてもいいけどlinux類にはしたい)にしようと思ってるからちょいちょいメモする．
とりあえず僕の今の環境はKubuntuかXubuntuかLubuntuかもしくは何かのubuntuフレーバーの2004だったと思うけど忘れた．
なんかinput sourceがバグり散らかしてない?


ターミナルをどうするか問題
============================

とりあえず今のところmacではiterm2を使っていて，そんなにカスタマイズしてないので，
用件としては
- ホットキーが今iterm2と同じ感じがいい
- ホットキーを押すと今開いてるwindowsに飛んでいってアクティブになる．
- アクティブな状態で押すとウィンドウが消えてくれる．
- なんか広い範囲(freeBSDとか使いたみあるし)で使えるといい
くらいなものか．．．
※ホットキーに関しては別の手段をとることにした．restに打ち消し線がないから消せないよ※

Tilix: 
今使ってるやつ．て言うか標準で載ってたやつを雑に使ってる．
使い心地は悪くないけどどうもホットキーは設定できなそう? openキーならあるけど． 評判は悪くない．
ヘッダの図体がでかい(小さくできそう)

Guake(Quake?):
トップダウンターミナルと言うらしい．それなん?と思ったけど使ってみたらわかった．デスクトップの上からニョキッと生えてくる．
最初気持ち悪かったけど，割といつも使う定位置の右から生えるようにしたらそんなに悪くない感じもあったりする．
ホットキー的なものはあったけど，サブディスプレイでやるとターミナルがディスプレイを飛び越えてついてくるのがいまいち．
これ入れるとF12常にこいつが食って何かと干渉しそう．

ホットキーについて
=====================

jumpappとxbindkeysを用いて実現することにした．
最初はxdotoolとxbindkeysを使おうとしてたのでそこら辺も含めて．

xdotool
-----------

fake input frome mouse and keyboard と windows manager 的なことができるやーつ
https://github.com/jordansissel/xdotool
https://www.semicomplete.com/projects/xdotool/
ちらっとソースコード見た感じわかりやすかった(ただトップディレクトリにファイルが散らばっていて見づらいのでそこだけ注意)

これを利用してwindowをアクティブにしたりみたいなことをする．

xbindkeys
-----------

Xbindkeys はコマンドをキーボードの特定のキーやキーの組み合わせに結びつけることができるプログラムです。Xbindkeys はマルチメディアキーを処理できます。ウィンドウマネージャやデスクトップ環境に依存しないので手軽に使うことが可能です。とのことです．
https://wiki.archlinux.jp/index.php/Xbindkeys

とりあえずコマンドにショートカットキーをくくりつけるらしい．

jumpapp
---------

https://github.com/mkropat/jumpapp
The idea is simple — bind a key for any given application that will:

- launch the application, if it's not already running, or
- focus the application's window, if it is running

と言うことでダイレクトに使いたい機能だけがあるアプリケーションだったので使う．
正直，アクティベートな時に押したら非表示になるみたいな機能があったら最高だった．

jumpappとxbindkeysの設定とかとか
-------------------------------------

::

  $ sudo apt install xbindkeys pandoc
  $ git clone https://github.com/mkropat/jumpapp && cd $_
  $ make && sudo make install                    // なんかここら辺ちょいこけあったりしたのであとで確認しよう．
  $ xbindkeys -d > ~/.xbindkeysrc
  $ vim ~/.xbindkeysrc
  + "jumpapp tilix"
  +   Control + i
  $ xbindkeys



そもそもxwindowとかgnomeとかについて
======================================

なんかあとで

GPU(nvidia)のドライバ
========================

とりあえず↓を見てやるとよい．あとでここ書き直す．
http://urusulambda.com/2018/04/14/ubuntu%E3%81%A7nvidia-driver%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%81%9F%E3%82%89nouveau%E6%AD%A2%E3%82%81%E3%82%8D%E3%81%A3%E3%81%A6%E8%A8%80%E3%82%8F%E3%82%8C/
https://qiita.com/kkk627/items/9ab959421804341f215e
それから，別のバージョンのドライバを持ってて更新したとかの時に，最後の質問にyesと答えないと自動起動設定が為されなかったりするので注意．

lightdm を disable(自動起動をoff) した場合，is-enabledで見るとstaticとなっていて，もう一度自動起動させようとenableとかreenableとかしても自動起動できなくなる．
ここら辺は依存関係が云々とかの話なんだけど，詳しい話はまた今度調べよう．
結論としては↓のようにすると元に戻る．

::

  $ sudo dpkg-reconfigure lightdm

まあとりあえず，lightdmはこれ自体を起動したりするものじゃなくて依存関係の中でどこかで起動されうるものって感じか．

参考:
https://forum.odroid.com/viewtopic.php?t=34109
https://milestone-of-se.nesuke.com/sv-basic/linux-basic/systemctl/

AppImageとかいうパッケージ?の話
==================================

stationをubuntuにもインストールしようとした時，形式がAppImageとか言うものだったのでそれのメモ．
それ自体が実行ファイルとなってアプリケーションが実行できるもので，割といろんなプラットフォームで動作するんだとか．
あとはAppImageLauncherというものがあるらしい．

https://www.virment.com/how-to-use-appimage-linux/
https://blog.desdelinux.net/ja/appimagelauncher-ejecuta-e-integra-facilmente-aplicaciones-en-appimage/#Eliminar_o_actualizar_la_aplicacion

と言うかstationは配布方法がgoogledriveになっててクソなんじゃ．．．

他のいろんな設定の話
=====================

設定に関していろんなものが詰まったところ

https://sicklylife.jp/ubuntu/2004/settings.html

https://sicklylife.hatenablog.com/entry/2019/01/04/200538




