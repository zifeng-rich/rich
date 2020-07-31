官方文档
> https://docs.docker.com/reference/

- [docker安装](#docker安装)
- [docker命令](#docker命令)
- [Dockerfile](#Dockerfile)

# docker安装
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

# docker命令  
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

# Dockerfile
**FROM**： 基础镜像，定制的镜像都基于基础镜像
```
示例：
FROM nginx
```  
多个FROM  
```
FROM golang:1.10.3
COPY server.go /build/
WORKDIR /build
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 GOARM=6 go build -ldflags '-w -s' -o server
# 运行阶段
FROM scratch
# 从前一个阶段中拷贝结果到当前镜像中
COPY --from=0 /build/server /
ENTRYPOINT ["/server"]
```
--from=0参数，从前边的阶段中拷贝文件到当前阶段中，多个FROM语句时，0代表第一个阶段。除了使用数字，我们还可以给阶段命名，比如：
```
# 编译阶段 命名为 builder
FROM golang:1.10.3 as builder
COPY server.go /build/
WORKDIR /build
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 GOARM=6 go build -ldflags '-w -s' -o server
# 运行阶段
FROM scratch
# 从编译阶段的中拷贝编译结果到当前镜像中
COPY --from=builder /build/server /
```
更为强大的是，COPY --from不但可以从前置阶段中拷贝，还可以直接从一个已经存在的镜像中拷贝。比如  
```
FROM ubuntu:16.04
COPY --from=quay.io/coreos/etcd:v3.3.9 /usr/local/bin/etcd /usr/local/bin/
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