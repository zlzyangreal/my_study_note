# cpp单例模式
饿汉模式
--------
```c++
#include<iostream>
using namespace std;
class Singleton
{
  private:                      
  	static Singleton instance;                          // 单例对象
  	
  private:                        
	Singleton(){ cout << "单例对象创建！" << endl; };    //构造函数
	Singleton(const Singleton &);                       //拷贝函数
	Singleton& operator=(const Singleton &);            //赋值运算符重载
	~Singleton(){ cout << "单例对象销毁！" << endl; };   //析构函数
 
  public:
	static Singleton* getInstance()                     //Singleton*是函数返回类型
	{		
		return &instance;                               //第一次调用时才会调用构建函数
                                                        //返回指针
	}
};

Singleton Singleton::instance;                          //声明全局性对象
int main()
{
	Singleton *ct1 = Singleton::getInstance();
	Singleton *ct2 = Singleton::getInstance();
	Singleton *ct3 = Singleton::getInstance();
 
	return 0;
}
```
```Singleton Singleton::instance;```这一步操作解释如下：
* **单例创建的对象只有一个**
* 在类外部定义并初始化了一个静态成员变量 instance，它是类 Singleton 的一个静态实例对象
* 尽管构造函数是私有的，但是在类的内部，私有成员可以被访问（对于这里是他本来已经在类里面创建了，和这一步无关）
* **静态成员属于类而不属于对象**，所以在类的外部定义和初始化它，即使构造函数是私有的。在这种情况下，类的静态成员变量 instance 在编译时就会被创建，并且只会有一个全局唯一的实例
* **他和类里面构建的是同一个对象**，他存在的意义是为了外部可以对对象进行额外的操作或初始化，否则是未定义的，因为它的定义在类里面


