# YOLOv3

论文译文 https://www.cnblogs.com/wj-1314/p/9744146.html

博文链接 https://blog.csdn.net/leviopku/article/details/82660381

## 算法基本思想
首先通过特征提取网络对输入特征提取特征，得到特定大小的特征图输出。输入图像分成13×13的grid cell，接着如果真实框中某个object的中心坐标落在某个grid cell中，那么就由该grid cell来预测该object。每个object有固定数量的bounding box，YOLO v3中有三个bounding box，使用逻辑回归确定用来预测的回归框

## 网络结构
![本地](<../../Document images/YOLO/YOLOv3网络结构.png>)
* `DBL` 也就是代码中的 `Darknetconv2d_BN_Leaky` ，是yolo_v3的基本组件。就是卷积+BN+Leaky relu。对于v3来说， `BN` 和 `leaky relu` 已经是和卷积层不可分离的部分了(最后一层卷积除外)，共同构成了最小组件
    * BN，全称Batch Normalization,是2015年提出的一种方法，在进行深度网络训练时，大都会采取这种算法，为了解决深度神经网络随着网络深度加深，训练起来越困难，收敛越来越慢
    * Leaky relu，ReLU函数将所有负值输入映射为零，而将非负值输入保持不变
* `resn` n代表数字，有res1，res2, … ,res8等等，表示这个 `res_block` 里含有多少个 `res_unit` 。这是 `yolo_v3` 的大组件， `yolo_v3` 开始借鉴了 `ResNet` 的残差结构，使用这种结构可以让网络结构更深(从v2的 `darknet-19` 上升到v3的 `darknet-53`，前者没有残差结构)。
* `concat` 张量拼接。将 `darknet` 中间层和后面的某一层的上采样进行拼接。拼接的操作和残差层add的操作是不一样的，拼接会扩充张量的维度，而add只是直接相加不会导致张量维度的改变

整个yolo_v3_body包含252层，组成如下
![本地](<../../Document images/YOLO/YOLOv3网络结构2.jpg>)
* add层23层(主要用于res_block的构成，每个res_unit需要一个add层，一共有1+2+8+8+4=23层)
* BN层和LeakyReLU层数量完全一样(72层)，在网络结构中的表现为： 每一层BN后面都会接一层LeakyReLU
* 卷积层一共有75层，其中有72层后面都会接BN+LeakyReLU的组合构成基本组件DBL
* 上采样和concat都有2次
* 每个res_block都会用上一个零填充，一共有5个res_block

## backbone
整个v3结构里面，是`没有池化层和全连接层`的。前向传播过程中，`张量的尺寸变换是通过改变卷积核的步长来实现的`，比如stride=(2, 2)，这就等于将图像边长缩小了一半(即面积缩小到原来的1/4)。在yolo_v2中，要经历5次缩小，会将特征图缩小到原输入尺寸的`1/(2)^5`即`1/32`。输入为`416x416`，则输出为`13x13x(416/32=13)`

yolo_v3也和v2一样，backbone都会将输出特征图缩小到输入的1/32。所以，通常都要求输入图片是32的倍数。（DarkNet-19 与 DarkNet-53）

![本地](<../../Document images/YOLO/YOLOv2网络结构.png>)![本地](<../../Document images/YOLO/YOLOv3网络结构3.png>)
* yolo_v2中对于前向过程中张量尺寸变换，都是通过 `最大池化`来进行，一共有5次
* v3是通过卷积核 `增大步长`来进行，也是5次(darknet-53最后面有一个全局平均池化，在yolo-v3里面没有这一层，所以张量维度变化只考虑前面那5次)

这也是416x416输入得到13x13输出的原因。darknet-19是不存在残差结构(resblock，从resnet上借鉴过来)的，和VGG是同类型的backbone(属于上一代CNN结构)，而darknet-53是可以和resnet-152正面刚的backbone

![本地](<../../Document images/YOLO/backbone对比图.png>)
* darknet-19在速度上仍然占据很大的优势
* (bounding box prior采用k=9)， `yolo_v3并没有那么追求速度，而是在保证实时性(fps>36)的基础上追求performance`
* tiny-darknet作为backbone可以替代darknet-53，在官方代码里用一行代码就可以实现切换backbone。搭用tiny-darknet的yolo，也就是tiny-yolo在轻量和高速两个特点上，显然是state of the art级别，tiny-darknet是和squeezeNet正面刚的网络

![本地](<../../Document images/YOLO/Tiny DarkNet轻量对比图.jpg>)

## Output
输出张量:

![本地](<../../Document images/YOLO/YOLOv3网络输出结构.png>)
* yolo v3输出了3个不同尺度的feature map，如上图所示的y1, y2, y3.这也是v3论文中提到的为数不多的改进点：predictions across scales

![本地](<../../Document images/YOLO/YOLOv3改进点predictions across scales原文.png>)![本地](<../../Document images/YOLO/YOLOv3改进点predictions across scales2原文.png>)
* 借鉴了FPN(feature pyramid networks)，采用多尺度来对不同size的目标进行检测，越精细的grid cell就可以检测出越精细的物体
* y1,y2和y3的深度都是255，边长的规律是13:26:52

yolo v3设定的是每个网格单元预测3个box，所以每个box需要有(x, y, w, h, confidence)五个基本参数，然后还要有80个类别的概率。所以3*(5 + 80) = 255。这个255就是这么来的。（yolo v1的输出张量 7x7x30，只能识别20类物体，而且每个cell只能预测2个box）

v3用上采样的方法来实现这种多尺度的feature map，concat连接的两个张量是具有一样尺度的(两处拼接分别是26x26尺度拼接和52x52尺度拼接，通过(2, 2)上采样来保证concat拼接的张量尺度相同)。作者并没有像SSD那样直接采用backbone中间层的处理结果作为feature map的输出，而是和后面网络层的上采样结果进行一个拼接之后的处理结果作为feature map。
