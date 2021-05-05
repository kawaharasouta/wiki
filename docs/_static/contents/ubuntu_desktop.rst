=================
ubuntu desktop
=================

そのうちubuntu(じゃなくてもいいけどlinux類にはしたい)にしようと思ってるからちょいちょいメモする．

Ubuntu MATE インストール時にやること
=======================================

caps ctrlの設定
------------------

  /etc/default/keyboardを書き換えるいつもの方法でやったけど正直 Mate Tweak からやった方がいい感じしたよね．．

言語と日本語入力の設定
--------------------------

初手ibusがいないらしいのでinstallする．ちなみにmozcは最初からいる．

::

  $ sudo apt install ibus-mozc

Language Supports から，Reagional Formats で英語表記にしておく．

再起動

IBus Preference を開く
Input Method にjapanese-mozcを追加して，できれば一番上にしたり一つにしたりしておく．
また，mozcの設定でZenkaku/hankakuをctrl spaceに設定し直しておく．
なんかMateは元からctrl spaceが何かに紐づいている気もする．


メモメモメモ
================

普通にubuntu desktopをインストールしたあと，budgie-desktopをインストールしてそっちで入ったらctrlがcapsになってた．
ubuntu desktopで入ったら普通だった．
なんか/etc/default/keyboardみたらなんか書き換わってるんだよね．
設定ファイルとかフレーバーのインストールの時に置き換わってるんかな．
でもだとしたらなんでubuntu-desktopが普通にctrlで動いてるのかわからんけど．
やっぱりフレーバーが混在してるとやっぱりいろんな干渉起こして問題怒るんかね．知らんけど．
と言うわけなので雑にフレーバーをぽこぽこインストールしてみたりするのは止めようと思う．最初は動いててもいつかどこかでガタがきそうな気がしてる．
で，もしどうしても複数のフレーバーを共存させたいんだったらひとまずベースをubuntu-desktopでインストールしておくのが多分いい気がする．

フレーバーについて
======================

フレーバーは基本的にはデスクトップ環境のためのもので，かなり柔軟に自由にインストールやアンインストールをすることができる．
システムのログイン時にフレーバーを選択し切り替えることが可能．
https://www.it-mure.jp.net/ja/software-installation/ubuntu%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97%E3%82%92%E5%88%A5%E3%81%AE%E3%83%95%E3%83%AC%E3%83%BC%E3%83%90%E3%83%BC%EF%BC%88kubuntu%E3%81%AA%E3%81%A9%EF%BC%89%E3%81%AB%E5%A4%89%E6%9B%B4%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%E3%81%8B%EF%BC%9F/961517186/

::

  $ sudo apt install [flavor]

  ### フレーバーの名前は次の通り
  デフォルト:   ubuntu-desktop
  バッジー:     budgie-desktop
  Kubuntu:      kubuntu-desktop
  Kylin:        ubuntukylin-desktop
  Lubuntu:      lubuntu-desktop
  MATE:         mate-desktop
  Xubuntu:      xubuntu-desktop
  Studio:       ubuntustudio-desktop

  ### 消したかったら普通に
  $ sudo apt remove --purge [flavor]        ### 結構でかいし --purge しとくのが無難かも

https://ubuntu.com/download/flavours
ただしこの中でubuntu studioに関しては結構注意した方がいいらしい? よくわからないけど．
クリエイター向けで音楽とか動画とかとかようのソフトウェアをたくさんインストールしちゃうとかそう言う感じではなかろうかとは思ってるけど試してない．

一応↑の通りフレーバーがインストールできるんだけど，なんかフレーバー付きのisoからインストールした時のパッケージ落としてきた時とだとガワが違うんだよなあ．．．

日本語入力やIBusやcapslockの話
================================

capslockをctrlにする
----------------------

xorgの設定ファイルを編集する

::

  $ sudo vim /etc/default/keyboard

  - XKBOPTIONS=""
  + XKBOPTIONS="ctrl:nocaps"

  $ sudo systemctl restart console-setup

console-setupのリスタートで反映されると言う情報もあるんだけど再起動しないとダメだったけど．


capsとctrlのところがイカれて1マシン潰した話
----------------------------------------------

題の通りで，突然イカれてどうしようもなくなった．
フレーザーを追加してGUI環境をいじいじしていたのでその辺がよくなかったのかもしれない．
変更のためにいろいろ試した時のurlを下に並べておく．




日本語入力について
---------------------

mozcがいなかった場合はインストールする(基本いるはず)．

::

  $ sudo apt install ibus-mozc mozc-utils-gui

GUIでmozc settingからmozcの設定をしておく(ctrl+spaceとか)．

GUIでsettingからRegion & Language で Input Sources にmozc を加えておく．できればデフォで入ってるやつよりも上にしておく．

IBusが何とかかんとか
-------------------------

普段デスクトップの右上にキーボードの(IBusの?)インジケータが見えているのにそれが見えなかったり，
日本語入力がおかしくなったり．
そう言うのがいろいろあるらしいけど，
IBusを再起動とか，このあとあげるリンクの対処とかをすると直るとか
僕がインジケータ見えなくなったときは，inputsourceにmozcを入れ直したら直ったりもした．
よくわかんないね．

https://sites.google.com/site/zoom2writej/ubuntu/ibus
https://lists.ubuntu.com/archives/ubuntu-jp/2012-April/004116.html
https://forums.ubuntulinux.jp/viewtopic.php?id=13768
https://pinehead.at.webry.info/201704/article_1.html


ターミナルをどうするか問題
============================

とりあえず今のところmacではiterm2を使っていて，そんなにカスタマイズしてないので，
用件としては
- ホットキーが今iterm2と同じ感じがいい
- ホットキーを押すと今開いてるwindowsに飛んでいってアクティブになる．
- アクティブな状態で押すとウィンドウが消えてくれる．
- なんか広い範囲(他のLinuxでの用途と，freeBSDとか使いたみあるし)で使えるといい
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
んだけどなんか動作怪しいところありそう? 仕様がよくわかってないからかも知らん．
https://github.com/jordansissel/xdotool/issues/220

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
正直，アクティブな時に押したら非表示になるみたいな機能があったら最高だった．

jumpappとxbindkeysの設定とかとか
-------------------------------------

※xbindkeysの使用についてだけど，もしかしたら普通にデスクトップの標準機能のshotcut設定を使った方が良さげな気がしてきた．

::

  $ sudo apt install xbindkeys pandoc
  $ sudo apt install wmctrl                      // mateに入れた時に怒られた
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

stationをubuntuにもインストールしようとした時，形式がAppImageとか言うものだったのでそれのメモ．(biscuitもそうだったわ．GUI割とこの形式多いんかね)
(Neovimもこの形式あってびっくりしたよ．割といろいろこれに対応してきているらしい)
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




