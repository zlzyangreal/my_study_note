# YOLOv5 

博文 https://blog.csdn.net/qq_37541097/article/details/123594351

当前(v6.1)官网贴出的关于不同大小模型以及输入尺度对应的mAP、推理速度、参数数量以及理论计算量FLOPs

![本地](YOLOv5v6.1数据.png images/YOLO/YOLOv5v6.1数据.png>))
## 网络结构
1. Backbone: New CSP-Darknet53
2. Neck: SPPF, New CSP-PAN
3. Head: [[YOLOv3]] Head

根据yolov5l.yaml绘制的网络整体结构，YOLOv5针对不同大小（n, s, m, l, x）的网络整体架构都是一样的，只不过会在每个子模块中采用不同的深度和宽度，分别应对yaml文件中的depth_multiple和width_multiple参数。还需要注意一点，官方除了n, s, m, l, x版本外还有n6, s6, m6, l6, x6，区别在于后者是针对更大分辨率的图片比如1280x1280，当然结构上也有些差异，后者会下采样64倍，采用4个预测特征层，而前者只会下采样到32倍且采用3个预测特征层。(讨论的前者)

![本地](YOLOv5网络结构.png images/YOLO/YOLOv5网络结构.png>))
* 与[[YOLOv4]]对比,YOLOv5在Backbone部分没太大变化。但是YOLOv5在v6.0版本后相比之前版本有一个很小的改动，把网络的第一层（原来是Focus模块）换成了一个6x6大小的卷积层。两者在理论上其实等价的，但是对于现有的一些GPU设备（以及相应的优化算法）使用6x6大小的卷积层比使用Focus模块更加高效下图是原来的Focus模块(和之前Swin Transformer中的Patch Merging类似)，将每个2x2的相邻像素划分为一个patch，然后将每个patch中相同位置（同一颜色）像素给拼在一起就得到了4个feature map，然后在接上一个3x3大小的卷积层。这和直接使用一个6x6大小的卷积层等效。

   ![本地](YOLOv5Backbone优化.png images/YOLO/YOLOv5Backbone优化.png>))
* 在Neck部分的变化还是相对较大的，首先是将SPP换成成了SPPF（Glenn Jocher自己设计的），两者的作用是一样的，但后者效率更高。SPP结构如下图所示，是将输入并行通过多个不同大小的MaxPool，然后做进一步融合，能在一定程度上解决目标多尺度问题。

   ![本地](YOLOv5SPP.png images/YOLO/YOLOv5SPP.png>))
* 而SPPF结构是将输入串行通过多个5x5大小的MaxPool层，这里需要注意的是串行两个5x5大小的MaxPool层是和一个9x9大小的MaxPool层计算结果是一样的，串行三个5x5大小的MaxPool层是和一个13x13大小的MaxPool层计算结果是一样的。

   ![本地](YOLOv5SPPF.png images/YOLO/YOLOv5SPPF.png>))

验证程序a(对比下SPP和SPPF的计算结果以及速度)
* 这里将SPPF中最开始和结尾处的1x1卷积层给去掉了，只对比含有MaxPool的部分
```python
import time
import torch
import torch.nn as nn

class SPP(nn.Module):
    def __init__(self):
        super().__init__()
        self.maxpool1 = nn.MaxPool2d(5, 1, padding=2)
        self.maxpool2 = nn.MaxPool2d(9, 1, padding=4)
        self.maxpool3 = nn.MaxPool2d(13, 1, padding=6)

    def forward(self, x):
        o1 = self.maxpool1(x)
        o2 = self.maxpool2(x)
        o3 = self.maxpool3(x)
        return torch.cat([x, o1, o2, o3], dim=1)


class SPPF(nn.Module):
    def __init__(self):
        super().__init__()
        self.maxpool = nn.MaxPool2d(5, 1, padding=2)

    def forward(self, x):
        o1 = self.maxpool(x)
        o2 = self.maxpool(o1)
        o3 = self.maxpool(o2)
        return torch.cat([x, o1, o2, o3], dim=1)


def main():
    input_tensor = torch.rand(8, 32, 16, 16)
    spp = SPP()
    sppf = SPPF()
    output1 = spp(input_tensor)
    output2 = sppf(input_tensor)

    print(torch.equal(output1, output2))

    t_start = time.time()
    for _ in range(100):
        spp(input_tensor)
    print(f"spp time: {time.time() - t_start}")

    t_start = time.time()
    for _ in range(100):
        sppf(input_tensor)
    print(f"sppf time: {time.time() - t_start}")


if __name__ == '__main__':
    main()
```
输出
```python
True
spp time: 0.5373051166534424
sppf time: 0.20780706405639648
```
* 两者的计算结果是一模一样的，但SPPF比SPP计算速度快了不止两倍

