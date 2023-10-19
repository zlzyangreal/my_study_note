#  c++拷贝构造函数

首先对于普通类型的对象来说，它们之间的复制是很简单的，例如：

```c++
int a = 100;
int b = a;
```

而类对象与普通对象不同，类对象内部结构一般较为复杂，存在各种成员变量。

## 类对象拷贝的例子

是一种特殊的构造函数，**用基于同一类的一个对象构造和初始化另一个对象**。

```c++
#include<iostream>
using namespace std;

class CExample
{
private:
    int a;
public:
    //构造函数
    CExample(int b)
    {
        a=b;
        printf("constructor is called\n");
    }
    //拷贝构造函数
    CExample(const CExample & c)
    {
        a=c.a; // 可以看到，在类的方法中（类内）对象是可以直接对属性进行引用的
        printf("copy constructor is called\n");
    }
    //析构函数
    ~CExample()
    {
        cout<<"destructor is called\n";
    }
    void Show()
    {
        cout<<a<<endl;
    }
};

int main()
{
    CExample A(100);
    CExample B=A;
    B.Show(); 
    return 0;
}
```

结果：

运行程序，屏幕输出100。
CExample B=A;是语法，在编译器内部还是会将其转化成函数格式

```c++
CExample B(A)//相当于下式
CExample B=A;
```

就是我们自定义的拷贝构造函数。可见，拷贝构造函数是一种**特殊的构造函数**，函数的名称必须和类名称一致

## 拷贝构造函数的调用时机

### 当函数的参数为类的对象时

```c++
#include<iostream>
using namespace std;

class CExample
{
private:
    int a;
public:
    CExample(int b)
    {
        a=b;
        printf("constructor is called\n");
    }
    CExample(const CExample & c)
    {
        a=c.a;
        printf("copy constructor is called\n");
    }
    ~CExample()
    {
     cout<<"destructor is called\n";
    }
    void Show()
    {
     cout<<a<<endl;
    }
};


void g_fun(CExample c)
{
    cout<<"g_func"<<endl;
}


int main()
{
    CExample A(100);
    CExample B=A;
    B.Show(); 
    g_fun(A);
    return 0;
}
```

结果：
```c++
constructor is called
copy constructor is called
100
g_func
destructor is called
destructor is called
```
调用g_fun()时，会产生以下几个重要步骤：

(1).A对象传入形参时，会先会产生一个临时变量，就叫 C 吧。（所以会调用3次析构函数）

(2).然后**调用拷贝构造函数把A的值给C**。 整个这两个步骤有点像：CExample C(A);

(3).等g_fun()执行完后, 析构掉 C 对象。

还有一个析构是主函数结束，析构A

### 函数的返回值是类的对象

```c++
#include<iostream>
using namespace std;

class CExample
{
private:
    int a;
public:
    //构造函数
    CExample(int b)
    {
     a=b;
        printf("constructor is called\n");
    }
    //拷贝构造函数
    CExample(const CExample & c)
    {
     a=c.a;
        printf("copy constructor is called\n");
    }
    //析构函数
    ~CExample()
    {
     cout<<"destructor is called\n";
    }
    void Show()
    {
     cout<<a<<endl;
    }
};


CExample g_fun()
{
    CExample temp(0);
    return temp;
}


int main()
{
    
    g_fun();
    return 0;
}
```

当g_Fun()函数执行到return时，会产生以下几个重要步骤：

(1). 先会产生一个临时变量，temp

(2). 在return之前，有一个编译器优化，编译器支持返回值优化（RVO），它可以避免实际的拷贝构造步骤，将返回值的对象直接构造在调用者的上下文中，而不是在函数内部创建一个临时对象，从而提高性能。所以，拷贝构造函数的调用有可能被优化掉，但其目的仍然是确保返回值的有效性。

(3). 在函数执行到最后先析构temp局部变量。

(4). 等主函数执行完执行完后再析构掉返回对象。

