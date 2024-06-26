# 类的框架模板、内联函数、构造函数

## 类的框架
* 以复数为例
```cpp
class complex {
public:
    complex (double r = 0, double i = 0) : re (r), im (i)
    {}
    complex& oprator += (const complex&);
    double real () const { return re; }
    double imag () const { return im; }
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&)
}
```
* `real ()` `imag ()`直接在类里定义了
* `complex& oprator += (const complex&);`只是一句声明

## inline函数
* 函数在类本体里定义就形成了inline函数,`real ()` `imag ()`
* 取决于编译器,只能做建议,具体取决于编译器

## 构造函数
```c
/////////////////////////////////////////////////////
complex (double r = 0, double i = 0) : re (r), im (i)
    {}
/////////////////////////////////////////////////////
int main {
    complex c1 (2,1);
    complex c2;
    complex* p = new complex(4);
    return 0;
}
```
* 构造函数与类名字相同
* 参数具备默认值 `double r = 0, double i = 0`
* `complex (double r = 0, double i = 0) : re (r), im (i)` (只有构造函数才有这个复制方法，初始化动作)
* `c1`创建对象，实部为2，虚部为1
* `c2`创建对象(使用默认值)
* `c3`动态创建指针

构造函数可以有很多个(overloading重载)，函数也可以重载
```cpp
//////////////////////////////////////////////////////
double real () const { return re; }

void real (double r) { re = r; }
//////////////////////////////////////////////////////
complex (double r = 0, double i =0) :re (r), im (i)
{}

complex () : re(0) , im(0) {}
//////////////////////////////////////////////////////
```
* 因为在编译器角度，函数是不同的，所以可以存在同名
* 这两给构造函数不可以同时存在，因为作用冲突了