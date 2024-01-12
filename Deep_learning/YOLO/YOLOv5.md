# YOLOv5 

博文 https://blog.csdn.net/qq_37541097/article/details/123594351

当前(v6.1)官网贴出的关于不同大小模型以及输入尺度对应的mAP、推理速度、参数数量以及理论计算量FLOPs

![本地](<../../Document images/YOLO/YOLOv5v6.1数据.png>)
## 网络结构
1. Backbone: New CSP-Darknet53
2. Neck: SPPF, New CSP-PAN
3. Head: YOLOv3 Head

根据yolov5l.yaml绘制的网络整体结构，YOLOv5针对不同大小（n, s, m, l, x）的网络整体架构都是一样的，只不过会在每个子模块中采用不同的深度和宽度，分别应对yaml文件中的depth_multiple和width_multiple参数。还需要注意一点，官方除了n, s, m, l, x版本外还有n6, s6, m6, l6, x6，区别在于后者是针对更大分辨率的图片比如1280x1280，当然结构上也有些差异，后者会下采样64倍，采用4个预测特征层，而前者只会下采样到32倍且采用3个预测特征层。(讨论的前者)

![本地](<../../Document images/YOLO/YOLOv5网络结构.png>)
* 与YOLOv4对比,YOLOv5在Backbone部分没太大变化。但是YOLOv5在v6.0版本后相比之前版本有一个很小的改动，把网络的第一层（原来是Focus模块）换成了一个6x6大小的卷积层。两者在理论上其实等价的，但是对于现有的一些GPU设备（以及相应的优化算法）使用6x6大小的卷积层比使用Focus模块更加高效下图是原来的Focus模块(和之前Swin Transformer中的Patch Merging类似)，将每个2x2的相邻像素划分为一个patch，然后将每个patch中相同位置（同一颜色）像素给拼在一起就得到了4个feature map，然后在接上一个3x3大小的卷积层。这和直接使用一个6x6大小的卷积层等效。

    ![本地](<../../Document images/YOLO/YOLOv5Backbone优化.png>)
* 在Neck部分的变化还是相对较大的，首先是将SPP换成成了SPPF（Glenn Jocher自己设计的），两者的作用是一样的，但后者效率更高。SPP结构如下图所示，是将输入并行通过多个不同大小的MaxPool，然后做进一步融合，能在一定程度上解决目标多尺度问题。

    ![本地](<../../Document images/YOLO/YOLOv5SPP.png>)
* 而SPPF结构是将输入串行通过多个5x5大小的MaxPool层，这里需要注意的是串行两个5x5大小的MaxPool层是和一个9x9大小的MaxPool层计算结果是一样的，串行三个5x5大小的MaxPool层是和一个13x13大小的MaxPool层计算结果是一样的。

    ![本地](<../../Document images/YOLO/YOLOv5SPPF.png>)

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

在Neck部分另外一个不同点就是New CSP-PAN了，在YOLOv4中，Neck的PAN结构是没有引入CSP结构的，但在YOLOv5中作者在PAN结构中加入了CSP，如网络图结构图，每个C3模块里都含有CSP结构。在Head部分，YOLOv3, v4, v5都是一样的

## 数据增强
### `Mosaic`
将四张图片拼成一张图片

![本地](<../../Document images/YOLO/YOLOv5Mosaic.png>)
### `Copy paste`
将部分目标随机的粘贴到图片中，前提是数据要有segments数据才行，即每个目标的实例分割信息。下面是Copy paste原论文中的示意图

![本地](<../../Document images/YOLO/YOLOv5Copy paste.png>)
### Random affine(Rotation, Scale, Translation and Shear)
随机进行仿射变换，但根据配置文件里的超参数发现只使用了Scale和Translation即缩放和平移

![本地](<../../Document images/YOLO/YOLOv5Random affine.png>)
### MixUp
就是将两张图片按照一定的透明度融合在一起，具体有没有用不太清楚，毕竟没有论文，也没有消融实验。代码中只有较大的模型才使用到了MixUp，而且每次只有10%的概率会使用到

![本地](<../../Document images/YOLO/YOLOv5MixUp.png>)
### Albumentations
主要是做些滤波、直方图均衡化以及改变图片质量等等，我看代码里写的只有安装了albumentations包才会启用，但在项目的requirements.txt文件中albumentations包是被注释掉了的，所以默认不启用
### Augment HSV(Hue, Saturation, Value)
随机调整色度，饱和度以及明度

![本地](<../../Document images/YOLO/YOLOv5Augment HSV.png>)
### Random horizontal flip
随机水平翻转

![本地](<../../Document images/YOLO/YOLOv5Random horizontal flip.png>)
## 训练策略
* `Multi-scale training(0.5~1.5x)`，多尺度训练，假设设置输入图片的大小为640 × 640 640 \times 640640×640，训练时采用尺寸是在0.5 × 640 ∼ 1.5 × 640 0.5 \times 640 \sim 1.5 \times 6400.5×640∼1.5×640之间随机取值，注意取值时取得都是32的整数倍（因为网络会最大下采样32倍）
* `AutoAnchor(For training custom data)`，训练自己数据集时可以根据自己数据集里的目标进行重新聚类生成Anchors模板
* `Warmup and Cosine LR scheduler`，训练前先进行Warmup热身，然后在采用Cosine学习率下降策略
* `EMA(Exponential Moving Average)`，可以理解为给训练的参数加了一个动量，让它更新过程更加平滑
* `Mixed precision`，混合精度训练，能够减少显存的占用并且加快训练速度，前提是GPU硬件支持
* `Evolve hyper-parameters`，超参数优化，没有炼丹经验的人勿碰，保持默认就好