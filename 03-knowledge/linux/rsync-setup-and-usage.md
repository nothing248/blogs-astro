---
title: "Rsync安装与使用"
filename: rsync-setup-and-usage
summary: Linux 下 Rsync 与 Sersync 实时文件同步解决方案。详述了 Rsync 本地与远程（SSH、Daemon模式）传输指令与参数。提供了 A 主机（运行 Sersync 监控文件变更）向 B 主机（运行 Rsyncd 守护进程）实时推送文件的配置方案，包括 Rsyncd 配置、密码文件安全管理、Sersync XML 配置、自动守护进程检测脚本及 Crontab 定时调度。
tags:
  - rsync
  - sersync
  - file-sync
  - linux-backup
  - real-time-replication
aliases:
  - Rsync安装与使用
  - Sersync实时同步配置
  - Linux备份方案
status: completed
date created: 星期二, 二月 25日 2025, 3:24:09 下午
date modified: 星期二, 六月 16日 2026, 6:24:21 晚上
---

<!-- toc -->

## 1. 简介

Rsync 是一个开源、快速、多功能、可实现全量及增量数据备份的优秀本地或远程文件同步工具。

## 2. 安装

```shell
apt install rsync
```

## 3. 命令

```shell
rsync -avh /source/directory/ /destination/directory/ # 本地同步
rsync -avh /source/directory/ username@remote_host:source/ # ssh 协议远程同步
rsync -avh --password-file=/etc/rsyncd.password /source/directory/ rsync@[IP已隐藏]::module  # rsync 协议远程同步, 需要远程主机启动 rsync 守护进程
```

- **常用参数说明**：
  - `-a` 或 `--archive`：归档模式，相当于 `-rlptgoD`（递归、保留符号链接、权限、时间戳、组、所有者、设备文件），是最常用的选项之一，通常用于备份操作。
  - `-v` 或 `--verbose`：详细模式，显示更多的操作信息。
  - `-z` 或 `--compress`：在传输时压缩文件，节省带宽。
  - `-o` 或 `--owner`：保留文件所有者信息。
  - `-g` 或 `--group`：保留文件组信息。
  - `-D` 或 `--devices`：保留设备文件（仅超级用户）。
  - `-h` 或 `--human-readable`：以可读的格式显示文件大小。
  - `-n` 或 `--dry-run`：执行模拟操作，不实际传输文件，仅用于测试。
  - `--delete`：删除目标目录中在源目录中不存在的文件。
  - `--partial`：允许中断后继续。
  - `--progress`：显示传输进度条。
  - `--exclude=PATTERN`：排除匹配指定模式的文件。
  - `--include=PATTERN`：包括匹配指定模式的文件。
  - `--bwlimit=RATE`：限制传输速率，单位为 KB/s。
  - `--ignore-existing`：只同步目标端不存在的新文件。
  - `-r` 或 `--recursive`：递归处理目录及其子目录。
  - `-l` 或 `--links`：保留符号链接。
  - `-p` 或 `--perms`：保留文件权限。
  - `-t` 或 `--times`：保留文件修改时间。
  - `--update`：只同步源端比目标端更新的文件。
  - `--backup`：启用备份，将源目录同步到目标目录的同时，将被覆盖的旧文件转移备份到指定目录。
  - `--password-file=/etc/rsyncd.password`：指定远程 rsync 守护进程的访问密码文件。

---

## 4. 使用

实现 A 主机文件实时更新自动同步到 B 主机。

### 4.1. B 主机

- **修改配置文件**

```ini
# /etc/rsyncd.conf
# /etc/rsyncd: configuration file for rsync daemon mode

uid = root
gid = root
use chroot = no
auth users = rsync
secrets file = /etc/rsyncd.secrets
max connections = 4
pid file = /var/run/rsyncd.pid
port = 873 # 默认端口号是873
log file = /var/log/rsyncd.log
lock file = /var/run/rsyncd.lock
read only = no 
transfer logging = yes
timeout = 900

[data]
path = /home/rsync/data
comment = test
```

- **添加验证文件**

```text
# /etc/rsyncd.secrets
rsync:test.     
```

- **启动服务**

```shell
systemctl start rsyncd
systemctl enable rsyncd
```

### 4.2. A 主机

- **验证文件**

```text
# /etc/rsyncd.password
rsync:test.     
```

- **测试同步文件**

```shell
rsync -avz --partial --password-file=/etc/rsyncd.password /home/app/test.txt rsync@[IP已隐藏]::data 
```

