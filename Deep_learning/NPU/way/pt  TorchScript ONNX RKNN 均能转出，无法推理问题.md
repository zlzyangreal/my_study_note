* pt文件是权重文件，训练出的best.pt，不存在问题
* TorchScript与ONNX是用野火修改头部后的主分支和负分支产物（我怀疑存在网上说的[置信度大于1，并且图像乱框问题](https://blog.csdn.net/zfenggo/article/details/136017885),也有其他可能这两篇帖子或许有参考价值）
		1. [自定义数据训练的rknn模型部署踩坑记录](https://blog.csdn.net/level_code/article/details/133810652)
		2.[ 模型 RKNN 量化模型后检测框失准](https://github.com/rockchip-linux/rknn-toolkit/issues/110)
* RKNN转换函数问题，这里我确定我成功的转换TorchScript到RKNN，应该可以排除这个可能，但是主流还是PT到ONNX到RKNN