# YOLOv3

论文译文 https://www.cnblogs.com/wj-1314/p/9744146.html

博文链接 https://blog.csdn.net/leviopku/article/details/82660381

## 算法基本思想
首先通过特征提取网络对输入特征提取特征，得到特定大小的特征图输出。输入图像分成13×13的grid cell，接着如果真实框中某个object的中心坐标落在某个grid cell中，那么就由该grid cell来预测该object。每个object有固定数量的bounding box，YOLO v3中有三个bounding box，使用逻辑回归确定用来预测的回归框

## 网络结构
![本地](YOLOv3网络结构.png images/YOLO/YOLOv3网络结构.png>)
* `DBL` 也就是代码中的 `Darknetconv2d_BN_Leaky` ，是yolo_v3的基本组件。就是卷积+BN+Leaky relu。对于v3来说， `BN` 和 `leaky relu` 已经是和卷积层不可分离的部分了(最后一层卷积除外)，共同构成了最小组件
    * BN，全称Batch Normalization,是2015年提出的一种方法，在进行深度网络训练时，大都会采取这种算法，为了解决深度神经网络随着网络深度加深，训练起来越困难，收敛越来越慢
    * Leaky relu，ReLU函数将所有负值输入映射为零，而将非负值输入保持不变
* `resn` n代表数字，有res1，res2, … ,res8等等，表示这个 `res_block` 里含有多少个 `res_unit` 。这是 `yolo_v3` 的大组件， `yolo_v3` 开始借鉴了 `ResNet` 的残差结构，使用这种结构可以让网络结构更深(从v2的 `darknet-19` 上升到v3的 `darknet-53`，前者没有残差结构)。
* `concat` [[张量基础知识]]拼接。将 `darknet` 中间层和后面的某一层的上采样进行拼接。拼接的操作和残差层add的操作是不一样的，拼接会扩充[[张量基础知识]]的维度，而add只是直接相加不会导致[[张量基础知识]]维度的改变

整个yolo_v3_body包含252层，组成如下

![本地](YOLOv3网络结构2.jpg images/YOLO/YOLOv3网络结构2.jpg>)
* add层23层(主要用于res_block的构成，每个res_unit需要一个add层，一共有1+2+8+8+4=23层)
* BN层和LeakyReLU层数量完全一样(72层)，在网络结构中的表现为： 每一层BN后面都会接一层LeakyReLU
* 卷积层一共有75层，其中有72层后面都会接BN+LeakyReLU的组合构成基本组件DBL
* 上采样和concat都有2次
* 每个res_block都会用上一个零填充，一共有5个res_block

## backbone
整个v3结构里面，是`没有池化层和全连接层`的。前向传播过程中，`张量的尺寸变换是通过改变卷积核的步长来实现的`，比如stride=(2, 2)，这就等于将图像边长缩小了一半(即面积缩小到原来的1/4)。在yolo_v2中，要经历5次缩小，会将特征图缩小到原输入尺寸的`1/(2)^5`即`1/32`。输入为`416x416`，则输出为`13x13x(416/32=13)`

yolo_v3也和v2一样，backbone都会将输出特征图缩小到输入的1/32。所以，通常都要求输入图片是32的倍数。（DarkNet-19 与 DarkNet-53）

![本地](YOLOv2网络结构.png images/YOLO/YOLOv2网络结构.png>)![本地](YOLOv3网络结构3.png images/YOLO/YOLOv3网络结构3.png>)
* yolo_v2中对于前向过程中[[张量基础知识]]尺寸变换，都是通过 `最大池化`来进行，一共有5次
* v3是通过卷积核 `增大步长`来进行，也是5次(darknet-53最后面有一个全局平均池化，在yolo-v3里面没有这一层，所以[[张量基础知识]]维度变化只考虑前面那5次)

这也是416x416输入得到13x13输出的原因。darknet-19是不存在残差结构(resblock，从resnet上借鉴过来)的，和VGG是同类型的backbone(属于上一代CNN结构)，而darknet-53是可以和resnet-152正面刚的backbone

![本地](backbone对比图.png images/YOLO/backbone对比图.png>)
* darknet-19在速度上仍然占据很大的优势
* (bounding box prior采用k=9)， `yolo_v3并没有那么追求速度，而是在保证实时性(fps>36)的基础上追求performance`
* tiny-darknet作为backbone可以替代darknet-53，在官方代码里用一行代码就可以实现切换backbone。搭用tiny-darknet的yolo，也就是tiny-yolo在轻量和高速两个特点上，显然是state of the art级别，tiny-darknet是和squeezeNet正面刚的网络

![本地](Tiny%20DarkNet轻量对比图.jpg images/YOLO/Tiny DarkNet轻量对比图.jpg>)

## Output
输出[[张量基础知识]]:

![本地](YOLOv3网络输出结构.png images/YOLO/YOLOv3网络输出结构.png>)
* yolo v3输出了3个不同尺度的feature map，如上图所示的y1, y2, y3.这也是v3论文中提到的为数不多的改进点：predictions across scales

![本地](YOLOv3改进点predictions%20across%20scales原文.png images/YOLO/YOLOv3改进点predictions across scales原文.png>)![本地](YOLOv3改进点predictions%20across%20scales2原文.png images/YOLO/YOLOv3改进点predictions across scales2原文.png>)
* 借鉴了FPN(feature pyramid networks)，采用多尺度来对不同size的目标进行检测，越精细的grid cell就可以检测出越精细的物体
* y1,y2和y3的深度都是255，边长的规律是13:26:52

