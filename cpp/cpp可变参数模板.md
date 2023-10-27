# 可变参数模板

```c++
template<typename ...Element> class tuple;
tuple<int, string> a;  // use it like this
```
* 在模板参数 Element 左边出现省略号 ... ，就是表示 Element 是一个模板参数包（template type parameter pack）。parameter pack（参数包）是新引入 C++ 中的概念，比如在这个例子中，Element 表示是一连串任意的参数打成的一个包。比如行中，Element 就是 int, string这个参数的合集。不仅“类型”的模板参数（也就是typename定义的参数）可以这样做，非类型的模板参数也可以这样做
```c++
template<typename T, unsigned PrimaryDimesion, unsigned...Dimesions>
class array { /**/ };
 
array<double, 3, 3> rotation_matrix; //3x3 ratiation matrix
```

例子
-----
```c++
void printf(const char *s)
{
    while (*s) {
        if (*s == '%') {
            if (*(s + 1) == '%') {
                ++s;
            }
            else {
                throw std::runtime_error("invalid format string: missing arguments");
            }
        }
        std::cout << *s++;
    }
}
 
template<typename T, typename... Args>
void printf(const char *s, T value, Args... args)
{
    while (*s) {
        if (*s == '%') {
            if (*(s + 1) == '%') {
                ++s;
            }
            else {
                std::cout << value;
                // call even when *s == 0 to detect extra arguments
                printf(s + 1, args...);
                return;
            }
        }
        std::cout << *s++;
    }
    throw std::logic_error("extra arguments provided to printf");
}
```