- [linux命令](#linux命令)

# linux命令
查看进程
```
ps -u root //显示root进程用户信息
ps -ef //显示所有命令，连带命令行
```
查看端口 
```
lsof -i:8000
netstat -tunlp | grep 8000
```
查找文件或文件夹
```
find / -name test  //在根目录查找包含test的文件或文件夹
```
grep的使用
```
grep test *conf  #在后缀有“conf”的文件中查找包含“test”字符串的文件  
grep -v test *conf #在后缀有“conf”的文件中查找不包含“test”字符串的文件
kubectl get po |grep nginx
```
awk的使用
```
输出指定列
ps -ef |grep nginx |awk '{print $1}'
or
ps -ef |grep nginx |awk 'NF=1'
输出指定行
ps -ef |grep nginx |awk 'NR=1'
```
xargs的使用
```
ps -ef |grep nginx |awk '{print $2}' |xargs kill -9  #将前一个命令的结果作为参数
```
sort的使用
```
ps -ef|awk '{print $2}'|sort -k 1 -n -r 
-k :指定按第几列排序
-n :按数值排序
-r :以相反的顺序来排序
```
查看文件或目录大小
```
du log2012.log
du /tmp
du -sh /tmp
```
将文件内容转化为字符串参数
```
./etcdctl put foo "`cat foo.json`"
```
文件授权
```
chmod [ugoa...][+-=][rwxX] file
u 表示该文件的拥有者，g 表示与该文件的拥有者属于同一个群体(group)者，o 表示其他以外的人，a 表示这三者皆是。
+ 表示增加权限、- 表示取消权限、= 表示唯一设定权限。
r 表示可读取，w 表示可写入，x 表示可执行，X 表示只有当该文件是个子目录或者该文件已经被设定过为可执行。
```
将结果输出到文件
```
echo 123 > test.txt  #原有的内容会覆盖
echo 123 >> test.txt #追加到原有内容的后面
```