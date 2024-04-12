
## EfficientAd
```python
    """PL Lightning Module for the EfficientAd algorithm.

    Args:
        input_size (tuple): 输入图像的大小
            Defaults to ``(256, 256)``.
        teacher_out_channels (int): 卷积输出通道的数量
            Defaults to ``384``.
        model_size (str): 学生和教师模型的大小
            Defaults to ``EfficientAdModelSize.S``.
        lr (float): 学习率
            Defaults to ``0.0001``.
        weight_decay (float): 优化器权重衰减
            Defaults to ``0.00001``.
        padding (bool): 在卷积层中使用填充
            Defaults to ``False``.
        pad_maps (bool): 如果填充设置为False则相关。在这种情况下，pad_maps = True填充输出异常映射，以便它们的大小与padding = True情况下的大小匹配.
            Defaults to ``True``.
        batch_size (int): imagenet数据加载器的批处理大小
            Defaults to ``1``.
    """
```
1. 接受多个参数，包括 input_size、teacher_out_channels、model_size、lr、weight_decay、padding、pad_maps 和 batch_size。
2. 创建了一个 EfficientAdModel 的实例，作为模型的主要组成部分。
3. 设置了一些属性，如模型大小 (model_size)、批处理大小 (batch_size)、图像大小 (image_size)、学习率 (lr) 和权重衰减 (weight_decay)。
4. 调用了 prepare_pretrained_model() 和 prepare_imagenette_data() 方法，用于准备预训练教师模型和准备ImageNette数据集转换

### 函数
1. `teacher_channel_mean_std` 
    * 计算教师模型激活的均值和std
    * Args: dataloader (DataLoader):相应数据集的数据加载程序.
    * Returns: dict[str, torch.Tensor]: 激活的均值和std
2. `map_norm_quantiles`
    * 计算学生(st)和自动编码器(ae)的90%和99.5%分位数
    * Args: dataloader (DataLoader): 相应数据集的数据加载程序.
    * Returns: dict[str, torch.Tensor]: 90%和99.5%分位数的字典,学生和自动编码器的特征映射.
3. `_get_quantiles_of_maps`
    * 计算给定异常图的90%和99.5%分位数
    * 如果给定映射中的元素总数大于16777216,返回的分位数是在给定的随机子集上计算的元素
    * Args: maps (list[torch.Tensor]): 异常图列表.
    * Returns: tuple[torch.Tensor, torch.Tensor]: 两个标量，90%和99.5%分位数.
4. `configure_optimizers`
    * 配置优化器和学习率调度器，以便在训练过程中对模型参数进行优化和调整学习率
5. `on_train_start`
    * 计算或加载训练数据集的图像的每个通道上的像素平均值和std，并推送到模型
## EfficientAdModel
```python
    """EfficientAd model.

    Args:
        teacher_out_channels (int): 预训练教师模型的卷积输出通道数
        input_size (tuple): 输入图像的大小
        model_size (str): 学生和教师模型的大小
        padding (bool): 在卷积层中使用填充
            Defaults to ``False``.
        pad_maps (bool): 如果填充设置为False则相关。在这种情况下，pad_maps = True填充输出异常映射，以便它们的大小与padding = True情况下的大小匹配.
            Defaults to ``True``.
    """
```
1. 参数包括 teacher_out_channels、input_size、model_size、padding 和 pad_maps。
2. 根据指定的 model_size 参数，创建了一个 MediumPatchDescriptionNetwork 或 SmallPatchDescriptionNetwork，分别作为师生模型的描述网络。
3. 创建了一个名为 ae 的自动编码器，参数包括 out_channels、padding 和 img_size。
4. 初始化了一些属性，如 teacher_out_channels、input_size 和 pad_maps。
5. 创建了一个 mean_std 参数字典，用于存储均值和标准差张量。
6. 创建了一个 quantiles 参数字典，包含四个张量，表示用于异常检测的分位数。

师生模型
* 根据 model_size 参数的值选择创建 MediumPatchDescriptionNetwork 或 SmallPatchDescriptionNetwork。
* 创建了师模型，并根据指定的 out_channels 和 padding 设置，将其设置为评估模式 (eval())。
* 学生模型的输出通道数是师模型的两倍。

自动编码器 (ae)
* 创建了一个自动编码器，参数包括指定的 out_channels、padding 和 img_size（输入图像尺寸）。

参数字典 (mean_std 和 quantiles)
* mean_std 包含了用于归一化的均值和标准差张量。
* quantiles 包含了用于异常检测的分位数张量。

异常处理
* 如果提供了未知的 model_size，则会引发 ValueError 异常，并附带相应的错误消息。