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
  $ sudo usermod -aG docker $USER   #sudoなしで現ユーザでdockerkコマンドを実行させるため．このあと再起動必要．

もっとも簡単なdocker公式セットアップ?
https://qiita.com/zembutsu/items/bedb18e1061303e217b8


commands
========

::
  
  $ docker run -it --name [name] ubuntu:18.04 bash        #名前をつける
  $ docker run -p 8080:80 -it ubuntu:18.04 bash           #ホストの8080ポートをコンテナの80ポートにフォアード
  $ docker run --link [container name]:{link name] nginx  #コンテナをリンクさせる例(nginxでリバースプロキシするときにやったので
  $ docker stop $(docker ps -q)                           #起動中のコンテナ全部停止
  $ docker rm $(docker ps -aq)                            #停止中コンテナ全削除
  $ docker rename [old name] [new name]                   #コンテナリネーム

  $ docker inspect [container id]           #コンテナ情報取得
  $ docker build -t khwarizmi/[name] .      #Dockerfileからbuildする(Dockerfileがいるディレクトリに入って)


images
========

# ソースコード眺めるやつのdockerコンテナらしいぞ! hayakawa-sanしゅごい!
https://hub.docker.com/r/yutarohayakawa/elixir/
