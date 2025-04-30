====================
Linuxの認証周りの話
====================

PAM
=====

Linuxには認証機能を使うソフトウェアがたくさんあるけど，それぞれのソフトウェアで独自に認証機能を実装してるのはよくないのでモジュールにしたものがある．
それが PAMとかPAM認証 とかってやつ．

/etc/pam.d を見ると，なんかよく見るデーモンの名前のファイルとかがあって，認証にはこいつらを使ってるぽいらしいくさい．
これ以上はよくわからなくなりそうだから触れない．こういうのがあったよっていうメモ．



参照: https://ozuma.hatenablog.jp/entry/20131005/1380942386

passwd変更
-----------

it is based on a dictionary word とかって怒られる時の対処
なんか↓のようにしたら動いた．

::

  $ sudo vim /etc/pam.d/passwd

  + password   sufficient   pam_unix.so nullok md5 shadow
  + password   required     pam_deny.so

参照: https://volvox.hateblo.jp/entry/20130813/1376399307


PAMの基本文法
---------------------

::

  type control module-path module-arguments

1. type（タイプ）
   PAMの4つの管理タイプを指定します：

auth: 認証プロセス（ユーザー確認）
account: アカウント管理（アカウント有効性確認）
password: パスワード変更メカニズム
session: セッション管理（ログイン前後の処理）

2. control（制御フラグ）
   モジュールの失敗時の動作を指定します：
2.1 単純な制御フラグ

required: 失敗するとスタック全体が失敗するが、処理は続行
requisite: 失敗するとすぐにスタック全体が失敗し、処理を中止
sufficient: 成功すれば、それまでのrequiredモジュールも成功していれば、処理成功として終了
optional: 成功/失敗が全体の結果に影響しない（他にモジュールがない場合は影響する）
include: 別のPAMサービス設定を現在の位置に含める
substack: includeと似ているが、サブスタック内のsufficientの効果がサブスタック内に限定される

2.2 詳細な制御構文
複雑な条件分岐が必要な場合、以下のような詳細な制御構文も使用できます：
[value1=action1 value2=action2 ...]
例：[success=1 default=ignore]
使用可能なアクションには以下があります：

ignore: 結果を無視
ok: モジュールの成功として扱う
done: スタック全体を成功として終了
die: スタック全体を失敗として終了
reset: スタックをリセット
N（数字）: N個のモジュールをスキップ

3. module-path（モジュールパス）
   モジュールファイルへのパスを指定します。通常は相対パスで記述され、/lib/security/または/lib64/security/を基準としています。
   例：pam_unix.so

4. module-arguments（モジュール引数）
   モジュールに渡す引数をスペース区切りで指定します。引数はモジュールによって異なります


特殊な構文要素

コメント: #で始まる行はコメントとして扱われます
インクルード: @include service-nameで他のサービス設定を含めることができます
モジュール省略: モジュール名の前に-をつけると、そのモジュールの失敗が無視されます
デフォルト設定: #%PAM-1.0のような行はバージョン情報を示します


LDAP認証したときのpam+authselectまわりの設定に関する考察
----------------------------------------------------------

やったことの概要
^^^^^^^^^^^^^^^^^^^^^

まず，Linuxのログイン(その他)の際の認証をLDAPを使うように設定変更
その後，sudo時の認証でLDAPパスワードを入力するのが許容できなかったので，sshキーペアを使うように設定変更．
なおAlmaLinux9


pamとそのまわりのソフトウェアの認証ステップの考察
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*sudoの場合*

1. sudoコマンドが実行されると，sudoは認証処理をPAMに移譲する．
2. sudoは`sudo`という名前のPAMサービスを呼び出す
3. PAMはその設定ファイルである/etc/pam.d/sudoファイルを読み込み，そこに定義された認証モジュールの順序にしたがって処理を行う．
4. その結果の認証の成功/失敗結果を返す

*sshdの場合(設定にもよるが一例)*

