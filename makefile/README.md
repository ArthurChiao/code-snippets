some makefile utilities
=========================

1. specify make file
  ```shell
  make -f my_makefile
  ```

2. step into sub-directory to build

  parent makefile looks like this:
  ```shell
  make_subdirs:
      cd sub-dir/ && make # after finish, it will automatically return to parent
                          # dir, so we do not need ` && cd ..` after `make`
      make all

  all:
  $(TARGET):
      $(CC) xxx
  ```
