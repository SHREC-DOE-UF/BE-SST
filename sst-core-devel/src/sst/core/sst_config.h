/* src/sst/core/sst_config.h.  Generated from sst_config.h.in by configure.  */
/* src/sst/core/sst_config.h.in.  Generated from configure.ac by autoheader.  */

/* Library directory where Boost can be found. */
#define BOOST_LIBDIR "/home/vol-ccmt2/local/packages/boost-1.56/lib"

/* Define to 1 if you have the `argz_add' function. */
#define HAVE_ARGZ_ADD 1

/* Define to 1 if you have the `argz_append' function. */
#define HAVE_ARGZ_APPEND 1

/* Define to 1 if you have the `argz_count' function. */
#define HAVE_ARGZ_COUNT 1

/* Define to 1 if you have the `argz_create_sep' function. */
#define HAVE_ARGZ_CREATE_SEP 1

/* Define to 1 if you have the <argz.h> header file. */
#define HAVE_ARGZ_H 1

/* Define to 1 if you have the `argz_insert' function. */
#define HAVE_ARGZ_INSERT 1

/* Define to 1 if you have the `argz_next' function. */
#define HAVE_ARGZ_NEXT 1

/* Define to 1 if you have the `argz_stringify' function. */
#define HAVE_ARGZ_STRINGIFY 1

/* Set to 1 Boost was found */
#define HAVE_BOOST 1

/* Define to 1 if you have the `closedir' function. */
#define HAVE_CLOSEDIR 1

/* Define to 1 if you have the <c_asm.h> header file. */
/* #undef HAVE_C_ASM_H */

/* Define to 1 if you have the declaration of `cygwin_conv_path', and to 0 if
   you don't. */
/* #undef HAVE_DECL_CYGWIN_CONV_PATH */

/* Define to 1 if you have the <dirent.h> header file. */
#define HAVE_DIRENT_H 1

/* Define if you have the GNU dld library. */
/* #undef HAVE_DLD */

/* Define to 1 if you have the <dld.h> header file. */
/* #undef HAVE_DLD_H */

/* Define to 1 if you have the `dlerror' function. */
#define HAVE_DLERROR 1

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the <dl.h> header file. */
/* #undef HAVE_DL_H */

/* Define if you have the _dyld_func_lookup function. */
/* #undef HAVE_DYLD */

/* Define to 1 if the system has the type `error_t'. */
#define HAVE_ERROR_T 1

/* Defines whether we have the hdf5 library */
/* #undef HAVE_HDF5 */

/* Define to 1 if you have the <intrinsics.h> header file. */
/* #undef HAVE_INTRINSICS_H */

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define if you have the libdl library or equivalent. */
#define HAVE_LIBDL 1

/* Define if libdlloader will be built on this platform */
#define HAVE_LIBDLLOADER 1

/* Define to 1 if you have the `ltdl' library (-lltdl). */
#define HAVE_LIBLTDL 1

/* Defines whether we have the libz library */
#define HAVE_LIBZ 1

/* Define this if a modern libltdl is already installed */
#define HAVE_LTDL 1

/* Define to 1 if you have the <mach/mach_time.h> header file. */
/* #undef HAVE_MACH_MACH_TIME_H */

/* Define to 1 if you have the <mach-o/dyld.h> header file. */
/* #undef HAVE_MACH_O_DYLD_H */

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Define to 1 if you have the `opendir' function. */
#define HAVE_OPENDIR 1

/* Define if libtool can extract symbol lists from object files. */
#define HAVE_PRELOADED_SYMBOLS 1

/* Define to 1 if you have the <Python.h> header file. */
#define HAVE_PYTHON_H 1

/* Define to 1 if you have the `readdir' function. */
#define HAVE_READDIR 1

/* Define if you have the shl_load function. */
/* #undef HAVE_SHL_LOAD */

/* Define if C++ supports C++14 features. */
#define HAVE_STDCXX_1Y 1

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the `strlcat' function. */
/* #undef HAVE_STRLCAT */

/* Define to 1 if you have the `strlcpy' function. */
/* #undef HAVE_STRLCPY */

/* Define to 1 if you have the <sys/dl.h> header file. */
/* #undef HAVE_SYS_DL_H */

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/time.h> header file. */
#define HAVE_SYS_TIME_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* This value is set to 1 to indicate that the system argz facility works */
#define HAVE_WORKING_ARGZ 1

/* Define if you have the Zoltan library. */
/* #undef HAVE_ZOLTAN */

/* Define to 1 if you have the <zoltan.h> header file. */
/* #undef HAVE_ZOLTAN_H */

/* Define if the OS needs help to load dependent libraries for dlopen(). */
/* #undef LTDL_DLOPEN_DEPLIBS */

/* Define to the system default library search path. */
#define LT_DLSEARCH_PATH "/lib:/usr/lib:/usr/lib/x86_64-linux-gnu/libfakeroot:/usr/local/lib:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu/mesa-egl:/usr/lib/x86_64-linux-gnu/mesa"

/* The archive extension */
#define LT_LIBEXT "a"

/* The archive prefix */
#define LT_LIBPREFIX "lib"

