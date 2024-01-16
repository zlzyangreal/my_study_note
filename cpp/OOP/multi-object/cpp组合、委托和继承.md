# 组合、委托和继承

Composition 组合
----------------
当一个类中包含另外一个类对象时，可称为复合，表现为has-a关系
```c++
template <class T, class Sequence = deque<T>>
class queue {
...
protected:
    Sequence c; //底层容器
public:
    bool empty() const {return c.empty();}
    size_type size() const {return c.size();}
    reference front() {return c.front();}
    reference back() {return c.back();}
    // deque是两端可进出，queue是末端进前端出（先进先出）
    void push(const value_type& x) {c.push_back(x);}
    void pop() {c.pop_front();}
};
```
* 由于queue的所有功能都由deque实现，即queue为deque的Adapter（适配器模式）
https://www.fa1c0n.cn/p/c-%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E9%AB%98%E7%BA%A7%E5%BC%80%E5%8F%91-%E7%BB%A7%E6%89%BF%E5%A4%8D%E5%90%88%E5%A7%94%E6%89%98%E4%B8%8E%E7%BB%84%E5%90%88%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/