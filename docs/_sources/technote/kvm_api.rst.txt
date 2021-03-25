kvm api でいろいろするやつ
==============================

参考:

公式のAPIに関してのドキュメント: 
https://github.com/torvalds/linux/blob/2861952/Documentation/virtual/kvm/api.txt

kvmを使ってみるやつ: 
http://yuma.ohgami.jp/Identeki-MBR/01_hello.html

初歩的な機能を出力だけのROMを用意してやってみる
------------------------------------------------


::

  ### とりあえず/dev/kvmをopenする． 当然kvm的な操作はここにioctlすることになる．
  int kvmfd = open("/dev/kvm", O_RDWR);

  ### VMを作成する．(VMのメモリのやつとかそこらへんができるんだと思う．←←←調べ直して書き直す)
  int vmfd = ioctl(kvmfd, KVM_CREATE_VM, 0);

  ### ROMを登録する．要はここにBIOSとかぶっ込んで(これハードディスクはどうすればいいのかわからんけど．別で同じように登録して良いんか)
  ### 起動すればいいという話
  ### とりあえずテスト用に雑なバイナリをくっつけておく．
  ### ROM_SIZE: romのサイズ
  ### ここmmapでいいのかallocate系にすべきなのかとかちょっとよくわかってない．
  // 領域を確保して
  uint8_t *mem = mmap(NULL, ROM_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS|MAP_NORESERVE, -1, 0);
  // romを確保したところにコピー
  memcpy(mem, rom_bin, sizeof(rom_bin));
  // このromの情報の構造体をioctlでVMに設定する．
  struct kvm_userspace_memory_region region = {
        .guest_phys_addr = 0,
        .memory_size = ROM_SIZE,
        .userspace_addr = (uin64_t)mem
  };
  ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region);

  ### VCPUを作成する
  ### ioctlのあとkvm側で作成されるkvm_runを利用する必要があるのでアクセスできるようにしておく．
  // 第3引数は作成するvcpu_id
  int vcpufd = ioctl(vmfd, KVM_CREATE_VCPU, 0);
  size_t mmap_size = ioctl(kvmfd, KVM_GET_VCPU_MMAP_SIZE, NULL);
  struct kvm_run *run = mmap(NULL, mmap_size, PROT_READ|PROT_WRITE, MAP_SHARED, vcpufd, 0);

  ### VCPUのレジスタの初期設定 ☆☆☆よくわかってないからあとで調べ直す．
  ### SREGSとREGSの二つあるらしく，それぞれ別のioctlで設定や取得をする．
  // SREGについて ※セグメントレジスタ
  struct kvm_sregs sregs;
  ioctl(vcpufd, KVM_GET_SREGS, &sregs);
  sregs.cs.base = 0;
  sregs.cs.selector = 0;
  ioctl(vcpufd, KVM_SET_SREGS, &sregs);
  ここで、この項のVMは「起動されると0x00000000の命令から実行を始める」こととします。そのための「セグメンテーション」と呼ばれるx86 CPUの機能の設定を行っているのがリスト1.8です。セグメンテーションとはアドレス空間を「セグメント」と呼ぶ領域に分けてアクセスする方式です。セグメントには用途が決まっているものもあり、リスト1.8では「コードセグメント(CS)」という「CPUが実行する命令が配置されているセグメント」の設定を行っています。やっていることは単にCSがアドレス0x00000000から始まる事を設定しているだけです。
  // REGSについて ※ステータスレジスタ
  struct kvm_regs regs = {
          .rip = 0x0,
          .rflags = 0x02, /* RFLAGS初期状態 */
  };
  ioctl(vcpufd, KVM_SET_REGS, &regs);
  レジスタripはCSの先頭からのオフセットです。KVM_SET_SREGSでCSは0x00000000から始まるように設定したので、ripも0を設定しておくことで、VCPUはVM起動後、0x00000000の命令から実行を始めるようになります。レジスタrflagsはCPUの状態を示すフラグです。予約ビットで1を書くことが決められているビットを除き、すべてのビットを0で初期化します。

  ### 実行する
  ### 特権命令やIO処理があったら動作が戻ってくるので，そこらへんのデバイスエミュレーションとかが本来はある．
  uint8_t is_running = 1;
  while (is_running) {
    ioctl(vcpufd, KVM_RUN, NULL);
    switch (run->exit_reason) {  /* exit_reasonで分岐 エミュレーションとかする */
    case KVM_EXIT_HLT:      /* HLTした */
      /* printf("KVM_EXIT_HLT\n"); */
      is_running = 0;
      fflush(stdout);
      break;
    case KVM_EXIT_IO:       /* IO操作 */
      if (run->io.port == 0x01 && run->io.direction == KVM_EXIT_IO_OUT) {
        putchar(*(char *)((unsigned char *)run + run->io.data_offset));
      }
    }
  }

とりあえずこれでromがちゃんとしていれば雑に動くVMが立てられるはず．
あとは割り込みコントローラとかタイマとか追加して，romがちゃんとBIOSとかになってて，
あとRAMもしっかり追加してやらないといけない．



