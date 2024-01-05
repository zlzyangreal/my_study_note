# git 命令操作
## 文件基础操作
1. git init  创建.git文件
2. git remote -v  查看是否连接到仓库 
## 分支操作
1. git fetch  更新分支图  
2. git checkout -b zlzyang 创建新分支
3. git push origin zlzyang:zlzyang 把新建的本地分支push到远程服务器，远程分支与本地分支同名
4. git branch  查看当前本地分支
5. git branch -r   查看远程的所有分支   
6. git branch -m master 将本地分支切换到master分支
7. git branch -d localBranchName 删除本地分支
8. git push origin --delete remoteBranchName 删除远程分支
## 推拉操作
1. git pull origin develop  拉develop分支
2. git push origin master 会直接推到master分支
3. git pull origin zlzyang:master 合并到master分支
4. git push origin master:develop  将本地的master分支合并到develop仓库分支 
-------



