---
title: "Ansible安装配置"
filename: ansible-automation-playbook-guide
summary: Ansible 是一款基于 Python 的无代理（Agentless）自动化运维与配置管理工具。本笔记全面汇总了 Ansible 主从节点的安装授权、Inventory 主机清单（别名与整组变量）及配置文件读取机制，详述了 Adhoc 临时命令与 Playbooks 的实战语法。涵盖了软件安装、用户与目录管理、系统服务配置、文件多方式修改、磁盘分区挂载、调试与条件循环等核心任务，并提供了图形化管理面板 Ansible Semaphore 的 Systemd 定时配置方案。
tags: ["Ansible", "Playbook", "Automation-Ops", "Linux-Sysadmin", "Semaphore"]
aliases: ["Ansible安装配置", "Ansible剧本实战", "Semaphore部署"]
status: completed
date created: 星期二, 二月 25日 2025, 4:11:57 下午
date modified: 星期五, 六月 19日 2026, 11:57:07 中午
---

<!-- toc -->

## 1. 简介

一个自动化运维工具

## 2. 安装

### 2.1. 主节点

```shell
apt install python3-pip
apt install ansible #直接安装
python3 -m pip install --user ansible #python 安装
```

### 2.2. 子节点

```shell
vim ~/.ssh/authorized_keys # 添加对应的公钥
```

## 3. 配置

### 3.1. Inventory 配置

```
# /etc/ansible/hosts 
slave1:2022 #不同的端口号
jumper ansible_ssh_port=5555 ansible_ssh_host=192.168.1.50 ansible_connection=ssh ansible_ssh_user=mpdehaan ansible_ssh_private_key_file=~/.ssh/id_rsa#别名设置
slave2 http_port=80 maxRequestsPerChild=808 # 分配变量
slave3

[group1] # 分组
slave1
slave2

[group1:vars] # 整组变量
ntp_server=ntp.atlanta.example.com
proxy=proxy.atlanta.example.com
```

> [!important] 主机解析规则
> 注意需要现在/etc/hosts 中配置对应解析规则

### 3.2. 配置文件

```
# 读取顺序
# ANSIBLE_CONFIG (一个环境变量)
# ansible.cfg (位于当前目录中)
# .ansible.cfg (位于家目录中)
# /etc/ansible/ansible.cfg
```

## 4. 使用

### 4.1. Adhoc

```shell
ansible all -m ping 
# all/192.168.56.101 对应的主机
# -u demo 对应额 ssh 账户
# -m 对应命令
# --sudo 是否 sudo 运行
# -f 10 并发数量
```

### 4.2. Playbooks

```shell
ansible-playbook playbook.yml -f 10
```

- demo

```yaml
---
- hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  remote_user: root
  tasks:
  - name: ensure apache is at the latest version
    yum: pkg=httpd state=latest
  - name: write the apache config file
    template: src=/srv/httpd.j2 dest=/etc/httpd.conf
    notify:
    - restart apache
  - name: ensure apache is running
    service: name=httpd state=started
  handlers:
    - name: restart apache
      service: name=httpd state=restarted
```

- 安装软件

```yaml
- name: install software
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Install dependencies
      apt:
        name:
          - wget
          - unzip
        state: present #确定软件是否存在
      when: ansible_os_family == "Debian" #RedHat 判断系统
```

- 创建用户

```yaml
- name: create user
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Create system user
      user: 
          name: minio-user
          shell: /sbin/nologin
          system: yes # 创建系统用户
    - name: Createregular user
      user:
        name: regular_user  # 用户名
        shell: /bin/bash    # 设置用户的 shell
        home: /home/regular_user  # 设置用户的主目录
        password: "{{ 'your_password' | password_hash('sha512') }}"  # 设置用户密码（使用哈希加密）
        state: present  # 确保用户存在
```

- 创建目录

```yaml
- name: Create directory
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Create directory
      file:
        path: /mnt/minio
        state: directory
        mode: '0755'
        owner: minio-user
        group: minio-user
```

- 下载

```yaml
- name: Create directory
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Download binary
      get_url:
        url: "https://dl.min.io/server/minio/release/linux-amd64/minio"
        dest: /usr/local/bin/minio
        mode: '0755'
```

- 创建文件

```yaml
- name: Create directory
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Create MinIO service file
      copy:
        dest: /etc/systemd/system/minio.service
        content: |
          [Unit]
          Description=MinIO
          Documentation=https://min.io/docs/minio/linux/index.html
          Wants=network-online.target
          After=network-online.target

          [Service]
          User=minio-user
          ExecStart=/usr/local/bin/minio server /mnt/minio
          Restart=always
          Environment=MINIO_ACCESS_KEY=your_access_key
          Environment=MINIO_SECRET_KEY=your_secret_key

          [Install]
          WantedBy=multi-user.target
```

- 管理服务

```yaml
- name: Create directory
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Start and enable MinIO service
      systemd:
        name: minio
        state: started
        enabled: yes #是否自动开启
```

- 修改文件

