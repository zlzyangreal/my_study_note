# pytorch 库

## 常用的几种参数总结

### dim参数
dim 这一参数通常指的是维度

详细解释 https://www.cnblogs.com/flix/p/11262606.html

![本地](dim参数.png images/python/python libraries/dim参数.png>)
```python
import torch
a = torch.Tensor([[[1, 2, 3],[7, 8, 9]],
                  [[4, 5, 6],[1, 1, 1]]])
print(a.sum(dim = 0))
print(a.sum(dim = 1))
print(a.sum(dim = 2))
####结果####################
tensor([[ 5.,  7.,  9.],
        [ 8.,  9., 10.]])
tensor([[ 8., 10., 12.],
        [ 5.,  6.,  7.]])
tensor([[ 6., 24.],
        [15.,  3.]])
```
### keepdim参数
保持keepdim的维度
```python
import torch
a = torch.Tensor([[1, 2, 3],[7, 8, 9],
                  [4, 5, 6],[1, 1, 1]])
print(a.sum(dim = 0, keepdim = True))
print(a.sum(dim = 0))
###结果#######################
tensor([[13., 16., 19.]])
tensor([13., 16., 19.])
```
## 函数

### torch.cat和torch.chunk

####  torch.cat
torch.cat是将两个张量（tensor）拼接在一起，cat是concatnate的意思，即拼接，联系在一起
```python
#用法
outputs = torch.cat(inputs, dim=?) → Tensor

C = torch.cat( (A,B),0 )  #按维数0拼接（竖着拼）
C = torch.cat( (A,B),1 )  #按维数1拼接（横着拼）
```
具体例子
```python
>>> import torch
>>> A=torch.ones(2,3) #2x3的张量（矩阵）                                     
>>> A
tensor([[ 1.,  1.,  1.],
        [ 1.,  1.,  1.]])
>>> B=2*torch.ones(4,3)#4x3的张量（矩阵）                                    
>>> B
tensor([[ 2.,  2.,  2.],
        [ 2.,  2.,  2.],
        [ 2.,  2.,  2.],
        [ 2.,  2.,  2.]])
>>> C=torch.cat((A,B),0)#按维数0（行）拼接
>>> C
tensor([[ 1.,  1.,  1.],
         [ 1.,  1.,  1.],
         [ 2.,  2.,  2.],
         [ 2.,  2.,  2.],
         [ 2.,  2.,  2.],
         [ 2.,  2.,  2.]])
>>> C.size()
torch.Size([6, 3])
>>> D=2*torch.ones(2,4) #2x4的张量（矩阵）
>>> C=torch.cat((A,D),1)#按维数1（列）拼接
>>> C
tensor([[ 1.,  1.,  1.,  2.,  2.,  2.,  2.],
        [ 1.,  1.,  1.,  2.,  2.,  2.,  2.]])
>>> C.size()
torch.Size([2, 7])
```
#### torch.chunk
torch.chunk(tensor, chunk_num, dim)与torch.cat()原理相反，它是将tensor按dim（行或列）分割成chunk_num个tensor块，返回的是一个元组
```python
c = torch.tensor([[1., 2., 4.],
        [4., 5., 7.],
        [3., 9., 8.],
        [9., 6., 7.]])
 #在dim=1这一个维度进行拆分， chunk_num是拆分的块数，当其大于等于dim=1中元
 #素的个数n, 则拆成n块，小于则平分。
 torch.chunk(c,4,dim = 1)
 #结果：
 (tensor([[1.],
         [4.],
         [3.],
         [9.]]),
 tensor([[2.],
         [5.],
         [9.],
         [6.]]),
 tensor([[4.],
         [7.],
         [8.],
         [7.]]))
torch.chunk(c,3,dim = 1)
#结果：
(tensor([[1.],
         [4.],
         [3.],
         [9.]]),
 tensor([[2.],
         [5.],
         [9.],
         [6.]]),
 tensor([[4.],
         [7.],
         [8.],
         [7.]]))
torch.chunk(c,2,dim = 1)
#结果：
(tensor([[1., 2.],
         [4., 5.],
         [3., 9.],
         [9., 6.]]),
 tensor([[4.],
         [7.],
         [8.],
         [7.]])) 
```
### squeeze和unsequeeze
torch.squeeze() 这个函数主要对数据的维度进行压缩，去掉维数为1的的维度，比如是一行或者一列这种，一个一行三列（1,3）的数去掉第一个维数为一的维度之后就变成（3）行。squeeze(a)就是将a中所有为1的维度删掉。不为1的维度没有影响。a.squeeze(N) 就是去掉a中指定的维数为一的维度。还有一种形式就是b=torch.squeeze(a，N) a中去掉指定的定的维数为一的维度。

