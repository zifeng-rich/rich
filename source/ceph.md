官方文档
>https://docs.ceph.com/docs/master/

- [ceph简介](#ceph简介)
- [ceph存储集群](#ceph存储集群)
    - [存储设备](#存储设备)
    - [启动和停止集群](#启动和停止集群)
    - [健康检查](#健康检查)
    - [监控集群](#监控集群)
- [ceph块设备](#ceph块设备)
    - [基本命令](#基本命令)

# ceph简介

无论您是要向Cloud Platforms提供Ceph对象存储和/或 Ceph块设备服务，部署Ceph文件系统还是将Ceph用于其他目的，所有Ceph Storage Cluster部署都要从设置每个Ceph节点，
您的网络和Ceph开始存储集群。一个Ceph存储群集至少需要一个Ceph监视器，Ceph管理器和Ceph OSD（对象存储守护程序）。运行Ceph文件系统客户端时，也需要Ceph Metadata Server。
<p align="center">
    <img src="/images/1.png">
</p>

- **监视器：** Ceph Monitor（ceph-mon）维护集群状态的映射，包括监视器映射，管理器映射，OSD映射，MDS映射和CRUSH映射。这些映射是Ceph守护程序相互协调所需的关键群集状态。
监视器还负责管理守护程序和客户端之间的身份验证。通常至少需要三个监视器才能实现冗余和高可用性。
  
- **管理器：** Ceph Manager守护进程（ceph-mgr）负责跟踪运行时指标和Ceph集群的当前状态，包括存储利用率，当前性能指标和系统负载。Ceph Manager守护程序还托管基于python的模块，
以管理和公开Ceph集群信息，包括基于Web的Ceph仪表板和 REST API。高可用性通常至少需要两个管理器。

- **Ceph OSD：** Ceph OSD（对象存储守护程序， ceph-osd）存储数据，处理数据复制，恢复，重新平衡，并通过检查其他Ceph OSD守护程序的心跳来向Ceph监视器和管理器提供一些监视信息。
通常至少需要3个Ceph OSD才能实现冗余和高可用性。

- **MDS：** Ceph元数据服务器（MDS，ceph-mds）代表Ceph文件系统存储元数据（即Ceph块设备和Ceph对象存储不使用MDS）。Ceph的元数据服务器允许POSIX文件系统的用户来执行基本的命令
（如 ls，find没有放置在一个Ceph存储集群的巨大负担，等等）。

Ceph将数据作为对象存储在逻辑存储池中。使用 CRUSH算法，Ceph计算哪个放置组应包含该对象，并进一步计算哪个Ceph OSD守护程序应存储该放置组。CRUSH算法使Ceph存储集群能够动态扩展，重新平衡和恢复。


# ceph存储集群
该Ceph的存储集群是所有Ceph的部署奠定了基础。基于RADOS，Ceph存储群集由两种类型的守护程序组成：Ceph OSD守护程序 （OSD）将数据作为对象存储在存储节点上。和Ceph的监视器（MON）维持群集映射的主副本。
一个Ceph存储集群可能包含数千个存储节点。一个最小的系统将至少具有一个Ceph Monitor和两个Ceph OSD守护程序用于数据复制。  

Ceph文件系统，Ceph对象存储和Ceph块设备从Ceph存储集群读取数据并将数据写入Ceph存储集群。  

## 存储设备

有两个在磁盘上存储数据的Ceph守护程序：

- Ceph OSD（或对象存储守护程序）是大多数数据存储在Ceph中的地方。一般而言，每个OSD都由单个存储设备（例如传统硬盘（HDD）或固态磁盘（SSD））支持。OSD也可以由多种设备组合来支持，例如用于大多数数据的
HDD和用于某些元数据的SSD（或SSD的分区）。群集中OSD的数量通常取决于存储的数据量，每个存储设备的容量以及冗余（复制或擦除编码）的级别和类型。

- Ceph Monitor 守护程序管理关键的群集状态，例如群集成员身份和身份验证信息。对于较小的群集，只需要几GB的容量，尽管对于较大的群集，监控器数据库可以达到数十或可能数百GB的容量。

OSD后端可以通过两种方式管理它们存储的数据。从Luminous 12.2.z版本开始，新的默认（推荐）后端是 BlueStore。在Luminous之前，默认（也是唯一的选项）是 FileStore。

## 启动和停止集群

启动或停止所有守护程序
```
# 要在Ceph节点上启动所有守护进程（与类型无关），请执行以下操作：
sudo systemctl start ceph-all

# 要停止Ceph节点上的所有守护程序（与类型无关），请执行以下操作：
sudo systemctl stop ceph-all
```
按类型启动或停止所有的守护程序
```
# 要在Ceph节点上启动特定类型的所有守护程序，请执行以下操作之一：
sudo start ceph-osd-all
sudo start ceph-mon-all
sudo start ceph-mds-all

# 要停止Ceph节点上所有特定类型的守护程序，请执行以下操作之一：
sudo stop ceph-osd-all
sudo stop ceph-mon-all
sudo stop ceph-mds-all
```
启动或停止守护进程
```
# 要在Ceph节点上启动特定的守护程序实例，请执行以下操作之一：
sudo start ceph-osd id={id}
sudo start ceph-mon id={hostname}
sudo start ceph-mds id={hostname}

# 要在Ceph节点上停止特定的守护程序实例，请执行以下操作之一：
sudo stop ceph-osd id={id}
sudo stop ceph-mon id={hostname}
sudo stop ceph-mds id={hostname}
```

## 健康检查


## 监控集群

**使用命令行交互模式**  
```
# 要ceph以交互方式运行该工具，请ceph在命令行中键入，不带参数。例如：
ceph
ceph> health
ceph> status
ceph> quorum_status
ceph> mon stat
```
**检查集群状态**  
```
ceph status
```
**观查集群**  
```
ceph -w
```
**监视健康检查**   

Ceph会根据自己的状态不断运行各种健康检查。当运行状况检查失败时，这将反映在（或 ）的输出中。此外，还会将消息发送到集群日志，以指示检查何时失败以及集群何时恢复。ceph statusceph health 
 
例如，当OSD发生故障时，health状态输出的部分可能会更新如下：
```
health: HEALTH_WARN
        1 osds down
        Degraded data redundancy: 21/63 objects degraded (33.333%), 16 pgs unclean, 16 pgs degraded
```
这时，还会发出集群日志消息以记录运行状况检查失败：
```
2017-07-25 10:08:58.265945 mon.a mon.0 172.21.9.34:6789/0 91 : cluster [WRN] Health check failed: 1 osds down (OSD_DOWN)
2017-07-25 10:09:01.302624 mon.a mon.0 172.21.9.34:6789/0 94 : cluster [WRN] Health check failed: Degraded data redundancy: 21/63 objects degraded (33.333%), 16 pgs unclean, 16 pgs degraded (PG_DEGRADED)
```
当OSD重新联机时，群集日志将记录群集返回到运行状况的状态：
```
2017-07-25 10:11:11.526841 mon.a mon.0 172.21.9.34:6789/0 109 : cluster [WRN] Health check update: Degraded data redundancy: 2 pgs unclean, 2 pgs degraded, 2 pgs undersized (PG_DEGRADED)
2017-07-25 10:11:13.535493 mon.a mon.0 172.21.9.34:6789/0 110 : cluster [INF] Health check cleared: PG_DEGRADED (was: Degraded data redundancy: 2 pgs unclean, 2 pgs degraded, 2 pgs undersized)
2017-07-25 10:11:13.535577 mon.a mon.0 172.21.9.34:6789/0 111 : cluster [INF] Cluster is now healthy
```
**网络性能检查**  
Ceph OSD在它们之间发送心跳ping消息以监视守护程序的可用性。我们还使用响应时间来监视网络性能。虽然繁忙的OSD可能会延迟ping响应，但我们可以假设，如果网络交换机发生故障，则会在不同的OSD对之间检测到多个延迟。

默认情况下，我们将警告ping时间超过1秒（1000毫秒）。
```
HEALTH_WARN Slow OSD heartbeats on back (longest 1118.001ms)
```

**检查集群的使用情况统计信息**  
要检查群集在池中的数据使用情况和数据分布，可以使用该df选项。它类似于Linux df。执行以下命令：
```
ceph df
```
**检查OSD状态**  
```
ceph osd stat
```
**检查监视器状态**  
```
ceph mon stat
```
**检查MDS状态**  
```
ceph mds stat
```

# ceph块设备
一块是字节序列（例如，一个512字节的数据块）。基于块的存储接口是使用旋转介质（例如硬盘，CD，软盘甚至传统的9轨磁带）存储数据的最常用方法。块设备接口的无处不在使虚拟块设备成为与海量数据存储系统（如Ceph）
进行交互的理想候选者。  

Ceph块设备经过精简配置，可调整大小，并在Ceph集群中的多个OSD上存储条带化数据。Ceph块设备利用了 RADOS功能，例如快照，复制和一致性。Ceph的 RADOS块设备（RBD）使用内核模块或librbd库与OSD进行交互。
<p align="center">
    <img src="/images/4.png">
</p>
Ceph的的块设备提供了无限的可扩展性，以高性能的 内核模块，或者KVM系列如QEMU和基于云计算系统，如OpenStack的和的CloudStack依赖的libvirt和QEMU与Ceph的块设备集成。您可以使用同一集群同时运行Ceph RADOS网关，
Ceph文件系统和Ceph块设备。

## 基本命令
创建一个块设备池
```
rbd pool init <pool-name>
```
创建块设备映像
```
rbd create --size {megabytes} {pool-name}/{image-name}
注： {megabytes} 单位为 GB
```
列出块设备映像
```
rbd ls {poolname}

# 列出特定池中的延迟删除块设备
rbd trash ls {poolname}
```
检索图像信息
```
rbd info {pool-name}/{image-name}
```
调整块设备映像的大小
```
rbd resize --size 2048 foo 
rbd resize --size 2048 foo --allow-shrink
```
删除块设备的图像
```
rbd rm {pool-name}/{image-name}

# 推迟从池中删除块设备
rbd trash mv {pool-name}/{image-name}
```
恢复块设备映像
```
rbd trash restore {pool-name}/{image-id}
```
