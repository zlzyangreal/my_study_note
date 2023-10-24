# ostream类

ostream的构造函数
----------------
```c++
public:
//explicit用来防止由构造函数定义的隐式转换
explicit
      basic_ostream(__streambuf_type* __sb)
      { this->init(__sb); }

protected:
      basic_ostream()
      { this->init(0); }

#if __cplusplus >= 201103L
      // Non-standard constructor that does not call init()
      basic_ostream(basic_iostream<_CharT, _Traits>&) { }

      basic_ostream(const basic_ostream&) = delete;

      basic_ostream(basic_ostream&& __rhs)
      : __ios_type()
      { __ios_type::move(__rhs); }

      basic_ostream& operator=(const basic_ostream&) = delete;

      basic_ostream&
      operator=(basic_ostream&& __rhs)
      {
    swap(__rhs);
    return *this;
      }
```
* ```basic_ostream(__streambuf_type* __sb){ this->init(__sb); }```
~~~
ostream类的显式构造函数。explicit关键字在C++中用于防止隐式类型转换。这意味着不能在不显式调用构造函数的情况下将一个__streambuf_type指针隐式地转换为basic_ostream对象。只有在显式调用构造函数时，这个类型转换才会发生
~~~

* ```protected```
~~~
ostream类的保护（protected）构造函数。protected成员可以被派生类访问，但不能被外部代码直接访问。这个构造函数初始化了basic_ostream的内部数据结构，同时它是保护的，所以不能被外部直接调用
~~~

* ```basic_ostream(basic_iostream<_CharT, _Traits>&) { }```
~~~
这是一个非标准的构造函数，它不调用init()方法。这个构造函数接受一个basic_iostream类型的参数，并且是删除的，也就是说，它不能被调用。删除的函数是在C++11标准中引入的一个特性，用于明确地阻止某个函数被调用
~~~

* ```basic_ostream(const basic_ostream&) = delete;```与``` basic_ostream& operator=(const basic_ostream&) = delete;```
~~~
删除拷贝构造函数与拷贝赋值操作
~~~

* ```basic_ostream(basic_ostream&& __rhs): __ios_type(){ __ios_type::move(__rhs); }```
~~~
移动构造函数。移动构造函数是C++11引入的特性，用于在不进行深拷贝的情况下将资源（比如内存）从一个对象转移到另一个对象。这个构造函数接受一个右值引用（rvalue reference），允许你将一个右值（例如，临时对象）的内容移动到当前的对象中
~~~

* ```basic_ostream&operator=(basic_ostream&& __rhs)```
~~~
移动赋值操作符。这个操作符允许你将一个右值的内容移动到当前对象中，并且在移动完成后，右值的状态会变为有效但未指定的状态
~~~

右移为<<操作符
-------------
```c++
    //重载一系列<<操作符，可以用于读取变量数据并放入到流缓冲区中
      __ostream_type&
      operator<<(long __n)
      { return _M_insert(__n); }

      __ostream_type&
      operator<<(unsigned long __n)
      { return _M_insert(__n); }

      __ostream_type&
      operator<<(bool __n)
      { return _M_insert(__n); }

      __ostream_type&
      operator<<(short __n);

      __ostream_type&
      operator<<(unsigned short __n)
      {

    return _M_insert(static_cast<unsigned long>(__n));
      }

      __ostream_type&
      operator<<(int __n);

      __ostream_type&
      operator<<(unsigned int __n)
      {

    return _M_insert(static_cast<unsigned long>(__n));
      }
```

put函数
-------
```c++
      //往缓冲区中插入一个字符
      __ostream_type&
      put(char_type __c);
```

write函数
---------
```c++
      //将__s指针所指向的字符串复制出来并插入到缓冲区中，最多插入__n个字符
      __ostream_type&
      write(const char_type* __s, streamsize __n);
```
~~~
ostream& write(const char* buffer, streamsize size);

write()函数是用于在二进制文件中写入数据的函数

参数说明：

    buffer：指向要写入数据的缓冲区的指针

    size：要写入的数据的字节数

函数功能：

write()函数将size个字节的数据从buffer指向的缓冲区写入到输出流中。输出流可以是文件流（如ofstream对象）、标准输出流（如cout对象）或其他派生自ostream的流对象。
write()函数将数据按照二进制形式写入，不会进行任何格式化或转换。它逐字节地将数据写入流，适用于处理二进制数据或自定义数据结构。
~~~

tellp函数
---------
```c++
//返回当前写缓冲区位置
     pos_type
      tellp();
```

~~~
streampos tellp();

tellp()函数是用于获取输出流的当前写入位置（写指针位置）的函数。它通常用于文件流（如ofstream对象）或其他支持写操作的流

返回值:

    类型为streampos，它是一个整数类型，表示流的位置

函数功能：

    tellp()函数的作用是返回当前写入位置的偏移量，即写指针指向的位置相对于流的起始位置的偏移量。这个偏移量可以用于记录当前写入位置，或者在需要的时候重新定位到该位置

tellp()函数在文本模式下返回的是逻辑位置（logical position），而在二进制模式下返回的是实际字节位置（byte position）
~~~

seekp函数
---------
```c++
      /**
     从当前位置开始，跳转pos个写位置
      */
      __ostream_type&
      seekp(pos_type pos);

      /**
      根据ios_base::seekdir定义的位置，跳转off个写位置
      */
       __ostream_type&
      seekp(off_type off, ios_base::seekdir);
```

~~~
seekp()函数有两种重载形式

ostream& seekp(streampos pos);
ostream& seekp(streamoff off, ios_base::seekdir dir);

第一种形式接受一个streampos参数，用于设置写入位置为指定的偏移量

    参数`pos`是一个表示偏移量的整数类型（如`streampos`或`size_t`），它指定了要设置的写入位置相对于流的起始位置的偏移量

第二种形式接受一个streamoff参数和一个ios_base::seekdir参数，用于相对于当前写入位置进行定位

    参数`off`是一个表示偏移量的整数类型（如`streamoff`或`int`），它指定了要设置的写入位置相对于当前位置的偏移量。参数`dir`是一个`ios_base::seekdir`枚举类型的值，用于指定偏移量的方向，可以是`ios_base::beg`（相对于起始位置）、`ios_base::cur`（相对于当前位置）或`ios_base::end`（相对于结束位置）

这两种形式的seekp()函数都返回一个指向输出流的引用，以便支持链式调用
~~~