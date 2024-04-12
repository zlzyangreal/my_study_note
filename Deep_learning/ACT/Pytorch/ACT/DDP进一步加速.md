[知乎原文：含原理](https://zhuanlan.zhihu.com/p/250471767)
# 一、在DDP中引入SyncBN

> [!NOTE] BN
> "Batch Normalization"，即批归一化。它是一种用于加速神经网络训练并提高模型性能的技术([论文](https://arxiv.org/abs/1502.03167))

**BN在多级多卡环境上的完整实现：SyncBN**

## SyncBN使用
```python
# DDP init
dist.init_process_group(backend='nccl')

# 按照原来的方式定义模型，这里的BN都使用普通BN就行了。
model = MyModel()
# 引入SyncBN，这句代码，会将普通BN替换成SyncBN。
model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model).to(device)

# 构造DDP模型
model = DDP(model, device_ids=[local_rank], output_device=local_rank)
```
# 二、DDP下的Gradient Accumulation的进一步加速
```python
# 单卡模式，即普通情况下的梯度累加
for 每次梯度累加循环
    optimizer.zero_grad()
    for _ in range(K):
        prediction = model(data)
        loss = loss_fn(prediction, label) / K  # 除以K，模仿loss function中的batchSize方向上的梯度平均，如果本身就没有的话则不需要。
        loss.backward()  # 积累梯度，不应用梯度改变
    optimizer.step()  # 应用梯度改变
########################################################################################
from contextlib import nullcontext
# 如果你的python版本小于3.7，请注释掉上面一行，使用下面这个：
# from contextlib import suppress as nullcontext

if local_rank != -1:
    model = DDP(model)

optimizer.zero_grad()
for i, (data, label) in enumerate(dataloader):
    # 只在DDP模式下，轮数不是K整数倍的时候使用no_sync
    my_context = model.no_sync if local_rank != -1 and i % K != 0 else nullcontext
    with my_context():
        prediction = model(data)
        loss = loss_fn(prediction, label) / K
        loss.backward()  # 积累梯度，不应用梯度改变
    if i % K == 0:
        optimizer.step()
        optimizer.zero_grad()
```
