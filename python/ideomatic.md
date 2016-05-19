Some Ideomatic Python Skills
========================

1. [Simplify code with `in`](#keyword_in)
1. [Use `"switch"` in Python](#python_switch)

---------------

1. <a name="keyword_in">Simplify code with `in`</a>

  ```python
  self.can_recv = zmq_type in (zmq.PULL, zmq.SUB)
  self.can_send = zmq_type in (zmq.PUSH, zmq.PUB)
  self.can_sub = zmq_type in (zmq.SUB, )
  ```

  This is really simple and intuitive, far better than
  ```python
  if zmq_type == zmq.PULL or zmq_type == zmq.SUB:
    self.can_recv = True
  else:
    self.can_recv = False
  ```

  or
  ```python
  self.can_recv = True if zmq_type == zmq.PULL or zmq_type == zmq.SUB else False
  ```

2. <a name="python_switch">Use `"switch"` in Python</a>

  Python has no builtin `switch` keyword, but we can achieve this effect with
  following skills:
  ```python
  do_sub = {
      list: subscribe,
      str: [subscribe],
      type(None): []
  }[type(subscribe)]
  ```

  This is has the similar functionality as following psudo code:
  ```shell
  switch(type(subscribe)) {
    case list: subscribe;break;
    case str: [subscribe]; break;
    default: [];break;
  }
  ```
