========================================
virshのソースコードを読んだ時のメモ
========================================


virshはlihbvirt内の https://github.com/libvirt/libvirt/tree/c6c23415706ee303a9fbeee5326a4e504645fe3e/tools にあるのでそこをみていく．

とりあえずvirsh.cの一番下を見ると，mainがあるので動作の発端が見える．
初期化周りが見えるが，consoleのescapekeyがハードコードしてあったりして笑う．
l. 489

::

  virshCtl.escapeChar = "^]";     /* Same default as telnet */

こんな大きなコードでも愚直にprognameを出してるもんなんだなあと思う．
l.852

::

  if (!(progname = strrchr(argv[0], '/')))
    progname = argv[0];
  else
    progname++;
  ctl->progname = progname;

コマンド実行させてそうな関数呼び出しvshCommandRunが見つかる．
ついでにinteractive modeとの場合分け部分も見つかる．
コマンドを読み解くにはctl(vshControlなる構造体)が重要そう．
ちょっと上にあるvirshParseArgvで引数を解釈して構造体を作り上げてよしなにしている感じがある．
l.885

::

  if (!virshParseArgv(ctl, argc, argv) ||
    !virshInit(ctl)) {
    virshDeinit(ctl);
    exit(EXIT_FAILURE);
  }

  if (!ctl->connname)
    ctl->connname = g_strdup(getenv("VIRSH_DEFAULT_CONNECT_URI"));

  if (!ctl->imode) {
    ret = vshCommandRun(ctl, ctl->cmd);
  } else {
    /* interactive mode */ 


vshCommandRunもしくはvirshParseArgvから続き書く．
