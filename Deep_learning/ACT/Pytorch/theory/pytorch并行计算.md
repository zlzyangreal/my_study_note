# 2.3 并行计算简介

在利用PyTorch做深度学习的过程中，可能会遇到数据量较大无法在单块GPU上完成，或者需要提升计算速度的场景，这时就需要用到并行计算。
## 2.3.1 [并行计算的三种实现方式](GPU并行训练)
## 2.3.2 使用CUDA加速训练

### 单卡训练
在PyTorch框架下，CUDA的使用变得非常简单，我们只需要显式的将数据和模型通过`.cuda()`方法转移到GPU上就可加速我们的训练。如下：

```python
model = Net()
model.cuda() # 模型显示转移到CUDA上

for image,label in dataloader:
    # 图像和标签显示转移到CUDA上
    image = image.cuda() 
    label = label.cuda()
```

### 多卡训练

[[DDP(显卡交火)]]
