Coding Style
======================

This is a brief summary of C coding style we have followed.

## Purpose
The current coding style is mainly based on `Google C++ Coding Style`,
but also incorporates some good rules from other styles.
Essentially, a good coding style makes the code more manageable, readable, and
professional. We choose `Google C++ Coding Style` because
we believe this is the best practice in industry for **userspace C/C++**
program developments.

One of the most important goals of a coding style is to to make the code base
consistent - a code base that looks like coming from one person but actually
may be implemented by couples, hundrads, or even thousands of people all over
the world, just like DPDK, OVS, Linux kerel.

Using one style consistently through entire
codebase lets us focus on other (more important) issues.
Consistency also allows for automation with some tools.

## Foundation
Here are some best known coding styles that we have followed or referenced,
actually they are beyond `coding style`, we can learn a lot of programming
skills and best practices in them:

1. [Google C++ Coding Style](https://google.github.io/styleguide/cppguide.html)
1. [openvswitch Coding Style](https://github.com/openvswitch/ovs/blob/master/CodingStyle.md)
1. [DPDK Coding Style](http://dpdk.org/doc/guides/contributing/coding_style.html)
1. [Linux Kernel Coding Style](https://www.kernel.org/doc/Documentation/CodingStyle)

Note that there are some contradictory advices/rules on the same topic, e.g,
some may suggest 8 characters per tab (kernel style), some insist on 4
characters (Google, DPDK). The key point here is that each suggestion serves
one specific target: the kernel suggests 8-character tab because it hates long
routines and deep recursions, which are beds of bugs hard to finding;
while in userspace code, debug in relatively easy and we need more recursions
than kernel to realize business logic. So at these controvercies, it is not
difficult for you to pick the best rule for your situation.

## C Coding Style Highlights
We are not going to explain all the benefits, which are left to you who are
going to contribute to the code base. Instead, Here lists some of the most
common convensions we have followed, and give some explanations:

1. **Keep each line within 80 characters**

  This is the NO.1. rule found in almost all coding styles.

  It needs little time to get used to it - if you have not, then life will be
  fantastic.

  Some exceptions are allowed to break this rule, although that's unsual.

2. **Code layout in each source file: public APIs first, internal routines second**

  Put public APIs in the first half of the file, and internal routines at the
  bottom half. This is benefits code readability.

3. **Naming conversions**

  * struct/class/enum names use CamelCase

  * macros/enums use UPPER_CASE_PLUS_UNDERLINE

  * varaibles use lower_case_plus_underline

    - prefer to use underscore for variables with larger scope
      e.g. `struct IpAddr src_ip`

    - prefer more shorter names for local variables
      e.g. `struct IpAddr srcip`

    - global varialbes are prefixed with `g_`

    - static varialbes are prefixed with `s_`

  * routines/functions use lower_case_plus_underline

    - public API should be prefixed with a short, meaningful module name
      e.g. APIs in udp module prefixed with `udp_`, the API looks like this:
      `udp_push_hdr`, `udp_pop_hdr`, `udp_check_xxx`.

    - internal routines do not need to prefix anything, but declear each
    internal routine as `static` (file scope)

  Examples:
  ```c
  struct ThisIsAStruct {
      uint32_t filed_a;
      uint32_t filed_b;
  };

  enum ThisIsAnEnum {
      ENUM_XXX = 0,
      ENUM_YYY,
      ENUM_ZZZ,
  };

  struct ThisIsAStruct this_is_a_variable;
  enum   ThisIsAnEnum  this_is_another_var;
  int                  g_this_is_a_global_var;
  static int           s_this_is_a_static_var;

  // this is a public API example from UDP module
  // prefer to put the API doc in udp.h instead of udp.c
  /**
  * push UDP header
  *
  * @param pkt - input packet
  * @param srcport - source UDP port
  * @param dstport - destination UDP port
  */
  void udp_push_hdr(struct PktBuf *pkt, uint16_t srcport, uint16_t dstport)
  {
      // do some processing
  }

  // this is a internal routine example in UDP module
  // doc for the internal routines is with the routine itself
  /**
  * do checksum for the input packet
  * @param pkt - input packet
  */
  static void do_checksum(struct PktBuf *pkt)
  {
      // do checksum
  }
  ```

4. **Avoid to use `typedef`**
  
  See linus's expalination in `Linux Kernel Coding Guide`

  Apparently, `struct SomeName some_var` and `enum SomeName some_var` is much
  more clearer than `SomeName some_var` in the code.

5. **Prefer to use c99 types to indicate the variable type length explicitly**

  e.g. `uint64_t var` instead of `unsigned long long var`
  e.g. `uint32_t var` instead of `unsigned long var` or `unsigned var`
  e.g. `int16_t var` instead of `short var`

  if integer type is not critical at some situations, use `int` is also ok.
  ```shell
  int i
  for (i = 0; i < 100; i++) {
      /* do something */
  }
  ```

6. Avoid trailing spaces on lines

  A `vim` regular expression can do this:

  ```shell
  :%s/\s\+$//gc
  ```

## Summary
This is a brief highlights of the C coding style we have followed, please
read `Google C++ Coding Style` carefully to learn more.

Our target is simple and straight-forward: make the code a masterpiece!

***Stay Hungry, Stay Foolish.***

We quote a block from `DPDK Coding Guide` to finish this document:

  > The rules and guidelines given in this document cannot cover every
  situation, so the following general guidelines should be used as a fallback:

  > * The code style should be consistent within each individual file.
  > * In the case of creating new files, the style should be consistent
  within each file in a given directory or module.
  > * The primary reason for coding standards is to increase code readability
  and comprehensibility, therefore always use whatever option will make the
  code easiest to read.