1. sshコマンドが実行され，接続先のsshdで認証が走る．
2. sshdは公開鍵が渡されているかを確認し，公開鍵認証が行えるようであれば認証を行う．
3. 2で公開鍵認証ができなかった場合(失敗した場合もここに流れる?)，PAMに認証を移譲する．
4. sshdは`sshd`という名前のPAMサービスを呼び出す
5. PAMはその設定ファイルである/etc/pam.d/sshdファイルを読み込み，そこに定義された認証モジュールの順序にしたがって処理を行う．
6. その結果の認証の成功/失敗結果を返す

ソフトウェアがPAMに認証処理を移譲してPAMにて認証を行っている．
当然だが，ソフトウェア内に認証処理が実装されていることもあり，PAMを通らないこともある．(sshdの例)
その点はソフトウェアの作りや設定に依存する．
設定によってはPAM以外の認証モジュールを使うこともできるようだが，詳細は不明．

authselectの役割
^^^^^^^^^^^^^^^^^^

※ authselectは結構RHEL系特有の可能性があるので気をつける．
  ubuntu2004とかのころはなかったかも? 今はありそうだけど．
  またarchlinuxにはなさそう．

authselectは，PAMの設定を管理するためのツール．
NSS(Name Service Switch) + その他?認証系? の設定も同時に管理されるっぽい?

authselectはプロファイルを持つ．
プロファイルを切り替えることで，PAMの設定ファイルを特定の用途向けにまとめて変更することができる．
イメージ的には例えばgccとかpythonとかのバージョンをシンボリックリンクで切り替えるupdate-alternativesとかのイメージ．
しかしauthselectの場合にはシンボリックリンク差し替えではなくて実際のファイルが切り替わることには注意．

後述する(と思う)が，実際にauthselectでプロファイルを切り替えるときの話
設定済みのプロファイルのファイル内容から変更がある(手動で変更している)ときにはコマンドは失敗する．
--forceオプションで強制上書きができる．
がそもそも思想として，PAMの設定ファイルを書き換えたい場合にはカスタムプロファイルを定義してauthselectからそのプロファイルに切り替えるのが正攻法なんだと思う．(ただの感想)

LDAPを使うように設定変更
^^^^^^^^^^^^^^^^^^^^^^^^^^^

LDAPサーバがある前提でクライアント側の設定のみを書く．
8系以前ではnss-pam-ldapdパッケージおよびnslcdが使われていたようなのだが，9系では削除されたとのこと．
代わりにsssdを用いる

sssdでLDAPサーバと通信するように設定をし，authselectはsssd向けのプロファイルに切り替える．
これによりPAMがsssd向けの設定に切り替わり，LDAPで認証してくれるようになる．

::

  ### 必要なパッケージインストール
  $ sudo dnf install sssd sssd-ldap sssd-tools openldap-clients

  ### sssd設定ディレクトリ
  $ sudo mkdir /etc/sssd

  ### sssd設定ファイル (設定は一例)
  $ sudo vi /etc/sssd/sssd.conf
    [sssd]
    domains = example.com
    config_file_version = 2
    services = nss, pam
    [domain/example.com]
    id_provider = ldap
    auth_provider = ldap
    ldap_uri = ldap://ldap1.example.com,ldap://ldap2.example.com
    ldap_search_base = dc=example,dc=com
    ldap_id_use_start_tls = false
    ldap_auth_disable_tls_never_use_in_production = true
    cache_credentials = true
    ldap_tls_reqcert = never

  ### authselectプロファイル切り替え
  $ sudo authselect select sssd --force

  ### sssd再起動
  $ sudo systemctl restart sssd

sudo時の認証をssh鍵認証のみでも通るようにする
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ここまででLDAP認証できるようになっているが，設定を追加して，sudoの認証時はssh鍵認証だけでも通るようにする．

::

  $ sudo dnf install pam_ssh_agent_auth

  $ sudo vi /etc/pam.d/sudo
  /////!!!!!!!! sufficientで，この認証のみで通過できるようにしたいので，コメント除いて一番上に書くようにする．
  + auth       sufficient   pam_ssh_agent_auth.so file=/etc/authorized_keys.d/%u'

  $ sudo vi /etc/sudoers
  //! sudo したときに， "SSH_AUTH_SOCK" 環境変数は維持するようにする．
  //! visudoの方がいいか?
  + Defaults env_keep += "SSH_AUTH_SOCK"

これでOK



