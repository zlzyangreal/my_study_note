

虚函数
------
```c++
class A
{
public:
    virtual void foo()
    {
        cout<<"A::foo() is called"<<endl;
    }
};
class B:public A
{
public:
    void foo()
    {
        cout<<"B::foo() is called"<<endl;
    }
};
int main(void)
{
    A *a = new B();     // 创建了一个指向A类型的指针，并将其指向一个动态分配的B类
    a->foo();           // 在这里，a虽然是指向A的指针，但是被调用的函数(foo)却是B的!
    return 0;
}
```
* 父类指向子类，相当于父类拓展了子类特性
* 虚函数虚就虚在所谓"推迟联编"或者"动态联编"上，一个类函数的调用并不是在编译时刻被确定的，而是在运行时刻被确定的。由于编写代码的时候并不能确定被调用的是基类的函数还是哪个派生类的函数，所以被成为"虚"函数

纯虚函数
--------
纯虚函数是在基类中声明的虚函数，它在基类中没有定义，但要求任何派生类都要定义自己的实现方法。在基类中实现纯虚函数的方法是在函数原型后加 =0
```c++
virtual void funtion1()=0
```
* 纯虚函数最显著的特征是：它们必须在继承类中重新声明函数（不要后面的＝0，否则该派生类也不能实例化），而且它们在抽象类中往往没有定义

抽象类
------
抽象类是一种特殊的类，它是为了抽象和设计的目的为建立的，它处于继承层次结构的较上层

***定义*** 称带有纯虚函数的类为抽象类

***作用*** 抽象类的主要作用是将有关的操作作为结果接口组织在一个继承层次结构中，由它来为派生类提供一个公共的根，派生类将具体实现在其基类中作为接口的操作。所以派生类实际上刻画了一组子类的操作接口的通用语义，这些语义也传给子类，子类可以具体实现这些语义，也可以再将这些语义传给自己的子类

***注意***
* 抽象类只能作为基类来使用，其纯虚函数的实现由派生类给出。如果派生类中没有重新定义纯虚函数，而只是继承基类的纯虚函数，则这个派生类仍然还是一个抽象类。如果派生类中给出了基类纯虚函数的实现，则该派生类就不再是抽象类了，它是一个可以建立对象的具体的类
* 抽象类是不能定义对象的

关键字virtual
-------------
virtual关键字主要有这样几种使用场景：第一，修饰父类中的函数 ；第二，修饰继承性。

注意：友元函数、构造函数、static静态函数不能用virtual关键字修饰。普通成员函数和析构函数可以用virtual关键字修饰。

virtual具有继承性：父类中定义为virtual的函数在子类中重写的函数也自动成为虚函数

**只有子类的虚函数和父类的虚函数定义完全一样才被认为是虚函数,比如父类后面加了const,如果子类不加的话就是隐藏了,不是覆盖**

修饰父类中的函数主要分为三种:普通函数、析构函数和纯虚函数

***普通函数***
```c++
#include <iostream>

class father {
public:
	void func1() {std::cout << "this is father func1" << std::endl;}
	virtual void func2() {std::cout << "this is father func2" <<std::endl;}
}

class son:public father {
public:
	void func1() {std::cout << "this is son func1" << std::endl;}
	void func2() {std::cout << "this is son func2" << std::endl;}
}

int main() {
	father *f1 = new son();
	f1.func1();
	f1.func2();
	return 0;
}
```
输出
```c++
this is father func1
this is son func2
```
***析构函数***
* 虚析构函数在销毁时会调用对象的析构函数，这样就不会出现像有的数据成员没有销毁导致内存泄露的问题或者程序直接崩溃
```c++
class GrandFather {
public:
	GrandFather() {std::cout << "construct grandfather" << std::endl;}
	~GrandFather() {std::cout << "destruct grandfather" << std::endl;}
};

class Father：public GrandFather{
public:
	Father() {std::cout << "construct father" << std::endl;}
	~Father() {std::cout << "destruct father" << std::endl;}
};

class Son：public Father{
public:
	Son() {std::cout << "construct son" << std::endl;}
	~Son() {std::cout << "destruct son" << std::endl;}
};

int main() {
	Father *f = new Son();
	delete f;
	return 0;
}
```
输出
```c++
construct grandfather
construct father
construct son
destruct father
destruct grandfather
```
* 由于 Son 类是从 Father 类继承而来，而 Father 类又是从 GrandFather 类继承而来，因此在创建 Son 对象时，会按照继承关系依次调用基类的构造函数

将Father或者GrandFather其中一个的析构函数修改为virtual后
```c++
construct grandfather
construct father
construct son
destruct son
destruct father
destruct grandfather
```
* 通过将析构函数声明为虚析构函数，可以实现在通过基类指针删除指向派生类对象的指针时，正确调用派生类的析构函数。这样可以确保对象的完全析构，包括派生类中可能存在的资源释放或特定的清理操作
* 如果派生类中有资源需要在析构阶段进行释放（例如动态分配的内存或打开的文件等），将基类的析构函数声明为虚析构函数可以保证在删除基类指针时，正确调用派生类的析构函数，并释放派生类中的资源
* 如果基类的析构函数不声明为虚析构函数，**当通过基类指针删除指向派生类对象的指针时，只会调用基类的析构函数，而不会触发派生类的析构函数**。这可能会导致派生类中的资源无法正确释放，从而导致内存泄漏。通过将析构函数声明为虚析构函数，可以避免此问题，确保派生类的析构函数被正确调用

***多父类***
```c++
class GrandFather {
public:
	GrandFather() {std::cout << "construct grandfather" << std::endl;}
	~GrandFather() {std::cout << "destruct grandfather" << std::endl;}
};

class Father1：public GrandFather{
public:
	Father1() {std::cout << "construct father1" << std::endl;}
	~Father1() {std::cout << "destruct father1" << std::endl;}
};

class Father2：public GrandFather{
public:
	Father2() {std::cout << "construct father2" << std::endl;}
	~Father2() {std::cout << "destruct father2" << std::endl;}
};

class Son：public Father1, Father2{
public:
	Son() {std::cout << "construct son" << std::endl;}
	~Son() {std::cout << "destruct son" << std::endl;}
};

int main() {
	Father *f = new Son();
	delete f;
	return 0;
}
```
输出
* 暂时省略上诉析构问题
```c++
construct grandfather
construct father1
construct grandfather
construct father2
construct son
destruct son
destruct father2
destruct grandfather
destruct father1
destruct grandfather
```
创建一个son会创建两个grandfather，不符合预期，而且还可能会导致程序挂掉。加上virtual，当把father1和father2继承grandfather修改为virtual继承的时候输出
```c++
construct grandfather
construct father1
construct father2
construct son
destruct son
destruct father2
destruct father1
destruct grandfather
```