# YOLOv4

博文 https://www.jiangdabai.com/2120

## 网络结构图
![本地](YOLOv4网络结构.jpg images/YOLO/YOLOv4网络结构.jpg>)
* Yolov4的结构图和[[YOLOv3]]相比，多了CSP结构，PAN结构，整体架构和[[YOLOv3]]是相同的，不过使用各种新的算法思想对各个子结构都进行了改进
* `CBM` Yolov4网络结构中的最小组件，由Conv+Bn+Mish激活函数三者组成
* `CBL` 由Conv+Bn+Leaky_relu激活函数三者组成
* `Res unit` 借鉴Resnet网络中的残差结构，让网络可以构建的更深
* `CSPX` 借鉴CSPNet网络结构，由卷积层和X个Res unint模块Concate组成
* `SPP` 采用1×1，5×5，9×9，13×13的最大池化的方式，进行多尺度融合
* `Concat` [[张量基础知识]]拼接，维度会扩充，和[[YOLOv3]]中的解释一样，对应于cfg文件中的route操作
* `add` [[张量基础知识]]相加，不会扩充维度，对应于cfg文件中的shortcut操作

## 核心基础内容
![本地](YOLOv4整体结构板块.jpg images/YOLO/YOLOv4整体结构板块.jpg>)
1. `输入端`：这里指的创新主要是训练时对输入端的改进，主要包括`Mosaic数据增强、cmBN、SAT自对抗训练`
2. `BackBone主干网络`：将各种新的方式结合起来，包括：`CSPDarknet53、Mish激活函数、Dropblock`
3. `Neck`：目标检测网络在BackBone和最后的输出层之间往往会插入一些层，比如Yolov4中的`SPP模块、FPN+PAN结构`
4. `Prediction`：输出层的锚框机制和[[YOLOv3]]相同，主要改进的是训练时的损失函数`CIOU_Loss`，以及预测框筛选的nms变为`DIOU_nms`
效果图

![本地](YOLOv4效果图.jpg images/YOLO/YOLOv4效果图.jpg>)
## 输入端创新
### Mosaic数据增强
Yolov4中使用的Mosaic是参考2019年底提出的CutMix数据增强的方式，但CutMix只使用了两张图片进行拼接，而Mosaic数据增强则采用了4张图片，随机缩放、随机裁剪、随机排布的方式进行拼接。

![本地](Mosaic数据增强效果.jpg images/YOLO/Mosaic数据增强效果.jpg>)
该方式优点
* `丰富数据集`：随机使用`4张图片`，随机缩放，再随机分布进行拼接，大大丰富了检测数据集，特别是随机缩放增加了很多小目标，让网络的鲁棒性更好
* `减少GPU`：可能会有人说，随机缩放，普通的数据增强也可以做，但作者考虑到很多人可能只有一个GPU，因此Mosaic增强训练时，可以直接计算4张图片的数据，使得Mini-batch大小并不需要很大，一个GPU就可以达到比较好的效果

##  BackBone创新
###  CSPDarknet53
* `CSPDarknet53`是在[[YOLOv3]]主干网络`Darknet53`的基础上，借鉴`2019年CSPNet`的经验，产生的Backbone结构，其中包含了`5个CSP`模块
* 每个CSP模块前面的卷积核的大小都是3*3，stride=2，因此可以起到下采样的作用。
* 因为Backbone有5个CSP模块，输入图像是608*608，所以特征图变化的规律是：608->304->152->76->38->19
经过5次CSP模块后得到19*19大小的特征图。
* 而且作者只在Backbone中采用了`Mish激活函数`，网络后面仍然采用`Leaky_relu激活函数`
* CSPNet全称是Cross Stage Paritial Network，主要从网络结构设计的角度解决推理中从计算量很大的问题,CSPNet的作者认为推理计算过高的问题是由于网络优化中的梯度信息重复导致的。
因此采用CSP模块先将基础层的特征映射划分为两部分，然后通过跨阶段层次结构将它们合并，在减少了计算量的同时可以保证准确率
* 优点
    1. 增强CNN的学习能力，使得在轻量化的同时保持准确性
    2. 降低计算瓶颈
    3. 降低内存成本

