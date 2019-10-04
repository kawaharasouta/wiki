=========
pthread
=========

最重要メソッド
===============


pthread_create
---------------

スレッドを生成する

宣言
````

::

  int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine) (void *), void *arg);

引数
`````

thread: スレッド識別子(スレッドID) 
attr: 作成するスレッドの属性指定パラメータ. 通常はNULLでいい. 
start_routine: 新しいスレッドで実行される関数 
arg: start_routineの引数になる. 必要ない場合はNULLでいい. 

返り値
``````

成功した場合は 0 
失敗した場合は エラーコード 

pthread_createが完了するとすぐに帰ってくる. 
また, スレッドの実行順序などについてはOSのみが知る.

pthread_exit
-------------

スレッドを終了する

宣言
````

::

  void pthread_exit(void *retval);

引数
`````

retval: これがスレッドの戻り値となる

pthread_join
--------------

スレッド終了待ち(消去)

宣言
`````

::

  int pthread_join(pthread_t thread, void **retval);

引数
`````

thread: 待つスレッドのスレッドID. 
retval: 対象スレッドの戻り値が入る. 使わない場合はNULLでいい. 

返り値
```````

*

注意
`````

一度pthread_joinを使って消去したスレッドに対して再度pthread_joinすることは
非常に危険なので絶対に行わない. 
これを実行した後には,

::

  thread = NULL

としておくと良い

pthread_self
-------------

自分のスレッドIDを取得する

宣言
````

::

  pthread_t pthread_self(void);

返り値
``````

自分のスレッドID

pthread_mutex_trylock
----------------------

ミューテックスがOFFの時はONにして0を返す. ONの時は0以外を返す. 
これはあまり使われない(後述)

宣言
`````

::

  int pthread_mutex_trylock(pthread_mutex_t *mutex);

pthread_mutex_lock
-------------------

ミューテックスがOFFの時にはONにして0を返す. ONの時はOFFになるまで待つ. 
trylock よりもこちらの方がよく使われる.

宣言
`````

::

  int pthread_mutex_lock(pthread_mutex_t *mutex);

引数

attr: スレッドの属性. 普通に使う時はNULLでいい.

pthread_mutex_destroy
----------------------

ミューテックスの破棄

宣言
``````

::

  int pthread_mutex_destroy(pthread_mutex *mutex);

pthread_mutex_unlock
----------------------

ミューテックスをOFFにする

宣言
``````

::

  int pthread_mutex_unlock(pthread_mutex_t *mutex);
  

スレッド変数について
======================

スレッドプログラミングで注意するべき点の一つに, 変数の扱いがある 
スレッドではメモリが共有されるため, 変数の扱いに気をつけなければならないが, 
スレッド変数を使うとうまくプログラミングすることができる時がある. 
ただし, これを用いるとコードが汚くなる傾向があるため, あまり用いられない. 
構造体を用いて綺麗にコーディングする方が良いと言われる.


pthread_key_create
pthread_key_delete
pthread_setspecific
pthread_getspecific
