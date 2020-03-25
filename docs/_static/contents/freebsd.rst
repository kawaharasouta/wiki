==========================
freebsd関連のメモする場所
==========================

整理されたら消しそう．

sshdが動いてない話
====================

install直後にやらないとsshできなくなって終わる(時がある)から気を付けろ．

::

  # ssh-keygen -A     # ホストキーを作る
  # /etc/rc.d/sshd start

sudo入れる
===========

https://hacolab.hatenablog.com/entry/2019/01/15/235905
ユーザをwhellに追加するのはインストールの時にやっとくのがいい．






vim
vimrcはそのまま行けた．プラグインのインストールもbundleちゃんと入れれば大丈夫だった．
viがまともにviだからvimにシンボリックリンク貼った方がいいかも．

::

  $ sudo pkg install vim 


bashにする
bashrc使えたけど，bash_profileが必要だった．

::

  $ sudo pkg install bash 
  $ chsh -s bash khwarizmi

git 

::

  $ sudo pkg install git 

tmux 
これも普通に大丈夫

::

  $ sudo pkg install tmux