yolo v3设定的是每个网格单元预测3个box，所以每个box需要有(x, y, w, h, confidence)五个基本参数，然后还要有80个类别的概率。所以3*(5 + 80) = 255。这个255就是这么来的。（yolo v1的输出[[张量基础知识]] 7x7x30，只能识别20类物体，而且每个cell只能预测2个box）

v3用上采样的方法来实现这种多尺度的feature map，concat连接的两个[[张量基础知识]]是具有一样尺度的(两处拼接分别是26x26尺度拼接和52x52尺度拼接，通过(2, 2)上采样来保证concat拼接的[[张量基础知识]]尺度相同)。作者并没有像SSD那样直接采用backbone中间层的处理结果作为feature map的输出，而是和后面网络层的上采样结果进行一个拼接之后的处理结果作为feature map。

## some tricks

### Bounding Box Prediction
#### 回顾v2版本,b-box预测
想借鉴faster R-CNN RPN中的anchor机制，但不屑于手动设定anchor prior(模板框)，于是用维度聚类的方法来确定anchor box prior(模板框)，最后发现聚类之后确定的prior在k=5也能够又不错的表现，于是就选用k=5。后来呢，v2又嫌弃anchor机制线性回归的不稳定性(因为回归的offset可以使box偏移到图片的任何地方)，所以v2最后选用了自己的方法：`直接预测相对位置`。预测出b-box中心点相对于网格单元左上角的相对坐标。

![本地](锚框优化公式.png images/YOLO/锚框优化公式.png>)

![本地](锚框定位.png images/YOLO/锚框定位.png>)
* yolo v2直接predict出(tx,ty,tw,th,to)，并不像RPN中anchor机制那样去遍历每一个pixel。可以从上面的公式看出，b-box的位置大小和confidence都可以通过(tx,ty,tw,th,to)计算得来，v2相当直接predict出了b-box的位置大小和confidence
#### 对于v3
在prior这里的处理有明确解释：选用的b-box priors 的k=9，对于tiny-yolo的话，k=6。priors都是在数据集上聚类得来的，有确定的数值
```
10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
```
* 一个代表高度另一个代表宽度

v3对b-box进行预测的时候，采用了`logistic regression`。这一波操作sao得就像RPN中的线性回归调整b-box。v3每次对b-box进行predict时，输出和v2一样都是(tx,ty,tw,th,to)然后通过公式1计算出绝对的(x, y, w, h, c)
* `logistic regression` 逻辑回归是一种数据分析技术，它使用数学来找出两个数据因子之间的关系。然后，使用此关系根据其中一个因子预测另一个因子的值。预测结果的数量通常是有限的，比如是或否。例如，假设您想猜测您的网站访客是否会点击购物车中的结账按钮。逻辑回归分析着眼于过去的访客行为，例如在网站上花费的时间和购物车中的商品数量。它确定，在过去，如果访客在网站上停留的时间超过五分钟，并且向购物车中添加了三件以上的商品，他们就会点击结账按钮。利用这些信息，逻辑回归函数可以预测新网站访客的行为。

logistic回归用于对anchor包围的部分进行一个目标性评分(objectness score)，即这块位置是目标的可能性有多大。这一步是在predict之前进行的，可以去掉不必要anchor，可以减少计算量
![本地](logistic回归原文1.png images/YOLO/logistic回归原文1.png>)![本地](logistic回归原文2.png images/YOLO/logistic回归原文2.png>)

如果模板框不是最佳的即使它超过我们设定的阈值，我们还是不会对它进行predict。
不同于faster R-CNN的是，yolo_v3只会对1个prior进行操作，也就是那个最佳prior。而logistic回归就是用来从9个anchor priors中找到objectness score(目标存在可能性得分)最高的那一个。logistic回归就是用曲线对prior相对于 objectness score映射关系的线性建模

### loss function
检测关键信息`(x,y),(w,h),class,confidence`
```python
xy_loss = object_mask * box_loss_scale * K.binary_crossentropy(raw_true_xy, raw_pred[..., 0:2],
                                                                       from_logits=True)
wh_loss = object_mask * box_loss_scale * 0.5 * K.square(raw_true_wh - raw_pred[..., 2:4])
confidence_loss = object_mask * K.binary_crossentropy(object_mask, raw_pred[..., 4:5], from_logits=True) + \
                          (1 - object_mask) * K.binary_crossentropy(object_mask, raw_pred[..., 4:5],
                                                                    from_logits=True) * ignore_mask
class_loss = object_mask * K.binary_crossentropy(true_class_probs, raw_pred[..., 5:], from_logits=True)

xy_loss = K.sum(xy_loss) / mf
wh_loss = K.sum(wh_loss) / mf
confidence_loss = K.sum(confidence_loss) / mf
class_loss = K.sum(class_loss) / mf
loss += xy_loss + wh_loss + confidence_loss + class_loss
```
* 这是一段keras框架描述的yolo v3 的loss_function代码。忽略恒定系数不看，可以从上述代码看出：`除了w, h的损失函数依然采用总方误差之外，其他部分的损失函数用的是二值交叉熵`。最后加到一起。
* `binary_crossentropy` 是一个最简单的交叉熵而已，一般用于二分类