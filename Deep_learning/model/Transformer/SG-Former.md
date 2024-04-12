**超越[[SWin Transformer]]和[[CSWin]] Transformer的新模型**
[论文](https://arxiv.org/pdf/2308.12216.pdf)
[源码](https://github.com/OliverRensu/SG-Former)
[[ViT]]在各种视觉任务中虽然成功，但它的计算成本随着Token序列长度的增加呈二次增长，这在处理大型特征图时大大限制了其性能.
# **模型目的**:减轻[[ViT]]计算成本
# 现有方法
1. 限制在局部小区域内的细粒度Self-Attention
2. 采用全局Self-Attention，但要缩短序列长度，从而导致粗粒度的问题
## 为了在高分辨率特征上计算Self-Attention，
#### 提出了将Self-Attention区域限制在局部窗口而不是整个特征图（即**细粒度的局部Self-Attention**）
[[Swin Transformer]]：设计了窗口注意力
[[CSWin]] ：设计了交叉形状注意力
**这些方法牺牲了在每个Self-Attention层中建模全局信息的能力**
#### 在整个键-值特征映射中聚合Token，以减少全局序列长度（即**粗粒度的全局注意力**）
金字塔视觉Transformer（[[PVT]]）：使用大步幅的大核心来均匀聚合整个特征映射上的Token，从而导致整个特征映射上的均匀粗糙信息。
# SG-Former
实现具有自适应细粒度的有效全局Self-Attention
**核心思想**：利用一个显著性图，通过混合尺度的Self-Attention估计并在训练过程中自我演化，以**根据每个区域的重要性重新分配Token**。
* 为显著区域分配更多的Token，以实现细粒度的注意力，同时将更少的Token分配给次要区域，以换取效率和全局感知字段。
* 保留了整个特征图上的远程依赖性，同时根据图像区域的重要性重新分配Token。
![[SG_Former1.png]]
SG-Former根据从自身获得的注意力图重新分配Token，例如在狗这样的显著区域分配更多的Token，而在墙这样的次要区域分配更少的Token。 [[PVT]]采用了预定义的策略均匀聚合Token。
