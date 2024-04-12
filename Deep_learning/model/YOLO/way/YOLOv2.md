# YOLOv2

YOLOv2 相对于 [[YOLOv1]] 的提升

![本地](YOLOv2与v1对比.png images/YOLO/YOLOv2与v1对比.png>)

Batch Normalization
----------------------
V2版本舍弃Dropout，卷积后全部加入Batch Normalization

![本地](Batch%20Normalization.png images/YOLO/Batch Normalization.png>)

* 网络的每一层的输入都做了归一化，收敛相对更容易
* 从现在的角度来看，Batch Normalization已经成网络必备处理
* 经过Batch Normalization处理后的网络会提升2%的mAP

更大的分辨率(high resolution classifier)
---------------------------------------
V1训练时用的是224 * 224，V2测试时用的448 * 448
* V2训练时额外又进行了10次448*448 的微调
* 使用高分辨率分类器后，YOLOv2的mAP提升了约4%

卷积和锚框(Convolutional With Anchor Boxes)
--------------------------------
* YOLOv2移除了[[YOLOv1]]中的全连接层而采用了卷积和anchor boxes来预测边界框,使得预测的box数量更多(13 * 13 * n)
* 实际输入416 * 416
* 通过引入anchor boxes，使得预测的box数量更多（13*13*n）
* 锚框的加入虽然降低了 mAP值，但是提高了召回率

聚类提取先验框(Dimension Clusters)
----------------------------------
* YOLOv2借鉴了Faster R-CNN中RPN网络的先验框策略,跟faster-rcnn系列不同的是先验框并不是直接按照长宽固定比给定
* 不采取欧几里得距离,为了解决物体大小不同问题

![本地](聚类提取先验框距离计算公式.png images/YOLO/聚类提取先验框距离计算公式.png>)

* YOLOv2采用k=5

![本地](聚类提取先验框效果.png images/YOLO/聚类提取先验框效果.png>)

Direct location prediction
---------------------------
在使用锚框的情况下会遇到模型稳定性问题

早期计算公式

![本地](锚框未优化公式.png images/YOLO/锚框未优化公式.png>)

优化公式

![本地](锚框优化公式.png images/YOLO/锚框优化公式.png>)

![本地](锚框定位.png images/YOLO/锚框定位.png>)

![本地](YOLOv2距离计算例子.png images/YOLO/YOLOv2距离计算例子.png>)

感受野
------
***概念***

![本地](感受野概念.png images/YOLO/感受野概念.png>)
![本地](卷积核选择.png images/YOLO/卷积核选择.png>)

Fine-Grained Features
----------------------
最后一层感受野太大了,小目标丢失,需要融合之前的特征

![本地](感受野融合.png images/YOLO/感受野融合.png>)
* 取的特征点就是前几层计算值,只不过将其转换成了13 * 13

多尺度(Multi-Scale Training)
----------------------------
YOLOv2 只有卷积层,不受尺度限制了

网络结构采用 Darknet-19
-----------------------
![本地](YOLOv2网络结构.png images/YOLO/YOLOv2网络结构.png>)
![本地](Darknet-19原文1.png images/YOLO/Darknet-19原文1.png>)
![本地](Darknet-19原文2.png images/YOLO/Darknet-19原文2.png>)