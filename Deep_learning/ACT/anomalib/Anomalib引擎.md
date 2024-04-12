
```python
    """
    Args:
        callbacks (list[Callback]): 添加回调函数或回调函数列表.
        normalization (NORMALIZATION, optional): 规范化方法.
            Defaults to NormalizationMethod.MIN_MAX.
        threshold (THRESHOLD):
            阈值化方法. Defaults to "F1AdaptiveThreshold".
        task (TaskType, optional): 任务类型. Defaults to TaskType.SEGMENTATION.
        image_metrics (str | list[str] | None, optional): 用于评估的图像度量.
            Defaults to None.
        pixel_metrics (str | list[str] | None, optional): 用于评估的像素度量.
            Defaults to None.
        visualizers (BaseVisualizationGenerator | list[BaseVisualizationGenerator] | None):
            网格显示参数. Defaults to None.
        **kwargs: PyTorch Lightning Trainer 参数.
    """
```
