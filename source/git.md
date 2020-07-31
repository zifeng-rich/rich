- [git安装](#git安装)
- [git命令](#git命令)

# git安装
```
1.安装依赖
yum install curl-devel expat-devel gettext-devel openssl-devel zlib-devel gcc perl-ExtUtils-MakeMaker
2.下载源码
git clone https://github.com/git/git.git
3.编译
make prefix=/usr/local/git
4.安装
make prefix=/usr/local/git install
5.配置环境变量
vim /etc/profile
添加下面配置,并保存：
PATH=$PATH:/usr/local/git/bin
export PATH
6.刷新/etc/profile
source /etc/profile
7.测试
git version
```

# git命令

下载代码
```
git clone https://github.com/git/git.git
```
从远程仓库更新代码
```
git pull
or
# 从指定远程仓库更新
git pull origin dev
```
将修改的文件添加到提交列表
```
git add Dockerfile
or 
git add .
```
从提交列表中移除
```
git reset Dockerfile
or 
git reset .
```
提交修改列表
```
git commit -m "修改备注"
```
推送修改到远程仓库
```
git push
or
# 推送到指定远程仓库
git push origin dev
```
查看提交记录
```
git log
or
# 查看近5次提交
git log -n 5
```
回滚远程仓库到某次提交记录
```
1. git reset {commitId}
2. git push origin HEAD -f
```
拉取某次提交记录到新分支
```
git checkout -b tmp {commitId}
```
从当前分支新建一个分支
```
git branch tmp
```