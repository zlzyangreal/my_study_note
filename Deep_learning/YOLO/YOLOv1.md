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
![IOU本地](<../../Document images/YOLO/IOU.png>)

***精度与召回率***

![本地](<../../Document images/YOLO/精度和召回率.png>)
* `TP`: `true positives`正类判断成正类
* `FP`: `false positives`负类判断成正类
* `FN`: `false negatives`正类判断为负类
* `TN`: `ture negatives`负类判断为负类

***基于置信度阈值计算精度和召回率***
![本地](<../../Document images/YOLO/计算精度召回率.png>)
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
![本地](<../../Document images/YOLO/计算map值.png>)
* MAP 值就是所有阈值类别的平均(所围成的面积[矩形取])

YOLOv1 核心思想
---------------
![本地](<../../Document images/YOLO/YOLOv1核心思想.png>)
1. 将输入图像分成 S*S的网格