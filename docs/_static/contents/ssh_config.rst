===========
ssh_config
===========

ssh_keygen
===========

::

  $ ssh-keygen -t rsa -b 4096 -C "kawahara6514@gmail.com"
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



ssh host key
==============

ホストキーがなくてsshd動かなかったりする時があるんだ．
sudoいるかも．

::

  $ ssh-keygen -A


known hosts duplication
==========================

今までvimで開いて該当行削除してたけど，お便利なコマンド

::

  $ ssh-keygen -R [hostname]



.. _github_keys: https://github.com/settings/keys


ssh-agent とか Forward の設定
===============================

ローカルの設定
----------------

ssh-agent に鍵を設定する

::

  $ ssh-add -K [path to secretkey]
  $ ssh-add -l  // 確認

configを書き換える

::

  $ vim ~/.ssh/config
  (ssh-agentを利用したいホストのところに)
  + ForwardAgent yes