###  Mish激活函数
论文地址 https://arxiv.org/abs/1908.08681

和Leaky_relu激活函数的图形对比如下

![本地](Mish激活函数与Leaky_relu激活函数对比.jpg images/YOLO/Mish激活函数与Leaky_relu激活函数对比.jpg>)
* Yolov4的Backbone中都使用了Mish激活函数，而后面的网络则还是使用leaky_relu函数
* Yolov4作者实验测试时，使用CSPDarknet53网络在ImageNet数据集上做图像分类任务，发现使用了Mish激活函数的TOP-1和TOP-5的精度比没有使用时都略高一些，因此在设计Yolov4目标检测任务时，主干网络Backbone还是使用Mish激活函数

### Dropblock
Yolov4中使用的Dropblock，其实和常见网络中的Dropout功能类似，也是缓解过拟合的一种正则化方式。

论文地址：https://arxiv.org/pdf/1810.12890.pdf

传统的Dropout很简单，一句话就可以说的清：`随机删除减少神经元的数量，使网络变得更简单`

![本地](有无Dropblock对比.png images/YOLO/有无Dropblock对比.png>)

而Dropblock和Dropout相似，比如下图

![本地](Dropblock与Dropout相似.png images/YOLO/Dropblock与Dropout相似.png>)

中间Dropout的方式会随机的删减丢弃一些信息，但Dropblock的研究者认为，卷积层对于这种随机丢弃并不敏感，因为卷积层通常是三层连用：卷积+激活+池化层，池化层本身就是对相邻单元起作用。而且即使随机丢弃，卷积层仍然可以从相邻的激活单元学习到相同的信息。

因此，在全连接层上效果很好的Dropout在卷积层上效果并不好。

所以右图Dropblock的研究者则干脆整个局部区域进行删减丢弃。

这种方式其实是借鉴2017年的cutout数据增强的方式，cutout是将输入图像的部分区域清零，而Dropblock则是将Cutout应用到每一个特征图。而且并不是用固定的归零比率，而是在训练时以一个小的比率开始，随着训练过程线性的增加这个比率。

Dropblock的研究者与Cutout进行对比验证时，发现有几个特点
1. Dropblock的效果优于Cutout
2. Cutout只能作用于输入层，而Dropblock则是将Cutout应用到网络中的每一个特征图上
3. Dropblock可以定制各种组合，在训练的不同阶段可以修改删减的概率，从空间层面和时间层面，和Cutout相比都有更精细的改进

Yolov4中直接采用了更优的Dropblock，对网络的正则化过程进行了全面的升级改进

## Neck创新
在目标检测领域，为了更好的提取融合特征，通常在Backbone和输出层，会插入一些层，这个部分称为Neck。相当于目标检测网络的颈部，也是非常关键的。

Yolov4的Neck结构主要采用了SPP模块、FPN+PAN的方式
### SPP模块
在Yolov4中，SPP模块仍然是在Backbone主干网络之后

![本地](SPP模块.jpg images/YOLO/SPP模块.jpg>)
* 作者在SPP模块中，使用k={1*1,5*5,9*9,13*13}的最大池化的方式，再将不同尺度的特征图进行Concat操作
* 注意：这里最大池化采用padding操作，移动的步长为1，比如13×13的输入特征图，使用5×5大小的池化核池化，padding=2，因此池化后的特征图仍然是13×13大小

![本地](padding操作.jpg images/YOLO/padding操作.jpg>)
* 采用SPP模块的方式，比单纯的使用`k*k`最大池化的方式，更有效的增加主干特征的接收范围，显著的分离了最重要的上下文特征。
* Yolov4的作者在使用`608*608`大小的图像进行测试时发现，在[[COCO资料]]目标检测任务中，以0.5%的额外计算代价将AP50增加了2.7%，因此Yolov4中也采用了SPP模块。

### FPN+PAN
PAN是借鉴图像分割领域PANet的创新点

