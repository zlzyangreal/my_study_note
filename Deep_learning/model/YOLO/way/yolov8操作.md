# 环境
使用Pip在一个**Python>=3.8**环境中安装`ultralytics`包，此环境还需包含**PyTorch>=1.7**。
yolo包下载
```bash
pip install ultralytics
```
```
依赖项
```txt
# Ultralytics requirements
# Usage: pip install -r requirements.txt
# Base ----------------------------------------
matplotlib>=3.2.2
numpy>=1.22.2 # pinned by Snyk to avoid a vulnerability
opencv-python>=4.6.0
pillow>=7.1.2
pyyaml>=5.3.1
requests>=2.23.0
scipy>=1.4.1
torch>=1.7.0
torchvision>=0.8.1
tqdm>=4.64.0
# Logging -------------------------------------
# tensorboard>=2.13.0
# dvclive>=2.12.0
# clearml
# comet
# Plotting ------------------------------------
pandas>=1.1.4
seaborn>=0.11.0
# Export --------------------------------------
# coremltools>=7.0.b1  # CoreML export
# onnx>=1.12.0  # ONNX export
# onnxsim>=0.4.1  # ONNX simplifier
# nvidia-pyindex  # TensorRT export
# nvidia-tensorrt  # TensorRT export
# scikit-learn==0.19.2  # CoreML quantization
# tensorflow>=2.4.1  # TF exports (-cpu, -aarch64, -macos)
# tflite-support
# tensorflowjs>=3.9.0  # TF.js export
# openvino-dev>=2023.0  # OpenVINO export
# Extras --------------------------------------
psutil  # system utilization
py-cpuinfo  # display CPU info
# thop>=0.1.1  # FLOPs computation
# ipython  # interactive notebook
# albumentations>=1.0.3  # training augmentations
# pycocotools>=2.0.6  # COCO mAP
# roboflow
```
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
## 继续训练
```bash
yolo detect train data=ultralytics/models/yolo/Fair/mydata.yaml model=yolov8n.yaml pretrained=last.pt epochs=100 imgsz=640 resume=True
```
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
# 导出([[rknn部署导出TorchScript形式]])
```bash
yolo export model=/home/aorus/Desktop/WJ/Code/ultralytics/runs/detect/train13/weights/best.pt format=onnx opset=12
```
* `opset`和onnx版本有关
* `torch模型` 在部署的情况下,保存格式会有大问题，[[pytorch模型保存三种格式]]
* [[rknn导出格式的修改]]
### 推理导出的onnx模型
```bash
yolo predict model=/home/aorus/Desktop/WJ/Code/ultralytics/runs/detect/train13/weights/best.onnxsource=/home/aorus/Desktop/WJ/Code/ultralytics/1.jpg device=0,1
```
### 问题
* 修改时尽量修改defuault.yaml,不新建
* voc格式训不起来直接串成COCO
	* [函数](voc_to_coco.py)
* yolo的初始配置如储存位置什么的，在`.config`