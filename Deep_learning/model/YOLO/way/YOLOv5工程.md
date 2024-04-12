# YOLOv5代码

## 权重文件
weights下加入权重文件 yolov5l/m/s/x.pt文件
* 由shell脚本生成
* 脚本的作用是通过调用utils.google_utils模块中的attempt_download函数，从GitHub上下载YOLOv5模型的权重文件。脚本中使用了一个循环，依次下载's', 'm', 'l', 'x'四个不同大小的模型权重文件。使用方法是在终端中运行bash weights/download_weights.sh命令，即可开始下载YOLOv5模型的权重文件。

## 文件配置 yaml文件
以VOC数据集为例，配置PASCAL VOC数据集的训练参数和相关信息
```yaml
#   /parent_folder
#     /VOC
#     /yolov5


# download command/URL (optional)
download: bash data/scripts/get_voc.sh

# train and val data as 1) directory: path/images/, 2) file: path/images.txt, or 3) list: [path1/images/, path2/images/]
train: ../VOC/images/train/  # 16551 images
val: ../VOC/images/val/  # 4952 images

# number of classes
nc: 20

# class names
names: [ 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
         'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor' ]
```
* download: 可选项，用于指定下载数据集的命令或URL。在这个例子中，使用了一个bash脚本data/scripts/get_voc.sh来下载数据集
* train: 指定训练数据集的路径。可以是一个目录路径，如../VOC/images/train/，也可以是一个包含图像路径的文件，如path/images.txt，还可以是一个包含多个目录路径的列表，如[path1/images/, path2/images/]
* val: 指定验证数据集的路径。与train类似，可以是目录路径、文件路径或列表
* nc: 指定数据集中的类别数量
* names: 指定数据集中每个类别的名称。这里给出了PASCAL VOC数据集中20个类别的名称

以coco数据集为例，配置在COCO数据集上从头开始训练目标检测模型的超参数
```yaml
lr0: 0.01  # initial learning rate (SGD=1E-2, Adam=1E-3)
lrf: 0.2  # final OneCycleLR learning rate (lr0 * lrf)
momentum: 0.937  # SGD momentum/Adam beta1
weight_decay: 0.0005  # optimizer weight decay 5e-4
warmup_epochs: 3.0  # warmup epochs (fractions ok)
warmup_momentum: 0.8  # warmup initial momentum
warmup_bias_lr: 0.1  # warmup initial bias lr
box: 0.05  # box loss gain
cls: 0.5  # cls loss gain
cls_pw: 1.0  # cls BCELoss positive_weight
obj: 1.0  # obj loss gain (scale with pixels)
obj_pw: 1.0  # obj BCELoss positive_weight
iou_t: 0.20  # IoU training threshold
anchor_t: 4.0  # anchor-multiple threshold
# anchors: 3  # anchors per output layer (0 to ignore)
fl_gamma: 0.0  # focal loss gamma (efficientDet default gamma=1.5)
hsv_h: 0.015  # image HSV-Hue augmentation (fraction)
hsv_s: 0.7  # image HSV-Saturation augmentation (fraction)
hsv_v: 0.4  # image HSV-Value augmentation (fraction)
degrees: 0.0  # image rotation (+/- deg)
translate: 0.1  # image translation (+/- fraction)
scale: 0.5  # image scale (+/- gain)
shear: 0.0  # image shear (+/- deg)
perspective: 0.0  # image perspective (+/- fraction), range 0-0.001
flipud: 0.0  # image flip up-down (probability)
fliplr: 0.5  # image flip left-right (probability)
mosaic: 1.0  # image mosaic (probability)
mixup: 0.0  # image mixup (probability)
```
* lr0: 初始学习率，用于优化器的学习率设置。在这个例子中，初始学习率为0.01。
* lrf: 最终的学习率，用于OneCycleLR学习率调度器。最终学习率等于初始学习率乘以lrf。在这个例子中，最终学习率为初始学习率的0.2倍。
* momentum: SGD优化器的动量参数或Adam优化器的beta1参数。
* weight_decay: 优化器的权重衰减参数。
* warmup_epochs: 热身阶段的训练周期数。热身阶段是指在训练开始时使用较低的学习率进行预热，然后逐渐增加学习率。
* warmup_momentum: 热身阶段的初始动量参数。
* warmup_bias_lr: 热身阶段的初始偏置学习率。
* box, cls, obj: 目标检测损失函数中的不同部分的权重。
* iou_t: 训练时的IoU阈值，用于判断预测框和真实框之间的重叠程度。
* anchor_t: 锚框的阈值，用于筛选与真实框匹配的锚框。
* fl_gamma: Focal Loss中的gamma参数。
* hsv_h, hsv_s, hsv_v: 图像HSV色彩空间增强的参数。
* degrees, translate, scale, shear, perspective: 图像几何变换增强的参数。
* flipud, fliplr: 图像翻转增强的概率。
* mosaic: 图像马赛克增强的概率。
* mixup: 图像混合增强的概率。
## 数据集文件
* images（图片）+label（标签）文件
    * images下包含训练集和测试集
    * label下包含训练集和测试集
## 训练指令
* 开始训练

    `python train.py --data data/voc_new.yaml --cfg models/yolov5s_voc.yaml --weights weights/yolov5s.pt --batch-size 6 --epochs 1 `
* 训练结果

    `tensorboard --logdir=./runs`