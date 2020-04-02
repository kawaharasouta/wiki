====
vim 
====

cheetsheetじゃなくてcontentsの方がいい気がしてきた．

vim日本語ドキュメント:
https://vim-jp.org/vimdoc-ja/usr_90.html
vim-jp:
https://vim-jp.org/docs/build_linux.html

ビルド
=======

インストール

::

  $ git clone https://github.com/vim/vim.git -b v8.2.0000
  $ cd vim
  $ ./configure --with-features=huge --enable-fail-if-missing
  $ make && sudo make install

アンインストール

::

  make uninstall

プラグイン(vundle)導入
========================

::

  $ git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim
  $ vim ~/.vimrc    # head
    + set nocompatible
    + filetype off
    + set rtp+=~/.vim/bundle/Vundle.vim
    + call vundle#begin()
    + 
    + Plugin 'VundleVim/Vundle.vim'
    + ......
    +
    + call vundle#end()
    + filetype plugin indent on
  $ vim +PluginInstall +qall

コマンド
==========

.. csv-table::
  :header: コマンド名, 機能
  :widths: 3, 3

  d, 削除
  c, 変更
  y, コピー

.. csv-table::
  :header: モーション, 機能
  :widths: 3, 3

  w, カーソル位置から空白を含む単語の末尾
  e, カーソル位置から空白を含まない単語の末尾
  $, カーソル位置から行末

tab空白
===========

tab -> 空白

::

  :set expandtab
  :retab

空白 -> tab

::

  :set noexpndtab
  :retab!

========
neovim
========

install
==========

::

  $ sudo apt-get install software-properties-common
  #######################    $ sudo add-apt-repository ppa:neovim-ppa/unstable
  $ sudo add-apt-repository ppa:neovim-ppa/stable
  $ sudo apt-get update
  $ sudo apt-get install neovim
  $ sudo apt install python3-dev python3-pip
  $ pip3 install -U pip3        # いらんかも
  $ pip3 install neovim

  $ sudo apt install xclip xsel
   
nvim開いて

::

  :echo has('python3')
  1

なるの確認しといた方が良さげ．

dein.vim
============

※なんかこれやったら/etc/alternatives/vimがnvimみるようになってビビったんだけど．

XDG系?の変数の定義
---------------------

これに関してはneovimのインストール時にやった方が良さげな気はしてる．

::

  $ vim 
  + set -x XDG_CONFIG_HOME $HOME/.config
  + set -x XDG_CACHE_HOME $HOME/.cache

  $ source ~/.config/fish/config.fish
  適当にechoして確認しとけ


init.vimの作成
---------------

::

  $ mkdir $XDG_CONFIG_HOME/nvim
  $ vim $XDG_CONFIG_HOME/nvim/init.vim
  + " dein.vim {{{
  + "  directory configuration
  + let s:config_home = empty($XDG_CONFIG_HOME) ? expand('~/.config') : $XDG_CONFIG_HOME
  + let s:dein_config_dir = s:config_home . '/nvim/dein'
  + let s:toml_file = s:dein_config_dir . '/toml/dein.toml'
  + let s:cache_home = empty($XDG_CACHE_HOME) ? expand('~/.cache') : $XDG_CACHE_HOME
  + let s:dein_dir = s:cache_home . '/dein'
  + let s:dein_repo_dir = s:dein_dir . '/repos/github.com/Shougo/dein.vim'
  + "  dein installation
  + if !isdirectory(s:dein_repo_dir)
  +   call system('git clone https://github.com/Shougo/dein.vim ' . shellescape(s:dein_repo_dir))
  + endif
  + "  path
  + let &runtimepath = s:dein_repo_dir . "," . &runtimepath
  + if dein#load_state(s:dein_dir)
  +   call dein#begin(s:dein_dir)
  +   call dein#load_toml(s:toml_file, {'lazy': 0})
  +   call dein#end()
  +   call dein#save_state()
  + endif
  + "  install new plugins
  + if has('vim_starting') && dein#check_install()
  +   call dein#install()
  + endif
  + " dein.vim }}}

Neovimを再起動したらdeinが取得される．
dein.vimのヘルプが↓のように見れたらOK．

::

  :helptags ~/.cache/dein/repos/github.com/Shougo/dein.vim/doc
  :h dein

プラグイン導入例
===================

::

  $ vim ~/.config/nvim/dein/toml/dein.toml
  + [[plugins]]
  + repo = 'itchyny/lightline.vim'

起動したら導入されるが，一部のプラグインで

::

  :UpdateRemotePlugins

して再起動しないといけないものもあるみたい．

参照
https://qiita.com/giwagiwa/items/128aec59af622efc7a97