#### [[YOLOv3]]中Neck的FPN结构
![本地](Yolov3中Neck的FPN结构.png images/YOLO/Yolov3中Neck的FPN结构.png>)
* 经过几次下采样，三个紫色箭头指向的地方，输出分别是76*76、38*38、19*19
* 最后的Prediction中用于预测的三个特征图`①19*19*255、②38*38*255、③76*76*255`。[注：255表示80类别(1+4+80)×3=255]

Neck部分用立体图画

![本地](YOLOv3Neck部分用立体图画.jpg images/YOLO/YOLOv3Neck部分用立体图画.jpg>)
* 如图所示，FPN是自顶向下的，将高层的特征信息通过`上采样`的方式进行传递融合，得到进行预测的特征图

#### Yolov4
Yolov4中Neck这部分除了使用FPN外，还在此基础上使用了PAN结构

![本地](YOLOv4FPN+PAN.jpg images/YOLO/YOLOv4FPN+PAN.jpg>)
* 每个CSP模块前面的卷积核都是3*3大小，步长为2，相当于下采样操作。因此可以看到三个紫色箭头处的特征图是`76*76、38*38、19*19`。
* 最后Prediction中用于预测的三个特征图：`①76*76*255，②38*38*255，③19*19*255`

Neck部分的立体图像

![本地](YOLOv4Neck部分的立体图像.jpg images/YOLO/YOLOv4Neck部分的立体图像.jpg>)
* 和[[YOLOv3]]的FPN层不同，Yolov4在FPN层的后面还添加了一个`自底向上的特征金字塔`,其中包含两个`PAN结构`
* 这样结合操作，FPN层自顶向下传达`强语义特征`，而特征金字塔则自底向上传达`强定位特征`，两两联手，从不同的主干层对不同的检测层进行参数聚合
* `FPN+PAN`借鉴的是18年CVPR的`PANet`，当时主要应用于`图像分割领域`，但Alexey将其拆分应用到Yolov4中，进一步提高特征提取的能力
* 注意
    1. [[YOLOv3]]的FPN层输出的三个大小不一的特征图①②③直接进行预测，但Yolov4的FPN层，只使用最后的一个76*76特征图①，而经过两次PAN结构，输出预测的特征图②和③。这里的不同也体现在cfg文件中
        ```
        比如Yolov3.cfg最后的三个Yolo层，

        第一个Yolo层是最小的特征图19*19，mask=6,7,8，对应最大的anchor box。

        第二个Yolo层是中等的特征图38*38，mask=3,4,5，对应中等的anchor box。

        第三个Yolo层是最大的特征图76*76，mask=0,1,2，对应最小的anchor box。

        而Yolov4.cfg则恰恰相反

        第一个Yolo层是最大的特征图76*76，mask=0,1,2，对应最小的anchor box。

        第二个Yolo层是中等的特征图38*38，mask=3,4,5，对应中等的anchor box。

        第三个Yolo层是最小的特征图19*19，mask=6,7,8，对应最大的anchor box。
        ```
    2. 原本的PANet网络的PAN结构中，两个特征图结合是采用shortcut操作，而Yolov4中则采用concat（route）操作，特征图融合后的尺寸发生了变化

    ![本地](YOLOv4PAN结构.jpg images/YOLO/YOLOv4PAN结构.jpg>) 

## Prediction创新
### CIOU_loss
目标检测任务的损失函数一般由`Classificition Loss（分类损失函数）`和`Bounding Box Regeression Loss（回归损失函数）`两部分构成。
* `Bounding Box Regeression`的Loss近些年的发展过程是：Smooth L1 Loss-> IoU Loss（2016）-> GIoU Loss（2019）-> DIoU Loss（2020）->CIoU Loss（2020）
* IOU_Loss

    ![本地](IOU_Loss.png images/YOLO/IOU_Loss.png>)
    * IOU的loss其实很简单，主要是`交集/并集`，但其实也存在两个问题

        ![本地](IOU_Loss问题.png images/YOLO/IOU_Loss问题.png>)
        1. 即状态1的情况，当预测框和目标框不相交时，IOU=0，无法反应两个框距离的远近，此时损失函数不可导，IOU_Loss无法优化两个框不相交的情况
        2. 即状态2和状态3的情况，当两个预测框大小相同，两个IOU也相同，IOU_Loss无法区分两者相交情况的不同
