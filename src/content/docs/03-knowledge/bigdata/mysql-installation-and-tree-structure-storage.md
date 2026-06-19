---
status: completed
filename: mysql-installation-and-tree-structure-storage
title: "MySQL 树状结构"
summary: 本笔记涵盖了 MySQL 关系型数据库的 Docker 部署及基础权限管理操作。重点深入探讨了在关系型数据库中存储树状结构（Tree Structure）的架构选型，对比了邻接表与枚举路径的优劣，并详细提供了一种折中且高效的“闭包表（存储完整树路径）”设计方案。通过具体的 SQL 示例，展示了如何基于该模型实现后代查询、祖先追溯、子树移动及节点删除等复杂的层级操作。
aliases: [MySQL 树状结构, 闭包表设计, 关系型数据库树形存储]
tags: [数据库, MySQL, 数据库设计, 树状结构, 闭包表, 架构设计, SQL]
date created: 星期四, 十月 9日 2025, 10:34:30 上午
date modified: 星期四, 六月 18日 2026, 10:45:00 晚上
---

<!-- toc -->

## 1. 基础环境部署与管理

### 1.1. Docker 容器化安装

使用 `docker-compose` 快速拉起指定版本，并挂载数据卷：

```yaml
version: '3.1'
services:
  db:
    image: mysql:8.0.26
    # 兼容旧版客户端密码认证
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    volumes: 
      - './data:/var/lib/mysql'
      - './conf:/etc/mysql'
    ports:
      - '3306:3306'
    environment:
      MYSQL_ROOT_PASSWORD: example
```

### 1.2. 核心用户与权限管理 SQL

```sql
-- 创建新用户并赋予全库权限
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';

-- 修改密码与刷新权限树
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

---

## 2. 进阶：树状结构 (Tree Structure) 的存储设计方案

在关系型数据库中存储层级关系（如部门架构、多级评论）一直是经典难题。

### 2.1. 常见方案对比

1. **邻接表 (Adjacency List)**：仅存 `parent_id`。设计极简，但查询整个子树极其复杂（需递归）。
2. **枚举路径 (Path Enumeration)**：存完整路径 `1/3/4/`。增删改查较简单，但强依赖 `LIKE` 查询，且路径长度受限。
3. **嵌套集 (Nested Sets)**：存左右值 `lft`, `rgt`。查询极快，但任何节点的增删都会导致全表大面积更新，实现极度复杂。

### 2.2. 推荐方案：闭包表 (Closure Table / Tree Path)

维护一张额外的关联表 `tree_path`，保存图中所有节点间祖先与后代的 **所有连通路径** 及深度。这是一种在查询效率和维护成本间取得平衡的优秀设计。

#### 2.2.1. 核心表结构

- 主表 `comments` (仅存节点本身的数据)
- 闭包表 `tree_path` (包含 `ancestor_id`, `descendant_id`, `depth`)

#### 2.2.2. 核心 SQL 实战

**1. 查询节点 000 的所有后代 (子树)**

```sql
SELECT c.* FROM comments c 
JOIN tree_path t ON c.comment_id = t.descendant_id 
WHERE t.ancestor_id = '000' AND t.depth != 0;
```

**2. 查询节点 003 的所有祖先 (链路)**

```sql
SELECT c.* FROM comments c 
JOIN tree_path t ON c.comment_id = t.ancestor_id 
WHERE t.descendant_id = '003' AND t.depth != 0;
```

**3. 插入新节点 004 (作为 001 的子节点)**
*逻辑：将 001 的所有祖先也作为 004 的祖先，深度+1，并插入 004 指向自身的零深度记录。*

```sql
INSERT INTO tree_path (ancestor_id, descendant_id, depth)
SELECT t.ancestor_id, '004', t.depth + 1
FROM tree_path
WHERE t.descendant_id = '001'
UNION ALL
SELECT '004', '004', 0;
```

**4. 删除 001 的整棵子树**

```sql
DELETE FROM tree_path
WHERE descendant_id IN (
  SELECT descendant_id FROM tree_path WHERE ancestor_id = '001'
);
```

*(注：移动节点通常采用“先删除旧关联，再插入新关联”的组合策略。)*

## 3. 参考资料

- [关系型数据库的树状结构存储探讨](https://howiefh.github.io/2020/05/06/relational-database-storage-tree-structure/)
