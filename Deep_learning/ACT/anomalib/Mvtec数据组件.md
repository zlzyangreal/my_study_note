
```python
    """MVTec Datamodule.

    Args:
        root (Path | str): 数据集根的路径.
            Defaults to ``"./datasets/MVTec"``.
        category (str): MVTec数据集的类别 (e.g. "bottle" or "cable").
            Defaults to ``"bottle"``.
        image_size (int | tuple[int, int] | None, optional): 输入图像的大小.
            Defaults to ``(256, 256)``.
        center_crop (int | tuple[int, int] | None, optional): 当提供时，图像将被居中裁剪到提供的维度
            Defaults to ``None``.
        normalization (InputNormalizationMethod | str): 将归一化方法应用于输入图像
            Defaults to ``InputNormalizationMethod.IMAGENET``.
        train_batch_size (int, optional): 训练批量大小.
            Defaults to ``32``.
        eval_batch_size (int, optional): 测试批量大小.
            Defaults to ``32``.
        num_workers (int, optional): 工作数量.
            Defaults to ``8``.
        task TaskType): 任务类型，“分类”，“检测”或“分割”
            Defaults to ``TaskType.SEGMENTATION``.
        transform_config_train (str | A.Compose | None, optional): 在训练过程中配置预处理.
            Defaults to ``None``.
        transform_config_val (str | A.Compose | None, optional): 在验证期间进行预处理的配置.
            Defaults to ``None``.
        test_split_mode (TestSplitMode): 确定如何获得测试子集的设置.
            Defaults to ``TestSplitMode.FROM_DIR``.
        test_split_ratio (float): 从训练集中保留用于测试的图像的一部分.
            Defaults to ``0.2``.
        val_split_mode (ValSplitMode): 确定如何获得验证子集的设置.
            Defaults to ``ValSplitMode.SAME_AS_TEST``.
        val_split_ratio (float):保留用于验证的训练或测试图像的一部分.
            Defaults to ``0.5``.
        seed (int | None, optional): 种子，可设置为一个固定的值，以再现性.
            Defualts to ``None``.

        """
```
```python
    """
    Examples:
        使用默认设置创建MVTec AD数据模块:

        >>> datamodule = MVTec()
        >>> datamodule.setup()
        >>> i, data = next(enumerate(datamodule.train_dataloader()))
        >>> data.keys()
        dict_keys(['image_path', 'label', 'image', 'mask_path', 'mask'])

        >>> data["image"].shape
        torch.Size([32, 3, 256, 256])

        更改数据集的类别:

        >>> datamodule = MVTec(category="cable")

        更改图像和批处理大小:

        >>> datamodule = MVTec(image_size=(512, 512), train_batch_size=16, eval_batch_size=8)

        MVTec AD数据集不提供验证集。如果您想使用一个单独的验证集，您可以使用' ' val_split_mode ' '和' ' val_split_ratio ' '参数来创建一个验证集.

        >>> datamodule = MVTec(val_split_mode=ValSplitMode.FROM_TEST, val_split_ratio=0.1)

        这将对测试集进行10%的次采样，并将其用作验证集。如果您想要创建一个不会更改测试集的综合验证集，您可以使用' 'ValSplitMode.SYNTHETIC ' '选项.

        >>> datamodule = MVTec(val_split_mode=ValSplitMode.SYNTHETIC, val_split_ratio=0.2)

    """
```
数据集下载
```python
    >>> datamodule = MVTec(root="./datasets/MVTec", category="bottle")
    >>> datamodule.prepare_data()
```