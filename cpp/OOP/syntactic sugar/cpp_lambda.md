# lambda表达式
概念和基本用法
-------------
语法形式
```[ capture ] ( params ) opt -> ret { body; };```
* capture是捕获列表
* params 是参数表
* opt 是函数选项
* ret 是返回值类型
* body是函数体
```c++
auto f = [](int a) -> int { return a + 1; };
std::cout << f(1) << std::endl;  // 输出: 2
```

C++11 中允许省略 lambda 表达式的返回值定义：
```c++
auto f = [](int a){ return a + 1; };
```
编译器就会根据 return 语句自动推导出返回值类型

**初始化列表不能用于返回值的自动推导**
```c++
auto x1 = [](int i){ return i; };  // OK: return type is int
auto x2 = [](){ return { 1, 2 }; };  // error: 无法推导出返回值类型
```

lambda 表达式在没有参数列表时，参数列表是可以省略的
```c++
auto f1 = [](){ return 1; };
auto f2 = []{ return 1; };  // 省略空参数表
```

使用lambda表达式捕获列表
-----------------------
* []        不捕获任何变量
* [&]       捕获外部作用域中所有变量，并作为引用在函数体中使用（按引用捕获）
* [=]       捕获外部作用域中所有变量，并作为副本在函数体中使用（按值捕获）
* [=，&foo] 按值捕获外部作用域中所有变量，并按引用捕获 foo 变量
* [bar]     按值捕获 bar 变量，同时不捕获其他变量
* [this]    捕获当前类中的 this 指针，让 lambda 表达式拥有和当前类成员函数同样的访问权限。如果已经使用了 & 或者 =，就默认添加此选项。捕获 this 的目的是可以在 lamda 中使用当前类的成员函数和成员变量

实例
----
```c++
class A
{
public:
    int i_ = 0;
    void func(int x, int y)
    {
        auto x1 = []{ return i_; };                     // error，没有捕获外部变量
        auto x2 = [=]{ return i_ + x + y; };            // OK，捕获所有外部变量
        auto x3 = [&]{ return i_ + x + y; };            // OK，捕获所有外部变量
        auto x4 = [this]{ return i_; };                 // OK，捕获this指针
        auto x5 = [this]{ return i_ + x + y; };         // error，没有捕获x、y
        auto x6 = [this, x, y]{ return i_ + x + y; };   // OK，捕获this指针、x、y
        auto x7 = [this]{ return i_++; };               // OK，捕获this指针，并修改成员的值
    }
};
int a = 0, b = 1;
auto f1 = []{ return a; };                              // error，没有捕获外部变量
auto f2 = [&]{ return a++; };                           // OK，捕获所有外部变量，并对a执行自加运算
auto f3 = [=]{ return a; };                             // OK，捕获所有外部变量，并返回a
auto f4 = [=]{ return a++; };                           // error，a是以复制方式捕获的，无法修改
auto f5 = [a]{ return a + b; };                         // error，没有捕获变量b
auto f6 = [a, &b]{ return a + (b++); };                 // OK，捕获a和b的引用，并对b做自加运算
auto f7 = [=, &b]{ return a + (b++); };                 // OK，捕获所有外部变量和b的引用，并对b做自加运算
```

**lambda 表达式的延迟调用的**
```c++
int a = 0;
auto f = [=]{ return a; };      // 按值捕获外部变量
a += 1;                         // a被修改了
std::cout << f() << std::endl;  // 输出？
```
* 最终输出结果是 0

***显式指明 lambda 表达式***
```c++
int a = 0;
auto f1 = [=]{ return a++; };             // error，修改按值捕获的外部变量
auto f2 = [=]() mutable { return a++; };  // OK，mutable
```
* 修改按值捕获的外部变量(修改了a的值，但是不同步f2()为0)
* 被 mutable 修饰的 lambda 表达式就算没有参数也要写明参数列表

lambda 表达式的类型
------------------
lambda 表达式的类型在 C++11 中被称为“闭包类型（Closure Type）”。它是一个特殊的，匿名的非 nunion 的类类型

可以认为它是一个带有 operator() 的类，即仿函数。因此，我们可以使用 std::function 和 std::bind 来存储和操作 lambda 表达式：
```c++
std::function<int(int)>  f1 = [](int a){ return a; };
std::function<int(void)> f2 = std::bind([](int a){ return a; }, 123);
```
对于没有捕获任何变量的 lambda 表达式，还可以被转换成一个普通的函数指针：
```c++
using func_t = int(*)(int);
func_t f = [](int a){ return a; };
f(123);
```

声明式的编程风格，简洁的代码
--------------------------
lambda 表达式的价值在于，就地封装短小的功能闭包，可以极其方便地表达出我们希望执行的具体操作，并让上下文结合得更加紧密

例子：
```c++
class CountEven
{
    int& count_;
public:
    CountEven(int& count) : count_(count) {}
    void operator()(int val)
    {
        if (!(val & 1))       // val % 2 == 0
        {
            ++ count_;
        }
    }
};
std::vector<int> v = { 1, 2, 3, 4, 5, 6 };
int even_count = 0;
for_each(v.begin(), v.end(), CountEven(even_count));
std::cout << "The number of even is " << even_count << std::endl;
```
```c++
std::vector<int> v = { 1, 2, 3, 4, 5, 6 };
int even_count = 0;
for_each( v.begin(), v.end(), [&even_count](int val)
        {
            if (!(val & 1))  // val % 2 == 0
            {
                ++ even_count;
            }
        });
std::cout << "The number of even is " << even_count << std::endl;
```

