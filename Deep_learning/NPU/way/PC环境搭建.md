# 1.创建虚拟环境
```bash
conda create -n RKNN python=3.8.10
conda activate RKNN
```
* **会与YOLOv8 ultralytics冲突，务必建一个新环境**
## 下载依赖项
```bash
sudo apt update
sudo apt-get install python3-dev python3-pip python3.8-venv gcc
sudo apt-get install libxslt1-dev zlib1g-dev libglib2.0 libsm6 \
libgl1-mesa-glx libprotobuf-dev gcc

pip3 install numpy
# 在doc文件夹下
# 这里不能偷懒挨着装，很容易出问题
pip3 install 包==版本 
```
### **普通包**
```txt
依赖项
# base deps
numpy==1.19.5
protobuf==3.12.2
flatbuffers==1.12

# utils
requests==2.27.1
psutil==5.9.0
ruamel.yaml==0.17.4
scipy==1.5.4
tqdm==4.64.0
opencv-python==4.5.5.64
fast-histogram==0.11

# base
onnx==1.10.0
onnxoptimizer==0.2.7
onnxruntime==1.10.0
```
### **特殊包**
1.pytorch
* 注意cuda版本，这里使用的pytorch版本是 **1.10.1** ，`torchvision==0.11.2`
查看cuda版本
```bash
nvidia-smi
```
* [[cuda不同版本切换]]