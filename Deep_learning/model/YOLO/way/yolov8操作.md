# 训练
```bash
yolo task=detect mode=train model=ultralytics/cfg/models/v8/yolov8.yaml data=ultralytics/models/yolo/Fair/mydata.yaml epochs=600 imgsz=640 resume=True
```
## 调库训练
```python
from ultralytics import YOLO
import os
os.environ["WANDB_API_KEY"] = "f9aa3e56900deba3c553b4764b5965cd86e86fe8"
os.environ["WANDB_MODE"] = "offline"
if __name__ == '__main__':

    model = YOLO()
    results = model.train(cfg="ultralytics/models/yolo/Fair/mydefault.yaml")
```
[[mydefault.yaml]]
### 结果
* `best.pt` 训练过程中在验证集上表现最好的模型权重，用来推理等
* `last.pt` 保存最后一次训练迭代结束后的模型权重，一般用来继续训练

# 推理
```bash
yolo detect predict model=/home/aorus/Desktop/WJ/Code/ultralytics/runs/detect/train13/weights/best.pt source=/home/aorus/Desktop/WJ/Code/ultralytics/1.jpg
```
## 两种数据集格式处理
[CoCo数据集格式](https://blog.csdn.net/m0_63493883/article/details/134786368)
[VOC数据集格式](https://blog.csdn.net/m0_63493883/article/details/134786368)
# 导出
```bash
yolo export model=/home/aorus/Desktop/WJ/Code/ultralytics/runs/detect/train13/weights/best.pt format=onnx opset=12
```
* `opset`和onnx版本有关
### 推理导出的onnx模型
```bash
yolo predict model=/home/aorus/Desktop/WJ/Code/ultralytics/runs/detect/train13/weights/best.onnxsource=/home/aorus/Desktop/WJ/Code/ultralytics/1.jpg device=0,1
```
### 问题
* 修改时尽量修改defuault.yaml,不新建
* voc格式训不起来直接串成COCO
	* [函数](voc_to_coco.py)
* yolo的初始配置如储存位置什么的，在`.config`