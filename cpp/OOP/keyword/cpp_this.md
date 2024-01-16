# this 指针
this指针指向被调用的成员函数所属的对象

this指针是隐含每一个非静态成员函数内的一种指针，this指针不需要定义，直接使用

this 的用途
-----------
* 当形参和成员变量同名时，可用this指针来区分
* 在类的非静态成员函数中返回对象本身，可使用return *this
```c++
#include<iostream>
using namespace std;
 
class Person {
public:
	Person(int age){
		//1、当形参和成员变量同名时，可用this指针来区分
		this->age = age;
	}
 
	Person& PersonAddPerson(Person p){
		this->age += p.age;
		//返回对象本身
		return *this;
	}
	int age;
};
 
int main() {
	Person p1(10);
	cout << "p1.age = " << p1.age << endl;
 
	Person p2(20);
	p2.PersonAddPerson(p1).PersonAddPerson(p1);	//20+10+10=40 
	cout << "p2.age = " << p2.age << endl;
	return 0;
}
```

this 指针的本质--指针常量
-------------------------
this指针的本质是一个指针常量：const Type* const pointer; 

他储存了调用他的对象的地址，并且不可被修改。这样成员函数才知道自己修改的成员变量是哪个对象的

this 指针的特点
---------------
* 只能在成员函数中使用，在全局函数、静态成员函数中都不能使用 this 。（this始终指向当前对象，静态成员函数属于类）
* this 指针是在成员函数的开始前构造，并在成员函数的结束后清除 。（和函数的其他参数生命周期一样）
* this 指针会因编译器不同而有不同的存储位置，可能是栈、寄存器或全局变量 。（编译器在生成程序时加入了获取对象首地址的相关代码并把获取的首地址存放在了寄存器中）