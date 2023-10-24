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

懒汉模式
--------
饿汉式的单例用法是线程安全的，不需要考虑线程同步，懒汉式的情况就不一样了。

懒汉式单例模式是在第一次调用getInstance()的时候，才创建实例对象。我们可以直接把对象定义为static，然后放在getInstance()中。第一次进入该函数，就创建实例对象，然后一直到程序结束

```c++
class Singleton
{
  private:
	Singleton(){ cout << "单例对象创建！" << endl; };	//构造函数
	Singleton(const Singleton &);					   //拷贝构造
	Singleton& operator=(const Singleton &);		   //拷贝赋值
	~Singleton(){ cout << "单例对象销毁！" << endl; };  //析构函数
 
  public:
	static Singleton * getInstance()
	{	
		static Singleton instance;		//第一次用到时才创建对象
		return instance;
	}
};
```
***对象在堆上***
```c++
class Singleton
{
  private:
    static Singleton *instance;						//单例对象(指向对象的指针)
												
	Singleton(){ cout << "单例对象创建！" << endl; };
	Singleton(const Singleton &);
	Singleton& operator=(const Singleton &);
	~Singleton(){ cout << "单例对象销毁！" << endl; };
 
  public:
	static Singleton * getInstance()
	{	
		if (nullptr == instance)					//判断单例对象是否为空(判断是否存在)，这里是创建对象
		{
			instance = new Singleton();
		}
		return instance;
	}

private:
	// 定义一个内部类
	class Nested{
	public:
		Nested(){};
		~Nested()
		{   	
		    // 定义一个内部类的静态对象
	        // 当该对象销毁时，顺带就释放instance指向的堆区资源
			if (nullptr != instance)
			{
				delete instance;
				instance = nullptr;
			}
		}
	};

	static Nested foo;//在用户程序中需要使用该object(对象)才会触发创建
};
```
**构造这个内部类就是为了当该对象销毁时，顺带就释放instance指向的堆区资源，防止内存泄漏**

***线程安全***
上面这种设计方式在单线程环境下是安全的，但是如果是多线程会在if (nullptr == instance)处，由于线程多个线程可能都得到instance==nullptr,就会创建多个对象，明显不符合要求，为了做到线程安全，需要做双重锁校验DLC
```c++
class Singleton
{
  private:
    static Singleton *instance;
  
	Singleton(){ cout << "单例对象创建！" << endl; };
	Singleton(const Singleton &);
	Singleton& operator=(const Singleton &);
	~Singleton(){ cout << "单例对象销毁！" << endl; };
 
  public:
	static Singleton * getInstance()
	{	
	    lock();//确保线程安全
		if (nullptr == instance)
		{
			instance = new Singleton();
		}
		unlock();
		return instance;
	}

private:
	// 定义一个内部类
	class Nested{
	public:
		Nested(){};
		~Nested()
		{   	
		    // 定义一个内部类的静态对象
	        // 当该对象销毁时，顺带就释放instance指向的堆区资源
	        lock();//编写确保线程安全的函数
			if (nullptr != instance)
			{
				delete instance;
				instance = nullptr;
			}
			unlock();
		}
	};

	static Nested foo;//在用户程序中需要使用该object才会触发创建
};
```
