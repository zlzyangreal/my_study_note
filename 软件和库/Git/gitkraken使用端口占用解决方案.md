# gitkraken使用端口占用解决方案

1. 检测端口使用情况
```bash
netstat -ano
```
2. 杀死占用端口进程
`cmd taskkill /f /pid [进程号]`