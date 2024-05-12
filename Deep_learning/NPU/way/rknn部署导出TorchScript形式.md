整个测试型导出，**注意测试的是rk_opt_v1分支**， 该分支将导出torchscript模型，如果使用main分支默认导出onnx模型
# 首先[[rknn导出格式的修改]]
## 其次配置default.yaml
更换模型为要转换模型
## 导出TorchScript
```bash
# 导入整个python文件夹，目的是调用当前工程，避免调库(调库没有参数传入会是默认值 yolov8n.yaml和TorchScript)
# 我们需要的是rknn(野火自加的format，生成的是适合NPU的推理格式)
export PYTHONPATH=./
python ./ultralytics/engine/exporter.py
```