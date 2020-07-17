# notes
笔记
##  目录
- [linux](#linux)
    - [常用命令](#常用命令)
- [docker](#docker)
    - [安装](#安装)
    - [命令](#命令)
    - [Dockerfile](#Dockerfile)
- [kubernetes](#kubernetes)
    - [架构](#架构)
    - [常用命令](#常用命令)
- [ceph](#ceph)
- [etcd](#etcd)
- [java](#java)
- [groovy](#groovy)
- [pipeline](#pipeline)
- [mysql](#mysql)
- [mongodb](#mongodb)
- [redis](#redis)
- [RabbitMQ](#RabbitMQ)
- [Apollo](#Apollo)
- [Consul](#Consul)


## linux

### 常用命令
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
ps -ef |grep nginx |awk '{print $2}'  #只输出第二列
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
## docker

### 安装
1. 卸载旧版本  
```
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```
2.安装 Docker Engine-Community  
>官方源地址：
```
$ sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
```
>阿里云地址：
```
$ sudo yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
3.安装 Docker Engine-Community  
```
$ sudo yum install docker-ce docker-ce-cli containerd.io
```
4.启动docker  
```
$ sudo systemctl start docker
```

### 命令  
查找镜像：  
```
docker search busybox
```
获取镜像：
```
docker pull busybox
```
运行镜像：
```
docker run --name mybusybox -itd -p 80:80 -v /data:/data busybox

参数：
-d: 后台运行容器，并返回容器ID；
-i: 以交互模式运行容器，通常与 -t 同时使用；
-p: 指定端口映射，格式为：主机(宿主)端口:容器端口
-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
--name="nginx-lb": 为容器指定一个名称
--expose=[]: 开放一个端口或一组端口；
--volume , -v: 绑定一个卷,格式为：主机(宿主)目录:容器目录
```
查看容器日志：
```
docker logs -f mybusybox
or
docker logs -f {containerId}
```
进入到容器：
```
docker exec -it mybusybox sh
docker exec -it mybusybox bash
or
docker exec -it {containerId} sh
docker exec -it {containerId} bash
```
复制宿主机文件到容器：
```
docker cp /test.txt mybusybox:/
or
docker cp /test.txt {containerId}:/
```
从容器复制文件到宿主机：
```
docker cp mybusybox:/test.txt /
or
docker cp {containerId}:/test.txt /
```
构建镜像：
```
docker build -t demo:v1 .

参数：
--build-arg=[] :设置镜像创建时的变量；
-f :指定要使用的Dockerfile路径；
--tag, -t: 镜像的名字及标签，通常 name:tag 或者 name 格式；可以在一次构建中为一个镜像设置多个标签。
--network: 默认 default。在构建期间设置RUN指令的网络模式
```
删除镜像：
```
docker rmi demo:v1
```
列出本地镜像：
```
docker images
```
停止容器：
```
docker stop mybusybox
or
docker stop {containerId}
```
移除容器：
```
docker rm mybusybox
or
docker rm {containerId}

注：需停止容器才能移除容器
```
列出所有容器：
```
docker ps -a
```
停止所有容器:
```
docker ps -a |awk '{print $1}' |xargs docker stop 
```
移除所有容器:
```
docker ps -a |awk '{print $1}' |xargs docker rm  
```
删除所有未使用的镜像：
```
docker system prune -a -f
参数：
--all , -a		删除所有未使用的镜像
--force , -f		不提示确认
```

### Dockerfile
**FROM**： 基础镜像，定制的镜像都基于基础镜像
```
示例：
FROM nginx
```  
**LABEL**： 添加元数据信息到镜像 
```
示例：
LABEL maintainer="芳华" version="1.0" description="描述信息"
```  
**RUN**： 构建镜像时执行的命令
```
示例：
RUN <command>  （shell 格式）
["executable", "param1", "param2"]  （exec 格式）
```
**COPY**： 从上下文目录中复制文件或者目录到容器里指定路径
>上下文路径，是指docker在构建镜像，有时候想要使用到本机的文件，docker build 命令得知这个路径后，会将路径下的所有内容打包。
 由于docker的运行模式是C/S。我们本机是 C，docker 引擎是 S。实际的构建过程是在docker引擎下完成的，所以这个时候无法用到我们本机的文件。这就需要把我们本机的指定目录下的文件一起打包提供给 docker 引擎使用。
 如果未说明最后一个参数，那么默认上下文路径就是Dockerfile所在的位置。
```
示例：
COPY dist /web/
```
**ADD**： ADD与COPY作用一样，唯一的区别ADD会自动复制并解压到目标路径（官方推荐使用 COPY）  
```
示例：
ADD hom* /mydir/
```
**CMD**： 为启动的容器指定默认要运行的程序，程序运行结束，容器也就结束。CMD 指令指定的程序可被 docker run 命令行参数中指定要运行的程序所覆盖。如果Dockerfile中如果存在多个CMD指令，仅最后一个生效。
```
示例：
CMD command param1 param2 （shell形式）
CMD ["executable","param1","param2"] （exec形式）
CMD ["param1","param2"] （作为ENTRYPOINT的默认参数）
```
**ENTRYPOINT**：类似于 CMD 指令，但其不会被 docker run 的命令行参数指定的指令所覆盖
```
示例：
ENTRYPOINT ["executable", "param1", "param2"]  （exec形式，优选的形式）
ENTRYPOINT command param1 param2  （shell形式）
```
**WORKDIR**： 指定工作目录。WORKDIR指令可以多次使用，如果提供了相对路径，则它将相对于上一条WORKDIR指令的路径 。
```
示例：
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
#最终的输出pwd命令结果是/a/b/c
```
**ARG**： 构建参数，ARG设置的环境变量仅对Dockerfile内有效，也就是说只有docker build的过程中有效。docker build中可用--build-arg <参数名>=<值>来覆盖
```
示例：
ARG user1=someuser
```
**ENV**： 设置容器环境变量
```
ENV <key> <value>
ENV <key>=<value> <key2>=<value2> ...
```
**EXPOSE**： 指定容器运行时监听的端口，docker run中可以使用-p 来覆盖
```
示例：
EXPOSE 80/tcp
EXPOSE 80/udp
```
**nginx镜像示例**：  
```
[Dockerfile]
---
ADD file:9fb8fd8bf970c4134f555964fe485a3baa84f1d4c91c5aa35276c24404de9d5d in /
CMD ["bash"]
LABEL maintainer=NGINX Docker Maintainers <docker-maint@nginx.com>
ENV NGINX_VERSION=1.19.0
ENV NJS_VERSION=0.4.1
ENV PKG_RELEASE=1~buster
/bin/sh -c set -x ...
COPY file:d68fadb480cbc781c3424ce3e42e1b5be80133bdcce2569655e90411a4045da2 in / 
COPY file:b96f664d94ca7bbe69241468d85ee421e9d310ffa36f3b04c762dcce9a42c7f1 in /docker-entrypoint.d
COPY file:cc7d4f1d03426ebd11e960d6a487961e0540059dcfad14b33762f008eed03788 in /docker-entrypoint.d
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["nginx" "-g" "daemon off;"]
```
```
[docker-entrypoint.sh]
---
#!/usr/bin/env sh
# vim:sw=4:ts=4:et

set -e

if [ "$1" = "nginx" -o "$1" = "nginx-debug" ]; then
    if /usr/bin/find "/docker-entrypoint.d/" -mindepth 1 -maxdepth 1 -type f -print -quit 2>/dev/null | read v; then
        echo "$0: /docker-entrypoint.d/ is not empty, will attempt to perform configuration"

        echo "$0: Looking for shell scripts in /docker-entrypoint.d/"
        find "/docker-entrypoint.d/" -follow -type f -print | sort -n | while read -r f; do
            case "$f" in
                *.sh)
                    if [ -x "$f" ]; then
                        echo "$0: Launching $f";
                        "$f"
                    else
                        # warn on shell scripts without exec bit
                        echo "$0: Ignoring $f, not executable";
                    fi
                    ;;
                *) echo "$0: Ignoring $f";;
            esac
        done

        echo "$0: Configuration complete; ready for start up"
    else
        echo "$0: No files found in /docker-entrypoint.d/, skipping configuration"
    fi
fi

exec "$@"
```

##  kubernetes

###  架构
<p align="right">
    <img src="/images/2.png" width=""/>
</p>
<p align="right">
    <img src="/images/3.png" width=""/>
</p>
在这张系统架构图中，我们把服务分为运行在工作节点上的服务和组成集群级别控制板的服务。  

Kubernetes主要由以下几个核心组件组成：

- etcd保存了整个集群的状态；
- apiserver提供了资源操作的唯一入口，并提供认证、授权、访问控制、API注册和发现等机制；
- controller manager负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- scheduler负责资源的调度，按照预定的调度策略将Pod调度到相应的机器上；
- kubelet负责维护容器的生命周期，同时也负责Volume（CVI）和网络（CNI）的管理；
- Container runtime负责镜像管理以及Pod和容器的真正运行（CRI）；
- kube-proxy负责为Service提供cluster内部的服务发现和负载均衡；  

除了核心组件，还有一些推荐的Add-ons：
- kube-dns负责为整个集群提供DNS服务
- Ingress Controller为服务提供外网入口
- Heapster提供资源监控
- Dashboard提供GUI
- Federation提供跨可用区的集群
- Fluentd-elasticsearch提供集群日志采集、存储与查询


### 常用命令

创建Deployment
```
# 创建一个nginx.yaml文件
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-demo
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
# 创建Deployment
kubectl -n default apply -f nginx.yaml
注：-n 指定命名空间，不指定默认为default
```
查看命名空间下pod 列表
```
kubectl -n default get po
or
kubectl -n default get pod
or
kubectl -n default get pods
```
查看pod日志
```
kubectl -n default logs -f nginx-demo-xxxxxxx
```
进入到pod容器内
```
kubectl -n default exec -it nginx-demo-xxxxxxx sh
or
kubectl -n default exec -it nginx-demo-xxxxxxx bash
```
查看pod模板
```
kubectl -n default get po nginx-demo-xxxxxxx -o yaml
or
kubectl -n default get po nginx-demo-xxxxxxx -o json
```
查看pod更多信息
```
kubectl -n default describe po nginx-demo-xxxxxxx
or
kubectl -n default get po nginx-demo-xxxxxxx -o wide
```
复制宿主机文件到pod
```
# 复制当前路径下test.txt到容器根目录
kubectl -n default cp test.txt nginx-demo-xxxxxxx:/
```
从容器复制文件到宿主机
```
从容器复制test.txt到宿主机根目录
kubectl -n default cp nginx-demo-xxxxxxx:/test.txt /
```
删除pod
```
kubectl -n default delete po nginx-demo-xxxxxxx
```
查看deployment列表
```
kubectl -n default get deploy
```
删除deployment
```
kubectl -n default delete deploy nginx-demo
```