```yaml
- name: Create directory
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Ensure a line is present in the file
      lineinfile:
        path: /path/to/your/file.txt  # 文件路径
        line: "This is a new line."    # 要添加或替换的行
        state: present                  # 确保该行存在
    - name: Insert a block of text into a file # 同文件只能存在一个
      blockinfile:
        path: /path/to/your/file.txt
        block: |
          This is a block of text.
          It can span multiple lines.
        state: present
        marker: "# {mark} zookeeper" # 使用该标记，否则可能新内容覆盖旧内容。注意：缺少{mark} 可能导致重复插入
    - name: Replace specific text in a file
      replace:
        path: /path/to/your/file.txt
        regexp: 'old text'            # 待替换的正则表达式
        replace: 'new text'          # 替换成的新文本
    - name: Create a configuration file from a template
      template:
        src: template.j2            # 模板文件路径
        dest: /path/to/your/file.txt # 目标文件路径
```

- 传输文件

```yaml
- name: Create directory
  hosts: demo  # 定义目标主机组
  become: yes  # 提升权限为 root
  tasks:
    - name: Copy a local file to the remote server
      copy:
        src: /path/to/local/file.txt
        dest: /path/to/remote/file.txt
```

- 分区

```yaml
- name: Create a new partition and format it
  hosts: vbox
  tasks:
    - name: Ensure parted is installed
      package:
        name:
          - parted
          - xfsprogs
        state: present

    - name: Create first primary partition
      parted:
        device: /dev/sdb
        number: 1
        state: present
        part_type: primary
        part_start: 0%
        part_end: 2.5GB

    - name: Format first partition to xfs
      filesystem:
        fstype: xfs
        dev: /dev/sdb1

    - name: Mount first partition
      mount:
        path: /mnt/minio1
        src: /dev/sdb1
        fstype: xfs
        state: mounted
```

- 解压文件

```yaml
- name: 解压文件示例
  hosts: localhost
  tasks:
    - name: 解压 ZIP 文件
      unarchive:
        src: /path/to/your/file.zip       # 源文件路径 tar.gz是否存在
        dest: /path/to/destination         # 解压目标路径
        remote_src: yes                    # 如果设置为 yes，表示源文件已经在目标主机上；如果为 no，Ansible 会尝试从控制节点复制文件到目标主机。
```

- 调试

```yaml
- name: 获取当前主机名
  hosts: vbox
  tasks:
    - name: 显示当前主机名
      debug:
        msg: "当前主机名是: {{ inventory_hostname }}"
    - name: 显示实际主机名
      debug:
        msg: "实际主机名是: {{ ansible_hostname }}"
    - name: 特定执行
      debug:
        msg: "特定主机执行: {{ ansible_default_ipv4.address }}"
      when: inventory_hostname == "slave1" # 注意此处变量不需要待{{}}
```

- 重复操作

```yaml
- name: Create multiple users
  hosts: localhost
  tasks:
    - name: Ensure users are present
      user:
        name: "{{ item }}"
        state: present
      loop:
        - alice
        - bob
        - charlie
```

- 检测目录是否存在

```yaml
- name: Unarchive file if not already extracted
  hosts: all
  tasks:
    - name: Check if the destination directory exists
      stat:
        path: /path/to/destination_directory
      register: dest_dir

    - name: Unarchive the file if the destination directory does not exist
      unarchive:
        src: /path/to/archive_file.tar.gz
        dest: /path/to/destination_directory
        remote_src: yes  # 如果 archive_file 是在目标主机上
      when: not dest_dir.stat.exists
```

- 检测命令是否存在

```yaml
- name: 检查命令是否存在
  command: which some_command # 使用 which 命令查找命令路径
  register: command_check
  ignore_errors: yes # 忽略命令不存在导致的错误
#  when: command_check.rc == 0 # 返回码为 0 表示命令存在
```

- 执行命令

```yaml
- name: install nvm
  command: /usr/local/nvm/install.sh
  environment:
    NVM_DIR: ${nvm_path}
```

### 4.3. Ansible Semaphore

一个简单的面板管理工具

- 安装

```shell
wget https://github.com/semaphoreui/semaphore/releases/\
download/v2.9.58/semaphore_2.9.44_linux_amd64.deb

sudo dpkg -i semaphore_2.9.44_linux_amd64.deb
```

- 配置 systemd

```shell
sudo cat > /etc/systemd/system/semaphore.service <<EOF
[Unit]
Description=Semaphore Ansible
Documentation=https://github.com/semaphoreui/semaphore
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/path/to/semaphore server --config=/path/to/config.json
SyslogIdentifier=semaphore
Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF
```

- 管理

```shell
sudo systemctl status semaphore
sudo systemctl start semaphore
sudo systemctl stop semaphore
sudo systemctl restart semaphore
```

## 5. 拓展信息

### 5.1. 环境依赖

- python
- pip

### 5.2. Python 版本可能存在见同行

及时将 ansible 升级为最新版本，建议使用 ansible ==9.13.0 版本或者 ansible-core== 2.16.14，可以支持 python2/3 版本

> <https://docs.ansible.org.cn/ansible/latest/reference_appendices/release_and_maintenance.html>

## 6. 参考资料

- [官方链接](https://www.ansible.com/)
- [中文文档](https://ansible-tran.readthedocs.io/en/latest/docs/)
- [Tower](https://docs.ansible.com/ansible-tower/latest/html/quickinstall/index.html)
- [Ansible Semaphore](https://docs.semaphoreui.com/administration-guide/installation#package-manager)
