
[知乎原文：含原理](https://zhuanlan.zhihu.com/p/178402798)
[tensorflow多卡方式](单机多卡训练：%20MirroredStrategy.md MirroredStrategy>)
[[DDP进一步加速]]
DistributedDataParallel（DDP）是一个支持多机多卡、[[DDP分布式]]训练的深度学习工程方法

***依赖***：PyThorch>=1.5 , python>=3.6 
## 在Pytorch上使用DDP
不需要修改网络的配置
```python
model = DDP(model, device_ids=[local_rank], output_device=local_rank)
```
* 原本的model就是PyTorch模型，新得到的model，就是DDP模型
### eg
```python
## main.py文件
import torch
import argparse

# 新增1:依赖
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# 新增2：从外面得到local_rank参数，在调用DDP的时候，其会自动给出这个参数，
# argparse是python的一个系统库，用来处理命令行调用
parser = argparse.ArgumentParser()
parser.add_argument("--local_rank", default=-1)
FLAGS = parser.parse_args()
local_rank = FLAGS.local_rank 

# 新增3：DDP backend初始化
# a.根据local_rank来设定当前使用哪块GPU
torch.cuda.set_device(local_rank)
# b.初始化DDP，使用默认backend(nccl)就行。如果是CPU模型运行，需要选择其他后端。
dist.init_process_group(backend='nccl')

# 新增4：定义并把模型放置到单独的GPU上，需要在调用`model=DDP(model)`前做
device = torch.device("cuda", local_rank)
# 替换为其他模型
# model = MyCustomModel().to(device)
model = nn.Linear(10, 10).to(device)
# ！！如果要加载(从磁盘上的文件中读取已保存的模型参数，并将这些参数应用到你定义的模型中)模型，也必须在这里做！！
# 可能的load模型...

# 新增5：之后才是初始化DDP模型
model = DDP(model, device_ids=[local_rank], output_device=local_rank)
```
### [[前向和后向传播]]
**数据并行处理，DDP已经做好了**
```python
my_trainset = torchvision.datasets.CIFAR10(root='./data', train=True)
# 新增1：使用DistributedSampler，DDP帮我们把细节都封装起来了。用，就完事儿！
train_sampler = torch.utils.data.distributed.DistributedSampler(my_trainset)
# 需要注意的是，这里的batch_size指的是每个进程下的batch_size。也就是说，总batch_size是这里的batch_size再乘以并行数(world_size)。
trainloader = torch.utils.data.DataLoader(my_trainset, batch_size=batch_size, sampler=train_sampler)

for epoch in range(num_epochs):
    # 新增2：设置sampler的epoch，DistributedSampler需要这个来维持各个进程之间的相同随机数种子
    trainloader.sampler.set_epoch(epoch)
    # 后面这部分，则与原来完全一致了。
    for data, label in trainloader:
        prediction = model(data)
        loss = loss_fn(prediction, label)
        loss.backward()
        optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)
        optimizer.step()
```
### 其他需要注意的地方

**保存参数**
```python
# 1. save模型的时候，和DP模式一样，有一个需要注意的点：保存的是model.module而不是model。
#    因为model其实是DDP model，参数是被`model=DDP(model)`包起来的。
# 2. 我只需要在进程0上保存一次就行了，避免多次保存重复的东西。
if dist.get_rank() == 0:
    torch.save(model.module, "saved_model.ckpt")
```

- 理论上，在没有buffer参数（如BN）的情况下，DDP性能和单卡Gradient Accumulation性能是完全一致的。

> [!NOTE] buffer参数（如BN）
> "Batch Normalization"，即批归一化。它是一种用于加速神经网络训练并提高模型性能的技术

- 并行度为8的DDP 等于 Gradient Accumulation Step为8的单卡

> [!NOTE] Gradient Accumulation（梯度累积）
> Gradient Accumulation（梯度累积）是一种训练神经网络时使用的技术，它允许在更新模型参数之前累积多个小批量（mini-batches）的梯度

- 速度上，DDP当然比Graident Accumulation的单卡快；
- 但是还有[加速空间](DDP进一步加速.md)
- 如果要对齐性能，需要确保喂进去的数据，在DDP下和在单卡Gradient Accumulation下是一致的。
- 对于复杂模型，可能是相当困难的。
### 示例 （数据并行 > DDP）

```python

def setup(rank, world_size):  

    # 初始化进程组  

    dist.init_process_group("nccl", init_method="tcp://localhost:23456", rank=rank, world_size=2)  

def cleanup():  

    # 清理进程组  

    dist.destroy_process_group()  

def train(rank, world_size, optimizers, train_dataset, epochs):  

    setup(rank, world_size)  

    device = torch.device(f'cuda:{rank}' if torch.cuda.is_available() else 'cpu')  # 开启多进程，选择rank  

    kwargs = {'num_workers': 4, 'pin_memory': True} if use_cuda else {}  

    train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)  #train_dataset 加载到train_sampler上  

    train_loader = torch.utils.data.DataLoader(train_dataset,  

                                               batch_size=1,  

                                               shuffle=False, **kwargs,  

                                               sampler=train_sampler)   #train_sampler 加载到train_loader上  

    STN = stn_net(pretrained=False).to(device)  #模型加载到rank中  

    STN_optimizer = optim.SGD(STN.parameters(), lr=args.lr, momentum=args.momentum) #STN_optimizer 参数设定  

    STN = parallel.DistributedDataParallel(STN, broadcast_buffers=False, find_unused_parameters=True) # 模型加载到DDP上  

    STN.train()  

    for epoch in range(1, epochs + 1):  

        train_sampler.set_epoch(epoch)  

          #########  

            # 前向传播，使用.to(rank)将中间变量加载到对应rank上  

          #########  

    cleanup() # 清理进程组  

def main():  

    world_size = 2  

    ####################  

    # 参数 加载，如args  

    ###################  

    # train_dataset 加载  

    mp.spawn(train,  

             args=(world_size, optimizers, train_dataset, args.epochs),  

             nprocs=world_size)  # 回调train  传递 train 参数  

if __name__ == '__main__':  

    main()

```
### DP 与 DDP 的优缺点

#### DP 的优势

`nn.DataParallel`没有改变模型的输入输出，因此其他部分的代码不需要做任何更改，非常方便，一行代码即可搞定。

#### DP 的缺点

`DP`进行分布式多卡训练的方式容易造成负载不均衡，第一块GPU显存占用更多，因为输出默认都会被gather到第一块GPU上，也就是后续的loss计算只会在`cuda:0`上进行，没法并行。

除此之外`DP`只能在单机上使用，且`DP`是单进程多线程的实现方式，比`DDP`多进程多线程的方式会效率低一些。

#### DDP的优势

**1. 每个进程对应一个独立的训练过程，且只对梯度等少量数据进行信息交换。**

**`DDP`** 在每次迭代中，每个进程具有自己的 `optimizer` ，并独立完成所有的优化步骤，进程内与一般的训练无异。

在各进程梯度计算完成之后，各进程需要将**梯度**进行汇总平均，然后再由 `rank=0` 的进程，将其 `broadcast` 到所有进程。之后，各进程用该梯度来独立的更新参数。而 `DP`是**梯度汇总到主** `GPU`，**反向传播更新参数**，再广播参数给其他的 GPU。

**`DDP`** 中由于各进程中的模型，初始参数一致 (初始时刻进行一次 `broadcast`)，而每次用于更新参数的梯度也一致，因此，各进程的模型参数始终保持一致。

而在`DP` 中，全程维护一个 `optimizer`，对各 `GPU` 上梯度进行求和，而在主 `GPU` 进行参数更新，之后再将模型参数 `broadcast` 到其他 `GPU`。

相较于**`DP`**，**`DDP`**传输的数据量更少，因此速度更快，效率更高。

**2. 每个进程包含独立的解释器和 GIL。**

一般使用的 `Python` 解释器 `CPython`：是用 `C` 语言实现 `Pyhon`，是目前应用最广泛的解释器。全局锁使 `Python` 在多线程效能上表现不佳，全局解释器锁（`Global Interpreter Lock`）是 `Python` 用于同步线程的工具，使得任何时刻仅有一个线程在执行。

由于每个进程拥有独立的解释器和 `GIL`，消除了来自单个 `Python` 进程中的多个执行线程，模型副本或 `GPU` 的额外解释器开销和 `GIL-thrashing` ，因此可以减少解释器和 `GIL` 使用冲突。这对于严重依赖 `Python runtime` 的 `models` 而言，比如说包含 `RNN` 层或大量小组件的 `models` 而言，这尤为重要。

#### DDP 的缺点

暂时来说，`DDP`是采用多进程多线程的方式，并且训练速度较高，他的缺点主要就是，需要修改比较多的代码，比`DP`的一行代码较为繁琐许多。