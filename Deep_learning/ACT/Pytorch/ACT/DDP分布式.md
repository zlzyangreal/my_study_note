# group

进程组，默认情况下只有一个组
# world size

全局并行数 ***（eg:例如16张显卡，world size为16）***
```python
# 获取world size，在不同进程里都是一样的，得到16
torch.distributed.get_world_size()
```
# rank
表现当前进程的序号，用于进程通讯 ***（对于16，就是1，2，3...15）***
**rank=0的进程就是master进程**
```python
# 获取rank，每个进程都有自己的序号，各不相同
torch.distributed.get_rank()
```
# local_rank
又一个序号 ***（这是每台机子上的进程的序号。假如有两台机子16张卡，机器一上有0,1,2,3,4,5,6,7，机器二上也有0,1,2,3,4,5,6,7）***
