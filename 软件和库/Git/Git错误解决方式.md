Git：解决报错：fatal: The remote end hung up unexpectedly
问题原因：推送的文件太大。
解决方式：**修改设置git config文件的postBuffer的大小**
```git
//修改为500M
$ git config --local http.postBuffer 524288000
```
**过于太大了直接分批次上传**
