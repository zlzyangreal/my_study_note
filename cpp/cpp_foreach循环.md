# foreach循环

C++中数组的foreach循环示例
-------------------------
```c++
#include<iostream>
using namespace std; 
int main() 
{ 
    int arr[]={1,2,3,4,5};   //array initialization
    cout<<"The elements are: ";
    for(int i : arr)
    {
    	cout<<i<<" ";
    }
    return 0;
}
```
输出``The elements are: 1 2 3 4 5``
* 数组 arr[] 初始化为一些值 {1 , 2 , 3 , 4 , 5}
* 在循环结构中，'i'是存储当前数组元素值的变量
* arr 是数组名，也是相应数组的基址
* 每次迭代打印“i”为我们提供了相应的数组元素，这与正常 for 循环情况下的数组索引形成对比

**在声明变量“i”时，也可以使用 auto 数据类型而不是 int**。这样可以保证变量的类型是从数组类型推导出来的，不会发生数据类型冲突

```c++
#include<iostream>
using namespace std; 
int main() 
{ 
    int array[]={1,4,7,4,8,4};
    cout<<"The elements are: ";
    for(auto var : array)
    {
    	cout<<var<<" ";
    }
    return 0;
}
```

C++ 中 Vector 的 foreach 循环示例
--------------------------------
```c++
#include<iostream>
#include<vector>
using namespace std; 
int main() 
{ 
    vector<int> vec={11,22,33,44,55,66};
    cout<<"The elements are: ";
    for(auto var : vec)
    {
    	cout<<var<<" ";
	}
    return 0;
}
```
输出    vector 的 for-each 循环的工作方式与数组相同。此外，唯一的区别是向量声明、初始化和可以对其执行的不同操作

C++中foreach循环的优缺点
-----------------------
***优点***
* 消除了出错的可能性并使代码更具可读性
* 易于实施
* 不需要迭代器的预初始化

***缺点***
* 不能直接访问对应的元素索引
* 不能逆序遍历元素
* 不允许用户在遍历每个元素时跳过任何元素