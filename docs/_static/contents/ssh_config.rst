===========
ssh_config
===========

configの書き方のドキュメント:
https://www.ssh.com/ssh/config/

ssh_keygen
===========

::

  $ ssh-keygen -t rsa -b 4096 -C "kawahara6514@gmail.com"     // -Cオプションの引数が鍵の識別子になるからわかるようにする．
  Enter file in which to save the key (/Users/khwarizmi/.ssh/id_rsa): <path to key>
  Enter passphrase (empty for no passphrase): <passphrase> ※ i recommend no passphrase.


gihub setting 
===============

accsess github_keys_

copy public key
-----------------

::

  $ cat <path to public key> | pbcopy 

config for git 
-----------------

::

  Host github
    HostName github.com
    User git

ssh-agent とか Forward の設定
===============================

サーバ設定
----------------

::

  $ vim /etc/ssh/sshd_config


ローカル設定
----------------

※ config で ForwardAgent を有効化するとき

::

  $ vim ~/.ssh/config
  (ssh-agentを利用したいホストのところに)
  + ForwardAgent yes

ssh-agent の起動と鍵登録
※ 端末開くごとにこれらやらなきゃいけない(ssh-agent が同じ数いる)んだけど，その辺どういう仕組みというかつながりになっているんだろう．
  ログインセッションのスライスごとに制御しているとか?

::

  $ eval `ssh-agent` 
    → なんかこれ，exec ssh-agent bash とかのほうがいいかも? こっちだと端末殺したら一緒に ssh-agent も死んでくれそう．
      ただコマンド試してないから微妙に動かんかも．調整はそのうちする．
  $ ssh-add -K [path to secretkey]
  $ ssh-add -l  // 確認

ssh 先で鍵が forward されているか確認  
参考: https://docs.github.com/ja/developers/overview/using-ssh-agent-forwarding#testing-ssh-agent-forwarding

::

  $ echo "$SSH_AUTH_SOCK"
  > /tmp/ssh-4hNGMk8AZX/agent.79453


踏み台設定
============

::

  $ vim ~/.ssh/config
  (踏み台を経由してsshしたいホストのところに追加する)
  + ProxyCommand ssh [踏み台にしたいホスト] -W %h:%p

ssh host key
==============

ホストキーがなくてsshd動かなかったりする時があるんだ．
sudoいるかも．

::

  $ ssh-keygen -A


known hosts duplication
==========================

known hostsに重複が出ちゃった時のやつ．
今までvimで開いて該当行削除してたけど，お便利なコマンド

::

  $ ssh-keygen -R [hostname]

.. _github_keys: https://github.com/settings/keys





