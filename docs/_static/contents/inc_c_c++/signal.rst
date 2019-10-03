==========
signal
==========



header
=======

::

  #include<signal.h>


method
======

::

	int sigaction(int sig, const struct sigaction *act, struct sigaction *oldact);
	
	struct sigaction {
	  /* sa_handler. sa_sigactionは片方のみ使う */
	  void (*sa_handler)(int);
	  void (*sa_sigaction)(int , siginfo_t*, void*);
	  sigset_t sa_mask;
	  int sa_flags;
	};


point
======

ハンドラの再設定
-----------------

sgiaction()は、OSにかかわらず
シグナルハンドラの設定を保持し続けることが保証されています。

システムコールの再起動
-----------------------

sigaction()は、デフォルトではシステムコールを再起動しません。
sa_flagsメンバにSA_RESTARTを追加すると再起動する設定になります。
一般的には再起動される方が便利なので、SA_RESTARTは常に追加しておくのが無難です。

シグナルのブロック
-------------------

struct sigactoinのメンバsa_maskで、ブロックするシグナルを指定できます。
さらに、シグナルハンドラの起動中は処理中のシグナルを自動的にブロックしてくれるので、
ほとんどの場合はsa_maskは空にしておけば十分です。
sa_maskを空にするには、sigemptyset()を使います。


例: `example <https://github.com/kawaharasouta/mysignal_samp>`_


signalで簡単にやる方法
======================

任意のSGINALを任意のfuncでトラップする.

::

  signal (SIGNAL, func)


.. csv-table::
  :header: シグナル, 概要
  :widths: 5, 5

  SIGINT, キーボードからの割り込み Ctrl + C 
  SIGQUIT, キーボードに夜中止 Ctrl + \ または Ctrl + 4
  SIGTSTP, 端末(tty)から入力された一旦停止 Ctrl + Z
  SIGTERM, 終了 (コマンド)kill pid
  SIGSTOP, 一時停止 (コマンド) Kill -s SIGSTOP pid
