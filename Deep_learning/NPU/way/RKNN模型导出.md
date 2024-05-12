# TorchScript文件
## 1.修改文件名
编译模型转换程序，将torchscript模型（**需要注意load_pytorch导入的模型后缀是.pt，模型需要重新命名**）转换成rknn模型
## 2.直接转
```bash
python3 pt2rknn.py yolov8n_rknnopt.pt rk3588
```
# onnx
需要修改一下转换文件，也是直接转