# 移动构造

在 C++ 11 标准之前（C++ 98/03 标准中），如果想用其它对象初始化一个同类的新对象，只能借助类中的复制（拷贝）构造函数

例子：
```c++
#include <iostream>
using namespace std;

class demo{
public:
   demo():num(new int(0)){
      cout<<"construct!"<<endl;
   }
   //拷贝构造函数
   demo(const demo &d):num(new int(*d.num)){
      cout<<"copy construct!"<<endl;
   }
   ~demo(){
      cout<<"class destruct!"<<endl;
   }
private:
   int *num;
};

demo get_demo(){
    return demo();
}

int main(){
    demo a = get_demo();
    return 0;
}
```
结果会因为编译器而异，多数编译器会优化如VS 2017、codeblocks 等这些编译器运行此程序时，看到的往往是优化后的输出结果：
~~~
construct!
class destruct!
~~~
但在Linux上使用g++ [文件]-fno-elide-constructors运行可看到完整输出结果
~~~
construct!                  <-- 这是在创建匿名的demo对象时输出的，表示对象的构造。这发生在get_demo函数内部，因为它返回一个匿名对象
copy construct!             <-- 执行 return demo()
class destruct!             <-- 销毁 demo() 产生的匿名对象，在get_demo函数内部产生的对象
copy construct!             <-- 执行 a = get_demo()
class destruct!             <-- 销毁 get_demo() 返回的临时对象
class destruct!             <-- 销毁 a
~~~
所谓移动语义，指的就是以移动而非深拷贝的方式初始化含有指针成员的类对象。简单的理解，移动语义指的就是将其他对象（通常是临时对象）拥有的内存资源“移为已用”
```c++
#include <iostream>
using namespace std;
class demo{
public:
    demo():num(new int(0)){
        cout<<"construct!"<<endl;
    }

    demo(const demo &d):num(new int(*d.num)){
        cout<<"copy construct!"<<endl;
    }
    //添加移动构造函数
    demo(demo &&d):num(d.num){
        d.num = NULL;
        cout<<"move construct!"<<endl;
    }
    ~demo(){
        cout<<"class destruct!"<<endl;
    }
private:
    int *num;
};
demo get_demo(){
    return demo();
}
int main(){
    demo a = get_demo();
    return 0;
}
```
结果：
~~~
construct!
move construct!
class destruct!
move construct!
class destruct!
class destruct!
~~~
* 减少资源的拷贝：添加移动构造函数可以避免不必要的资源拷贝操作。在原始代码中，返回匿名对象时会触发拷贝构造函数，进行深拷贝操作。而在优化后的代码中，添加了移动构造函数，当返回匿名对象时可以通过移动语义将资源所有权转移给目标对象，避免了不必要的拷贝，提高了效率
* 更高效的对象构造：在原始代码中，返回匿名对象时会进行拷贝构造函数的调用，其中包括在堆上分配新的内存和复制数据的操作。而在优化后的代码中，通过移动构造函数，可以**直接将资源指针转移给目标对象**，避免了分配新内存和数据复制的开销，提高了对象构造的效率