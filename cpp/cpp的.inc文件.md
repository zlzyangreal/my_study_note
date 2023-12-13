# .inc文件

.h与.inc的区别
--------------
C/C++的标准惯例是将class、function的声明信息写在.h文件中。.c文件写class现、function实现、变量定义等等。

然而对于template来说，它既不是class也不是function，而是可以生成一组class或function的东西。编译器（compiler）为了给template生成代码，
他需要看到声明（declaration ）和定义（definition ），因此他们必须不被包含在.h里面。

为了使声明、定义分隔开，定义写在自己文件内部，即.inc文件，然后在.h文件的末尾包含进来。当然除了.inc的形式，还可能有许多其他的写法.inc, .imp, .impl, .tpp, etc.
在编译器预处理阶段会将 .h，.inc 文件内容合并到 .i 文件中，虽然我们在写代码时将模板代码分开了，但是在编译器预处理阶段又被合并，所以这是合理的.
