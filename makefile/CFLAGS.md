CFLAGS
====================

1. treat warnings as errors
  ```shell
  -W -Wall Werror
  ```

2. define macro in CFLAGS with `-D`
  ```shell
  CFLAGS = -std=c99 -DMY_MACRO

  all:
      gcc test.c $(CFLAGS)
  ```

  then in `test.c`, you can test whether `MY_MACRO` is defined by:
  ```c
  #if defined(MY_MACRO) // this should be true if `-DMY_MACRO` is provided in CFLAGS

  //do something

  #else

  //do other things

  #endif
```

