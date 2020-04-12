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

vimrcの書き方
===============

参考
https://thinca.hatenablog.com/entry/20100205/1265307642

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

  $ sudo apt install software-properties-common
  #######################    $ sudo add-apt-repository ppa:neovim-ppa/unstable
  $ sudo add-apt-repository ppa:neovim-ppa/stable
  $ sudo apt update
  $ sudo apt install neovim
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

  $ vim ~/.bashrc
  + export XDG_CONFIG_HOME=$HOME/.config
  + export XDG_CACHE_HOME=$HOME/.cache

  $ source ~/.bashrc
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

hookの使い方とか
-----------------

.. csv-table:: hookの種類
  :header: "名前", "実行のタイミング", "lazy OFF", "lazy ON"
  :widths: 5, 5, 5, 5

  "hook_add",           "プラグインが追加されたとき",         "OK", "OK"
  "hook_source",        "プラグインが読み込まれる直前",       "NG", "OK" 
  "hook_post_source",   "プラグインが読み込まれた直後",       "NG", "OK" 
  "hook_post_update",   "プラグインが更新された直後",         "OK", "OK" 
  "hook_done_update",   "プラグイン全ての更新が終わった直後", "OK", "OK" 


参考
https://qiita.com/delphinus/items/cd221a450fd23506e81a

プラグイン導入例
-----------------

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

プラグインアンインストール
--------------------------

tomlファイルから該当行を消したあと，

::

  :call map(dein#check_clean(), "delete(v:val, 'rf')")
  :call dein#recache_runtimepath()



設定????
-------------

これ init.vim に入れないとコマンドが正しく動かなかった

::

  " Define mappings
  	autocmd FileType denite call s:denite_my_settings()
  	function! s:denite_my_settings() abort
  	  nnoremap <silent><buffer><expr> <CR>
  	  \ denite#do_map('do_action')
  	  nnoremap <silent><buffer><expr> d
  	  \ denite#do_map('do_action', 'delete')
  	  nnoremap <silent><buffer><expr> p
  	  \ denite#do_map('do_action', 'preview')
  	  nnoremap <silent><buffer><expr> q
  	  \ denite#do_map('quit')
  	  nnoremap <silent><buffer><expr> i
  	  \ denite#do_map('open_filter_buffer')
  	  nnoremap <silent><buffer><expr> <Space>
  	  \ denite#do_map('toggle_select').'j'
  	endfunction

他にも公式の資料に設定の例とか書いてあるんだけどマジよくわからんからわからない．

denite.txt
https://github.com/Shougo/denite.nvim/blob/master/doc/denite.txt#L127

参考
https://github.com/Shougo/denite.nvim/issues/640
