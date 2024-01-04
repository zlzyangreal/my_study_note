### 命令
1. git init  创建.git文件
2. git remote -v  查看是否连接到仓库 
3. git fetch  更新分支图  
4. git checkout -b zlzyang 创建新分支
5. git push origin zlzyang:zlzyang 把新建的本地分支push到远程服务器，远程分支与本地分支同名
4. git branch  查看当前本地分支
5. git branch -r   查看远程的所有分支   
6. git branch -m master 将本地分支切换到master分支
7. git pull origin develop  拉develop分支
8. git push origin master 会直接推到master分支
9. git pull origin zlzyang:master 合并到master分支
10. git push origin master:develop  将本地的master分支合并到develop仓库分支 
-------

### push错误

```上传容量
1.Total 18 (delta 0), reused 0 (delta 0), pack-reused 0
2.fatal: the remote end hung up unexpectedly
3.Everything up-to-date
```
------

use指令： git config http.sslVerify "false"




