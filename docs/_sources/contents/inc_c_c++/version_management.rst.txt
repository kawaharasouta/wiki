=============================
コンパイラとかのバージョン管理
==============================

update-alternativesによる複数バージョン管理
============================================

登録
-----

最後の数字は優先度

::

  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 20
  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 10
  
  sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 20
  sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 10

切り替え

::

  sudo update-alternatives --config gcc
