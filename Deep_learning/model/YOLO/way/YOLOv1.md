# YOLOv1

YOLO是one-stage
---------------
* 核心优势:速度非常快
* 相对two-stage较为粗糙

指标分析
-------
***map 值***
* 综合衡量检测效果

***IOU***
![IOU本地](IOU.png images/YOLO/IOU.png>)
* 后续置信度

***精度与召回率***

![本地](精度和召回率.png images/YOLO/精度和召回率.png>)
* `TP`: `true positives`正类判断成正类
* `FP`: `false positives`负类判断成正类
* `FN`: `false negatives`正类判断为负类
* `TN`: `ture negatives`负类判断为负类

***基于置信度阈值计算精度和召回率***

![本地](计算精度召回率.png images/YOLO/计算精度召回率.png>)
* 三个置信度为 0.9 0.8 0.7
~~~
设置阈值为0.9
    TP + FP = 1
    TP = 1
    FN = 2
    Precision = 1/1
    Recall = 1/3
~~~

***计算 map 值***

![本地](计算map值.png images/YOLO/计算map值.png>)
* MAP 值就是所有阈值类别的平均(所围成的面积[矩形取])

YOLOv1 核心思想
---------------
![本地](YOLOv1核心思想.png images/YOLO/YOLOv1核心思想.png>)

1. 将输入图像分成` S*S`的网格(物体中心在该网格，这个网格负责检测物体)

![本地](核心思想原文.png images/YOLO/核心思想原文.png>)

2. 计算每个格子的两个 bounding boxes(正方形和矩形)
    * bounding boex 包括 x y(坐标(x,y)表示相对于网格中心点位置) w h 和 confident(置信度)
3.  每个网格还要预测一个类别信息
4. 综合考虑，输出结果框(7 * 7 * 30结果[[张量基础知识]])

YOLOv1 网路架构
---------------
![本地](YOLOv1网络架构.png images/YOLO/YOLOv1网络架构.png>)

* 前5层均为卷积神经网络层
* 输出7 * 7 * 30结果[[张量基础知识]]

![本地](YOLOv1结果张量.png images/YOLO/YOLOv1结果张量.png>)

YOLOv1 损失函数
---------------
损失函数:

![本地](损失函数公式.png images/YOLO/损失函数公式.png>)

损失函数解析:

![本地](损失函数.png images/YOLO/损失函数.png>)

* 在位置误差位置,宽高取根号的原因是因为方便体现不同大小的物体不同宽高影响

YOLOv1 缺点
-----------
1. 每一个cell只预测一个类别，重叠无法解决
2. 小物体效果一般,长宽比可选但单一