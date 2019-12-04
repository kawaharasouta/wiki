=======
Docker
=======


install (ubuntu)
===================

::

  $ sudo apt update && sudo apt install -y \
    apt-transport-https ca-certificates curl software-properties-common
  $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  $ sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable"
  $ sudo apt update && sudo apt install -y docker-ce
  $ sudo usermod -aG docker $USER   #sudoなしで現ユーザでdockerkコマンドを実行させるため．このあとデーモンの再起動とリログ必要かも?

※tmuxのセッションからだとsudoなしがうまく行かなくなる．


commands
========

::
  
  $ docker run -it --name "name" ubuntu:18.04 bash    #名前をつける
  $ docker run -p 8080:80 -it ubuntu:18.04 bash       #ホストの8080ポートをコンテナの80ポートにフォアード
  $ docker stop $(docker ps -q)                       #起動中のコンテナ全部停止
  $ docker rm $(docker ps -aq)                        #停止中コンテナ全削除

  #コンテナ情報取得
  $ docker inspect [container id]



images
========

# ソースコード眺めるやつのdockerコンテナらしいぞ! hayakawa-sanしゅごい!
https://hub.docker.com/r/yutarohayakawa/elixir/
