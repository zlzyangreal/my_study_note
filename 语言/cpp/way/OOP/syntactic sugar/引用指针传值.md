# 传值调用 function call by value指针调用 function call by pointer引用调用 function call by reference
## 传值调用
向函数传递参数的值，即把参数的值复制给函数的形式参数。
这种情况下，修改函数内的形式参数，并不会影响到函数外的实际参数。

```c++
void swap_by_value(int x，int y)
{ 
    cout << "&x: " << &x < < "，& y:" < < & y < < endl;
    int tmp = x;
    x = y;y = tmp
    cout << "&x: " << &x < < "，& y:" < < & y < < endl;
} 
int main()
{ 
    int a = 3；
    int b = 7；
    cout << "before: a: " << a < < "，b:" < < b < < endl;
    cout << "&a: " << &a < < "，& b:" < < & b < < endl;
    swap_by_value(a，b)；
    cout << "after : a: " << a < < "，b:" < < b < < endl；
    return 0;
}
```

# 运行结果如下所示
由于形参是实参的拷贝，形参和实参的地址是不同的。因此改变形参的值，并不会影响外部实参的值。

```c++
    before:a:3，b: 7
    &a: 0x7ffee6eefa88，&b:0x7ffee6eefa84
    &x: 0x7ffee6eefa4c，&y:0x7ffee6eefa48
    &x: 0x7ffee6eefa4c，&y:0x7ffee6eefa48
    after : a:3,b:7
```

当只在函数内部改变参数，且不希望这个改变影响外部参数时，采用值传递。

## 指针调用
向函数传递参数的指针，即把参数的地址复制给形式参数。
在函数内，该地址用于访问要用到的实际参数，这意味着修改形式参数会影响实际参数。

```c++
#include <iostream> 
using namespace std; 
void swap_by_pointer(int* x，int* y)
{
    cout << "&x: " << x < < "，& y:" < < y < < endl;
    int tmp = * x；* x = * y；* y = tmp;
    cout << "&x: " << x < < "，& y:" < < y < < endl;
} 
int main()
{ 
    int a = 3；
    int b = 7；
    cout << "before: a: " << a < < "，b:" < < b < < endl;
    cout << "&a: " << &a < < "，& b:" < < & b < < endl;
    swap_by_pointer(&a，& b);
    cout << "after : a: " << a < < "，b:" < < b < < endl;
    return 0;
}
```

# 运行结果如下所示
形参为指向实参地址的指针，因此对形参的指向操作，就相当于对实参本身进行操作。

```c++
before: a:3, b: 7
&a: 0x7ffee6eefa88, &b:0x7ffee6eefa84
&x: 0x7ffee6eefa4c, &y:0x7ffee6eefa48
&x: 0x7ffee6eefa88, &y:0x7ffee6eefa84
after : a:7,b:3
```

## 引用调用
向函数传递参数的引用，即把引用的地址复制给形式参数。
在函数内，该引用用于访问要用到的实际参数，这也意味着修改形式参数会影响实际参数。
```c++
#include <iostream> 
using namespace std;
void swap_by_reference(int& x, int& y) 
{ 
    cout << "&x: " << &x << ", &y: " << &y << endl; 
    int tmp = x; x = y; y = tmp; 
    cout << "&x: " << &x << ", &y: " << &y << endl; 
} 
int main() 
{ 
    int a = 3; int b = 7; 
    cout << "before: a: " << a << ", b: " << b << endl; 
    cout << "&a: " << &a << ", &b: " << &b << endl; 
    swap_by_reference(a, b); 
    cout << "after : a: " << a << ", b: " << b << endl; return 0; 
}
```

# 运行结果如下所示
形参相当于是实参的“别名”，两者的地址是相同的，因此对形参的操作其实就是对实参的操作。

```c++
before: a:3, b: 7
&a: 0x7ffee6eefa88, &b:0x7ffee6eefa84
&x: 0x7ffee6eefa88, &y:0x7ffee6eefa84
&x: 0x7ffee6eefa88, &y:0x7ffee6eefa84
after : a:7,b:3
```