torch.unsqueeze()这个函数主要是对数据维度进行扩充。给指定位置加上维数为一的维度，比如原本有个三行的数据（3），在0的位置加了一维就变成一行三列（1,3）。a.squeeze(N) 就是在a中指定位置N加上一个维数为1的维度。还有一种形式就是b=torch.squeeze(a，N) a就是在a中指定位置N加上一个维数为1的维度

#### squeeze
```python
c = torch.tensor([[[1., 2., 4.],
        [4., 5., 7.],
        [3., 9., 8.],
        [9., 6., 7.]]])
c.shape
#torch.Size([1, 4, 3])
b = c.squeeze(0)
print(b, b.shape)
tensor([[1., 2., 4.],
        [4., 5., 7.],
        [3., 9., 8.],
        [9., 6., 7.]]) torch.Size([4, 3])
```
#### unsqueeze
```python
c = torch.tensor([[1., 2., 4.],
        [4., 5., 7.],
        [3., 9., 8.],
        [9., 6., 7.]])
c.shape
#torch.Size([4, 3])
b = c.unsqueeze(1)
print(b, b.shape)
tensor([[[1., 2., 4.]],

        [[4., 5., 7.]],

        [[3., 9., 8.]],

        [[9., 6., 7.]]]) torch.Size([4, 1, 3])
```

## 数据处理
### TensorDataset
TensorDataset将简单的数据进行绑定，使其相对应的数据何以同时获取
```python
from torch.utils.data import TensorDataset
import torch
from torch.utils.data import DataLoader
 
a = torch.tensor([[11, 22, 33], [44, 55, 66], [77, 88, 99], [11, 22, 33], [44, 55, 66], [77, 88, 99], [11, 22, 33], [44, 55, 66], [77, 88, 99], [11, 22, 33], [44, 55, 66], [77, 88, 99]])
b = torch.tensor([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
train_ids = TensorDataset(a, b)

train_loader = DataLoader(dataset=train_ids, batch_size=4, shuffle=True)
for i, data in enumerate(train_loader, 1):  
# 注意enumerate返回值有两个,一个是序号，一个是数据（包含训练数据和标签）
    x_data, label = data
    print(' batch:{0} x_data:{1}  label: {2}'.format(i, x_data, label)) 
```
* 代码导入了TensorDataset类，它是PyTorch中用于处理张量数据的数据集类
* 导入了DataLoader类，它是PyTorch中用于加载数据的工具类
* 创建了一个张量a，其中包含了12个样本，每个样本有3个特征
* `train_ids = TensorDataset(a, b)`: 这行代码使用TensorDataset类将特征张量a和标签张量b组合成一个数据集train_ids
* `train_loader = DataLoader(dataset=train_ids, batch_size=4, shuffle=True)`: 这行代码创建了一个数据加载器train_loader，它使用数据集train_ids作为输入，每个批次包含4个样本，并且在每个迭代中对数据进行洗牌（shuffle）

![本地](TensorDataset运行结果.png images/python/python libraries/TensorDataset运行结果.png>)

### Datase
Dataset主要用于自定义类型，实现不同的复杂类型，其核心点在两个基础的函数
```python
__len__：一般用来返回数据集大小。
__getitem__：实现这个方法后，可以通过下标的方式 dataset[i] 的来取得第 i 个数据。
```
使用方法
```python
#创建子类
class subDataset(Dataset.Dataset):
    #初始化，定义数据内容和标签
    def __init__(self, Data, Label):
        self.Data = Data
        self.Label = Label
    #返回数据集大小
    def __len__(self):
        return len(self.Data)
    #得到数据内容和标签
    def __getitem__(self, index):
        data = torch.Tensor(self.Data[index])
        label = torch.Tensor(self.Label[index])
        return data, label
```
### DataLoader
对来自Dataset的数据进行shuffle和batch等操作
```python
loader = Data.DataLoader(
    dataset=torch_dataset,      # torch TensorDataset format
    batch_size=BATCH_SIZE,      # mini batch size
    shuffle=True,               # 要不要打乱数据 (打乱比较好)
    num_workers=2,              # 多线程来读数据
)
for step, (batch_x, batch_y) in enumerate(loader):
	print(batch_x, batch_y)
```
### 单独shuffle
当我们处理完的数据，需要进行shuffle时，不能采用上述操作DataLoader进行shuffle时，我们可以采用其他的方法进行shuffle，采用random类中的shuffle函数数据进行shuffle
```python
import torch
from random import shuffle
a = torch.Tensor([1, 2, 3, 4, 5, 6, 7, 8, 9])
print("原始数据:", a)
index = [i for i in range(a.shape[0])]
shuffle(index)
print(index)
print("shuffle之后的数据：",a[index])
```
![本地](单独shuffle运行结果.png images/python/python libraries/单独shuffle运行结果.png>)