在Neck部分另外一个不同点就是New CSP-PAN了，在[[YOLOv4]]中，Neck的PAN结构是没有引入CSP结构的，但在YOLOv5中作者在PAN结构中加入了CSP，如网络图结构图，每个C3模块里都含有CSP结构。在Head部分，[[YOLOv3]], [v4](YOLOv4.md), v5都是一样的

## 数据增强
### `Mosaic`
将四张图片拼成一张图片

![本地](YOLOv5Mosaic.png images/YOLO/YOLOv5Mosaic.png>))
### `Copy paste`
将部分目标随机的粘贴到图片中，前提是数据要有segments数据才行，即每个目标的实例分割信息。下面是Copy paste原论文中的示意图

![本地](YOLOv5Copy%20paste.png images/YOLO/YOLOv5Copy paste.png>))
### Random affine(Rotation, Scale, Translation and Shear)
随机进行仿射变换，但根据配置文件里的超参数发现只使用了Scale和Translation即缩放和平移

![本地](YOLOv5Random%20affine.png images/YOLO/YOLOv5Random affine.png>))
### MixUp
就是将两张图片按照一定的透明度融合在一起，具体有没有用不太清楚，毕竟没有论文，也没有消融实验。代码中只有较大的模型才使用到了MixUp，而且每次只有10%的概率会使用到

![本地](YOLOv5MixUp.png images/YOLO/YOLOv5MixUp.png>))
### Albumentations
主要是做些滤波、直方图均衡化以及改变图片质量等等，我看代码里写的只有安装了albumentations包才会启用，但在项目的requirements.txt文件中albumentations包是被注释掉了的，所以默认不启用
### Augment HSV(Hue, Saturation, Value)
随机调整色度，饱和度以及明度

![本地](YOLOv5Augment%20HSV.png images/YOLO/YOLOv5Augment HSV.png>))
### Random horizontal flip
随机水平翻转

![本地](YOLOv5Random%20horizontal%20flip.png images/YOLO/YOLOv5Random horizontal flip.png>))
## 训练策略
* `Multi-scale training(0.5~1.5x)`，多尺度训练，假设设置输入图片的大小为640 × 640 640 \times 640640×640，训练时采用尺寸是在0.5 × 640 ∼ 1.5 × 640 0.5 \times 640 \sim 1.5 \times 6400.5×640∼1.5×640之间随机取值，注意取值时取得都是32的整数倍（因为网络会最大下采样32倍）
* `AutoAnchor(For training custom data)`，训练自己数据集时可以根据自己数据集里的目标进行重新聚类生成Anchors模板
* `Warmup and Cosine LR scheduler`，训练前先进行Warmup热身，然后在采用Cosine学习率下降策略
* `EMA(Exponential Moving Average)`，可以理解为给训练的参数加了一个动量，让它更新过程更加平滑
* `Mixed precision`，混合精度训练，能够减少显存的占用并且加快训练速度，前提是GPU硬件支持
* `Evolve hyper-parameters`，超参数优化，没有炼丹经验的人勿碰，保持默认就好

## 损失计算
1. `Classes loss`，分类损失，采用的是BCE loss，注意只计算正样本的分类损失
2. `Objectness loss`，obj损失，采用的依然是BCE loss，注意这里的obj指的是网络预测的目标边界框与GT Box的CIoU。这里计算的是所有样本的obj损失
3. `Location loss`，定位损失，采用的是CIoU loss，注意只计算正样本的定位损失

![本地](损失计算.png images/YOLO/损失计算.png>))
* λ 1 , λ 2 , λ 3 为平衡系数
## 平衡不同尺度的损失
这里是指针对三个预测特征层（P3, P4, P5）上的obj损失采用不同的权重。在源码中，针对预测小目标的预测特征层（P3）采用的权重是4.0，针对预测中等目标的预测特征层（P4）采用的权重是1.0，针对预测大目标的预测特征层（P5）采用的权重是0.4，作者说这是针对[[COCO资料]]数据集设置的超参数。

![本地](YOLOv5平衡不同尺度的损失.png images/YOLO/YOLOv5平衡不同尺度的损失.png>))
## 消除Grid敏感度
[[YOLOv2]]，[v3](YOLOv3.md)的计算公式

![本地](YOLOv2，v3的计算公式.png images/YOLO/YOLOv2，v3的计算公式.png>))
* tx是网络预测的目标中心x坐标偏移量（相对于网格的左上角）
* ty是网络预测的目标中心y坐标偏移量（相对于网格的左上角）
* cx是对应网格左上角的x坐标
* cy是对应网格左上角的y坐标
* σ是Sigmoid激活函数，将预测的偏移量限制在0到1之间，即预测的中心点不会超出对应的Grid Cell区域

