官方文档
>https://kubernetes.io/docs/tasks/configure-pod-container

- [kubernetes架构](#kubernetes架构)
- [kubectl命令](#kubectl命令)
- [Deployment](#Deployment)
- [PV/PVC](#PV/PVC)
- [Service](#Service)
- [Ingress](#Ingress)
- [Volumes](#Volumes)
- [ConfigMap](#ConfigMap)
 

#  kubernetes架构
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

# kubectl命令

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
or
kubectl -n default create -f nginx.yaml
注：-n 指定命名空间，不指定默认为default
```
查看命名空间下pod 列表
```
kubectl -n default get po
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
or
# 输出指定内容
kubectl -n default get po nginx-demo-xxxxxxx -o=custom-columns=LABELS:.metadata.labels.app
注：LABELS是自定义列名
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
kubectl get
```
#列出资源列表和简写
kubectl api-resources

# 查看命名空间
kubectl get namespace
or 
kubectl get ns

# 查看配置
kubectl get cm

# 查看service
kubectl get svc

# 查看ingress
kubectl get ing
```

# Deployment  

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

# Service

```
apiVersion: v1
kind: Service
metadata:
  labels:
    run: nginx
  name: nginx-service
spec:
  ports:
  - port: 80    #容器的端口
    protocol: TCP
    targetPort: 80   #pod的端口
  selector:
    app: nginx
  type: ClusterIP
```

# Ingress
```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-ingress
spec:
  rules:
  - http:
      paths:
      - path: /
        backend:
          serviceName: nginx-service   #service名称
          servicePort: 80        #service port
```
# PV/PVC

**介绍**  
PersistentVolume（PV）是集群中已由管理员配置的一段网络存储。
PersistentVolumeClaim（PVC）是用户存储的请求。  

**Persistent Volumes 例子**
```
apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv0003
  spec:
    capacity:
      storage: 5Gi
    accessModes:
      - ReadWriteOnce
    persistentVolumeReclaimPolicy: Recycle
    storageClassName: slow
    nfs:
      path: /tmp
      server: 172.17.0.2
```

**PersistentVolumeClaims**
```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 8Gi
  storageClassName: slow
  selector:
    matchLabels:
      release: "stable"
    matchExpressions:
      - {key: environment, operator: In, values: [dev]}
```

**Deployment中声明PVC作为Volumes**
```
kind: Pod
apiVersion: v1
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: dockerfile/nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

# Volumes
容器中的磁盘的生命周期是短暂的，这就带来了一系列的问题，第一，当一个容器损坏之后，kubelet 会重启这个容器，但是文件会丢失-这个容器会是一个全新的状态，
第二，当很多容器在同一Pod中运行的时候，很多时候需要数据文件的共享。Kubernete Volume解决了这个问题  

Kubernete 支持如下类型的volume:  
```
emptyDir
hostPath
gcePersistentDisk
awsElasticBlockStore
nfs
iscsi
glusterfs
rbd
gitRepo
secret
configMap
persistentVolumeClaim
```

**emptyDir**  
一个emptyDir 第一次创建是在一个pod被指定到具体node的时候，并且会一直存在在pod的生命周期当中，
正如它的名字一样，它初始化是一个空的目录，pod中的容器都可以读写这个目录，这个目录可以被挂在到各个
容器相同或者不相同的的路径下。当一个pod因为任何原因被移除的时候，这些数据会被永久删除

**hostPath**  
一个hostPath类型的磁盘就是挂在了主机的一个文件或者目录，这个功能可能不是那么常用，但是这个功能提供了一个很强大的突破口对于某些应用来说  
例如，如下情况我们旧可能需要用到hostPath  
- 某些应用需要用到docker的内部文件，这个时候只需要挂在本机的/var/lib/docker作为hostPath
- 在容器中运行cAdvisor，这个时候挂在/dev/cgroups

**awsElasticBlockStore**  
一个awsElasticBlockStore是一个挂在aws EBS 磁盘到我们的pod中，和emptyDir不同的是，emptyDir会被删除当我们的Pod被删除的时候，
但是awsElasticBlockStore不会被删除，仅仅是解除挂在状态而已,这就意味着EBS能够允许我们提前对数据进行处理，而且这些数据可以在Pod之间相互传递.  
注意，我们首先要使用aws api或者图形操作界面创建EBS 在我们使用之前awsElasticBlockStore 有如下几个限制：
- 节点必须运行在aws的虚拟机上
- 节点和卷宗必须在同一个区域
- EBS只支持单个EC2的实例进行挂载

**nfs**  
nfs使的我们可以挂在已经存在的共享到的我们的Pod中，和emptyDir不同的是，emptyDir会被删除当我们的Pod被删除的时候，但是nfs不会被删除，
仅仅是解除挂在状态而已，这就意味着NFS能够允许我们提前对数据进行处理，而且这些数据可以在Pod之间相互传递.并且，nfs可以同时被多个pod挂在并进行读写

**iscsi**  
iscsi允许将现有的iscsi磁盘挂载到我们的pod中，和emptyDir不同的是，emptyDir会被删除当我们的Pod被删除的时候，但是iscsi不会被删除，
仅仅是解除挂在状态而已，这就意味着iscsi能够允许我们提前对数据进行处理，而且这些数据可以在Pod之间相互传递

**rbd**  
rbd允许Rados Block Device格式的磁盘挂载到我们的Pod中，同样的，当pod被删除的时候，rbd也仅仅是被解除挂载，就意味着rbd能够允许我们提前对数据
进行处理，而且这些数据可以在Pod之间相互传递

**Secrets**  
一个Secrets磁盘是存储敏感信息的磁盘，例如密码之类。我们可以将secrets存储到api中，使用的时候以文件的形式挂载到pod中，而不用连接api,Secrets
是通过tmpfs来支撑的，所有secrets永远不会存储到不稳定的地方

# ConfigMap

创建ConfigMap
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
  labels:
      addonmanager.kubernetes.io/mode: EnsureExists
data:
  Corefile: |
    .:53 {
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          upstream /etc/resolv.conf
          fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf {
          prefer_udp
        }
        cache 30
        loop
        reload
        loadbalance
    }
    service.consul:53 {
        errors
        cache 30
        forward . 127.0.0.1
    }
```
在Deployment中引用
```
# 挂载到容器指定目录
volumeMounts:
- mountPath: /etc/coredns
  name: config-volume

# 引用ConfigMap
volumes:
- configMap:
  items:
  name: coredns
name: config-volume
```