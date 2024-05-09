在 /usr/local 目录下软连接cuda
1. 删除原来的cuda软连接
```bash
sudo rm -rf cuda
```
2. 连接新的cuda版本
```bash
sudo ln -s /usr/local/cuda-12.3 /usr/local/cuda
```
* 以12.3版本为例
3. 查看当前cuda版本
```bash
nvcc --version
```