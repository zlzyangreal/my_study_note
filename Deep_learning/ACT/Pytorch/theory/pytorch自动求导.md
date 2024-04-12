# 2.2 自动求导

PyTorch 中，所有神经网络的核心是 `autograd `包。autograd包为张量上的所有操作提供了自动求导机制。它是一个在运行时定义 ( define-by-run ）的框架，这意味着反向传播是根据代码如何运行来决定的，并且每次迭代可以是不同的。
## [Autograd简介](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html#sphx-glr-beginner-blitz-autograd-tutorial-py)
## 2.2.1 梯度

现在开始进行反向传播，因为` out` 是一个标量，因此` out.backward() `和` out.backward(torch.tensor(1.))` 等价。

```python
out.backward()
```

输出导数` d(out)/dx`

```python
print(x.grad)
```
```python
tensor([[3., 3.],
        [3., 3.]])
```
![[梯度.png]]
**注意：grad在反向传播过程中是累加的(accumulated)，这意味着每一次运行反向传播，梯度都会累加之前的梯度，所以一般在反向传播之前需把梯度清零**

```python
# 再来反向传播⼀一次，注意grad是累加的
out2 = x.sum()
out2.backward()
print(x.grad)

out3 = x.sum()
x.grad.data.zero_()
out3.backward()
print(x.grad)
```
```python
tensor([[4., 4.],
        [4., 4.]])
tensor([[1., 1.],
        [1., 1.]])
```
现在我们来看一个雅可比向量积的例子：

```python
x = torch.randn(3, requires_grad=True)
print(x)

y = x * 2
i = 0
while y.data.norm() < 1000:
    y = y * 2
    i = i + 1
print(y)
print(i)
```
```python
tensor([-0.9332,  1.9616,  0.1739], requires_grad=True)
tensor([-477.7843, 1004.3264,   89.0424], grad_fn=<MulBackward0>)
8
```

在这种情况下，`y `不再是标量。`torch.autograd` 不能直接计算完整的雅可比矩阵，但是如果我们只想要雅可比向量积，只需将这个向量作为参数传给 `backward：`

```python
v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)
y.backward(v)

print(x.grad)
```
```python
tensor([5.1200e+01, 5.1200e+02, 5.1200e-02])
```

也可以通过将代码块包装在` with torch.no_grad():` 中，来阻止 autograd 跟踪设置了` .requires_grad=True `的张量的历史记录。

```python
print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
    print((x ** 2).requires_grad)
```
```python
True
True
False
```

如果我们想要修改 tensor 的数值，但是又不希望被 autograd 记录(即不会影响反向传播)， 那么我们可以对 tensor.data 进行操作。

```python
x = torch.ones(1,requires_grad=True)

print(x.data) # 还是一个tensor
print(x.data.requires_grad) # 但是已经是独立于计算图之外

y = 2 * x
x.data *= 100 # 只改变了值，不会记录在计算图，所以不会影响梯度传播

y.backward()
print(x) # 更改data的值也会影响tensor的值 
print(x.grad)
```
```python
tensor([1.])
False
tensor([100.], requires_grad=True)
tensor([2.])
```