关于预测目标中心点相对Grid网格左上角( cx , cy )偏移量为σ ( tx ) , σ ( ty ) [[YOLOv4]]的作者认为这样做不太合理，比如当真实目标中心点非常靠近网格的左上角点（σ ( tx ) 和σ ( ty ) 应该趋近与0）或者右下角点（σ ( tx )和σ ( ty )应该趋近与1）时，网络的预测值需要负无穷或者正无穷时才能取到，而这种很极端的值网络一般无法达到。为了解决这个问题，作者对偏移量进行了缩放从原来的( 0 , 1 ) (0, 1)(0,1)缩放到( − 0.5 , 1.5 ) (-0.5, 1.5)(−0.5,1.5)这样网络预测的偏移量就能很方便达到0或1，故最终预测的目标中心点bx , by的计算公式为

![本地](YOLOv2,v3最终预测的目标中心点计算公式.png images/YOLO/YOLOv2,v3最终预测的目标中心点计算公式.png>))
* y = σ ( x )对应before曲线和y = 2 ⋅ σ ( x ) − 0.5 对应after曲线，很明显通过引入缩放系数scale以后，y对x更敏感了，且偏移的范围由原来的( 0 , 1 )调整到了( − 0.5 , 1.5 )

   ![本地](对比曲线.png images/YOLO/对比曲线.png>))
    
在YOLOv5中除了调整预测Anchor相对Grid网格左上角( cx , cy )偏移量以外，还调整了预测目标高宽的计算公式

* 之前

   ![本地](YOLOv5调整前计算公式.png images/YOLO/YOLOv5调整前计算公式.png>))
* 调整后

   ![本地](YOLOv5调整后计算公式.png images/YOLO/YOLOv5调整后计算公式.png>))
* 前后对比曲线，（相对Anchor宽高的倍率因子）的变化曲线

   ![本地](（相对Anchor宽高的倍率因子）的变化曲线.png images/YOLO/（相对Anchor宽高的倍率因子）的变化曲线.png>))
    * 调整后倍率因子被限制在( 0 , 4 )之间
* 作者的大致意思是，原来的计算公式并没有对预测目标宽高做限制，这样可能出现梯度爆炸，训练不稳定等问题
## 匹配正样本(Build Targets)
YOLOv5与[[YOLOv4]]差不多，主要的区别在于GT Box与Anchor Templates模板的匹配方式。在[[YOLOv4]]中是直接将每个GT Box与对应的Anchor Templates模板计算IoU，只要IoU大于设定的阈值就算匹配成功。但在YOLOv5中，作者先去计算每个GT Box与对应的Anchor Templates模板的高宽比例，即

![本地](YOLOv5高宽比例.png images/YOLO/YOLOv5高宽比例.png>))

然后统计这些比例和它们倒数之间的最大值，这里可以理解成计算GT Box和Anchor Templates分别在宽度以及高度方向的最大差异（当相等的时候比例为1，差异最小）

![本地](YOLOv5高宽比例2.png images/YOLO/YOLOv5高宽比例2.png>))

接着统计两者之间最大值，即宽度和高度方向差异最大的值

![本地](YOLOv5高宽比例3.png images/YOLO/YOLOv5高宽比例3.png>))

如果GT Box和对应的Anchor Template的rmax小于阈值anchor_t（在源码中默认设置为4.0），即GT Box和对应的Anchor Template的高、宽比例相差不算太大，则将GT Box分配给该Anchor Template模板
* 图解:假设对某个GT Box而言，其实只要GT Box满足在某个Anchor Template宽和高的× 0.25倍和× 4.0倍之间就算匹配成功

   ![本地](YOLOv5例图.png images/YOLO/YOLOv5例图.png>))
    * 剩下的步骤和[[YOLOv4]]中一致
        * 将GT投影到对应预测特征层上，根据GT的中心点定位到对应Cell，注意图中有三个对应的Cell。因为网络预测中心点的偏移范围已经调整到了( − 0.5 , 1.5 )，所以按理说只要Grid Cell左上角点距离GT中心点在( − 0.5 , 1.5 )范围内它们对应的Anchor都能回归到GT的位置处。这样会让正样本的数量得到大量的扩充
        * 则这三个Cell对应的AT2和AT3都为正样本

       ![本地](YOLOv5例图2.png images/YOLO/YOLOv5例图2.png>))
    * 还需要注意的是，YOLOv5源码中扩展Cell时只会往上、下、左、右四个方向扩展，不会往左上、右上、左下、右下方向扩展。下面又给出了一些根![本地](插入公式.png images/YOLO/插入公式.png>))的位置扩展的一些Cell案例，其中%1表示取余并保留小数部分。

       ![本地](YOLOv5例图3.png images/YOLO/YOLOv5例图3.png>))