/* Define to the extension used for runtime loadable modules, say, ".so". */
#define LT_MODULE_EXT ".so"

/* Define to the name of the environment variable that determines the run-time
   module search path. */
#define LT_MODULE_PATH_VAR "LD_LIBRARY_PATH"

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#define LT_OBJDIR ".libs/"

/* Define to the shared library suffix, say, ".dylib". */
/* #undef LT_SHARED_EXT */

/* Define to the shared archive member specification, say "(shr.o)". */
/* #undef LT_SHARED_LIB_MEMBER */

/* Define if dlsym() requires a leading underscore in symbol names. */
/* #undef NEED_USCORE */

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "sst@sandia.gov"

/* Define to the full name of this package. */
#define PACKAGE_NAME "SSTCore"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "SSTCore -dev"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "sstcore"

/* Define to the home page for this package. */
#define PACKAGE_URL ""

/* Define to the version of this package. */
#define PACKAGE_VERSION "-dev"

/* SST-Core Git Branch */
#define SSTCORE_GIT_BRANCH "N/A"

/* SST-Core Git Commit Count */
#define SSTCORE_GIT_COMMITCOUNT "0"

/* SST-Core Git Head SHA */
#define SSTCORE_GIT_HEADSHA "-dev"

/* Defines the CPPFLAGS needed to compile Boost into SST */
#define SST_BOOST_CPPFLAGS "-I/home/vol-ccmt2/local/packages/boost-1.56/include"

/* Defines the LDFLAGS needed to compile Boost into SST */
#define SST_BOOST_LDFLAGS "-L/home/vol-ccmt2/local/packages/boost-1.56/lib"

/* Defines the LIBDIR needed to load dynamic libraries for Boost */
#define SST_BOOST_LIBDIR "/home/vol-ccmt2/local/packages/boost-1.56/lib"

/* Defines the LIBS needed to compile Boost into SST */
#define SST_BOOST_LIBS ""

/* Defines the C compiler used to build SST */
#define SST_CC "gcc"

/* Defines the CFLAGS used to build SST */
#define SST_CFLAGS "-g -O2 -Wall -Wextra"

/* Defines compile for Mac OS-X */
/* #undef SST_COMPILE_MACOSX */

/* Define if you have the MPI library. */
#define SST_CONFIG_HAVE_MPI 1

/* Set to 1 if Python was found */
#define SST_CONFIG_HAVE_PYTHON 1

/* Defines the C preprocessor used to build SST */
#define SST_CPP "gcc -E"

/* Defines the CPPFLAGS used to build SST */
#define SST_CPPFLAGS "-I$(top_builddir) -I$(top_srcdir) -I$(top_srcdir)/src -I$(top_builddir)/src "

/* Defines the C++ compiler used to build SST */
#define SST_CXX "g++"

/* Defines the C++ preprocessor used to build SST */
#define SST_CXXCPP "g++ -E"

/* Defines the CXXFLAGS used to build SST */
#define SST_CXXFLAGS "-g -O2 -std=c++1y -D__STDC_FORMAT_MACROS -Wall -Wextra"

/* Defines the location SST will be installed in */
#define SST_INSTALL_PREFIX "/home/vol-ccmt2/local/sst-core-devel"

/* Defines the linker used to build SST */
#define SST_LD "/usr/bin/ld -m elf_x86_64"

/* Defines the LDFLAGS used to build SST */
#define SST_LDFLAGS ""

/* Defines the MPI C compiler used to build SST */
#define SST_MPICC "mpicc"

/* Defines the MPI C++ compilers used to build SST */
#define SST_MPICXX "mpicxx"

/* Defines the CPPFLAGS needed to compile Python into SST */
#define SST_PYTHON_CPPFLAGS "-I/usr/include/python2.7 -I/usr/include/x86_64-linux-gnu/python2.7"

/* Defines the LDFLAGS needed to compile Python into SST */
#define SST_PYTHON_LDFLAGS "-L/usr/lib/python2.7/config-x86_64-linux-gnu -L/usr/lib -lpython2.7 -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions"

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Define to 1 if you can safely include both <sys/time.h> and <time.h>. */
#define TIME_WITH_SYS_TIME 1

/* Set to 1 to use memory pools in the SST core */
#define USE_MEMPOOL 1

/* Tracks extra information about events and activities. */
/* #undef __SST_DEBUG_EVENT_TRACKING__ */

/* Defines additional debug output is to be printed */
/* #undef __SST_DEBUG_OUTPUT__ */

/* Defines if core should have profiling enabled. */
/* #undef __SST_ENABLE_PROFILE__ */

/* Defines that standard PRI macros should be enabled */
#define __STDC_FORMAT_MACROS 1

/* Define so that glibc/gnulib argp.h does not typedef error_t. */
/* #undef __error_t_defined */

/* Define to a type to use for 'error_t' if it is not otherwise available. */
/* #undef error_t */

/* Define to `__inline__' or `__inline' if that's what the C compiler
   calls it, or to nothing if 'inline' is not supported under any name.  */
#ifndef __cplusplus
/* #undef inline */
#endif
