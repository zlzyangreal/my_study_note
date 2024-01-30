# 类模板
c++类模板写法
------------
```c++
template <类型参数表>
class 类模板名{
    成员函数和成员变量
};
```
***类型参数表***
```c++
class类塑参数1, class类型参数2, ...
```
***类模板中的成员函数放到类模板定义外面写时的语法***
```c++
template <类型参数表>
返回值类型  类模板名<类型参数名列表>::成员函数名(参数表)
{
    ...
}
```
***类模板定义对象的写法***
```c++
类模板名<真实类型参数表> 对象名(构造函数实际参数表);
```
***类模板有无参构造函数写法***
```c++
类模板名 <真实类型参数表> 对象名;
```

类模板例子
---------
```c++
#include <iostream>
#include <string>
using namespace std;
template <class T1,class T2>
class Pair
{
public:
    T1 key;                             //关键字
    T2 value;                           //值
    Pair(T1 k,T2 v):key(k),value(v) {}; //这里使用了快速赋值的用法
    bool operator < (const Pair<T1,T2> & p) const;
};
template<class T1,class T2>
bool Pair<T1,T2>::operator < (const Pair<T1,T2> & p) const
//Pair的成员函数 operator <
{ 
    //"小"的意思就是关键字小
    return key < p.key;
}
int main()
{
    Pair<string,int> student("Tom",19); //实例化出一个类 Pair<string,int>
    cout << student.key << " " << student.value;
    return 0;
}
```
```bool operator < (const Pair<T1,T2> & p) const;```解释：
* 传入参数```const```表示传入值不可修改，类模板需要加上模板参数```<T1,T2>```
* 函数最后的```const```表示函数不修改对象变量
* 若表示返回值不修改应该```const bool ···```
***函数模板作为类模板成员***
```c++
#include <iostream>
using namespace std;
template <class T>
class A
{
public:
    template <class T2>
    void Func(T2 t) { cout << t; }  //成员函数模板
};
int main()
{
    A<int> a;
    a.Func('K');  //成员函数模板Func被实例化，注意这里是const char*
    a.Func("hello");
    return 0;
}
```
c++函数模板写法
--------------
```c++
template <class 类型参数1, class类型参数2, ...>
返回值类型  模板名(形参表)
{
    函数体
}
```
***class 关键字也可以用 typename 关键字替换***
```c++
template <typename 类型参数1, typename 类型参数2, ...>
```

函数模板例子
-----------
```c++
#include <iostream>
using namespace std;
template<class T>
void Swap(T & x, T & y)
{
    T tmp = x;
    x = y;
    y = tmp;
}
int main()
{
    int n = 1, m = 2;
    Swap(n, m);  //编译器自动生成 void Swap (int &, int &)函数
    double f = 1.2, g = 2.3;
    Swap(f, g);  //编译器自动生成 void Swap (double &, double &)函数
    return 0;
}
```
* ```T```类型参数，可以使用任何类型
***[实例]一个求数组中最大元素的函数模板***
```c++
#include <iostream>
using namespace std;
template <class T>
T MaxElement(T a[], int size) //size是数组元素个数
{
    T tmpMax = a[0];
    for (int i = 1; i < size; ++i)
        if (tmpMax < a[i])
            tmpMax = a[i];
    return tmpMax;
}
class CFraction //分数类
{
    int numerator;   //分子
    int denominator; //分母
public:
    CFraction(int n, int d) :numerator(n), denominator(d) { };
    bool operator <(const CFraction & f) const
    {//为避免除法产生的浮点误差，用乘法判断两个分数的大小关系
        if (denominator * f.denominator > 0)
            return numerator * f.denominator < denominator * f.numerator;
        else
            return numerator * f.denominator > denominator * f.numerator;
    }
    bool operator == (const CFraction & f) const
    {//为避免除法产生的浮点误差，用乘法判断两个分数是否相等
        return numerator * f.denominator == denominator * f.numerator;
    }
    friend ostream & operator <<(ostream & o, const CFraction & f);
};
ostream & operator <<(ostream & o, const CFraction & f)
{//重载 << 使得分数对象可以通过cout输出
    o << f.numerator << "/" << f.denominator; //输出"分子/分母" 形式
    return o;
}
int main()
{
    int a[5] = { 1,5,2,3,4 };
    CFraction f[4] = { CFraction(8,6),CFraction(-8,4),
        CFraction(3,2), CFraction(5,6) };
    cout << MaxElement(a, 5) << endl;
    cout << MaxElement(f, 4) << endl;
    return 0;
}
```