# 类型转换运算符
```c++
operator type() const;
```
* operator  关键字用于声明运算符函数
* type      目标类型，指定要将自定义类型转换为的类型
* const     表示运算符函数是一个常量成员函数

通过在类中定义这样的类型转换运算符，可以让对象在特定上下文中自动转换为目标类型。这种转换是隐式的，不需要显式调用类型转换函数

例子
---
```c++
class MyInt {
private:
    int value;
public:
    MyInt(int val) : value(val) {}

    operator int() const {
        return value;
    }
};

int main() {
    MyInt myNum(42);
    int num = myNum; // 隐式转换为int类型

    cout << "num: " << num << endl;

    return 0;
}
```