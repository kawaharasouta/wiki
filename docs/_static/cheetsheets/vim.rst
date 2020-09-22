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

操作系
==========

一応，dotfilesにcheetsheetがおいてあって，<c-h>で見れるようにしてあるけど，ほとんど意味がない．
何かあった時，(しばらくコード書いてなくて慣らしたいとか，キーボード変わってちょめちょめしてるとか)
の時に雑に編集してみたりしてる．
https://github.com/kawaharasouta/dotfiles/blob/master/configs/vim/cheatsheet.md

マジここ見た方がいいんじゃね的参照ページ
https://www.ne.jp/asahi/hishidama/home/tech/unix/vi.html

*以下メモ的な奴ら*

tab空白
--------

tab -> 空白

::

  :set expandtab
  :retab

空白 -> tab

::

  :set noexpndtab
  :retab!

helpの使い方
===============

vimにはめっちゃ充実したオンラインドキュメントがついていて，これを活用しない手はないらしいから使おう．

::

  ### 基本的な使い方
  :h [わかんないこと]

  ### 便利な使い方
  :h [わかんないこと] | only    // ウィンドウを分割しないで開く
  :h                            // ドキュメントのトップページを開く
  :h user-manual                // ユーザマニュアル(リンクドキュメント)
  :h howto                      // How-toリンク(リンクドキュメント)
  :h index                      // 各モードのコマンド一覧らしい


参照
-----------

https://nanasi.jp/articles/howto/help/vim_help.html

========
neovim
========

install
==========

https://github.com/neovim/neovim/wiki/Installing-Neovim

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



==========================
vim pluginの作り方
==========================

※とりあえず細かい知識とか文法とか
====================================

pluginの作り方と言うか基本的にvim scriptに関して．

- そもそもvim scriptはvimのExコマンド(:から始まるやつ)の集まりらしい．ただ，言語と呼ぶに差し支えない機能がしっかり備わってる．
  このファイルの基本的な実行には，:source [file name]をする．

::

  $ vim sample.vim
  + echo "unko"
  :source sample.vim

- 変数にはスコープがあるが，接頭子によって指定する． :h internal-variables

::

  |buffer-variable|    b:	  Local to the current buffer.
  |window-variable|    w:	  Local to the current window.
  |tabpage-variable|   t:	  Local to the current tab page.
  |global-variable|    g:	  Global.
  |local-variable|     l:	  Local to a function.
  |script-variable|    s:	  Local to a |:source|'ed Vim script.
  |function-argument|  a:	  Function argument (only inside a function).
  |vim-variable|       v:	  Global, predefined by Vim.



その他基本的な文法は
https://knowledge.sakura.ad.jp/23436/
ここを見る随時ググれ．


ディレクトリ構成
=================

::

  [plugin]/
  ├── autoload
  │   └── [plugin].vim
  ├── doc
  │   └── [plugin].txt
  └── plugin
       └── [plugin].vim

- pluginディレクトリ
  プラグインが提供するExコマンドやオプションを記述したスクリプトファイルをおく．
  メインの処理はautoloadに記述する．

- autoloadディレクトリ
  メインの処理を記述したスクリプトファイルをおく．
  配下のスクリプトファイルはvim起動時ではなくコマンド実行時に一度だけ読み込まれる．
  plugin配下から呼ぶことができる関数をautoload配下に定義する時、ファイル名#関数名()という命名規則に従う必要があります。これはpluginで定義したコマンドを実行する時にautoload配下のどのファイルのどの関数を呼べば良いのかを知る必要があるからです。そのため、プラグイン名が被るとautoload配下のスクリプトファイル名も被り、最悪違うプラグインの関数で上書きされる可能性があります。これがプラグイン名が被らないようにする必要がある理由です。



- ヘルプファイルをおく．:helpでコマンドのヘルプを引けるようになる．



