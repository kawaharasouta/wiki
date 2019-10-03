=======
option
=======

getopt()を使用するが、マルチモジュールの場合はgetopt_long()を使うらしい？

以下、lagopusのparse_argsの例

::

	static void
	parse_args(int argc, const char *const argv[]) {
	  int o;
	
	  /*
	   * FIXME:
	   *    Avoid to use getopt() for proper multi-modules initialization.
	   */
	  while ((o = getopt_long(argc, (char * const *)argv,
	                          "dh?vl:p:C:", s_longopts, NULL)) != EOF) {
	    switch (o) {
	      case 0: {
	        break;
	      }
	      case 'd': {
	        s_debug_level++;
	        break;
	      }
	      case 'h':
	      case '?': {
	        usage(stdout, 0);
	        break;
	      }
	      case 'v': {
	        fprintf(stdout, "%s version %d.%d.%d%s\n",
	                LAGOPUS_PRODUCT_NAME,
	                LAGOPUS_VERSION_MAJOR,
	                LAGOPUS_VERSION_MINOR,
	                LAGOPUS_VERSION_PATCH,
	                LAGOPUS_VERSION_RELEASE);
	        exit(0);
	        /* NOTREACHED */
	      }
	      case 'l': {
	        s_logfile = optarg;
	        break;
	      }
	      case 'p': {
	        s_pidfile = optarg;
	        break;
	      }
	      case 'C': {
	        s_configfile = optarg;
	        break;
	      }
	      default: {
	        usage(stderr, 1);
	        break;
	      }
	    }
	  }
	}
