# 左值右值
左值与右值这两个概念是从 C 中传承而来的，左值指既能够出现在等号左边，也能出现在等号右边的变量；右值则是只能出现在等号右边的变量
```c++
int a; // a 为左值
a = 3; // 3 为右值
```
* 左值是可寻址的变量，有持久性
* 右值一般是不可寻址的常量，或在表达式求值过程中创建的无名临时对象，短暂性的

左值和右值主要的区别之一是左值可以被修改，而右值不能

左值引用和右值引用
-----------------
引用本质是别名，可以通过引用修改变量的值，传参时传引用可以避免拷贝，其实现原理和指针类似

***左值引用：***
---------------
引用一个对象,能指向左值，不能指向右值的就是左值引用；
```c++
int a = 5;
int &ref_a = a; // 左值引用指向左值，编译通过
int &ref_a = 5; // 左值引用指向了右值，会编译失败
```
* 引用是变量的别名，由于右值没有地址，没法被修改，所以左值引用无法指向右值

但是，const左值引用是可以指向右值的：
```c++
const int &ref_a = 5;  // 编译通过
```
* const左值引用不会修改指向值，因此可以指向右值，这也是为什么要使用const &作为函数参数的原因之一

***右值引用：***
----------------
就是必须绑定到右值的引用，C++11中右值引用可以实现“移动语义”，通过 && 获得右值引用
```c++
int &&ref_a_right = 5;  // ok
 
int a = 5;
int &&ref_a_left = a;   // 编译不过，右值引用不可以指向左值
 
ref_a_right = 6;        // 右值引用的用途：可以修改右值
```
左右值引用的本质
---------------

***右值引用指向左值***
```c++
int a = 5;                          // a是个左值
int &ref_a_left = a;                // 左值引用指向左值
int &&ref_a_right = std::move(a);   // 通过std::move将左值转化为右值，可以被右值引用指向
 
cout << a;                          // 打印结果：5
```
* std::move移动不了什么，唯一的功能是把左值强制转化为右值，让右值引用可以指向左值。其实现等同于一个类型转换：static_cast<T&&>(lvalue)。 所以，单纯的std::move(xxx)不会有性能提升

* 右值引用能指向右值，本质上也是把右值提升为一个左值，并定义一个右值引用通过std::move指向该左值：
~~~
int &&ref_a = 5;
ref_a = 6; 

等同于以下代码：

int temp = 5;
int &&ref_a = std::move(temp);
ref_a = 6;
~~~

***左值引用、右值引用本身是左值***

被声明出来的左、右值引用都是左值。 因为被声明出的左右值引用是有地址的，也位于等号左边
```c++
// 形参是个右值引用
void change(int&& right_value) {
    right_value = 8;
}
 
int main() {
    int a = 5;                          // a是个左值
    int &ref_a_left = a;                // ref_a_left是个左值引用
    int &&ref_a_right = std::move(a);   // ref_a_right是个右值引用
 
    change(a);                          // 编译不过，a是左值，change参数要求右值
    change(ref_a_left);                 // 编译不过，左值引用ref_a_left本身也是个左值
    change(ref_a_right);                // 编译不过，右值引用ref_a_right本身也是个左值
     
    change(std::move(a));               // 编译通过
    change(std::move(ref_a_right));     // 编译通过
    change(std::move(ref_a_left));      // 编译通过
 
    change(5);                          // 当然可以直接接右值，编译通过
     
    cout << &a << ' ';
    cout << &ref_a_left << ' ';
    cout << &ref_a_right;
    // 打印这三个左值的地址，都是一样的
}
```
* 从性能上讲，左右值引用没有区别，传参使用左右值引用都可以避免拷贝
* 右值引用可以直接指向右值，也可以通过std::move指向左值；而左值引用只能指向左值(const左值引用也能指向右值)
* 作为函数形参时，右值引用更灵活。虽然const左值引用也可以做到左右值都接受，但它无法修改，有一定局限性

右值引用和std::move的应用场景
----------------------------

***实现移动语义***

在实际场景中，右值引用和std::move被广泛用于在STL和自定义类中实现移动语义，避免拷贝，从而提升程序性能。 在没有右值引用之前，一个简单的数组类通常实现如下，有构造函数、拷贝构造函数、赋值运算符重载、析构函数等

```c++
class Array {
public:
    Array(int size) : size_(size) {
        data = new int[size_];
    }
     
    // 深拷贝构造
    Array(const Array& temp_array) {
        size_ = temp_array.size_;
        data_ = new int[size_];
        for (int i = 0; i < size_; i ++) {
            data_[i] = temp_array.data_[i];
        }
    }
     
    // 深拷贝赋值
    Array& operator=(const Array& temp_array) {
        delete[] data_;
 
        size_ = temp_array.size_;
        data_ = new int[size_];
        for (int i = 0; i < size_; i ++) {
            data_[i] = temp_array.data_[i];
        }
    }
 
    ~Array() {
        delete[] data_;
    }
 
public:
    int *data_;
    int size_;
};
```
该类的拷贝构造函数、赋值运算符重载函数已经通过使用左值引用传参来避免一次多余拷贝了，但是内部实现要深拷贝，无法避免。 这时，有人提出一个想法：是不是可以提供一个移动构造函数，把被拷贝者的数据移动过来，被拷贝者后边就不要了，这样就可以避免深拷贝了，如：
```c++
class Array {
public:
    Array(int size) : size_(size) {
        data = new int[size_];
    }
     
    // 深拷贝构造
    Array(const Array& temp_array) {
        ...
    }
     
    // 深拷贝赋值
    Array& operator=(const Array& temp_array) {
        ...
    }
 
    // 移动构造函数，可以浅拷贝
    Array(const Array& temp_array, bool move) {
        data_ = temp_array.data_;
        size_ = temp_array.size_;
        // 为防止temp_array析构时delete data，提前置空其data_      
        temp_array.data_ = nullptr;
    }
     
 
    ~Array() {
        delete [] data_;
    }
 
public:
    int *data_;
    int size_;
};
```
后果：
* 不优雅，表示移动语义还需要一个额外的参数(或者其他方式)
* 无法实现！temp_array是个const左值引用，无法被修改，所以``temp_array.data_ = nullptr``;这行会编译不过。当然函数参数可以改成非``const：Array(Array& temp_array, bool move){...}``，这样也有问题，由于左值引用不能接右值，``Array a = Array(Array(), true)``;这种调用方式就没法用了

