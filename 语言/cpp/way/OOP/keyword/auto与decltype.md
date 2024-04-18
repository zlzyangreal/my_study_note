# auto关键字
类型自动推断

用法包括两种：一是在变量声明时根据初始化表达式自动推断该变量的类型，二是在声明函数时作为函数返回值的占位符

自动类型推断
--------------
例子：对于vector类型的变量，如果我们需要获取它的迭代器，我们需要这样声明``vector::iterator iter``，而使用auto关键字后我们可以让编译器帮我们推断出迭代器的具体类型。另外，在模板函数定义时，如果变量的类型依赖于模板参数，我们也很难确定变量的类型，使用auto关键字则可以把这些“脏活累活”交给编译器完成
```c++
#include <iostream> 
#include <vector> 
using namespace std;

template<class T, class U>
void add(T t, U u)
{
    auto s = t + u;
    cout << "type of t + u is " << typeid(s).name() << endl;
}

int main()
{
    // 简单自动类型推断
    auto a = 123;
    cout << "type of a is " << typeid(a).name() << endl;
    auto s("fred");
    cout << "type of s is " << typeid(s).name() << endl;

    // 冗长的类型说明（如迭代器）
    vector<int> vec;
    auto iter = vec.begin();
    cout << "type of iter is " << typeid(iter).name() << endl;

    // 使用模板技术时，如果某个变量的类型依赖于模板参数，使用auto确定变量类型
    add(101, 1.1);
}
```

函数返回值占位符
---------------
auto主要与decltype关键字配合使用，作为返回值类型后置时的占位符。此时，关键字不表示自动类型检测，仅仅是表示后置返回值的语法的一部分
```c++
template<class T, class U>
auto add(T t, U u) -> decltype(t + u) 
{
    return t + u;
}
```

注意点
------
1   使用auto关键字的变量必须有初始值

2   可以使用valatile，*（指针类型说明符），&（引用类型说明符），&&（右值引用）来修饰auto关键字
```c++
auto a = 10;
auto *pa = new auto(a);
auto **rpa = new auto(&a);
cout << typeid(a).name() << endl;   // 输出： int
cout << typeid(pa).name() << endl;  // 输出： int *
cout << typeid(rpa).name() << endl; // 输出： int **
```
3   函数参数和模板参数不能被声明为auto

4   使用auto关键字声明变量的类型，不能自动推导出顶层的CV-qualifiers和引用类型，除非显示声明
* 使用auto关键字进行类型推导时，如果初始化表达式是引用类型，编译器会去除引用，除非显示声明
```c++
int i = 10;
int &r = i;
auto a = r;
a = 13; // 重新赋值
cout << "i = " << i << " a = " << a << endl;    // 输出i=10，a=13

// 显式声明
auto &b = r;
b = 15; // 重新赋值
cout << "i = " << i << " b = " << b << endl;    // 输出i=15，a=15
```
* 使用auto使用auto关键字进行类型推导时，编译器会自动忽略顶层const，除非显示声明
```c++
const int c1 = 10;
auto c2 = c1;
c1 = 11; // 报错，c1为const int类型，无法修改const变量
c2 = 14; // 正确，c2为int类型

// 显示声明
const auto c3 = c1;
c3 = 15; // 报错，c3为const int类型，无法修改const变量
```
* 对于数组类型，auto关键字会推导为指针类型，除非被声明为引用
```c++
int a[10];
auto b = a;
cout << typeid(b).name() << endl;   // 输出：int *

auto &c = a;
cout << typeid(c).name() << endl;   // 输出：int [10]
```

# 关键字decltype

decltype与auto区别
-----------------
有时希望从表达式的类型推断出要定义的变量的类型（这一点auto可以做到），但是不想用该表达式的值初始化变量（auto依赖这一点才能推导类型）
```c++
int a = 10,b = 11;
auto c = a + b; //c为int型
decltype(a + b) d ; //d为int型
```
auto通过初始化它的表达式来推断c的类型，也就是说，auto推导变量依赖于初始化它的表达式，并且auto声明的变量必须初始；而decltype是直接通过某一个表达式来获取数据类型，从而定义d的类型

