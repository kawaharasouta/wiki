# wiki

setup env on ubuntu
```
sudo pip3 install sphinx sphinx_rtd_theme sphinx-ustack-theme
sudo apt install -y python3-sphinx
```

make page
```
git clone <this-repo> && cd $_
make docs
```

# ポリシー

## 章題構成

CONTENTS: 技術的に重要な対象に対する使い方等を示すもの．
TECHNOTE: 調査内容等をまとめるもの．
CHEETSHEET: コマンドリファレンスに近いようなもの．
SYSTEM TRACING: トレースツールに関するもの．(CONTENTSのサブセットにすべきと思われる)
DOCUMENT: ドキュメント生成に関するもの．(CONTENTSまたはCHEETSHEETに写すべきであるし，そもそもいらない説もある．)
TEST: test用．

## ディレクトリ階層

- source: ソースファイルの配置場所．
	- index.rst: indexだ．[topics].rstを全てtoctreeで読み込む．
	- conf.rst: configだ．
	- [sections]: 上で述べたセクションに該当するディレクトリ．
		- [topics].rst: セクションに該当するトピックに関するrstファイル．トピックがさらに小さなサブセットを持つ場合はそれのindexにもなりうる．
		- inc_[topics]: トピックのサブセットはこのディレクトリに入れられる．
			- [sub topics].rst: サブトピックのrst．
- docs: HTMLファイルの置き場でかつビルドの際の出力先．何も触るな．
