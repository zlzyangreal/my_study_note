# 函数类对象

如果一个类将()运算符重载为成员函数，这个类就称为函数对象类，这个类的对象就是函数对象。函数对象是一个对象，但是使用的形式看起来像函数调用，实际上也执行了函数调用，因而得名

例子
----
```c++
#include <iostream>

class Adder {
public:
    int operator()(int a, int b) {
        return a + b;
    }
};

int main() {
    Adder add; // 创建函数类对象

    int result = add(3, 4); // 调用函数类对象

    std::cout << "Result: " << result << std::endl; // 输出：Result: 7

    return 0;
}
```
函数类对象的优点之一是它们可以具有内部状态。因为函数类对象是对象，可以在对象内部存储数据成员，并通过函数调用运算符访问和修改这些成员。这使得函数类对象可以在不同的函数调用之间保持状态，提供更灵活的行为

