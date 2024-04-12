# YOLOv1 代码

## train.py 结构
按照一定的流程加载数据、构建模型、进行训练和评估，并保存训练好的模型参数
1. 定义了一个名为train()的函数，用于执行整个训练过程
2. 调用parse_args()函数解析命令行参数，并将解析结果`保存在args变量中`
3. 创建保存模型的文件夹：根据参数设置保存模型的文件夹路径，并`使用os.makedirs()函数创建文件夹`
4. 根据参数args的设置，`确定是否使用高分辨率预训练、是否使用多尺度技巧、是否使用CUDA加速等`
5. 根据参数args的设置，`确定训练和验证图像的尺寸`
6. 根据参数args的设置，`加载相应的数据集和评估器`。如果数据集类型是VOC，就加载VOC数据集和VOCAPIEvaluator评估器；如果数据集类型是COCO，就加载COCODataset数据集和COCOAPIEvaluator评估器
7. 使用torch.utils.data.DataLoader`创建数据加载器`，用于加载训练数据
8. 根据参数args的设置，`选择构建相应版本的模型。这里只支持YOLO模型`。
9. 将模型移动到设备上并设置为训练模式：将模型移动到指定的设备（CPU或GPU）上，并设置为训练模式
10. 如果参数args中设置了使用TensorBoard，则创建一个SummaryWriter对象，用于`记录训练过程中的损失值等信息`
11. 如果参数args中设置了继续训练，就`加载预训练模型的参数`。
12. 根据参数args的设置，`设置优化器和初始学习率`
13. 根据最大训练轮数进行循环
14. 根据参数args的设置，`选择学习率的调整策略`
15. 对于每个批次的图像和目标：
    1. 如果设置了使用`预热策略`，则根据当前迭代次数和预热周期设置学习率
    2. 将图像移动到设备上
    3. 如果设置了`多尺度技巧且满足条件`，则随机选择一个新的尺寸，并对图像进行插值
    4. 创建训练标签
    5. 前向传播和计算损失
    6. 反向传播和优化模型
    7. 如果设置了`使用TensorBoard`，则`记录损失值`
    8. 打印训练信息
    9. 如果当前轮数达到了`评估周期`（由参数args的设置决定），则在验证集上评估模型的性能
    10. 如果当前轮数达到了`保存周期`（由参数args的设置决定），则保存模型的参数
## YOLOv1网络模型初始化
```python
def __init__(self, device, input_size=None, num_classes=20, trainable=False, conf_thresh=0.01, nms_thresh=0.5, hr=False):
        super(myYOLO, self).__init__()
        #保存设备信息，用于将数据移动到正确的设备上进行计算
        self.device = device
        #保存目标类别的数量
        self.num_classes = num_classes
        #表示模型是否可训练，如果为True，则模型的参数可以进行训练
        self.trainable = trainable 
        #保存置信度阈值，用于筛选检测结果中置信度高于阈值的目标
        self.conf_thresh = conf_thresh
        #保存非极大值抑制的阈值，用于去除重叠较多的检测框
        self.nms_thresh = nms_thresh
        #保存模型的步长，用于计算特征图上的真实坐标
        self.stride = 32
        #创建一个网格，用于在特征图上定位目标
        self.grid_cell = self.create_grid(input_size)
        #保存输入图像的尺寸
        self.input_size = input_size
        #保存一个尺度因子，用于将预测的边界框坐标映射回原始图像尺寸
        self.scale = np.array([[[input_size[1], input_size[0], input_size[1], input_size[0]]]]) # shape: [1, 1, 4]
        #将尺度因子转换为PyTorch张量，并移动到指定的设备上
        self.scale_torch = torch.tensor(self.scale.copy(), device=device).float()

        # 使用预训练的ResNet-18作为模型的主干网络
        self.backbone = resnet18(pretrained=True)

        #构建一个包含多尺度空间金字塔池化（SPP）的网络模块
        self.SPP = nn.Sequential(
            Conv(512, 256, k=1),
            SPP(),
            BottleneckCSP(256*4, 512, n=1, shortcut=False)
        )
        #构建一个空间注意力模块（SAM）
        self.SAM = SAM(512) 
        #构建一个包含多个残差块的网络模块
        self.conv_set = BottleneckCSP(512, 512, n=3, shortcut=False)
        # 构建一个卷积层，用于预测目标的类别、置信度和边界框坐标
        self.pred = nn.Conv2d(512, 1 + self.num_classes + 4, 1) # only one box
```
## 训练过程
![本地](YOLOv3训练过程.png images/YOLO/YOLOv3训练过程.png>))
* `obj` `object loss` 置信度损失
* `cls` `class loss` 类别损失
* `bbox` `local loss` 中心坐标和宽高损失
* `total` 总损失

源码
```python
print('[Epoch %d/%d][Iter %d/%d][lr %.6f]''[Loss: obj %.2f || cls %.2f || bbox %.2f || total %.2f || size %d || time: %.2f]'
        % (epoch+1, max_epoch, iter_i, epoch_size, tmp_lr,conf_loss.item(), cls_loss.item(), txtytwth_loss.item(), total_loss.item(), train_size[0], t1-t0),
        flush=True)
```
