---
title: "Postgresql安装"
filename: postgresql-database-administration
description: PostgreSQL是功能强大的开源对象关系型数据库。本文罗列了PostgreSQL的基础操作，包含APT包管理器的裸机安装、基于Docker Compose的轻量部署，并系统解释了所有者权限体系、多模式隔离机制，以及多表继承的定义，为数据库日常管理和架构选型提供指导。
tags: [postgresql, rdbms, database-administration, docker-compose]
aliases: [Postgresql安装, PG模式隔离, Postgresql配置]
status: completed
date created: 星期一, 十二月 1日 2025, 9:59:28 上午
date modified: 星期五, 六月 19日 2026, 12:07:30 中午
---

<!-- toc -->

## 1. 简介

对象关系型数据库管理系统

## 2. 安装

### 2.1. 直接安装

```shell
apt install postgresql
```

### 2.2. Docker 安装

- docker-compose
...

- 启动

```shell
docker-compose up -d
```

## 3. 概念

### 3.1. 所有者

所有者是数据库对象的创建者，通常是创建对象的数据库用户。所有者拥有对该对象的完全控制权，包括权限管理、修改和删除对象等。

### 3.2. 模式

一个模式可以包含视图、索引、数据类型、函数和操作符等。

相同的对象名称可以被用于不同的模式中而不会出现冲突，例如 schema1 和 myschema 都可以包含名为 mytable 的表。

- 允许多个用户使用一个数据库并且不会互相干扰。
- 将数据库对象组织成逻辑组以便更容易管理。
- 第三方应用的对象可以放在独立的模式中，这样它们就不会与其他对象的名称发生冲突。

### 3.3. 权限

- SELECT：允许用户查询表中的数据。
- INSERT：允许用户向表中插入数据。
- UPDATE：允许用户更新表中的现有数据。
- DELETE：允许用户从表中删除数据。
- TRUNCATE：允许用户快速删除表中的所有行。
- REFERENCES：允许用户在外键约束中引用该表。
- USAGE：适用于序列、模式等，允许用户使用该对象。
- CREATEDB：创建数据库
- CONNECT：链接权限
- CREATEROLE：创建角色
- SUPERUSER：管理员权限
- LOGIN：登录权限

### 3.4. 角色

1.1 postgres  
描述：这是 PostgreSQL 安装时创建的默认超级用户角色。  
权限：具备最高权限，可以执行所有数据库操作，包括创建数据库、创建角色、备份数据库等。  
用途：通常用于数据库的管理和维护，建议在日常操作中使用其他角色，以降低安全风险。  

1.2 pg_read_all_data  
描述：这是一个内置角色，用于授予读取所有数据的权限。  
权限：允许角色访问数据库中的所有表、视图和序列的读取权限。  
用途：适用于需要读取所有数据但不需要修改数据的用户。  

1.3 pg_write_all_data  
描述：这是一个内置角色，用于授予写入所有数据的权限。  
权限：允许角色对数据库中的所有表、视图和序列进行写入操作。  
用途：适用于需要对所有数据进行修改的用户。  

1.4 pg_execute_server_program  
描述：这个角色允许执行服务器程序。  
权限：使得用户可以调用 pg_proc 中定义的函数。  
用途：适用于需要执行特定数据库函数的角色。  

1.5 pg_monitor  
描述：这个角色用于监控数据库状态。  
权限：允许角色查看所有数据库的状态信息、性能统计信息和活动。  
用途：适用于需要监控数据库性能和活动的用户。  

1.6 pg_signal_backend  
描述：这个角色用于发送信号给其他进程。  
权限：允许角色发送信号以终止或中断其他数据库进程。  
用途：适用于需要管理和控制数据库并发连接的用户。  

```sql
CREATE ROLE my_role;
GRANT SELECT, INSERT ON my_table TO manager;
GRANT my_role TO my_user;
ALTER ROLE my_user CREATEDB;# 修改权限
```

### 3.5. 范本

模板数据库是用于生成新数据库的原型。PostgreSQL 默认提供两个模板数据库：

- template0：这是一个只读模板，包含一个干净的 PostgreSQL 安装的基本结构。这个模板不能被修改，通常用于创建全新的数据库。
- template1：这是一个可修改的模板，用户可以在此基础上添加扩展、表、数据等。每当你创建一个新数据库时，PostgreSQL 会默认使用 template1 作为基础。

### 3.6. 表空间

定义：表空间是一个数据库对象的逻辑命名空间，它映射到文件系统中的一个目录，可以包含数据库中的表、索引和其他对象。

作用：通过使用表空间，用户可以将不同的数据库对象存储在不同的物理位置，从而实现数据分离和存储管理。

## 4. 配置

```
# /etc/postgresql/{version}/main/postgresql.conf
port=5433
```

## 5. 使用

### 5.1. 管理服务

```shell
systemctl restart postgresql 
systemctl status postgresql 
systemctl stop postgresql 
```

### 5.2. 连接

```shell
sudo -i -u postgres #初始化用户
psql #进入交互模式
psql -U username -d database_name
\du #查看当前的用户
\l #查看数据库机器权限
\dt #查看数据库中的所有表
\q # 退出交互
\conninfo #查看当前链接信息
\c + 数据库名 #进入数据库
\password postgre #设置密码
\d tablename #查看表结构
```

### 5.3. 常用 sql

```sql
SELECT current_database(); #查看当前数据库
SELECT current_user; #查看当前用户
CREATE USER username WITH PASSWORD 'password'; 创建用户
ALTER USER postgres WITH PASSWORD '你的新密码'; 
CREATE DATABASE your_database OWNER your_username; 创建数据库
GRANT ALL PRIVILEGES ON DATABASE postgres TO your_username; 数据库授权
GRANT ALL PRIVILEGES ON TABLE your_table TO your_username; 表授权
REVOKE ALL PRIVILEGES ON DATABASE your_database FROM your_username; 撤销权限
```

## 6. 拓展信息

### 6.1. 与 mysql 对比

- 相同
  - 都已 sql 作为查询与编辑数据的接口

## 7. 参考资料

- [官方链接](https://www.postgresql.org/download/)
