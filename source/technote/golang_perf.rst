========================================================
golangでちょっと文字列関連性能計測した時のいろんなメモ
========================================================

この調査に至った動機
======================

libvirt-go を使ってちょっとしたプログラムを書いていて，
各ドメインから情報をゲットして雑に文字列をいじらなきゃいけないなーと思っていたんだが，
stringや[]byteでの文字列操作に関するパフォーマンスについて触れた記事がいくつかあって，少しいじいじした．

文字列の結合とかそこら辺の話
===============================

文字列の操作に関して，↑に書いたようにstringと[]byteで文字列の操作をできるんだけど，
結合に関してもそのどちらを使うかとかメソッドをどうするかで当然パフォーマンスは変わる．
ところで，stringはgolangではどうもimmutable(不変)なため，
文字列に追加したいときはallocateが必要でそれがめっちゃ遅いみたいな話があって，
[]byteでappendした方がいいとか，
いやいやなんかstrings.Join(というかstrings.Builder)が意外と速いんですよみたいな話とかがあったりする．
それについてはリンクを貼っておくのでそこをみて確認するようにしよう．

- https://qiita.com/ono_matope/items/d5e70d8a9ff2b54d5c37
- https://qiita.com/ruiu/items/2bb83b29baeae2433a79
- https://qiita.com/spiegel-im-spiegel/items/16ab7dabbd0749281227
- https://text.baldanders.info/golang/join-strings-2/     ☆

僕の状況と↑の話
========================

↑の話なんですが，[]stringが与えられて，それを結合する話でした．
strings.Joinは第一引数が[]stringだしね．
ところで今の僕の状況は，
各ドメインから情報をとってきてその情報がstringで帰ってきていて，
それはループで回しながら取る感じだったわけだが，
ここで思うのが，
この状況でstrings.Joinを使いたかったらstringsを[]stringsにするためにappennd祭りを開催する必要があるなと思うわけである．
appendが結構重いみたいな話も聞くから，これだったら実は+してった方が速い可能性あるかもとか，
[]byteで処理させる方法と無視できないくらいの性能差が出てくるんじゃないか(↑の結合の話では差はほとんどないよねくらいの話で終わっている)
みたいなことも思ったりするわけである．
あと，stringと[]byte変換でうんぬんみたいな記事もあったりしてその辺りもどんなもんかと気になった．
https://qiita.com/ikawaha/items/3c3994559dfeffb9f8c9
https://medium.com/a-journey-with-go/go-string-conversion-optimization-767b019b75ef

と言うわけで実験

::

  package main

  import (
    // "fmt"
    // "log"
    "testing"
    "strings"
    // "os"

    // libvirt "libvirt.org/libvirt-go"
  )

  var nn int = 500

  func ret_string() string {
    return "this is test strings"
  }

  func Benchmark_Join(b *testing.B) {
    var names []string
    // conn, _ := libvirt.NewConnect("qemu:///system")
    // doms, _ := conn.ListAllDomains(libvirt.CONNECT_LIST_DOMAINS_ACTIVE)
    for range (make([]int, nn)) {
      // name, _ := dom.GetName()
      names = append(names, ret_string())
      _ = strings.Join(names, "\n")
      // dom.Free()
    }
  }

  func Benchmark_Plus(b *testing.B) {
    var names string
    // conn, _ := libvirt.NewConnect("qemu:///system")
    // doms, _ := conn.ListAllDomains(libvirt.CONNECT_LIST_DOMAINS_ACTIVE)
    for range (make([]int, nn)) {
      // name, _ := dom.GetName()
      // names = names + ret_string()
      names = names + ret_string() + "\n"
      // dom.Free()
    }
  }

  func Benchmark_Byte(b *testing.B) {
    byt := []byte{}
    for range (make([]int, nn)) {
      byt = append(byt, ret_string()...)
      byt = append(byt, "\n"...)
      // byt = append(byt, []byte(ret_string()))
      // byt = append(byt, []byte("\n"))
    }
  }


結果

::

  ### nn = 500
  $ go test -bench . -benchmem
  goos: linux
  goarch: amd64
  pkg: dev/string
  Benchmark_Join-20       1000000000               0.00334 ns/op         0 B/op          0 allocs/op
  Benchmark_Plus-20       1000000000               0.00113 ns/op         0 B/op          0 allocs/op
  Benchmark_Byte-20       1000000000               0.000085 ns/op        0 B/op          0 allocs/op
  PASS
  ok      dev/string      0.061s

  ### nn = 1000
  $ go test -bench . -benchmem
  goos: linux
  goarch: amd64
  pkg: dev/string
  Benchmark_Join-20       1000000000               0.0173 ns/op          0 B/op          0 allocs/op
  Benchmark_Plus-20       1000000000               0.00557 ns/op         0 B/op          0 allocs/op
  Benchmark_Byte-20       1000000000               0.000136 ns/op        0 B/op          0 allocs/op
  PASS
  ok      dev/string      0.198s

  ### nn = 5000
  $ go test -bench . -benchmem
  goos: linux
  goarch: amd64
  pkg: dev/string
  Benchmark_Join-20       1000000000               0.483 ns/op           0 B/op          0 allocs/op
  Benchmark_Plus-20       1000000000               0.108 ns/op           0 B/op          0 allocs/op
  Benchmark_Byte-20       1000000000               0.000263 ns/op        0 B/op          0 allocs/op
  PASS
  ok      dev/string      13.154s

  ### nn = 10000
  $ go test -bench . -benchmem
  goos: linux
  goarch: amd64
  pkg: dev/string
  Benchmark_Join-20              1        1918141134 ns/op        1087301816 B/op    10056 allocs/op
  Benchmark_Plus-20       1000000000               0.408 ns/op           1 B/op          0 allocs/op
  Benchmark_Byte-20       1000000000               0.000467 ns/op        0 B/op          0 allocs/op
  PASS
  ok      dev/string      9.631s

予想以上に[]stringのappendが遅いようだった．
ここの考察部分あとでかこ〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜〜

