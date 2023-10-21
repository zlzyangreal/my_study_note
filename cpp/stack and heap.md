# stack and heap基础概念
栈是用来静态分配内存的而堆是动态分配内存的，它们都是存在于计算机内存之中。

栈的分配是在程序编译的时候完成的，直接存储在内存中，接触内存很快。栈是后进先出的顺序，最后被申请的块最先被释放，这样就很容易跟踪到栈，释放栈的过程简单到仅仅是移动下指针就能完成。

堆的分配是在程序运行时完成的，分配速度较为缓慢，但是堆的可用空间非常的大。堆中的元素相互之间没有关联，各自都可以被任何时候随机访问。我们可以任何时候申请和释放一块内存，这样会使得我们很难随时随地追踪到堆中某块位置被分配了还是被释放了。

当你知道在编译前需要分配多少数据时且数据量不是很大时可以使用栈。如果不知道在运行时需要多少数据那么就该使用堆。在多线程的程序里，每个线程都有其自己独立的栈，它们都共享一个堆。

栈是面向线程的而堆是面向进程的。
# stack static and heap
```c++
class Complex{...};
{
  Complex c1(1,2);            //这就是一个stack构造对象
  static Complex c2(1,2);     //构造静态对象
  Complex* p = new Complex(3);//这是heap构造对象
}
```
stack在运行完函数自动销毁

static在运行完函数不会被销毁，运行完整个程序会自动销毁

heap需要手动销毁
# new and delete
c++中构造heap对象
```c++
Complex* pc = new Comple;
```
编译器执行操作：
```c++
void* men = operator new(sizeof(Complex));  //分配内存
pc = static_cast<Complex*>(men);             //转型
pc -> Complex::Complex(1,2);                //构造函数
```
c++的释放内存
```c++
Complex* ps = new Comple;
...
delete ps;
```
编译器操作：
```c++
String::~String(ps);
operator delete(ps);
```