- **安装 sersync**  
  Sersync 是一款基于 Google 开源的，利用 inotify 技术实现监测文件变动的实时数据同步工具。

```shell
cd /usr/local/
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/sersync/sersync2.5.4_64bit_binary_stable_final.tar.gz
tar zxf sersync2.5.4_64bit_binary_stable_final.tar.gz
mv /usr/local/GNU-Linux-x86/ /usr/local/sersync
```

- **编辑 sersync 配置文件**

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<head version="2.5">
    <host hostip="localhost" port="8008"></host>
    <debug start="false"/>
    <fileSystem xfs="false"/>  <!-- 文件系统 -->
    <filter start="false">  <!-- 排除不想同步的文件 -->
        <exclude expression="(.*)\.svn"></exclude>
        <exclude expression="(.*)\.gz"></exclude>
        <exclude expression="^info/*"></exclude>
        <exclude expression="^static/*"></exclude>
    </filter>
    <inotify>  <!-- 监控的事件类型 -->
        <delete start="true"/>
        <createFolder start="true"/>
        <createFile start="true"/>
        <closeWrite start="true"/>
        <moveFrom start="true"/>
        <moveTo start="true"/>
        <attrib start="false"/>
        <modify start="false"/>
    </inotify>

    <sersync>
        <localpath watch="/data">  <!-- 监控的目录 -->
            <remote ip="0.0.0.0" name="data"/>  <!--服务端IP地址和模块-->
        </localpath>
        <rsync>
            <commonParams params="-arvtz"/>  <!--开启用户认证，虚拟用户和密码文件路径-->
            <auth start="true" users="rsync" passwordfile="/etc/rsyncd.password"/>
            <userDefinedPort start="false" port="873"/><!-- port=874 -->
            <timeout start="false" time="100"/><!-- timeout=100 -->
            <ssh start="false"/>
        </rsync>
        <failLog path="/tmp/rsync_fail_log.sh" timeToExecute="60"/><!--default every 60mins execute once  默认配置60分钟执行一次检查-->
        <crontab start="false" schedule="600"><!--600mins-->
            <crontabfilter start="false">
                <exclude expression="*.php"></exclude>
                <exclude expression="info/*"></exclude>
            </crontabfilter>
        </crontab>
        <plugin start="false" name="command"/>
    </sersync>

    <plugin name="command">
        <param prefix="/bin/sh" suffix="" ignoreError="true"/>    <!--prefix /opt/tongbu/mmm.sh suffix-->
        <filter start="false">
            <include expression="(.*)\.php"/>
            <include expression="(.*)\.sh"/>
        </filter>
    </plugin>

    <plugin name="socket">
        <localpath watch="/opt/tongbu">
            <deshost ip="[IP已隐藏]" port="8009"/>
        </localpath>
    </plugin>
    <plugin name="refreshCDN">
        <localpath watch="/data0/htdocs/cms.xoyo.com/site/">
            <cdninfo domainname="ccms.chinacache.com" port="80" username="xxxx" passwd="xxxx"/>
            <sendurl base="http://pic.xoyo.com/cms"/>
            <regexurl regex="false" match="cms.xoyo.com/site([/a-zA-Z0-9]*).xoyo.com/images"/>
        </localpath>
    </plugin>
</head>
```

- **启动 sersync 服务**

```shell
/usr/local/sersync/sersync2 -r -d -o /usr/local/sersync/confxml.xml >/usr/local/sersync/sersync2.log 2>&1 &
#-d: 启用守护进程模式
#-r: 在监控前，将监控目录与远程主机用 rsync 命令推送一遍
#-n: 指定开启守护线程的数量，默认为 10 个
#-o: 指定配置文件，默认使用 confxml.xml 文件
```

- **检测 sersync 服务**

```shell
# /app/local/sersync/check_sersync.sh
#!/bin/sh                                                                                                                                                                          
sersync="/usr/local/sersync/sersync2"                                                                                                                                              
confxml="/usr/local/sersync/confxml.xml"                                                                                                                                           
status=$(ps aux |grep 'sersync2'|grep -v 'grep'|wc -l)                                                                                                                             
if [ $status -eq 0 ];                                                                                                                                                              
then                                                                                                                                                                               
$sersync -d -r -o $confxml &                                                                                                                                                       
else                                                                                                                                                                               
exit 0;                                                                                                                                                                            
fi
```

- **定时检测守护**

```text
*/5 * * * * sh /app/local/sersync/check_sersync.sh >/dev/null 2>&1  # 检测同步脚本是否正常
```

---

## 5. 参考资料

- [syncthing](https://github.com/syncthing/syncthing)