decltype用法
------------
***decltype变量***

和auto不同，decltype会保留const属性和引用属性
```c++
const int ci = 0, &cj = ci;

decltype(ci) x = 0; //x的类型为const int
decltype(cj) y = x; //y的类型为const int&
decltype(cj) z;     //错误，因为z的类型为const int&，必须初始化(引用需要对象)

auto w = ci;        //w的类型是int
w = 9;
auto n = cj;        //n的类型是int
```

***decltype表达式***

decltype表达式时，返回的类型根据表达式的结果不同而不同：表达式返回左值，得到该类型的左值引用；表达式返回右值，得到该类型

右值    
```c++
int i = 42, &r = i;
decltype(r + 0) b; //b类型是int，而不是int&
```
* 尽管r是引用类型，但是r+0是一个具体的值，只能做右值，值对应的类型是int型，所以b为int类型

左值    表达式能做左值，推导为类型的引用
```c++
int ii = 42, *p = &ii;
decltype(*p) c;     //错误，c是int&，必须初始化
decltype((ii)) d;   //错误，d是int&，必须初始化
```
* 对于解引用``*p``，它代表的是``p``指向地址中的值，同时我们可以给这个值赋值，即为左值。所以，``decltype(*p)``是``int&`` ，这样才能有给绑定变量的值赋值的特点
* ``ii``是一个变量，加上括号后变为表达式，即``(ii)``是一个表达式，又我们可以``ii``赋值，即为左值。所以，``decltype((var))``永远是一个引用类型，``decltype((ii))``声明变量``d``时，``d``就为``int&``类型

***decltype函数***

``decltype(f()) sum = x; ``,sum的类型就是函数f的返回类型，sum的类型就是假如函数f被调用，它会返回那个类型

例子
```c++
template <typename T>
T add(T a, T b)
{ 
   
	return a+b;
}
decltype(add(1,2)) m = 10; //m的类型是int
decltype(add(1.0,2.0)) m2 = 20; //m2的类型是double
```

``decltype(f)``

例子
```c++
int add_to(int a, int b)
{ 
   
	return a + b;
}
decltype(add_to) *pf = add_to; //pf就是一个函数指针，类型为int (int,int)
pf(1,2);
```
* decltype(add_to)直接返回函数类型，所以pf是一个函数指针
* **模板函数无法返回函数指针**模板函数依赖于参数列表，只根据函数名是无法推断函数类型的，所以说函数指针pf的类型无法确认
* **函数是重载的**，也无法通过函数名来推断返回的函数类型，那么也无法返回函数指针，如下面的例子中声明pf为函数指针是**错误的**
```c++
int add_to(int a, int b)
{ 
   
	return a + b;
}
int add_to(int a, int b,int c)
{ 
   
	return a + b +c;
}
decltype(add_to) *pf = add_to; 
pf(1,2);
```

c++11中decltype的主要作用
------------------------
Decltype在C++11中的主要作用是用于申明返回值类型依赖于其参数类型的模板函数

```c++
template <typename _Tx, typename _Ty>
auto multiply(_Tx x, _Ty y)->decltype(x*y)
{ 
   
    return x*y;
}
```
* decltype(x*y) 的作用是根据给定表达式的类型来推导出函数的返回类型，使函数能够返回正确的乘积结果类型，而无需手动指定返回类型

注意这里的auto并没有做任何类型推断，只是用来表明这里使用的是C++11 的拖尾返回类型（trailing return type）语法，**也就是函数返回类型将在参数列表之后进行声明**（在”->”之后），优点是可以使用函数参数来声明函数返回类型（如果将返回类型放置于函数之前，这里的参数x和y还没有被声明，因此不能被使用）