# 拷贝赋值
拷贝赋值是一种操作，用于将一个对象的值赋给另一个对象。通常，拷贝赋值操作涉及将一个对象的数据成员的值复制到另一个对象，使它们具有相同的内容。拷贝赋值操作通常在类的成员函数中实现，这个函数通常称为拷贝赋值运算符（operator=）。
以下是一个简单的示例，演示了拷贝赋值的基本概念：
```c++
class MyClass {
public:
    int data;

    // 拷贝赋值运算符的定义
    MyClass&amp; operator=(const MyClass&amp; other) {
        if (this == &amp;other) {
            // 防止自我赋值
            return *this;
        }
        data = other.data;
        return *this;
    }
};

int main() {
    MyClass obj1;
    obj1.data = 42;

    MyClass obj2;
    obj2 = obj1; // 使用拷贝赋值运算符将 obj1 的值赋给 obj2

    return 0;
}
```

在这个示例中，MyClass 类定义了一个拷贝赋值运算符，它将一个 MyClass 对象的值赋给另一个对象。在 main() 函数中，obj2 = obj1; 这个语句调用了拷贝赋值运算符，将 obj1 的值赋给了 obj2。
拷贝赋值运算符通常用于确保对象之间的数据正确复制，以使它们具有相同的值。它们还可以执行必要的清理和分配操作，以确保新对象正确地接管原对象的资源。
需要注意的是，拷贝赋值操作应该防止自我赋值，即对象不能赋值给自己。这是通过检查 this == &amp;other 来实现的，其中 this 是正在赋值的对象的指针，other 是要赋值的对象。自我赋值检查可以避免资源泄漏和不确定行为。

拷贝赋值运算符就是重载赋值运算符调用operaotr =;如：Foo& operator = (const Foo&);返回值必须为引用类型

拷贝赋值运算符会将右侧运算符对象的每个非static成员赋予左侧对象，静态数据成员是公有的无须拷贝

只有整形常量数据成员才能在类内初始化，一般静态成员是在类外初始化。int Point::b = 0;静态数据成员的生存周期是从定义出开始到源程序结束。

## 浅拷贝（Shallow Copy）和深拷贝（Deep Copy）是在计算机编程中用于复制对象或数据结构的两个不同概念。它们在数据的复制方式和生命周期管理方面有重要区别：
### 浅拷贝（Shallow Copy）：

1.浅拷贝创建一个新的对象，但该对象的一部分数据成员或元素仍然是对原始对象中相同数据的引用。换句话说，它只复制对象的引用，而不复制实际数据。

2.如果原始对象中的数据是可变的，对浅拷贝的更改也会影响原始对象，因为它们引用相同的数据。

3.浅拷贝通常更快，因为它不需要复制大量数据，只需复制引用。

```c++
class ShallowCopyExample {
public:
    int *data;
    ShallowCopyExample(int val) {
        data = new int(val);
    }
};

ShallowCopyExample original(42);
ShallowCopyExample copy = original; // 这是浅拷贝
```

### 深拷贝（Deep Copy）：

4.深拷贝创建一个新的对象，并复制原始对象的所有数据，包括内部的数据，而不仅仅是引用。

5.如果原始对象中的数据是可变的，对深拷贝的更改不会影响原始对象，因为它们操作不同的数据。

6.深拷贝通常更慢，因为它需要复制整个数据结构，包括嵌套的数据。

```c++
class DeepCopyExample {
public:
    int *data;
    DeepCopyExample(int val) {
        data = new int(val);
    }
    DeepCopyExample(const DeepCopyExample&amp; other) {
        data = new int(*(other.data)); // 这是深拷贝
    }
};

DeepCopyExample original(42);
DeepCopyExample copy = original; // 这是深拷贝
```
7.浅拷贝复制引用，多个对象共享相同的数据。

8.深拷贝复制数据，每个对象都有其自己的数据拷贝。

9.深拷贝通常更安全，因为它避免了数据之间的意外相互影响，但也可能更昂贵。

在C++中，如果你定义了一个自定义类，需要特别小心如何处理拷贝构造函数和赋值操作符，以确保正确地处理浅拷贝和深拷贝。