右值引用修改
```c++
class Array {
public:
    ......
 
    // 优雅
    Array(Array&& temp_array) {
        data_ = temp_array.data_;
        size_ = temp_array.size_;
        // 为防止temp_array析构时delete data，提前置空其data_      
        temp_array.data_ = nullptr;
    }
     
 
public:
    int *data_;
    int size_;
};
// 例1：Array用法
int main(){
    Array a;
 
    // 做一些操作
    .....
     
    // 左值a，用std::move转化为右值
    Array b(std::move(a));
}
```

***vector::push_back使用std::move提高性能***
```c++
// 例2：std::vector和std::string的实际例子
int main() {
    std::string str1 = "aacasxs";
    std::vector<std::string> vec;
     
    vec.push_back(str1);                // 传统方法，copy
    vec.push_back(std::move(str1));     // 调用移动语义的push_back方法，避免拷贝，str1会失去原有值，变成空字符串
    vec.emplace_back(std::move(str1));  // emplace_back效果相同，str1会失去原有值
    vec.emplace_back("axcsddcas");      // 当然可以直接接右值
}
 
// std::vector方法定义
void push_back (const value_type& val);
void push_back (value_type&& val);
 
void emplace_back (Args&&... args);
```
在vector和string这个场景，加个std::move会调用到移动语义函数，避免了深拷贝。

除非设计不允许移动，STL类大都支持移动语义函数，即可移动的。 另外，编译器会默认在用户自定义的class和struct中生成移动语义函数，但前提是用户没有主动定义该类的拷贝构造等函数(具体规则自行百度哈)。 因此，可移动对象在<需要拷贝且被拷贝者之后不再被需要>的场景，建议使用std::move触发移动语义，提升性能

~~~
moveable_objecta = moveable_objectb; 
改为： 
moveable_objecta = std::move(moveable_objectb);
~~~

还有些STL类是move-only的，比如unique_ptr，这种类只有移动构造函数，因此只能移动(转移内部对象所有权，或者叫浅拷贝)，不能拷贝(深拷贝):
```c++
std::unique_ptr<A> ptr_a = std::make_unique<A>();

std::unique_ptr<A> ptr_b = std::move(ptr_a);    // unique_ptr只有‘移动赋值重载函数‘，参数是&& ，只能接右值，因此必须用std::move转换类型

std::unique_ptr<A> ptr_b = ptr_a;               // 编译不通过
```
std::move本身只做类型转换，对性能无影响。 我们可以在自己的类中实现移动语义，避免深拷贝，充分利用右值引用和std::move的语言特性

完美转发 std::forward
---------------------
和std::move一样，它的兄弟std::forward也充满了迷惑性，虽然名字含义是转发，但他并不会做转发，同样也是做类型转换.

与move相比，forward更强大，move只能转出来右值，forward都可以。

``std::forward<T>(u)``有两个参数：``T``与`` u``。 
~~~
a. 当T为左值引用类型时，u将被转换为T类型的左值； 
b. 否则u将被转换为T类型右值。
~~~
举个例子，有main，A，B三个函数，调用关系为：main->A->B
```c++
void B(int&& ref_r) {
    ref_r = 1;
}
 
// A、B的入参是右值引用
// 有名字的右值引用是左值，因此ref_r是左值
void A(int&& ref_r) {
    B(ref_r);                       // 错误，B的入参是右值引用，需要接右值，ref_r是左值，编译失败
     
    B(std::move(ref_r));            // ok，std::move把左值转为右值，编译通过
    B(std::forward<int>(ref_r));    // ok，std::forward的T是int类型，属于条件b，因此会把ref_r转为右值
}
 
int main() {
    int a = 5;
    A(std::move(a));
}
```
例2：
```c++
void change2(int&& ref_r) {
    ref_r = 1;
}
 
void change3(int& ref_l) {
    ref_l = 1;
}
 
// change的入参是右值引用
// 有名字的右值引用是 左值，因此ref_r是左值
void change(int&& ref_r) {
    change2(ref_r);                         // 错误，change2的入参是右值引用，需要接右值，ref_r是左值，编译失败
     
    change2(std::move(ref_r));              // ok，std::move把左值转为右值，编译通过
    change2(std::forward<int &&>(ref_r));   // ok，std::forward的T是右值引用类型(int &&)，符合条件b，因此u(ref_r)会被转换为右值，编译通过
     
    change3(ref_r);                         // ok，change3的入参是左值引用，需要接左值，ref_r是左值，编译通过
    change3(std::forward<int &>(ref_r));    // ok，std::forward的T是左值引用类型(int &)，符合条件a，因此u(ref_r)会被转换为左值，编译通过
    // 可见，forward可以把值转换为左值或者右值
}
 
int main() {
    int a = 5;
    change(std::move(a));
}
```