* GIOU_Loss

    ![本地](GIOU_Loss.png images/YOLO/GIOU_Loss.png>)
    * 可以看到右图GIOU_Loss中，增加了相交尺度的衡量方式，缓解了单纯IOU_Loss时的尴尬
    * 还存在一种不足

        ![本地](GIOU_Loss存在的一种不足.jpg images/YOLO/GIOU_Loss存在的一种不足.jpg>)  
        1. 状态1、2、3都是预测框在目标框内部且预测框大小一致的情况，这时预测框和目标框的差集都是相同的，因此这三种状态的GIOU值也都是相同的，这时GIOU退化成了IOU，无法区分相对位置关系
* DIOU_Loss
    * 好的目标框回归函数应该考虑三个重要几何因素：重叠面积、中心点距离，长宽比
    * 针对如何最小化预测框和目标框之间的归一化距离？提出了DIOU_Loss（Distance_IOU_Loss）

        ![本地](DIOU_Loss.png images/YOLO/DIOU_Loss.png>)
        * DIOU_Loss考虑了重叠面积和中心点距离，当目标框包裹预测框的时候，直接度量2个框的距离，因此DIOU_Loss收敛的更快
        * 没有考虑到长宽比

            ![本地](DIOU_Loss起作用情况.png images/YOLO/DIOU_Loss起作用情况.png>)
            1. 比如上面三种情况，目标框包裹预测框，本来DIOU_Loss可以起作用
            2. 但预测框的中心点的位置都是一样的，因此按照DIOU_Loss的计算公式，三者的值都是相同的。
* CIOU_Loss
    * CIOU_Loss和DIOU_Loss前面的公式都是一样的，不过在此基础上还增加了一个影响因子，将预测框和目标框的长宽比都考虑了进去。

    ![本地](CIOU_Loss公式1.png images/YOLO/CIOU_Loss公式1.png>)
    * 其中v是衡量长宽比一致性的参数，我们也可以定义为

    ![本地](CIOU_Loss公式2.png images/YOLO/CIOU_Loss公式2.png>)
    * 这样CIOU_Loss就将目标框回归函数应该考虑三个重要几何因素：重叠面积、中心点距离，长宽比全都考虑进去了

Loss函数的不同点
* `IOU_Loss`：主要考虑检测框和目标框重叠面积。
* `GIOU_Loss`：在IOU的基础上，解决边界框不重合时的问题。
* `DIOU_Loss`：在IOU和GIOU的基础上，考虑边界框中心点距离的信息。
* `CIOU_Loss`：在DIOU的基础上，考虑边界框宽高比的尺度信息。

Yolov4中采用了CIOU_Loss的回归方式，使得预测框回归的速度和精度更高一些
### DIOU_nms
Nms主要用于预测框的筛选，常用的目标检测算法中，一般采用普通的nms的方式，Yolov4则借鉴上面D/CIOU loss的论文：https://arxiv.org/pdf/1911.08287.pdf

将其中计算IOU的部分替换成DIOU的方式

案例

![本地](DIOU_nms案例.png images/YOLO/DIOU_nms案例.png>)
* 在重叠目标的检测中，DIOU_nms的效果优于传统的nms
* 这里为什么不用CIOU_nms，而用DIOU_nms?
    * 因为前面讲到的CIOU_loss，是在DIOU_loss的基础上，添加的影响因子，包含groundtruth标注框的信息，在训练时用于回归。但在测试过程中，并没有groundtruth的信息，不用考虑影响因子，因此直接用DIOU_nms即可

## Yolov4 主要带来了 3 点新贡献
1. 提出了一种高效而强大的目标检测模型，使用 1080Ti 或 2080Ti 就能训练出超快、准确的目标检测器
2. 在检测器训练过程中，验证了最先进的一些研究成果对目标检测器的影响
3. 改进了 SOTA 方法，使其更有效、更适合单 GPU 训练