---
title: "xargs-guide"
filename: linux-xargs-command-tutorial
summary: 本文梳理了 Linux 命令行工具 xargs 的核心作用与高频参数用法。xargs 可将标准输入转换为后续命令的参数，用于解决不支持管道参数传递的问题。文中通过实例详细讲解了调试输出（-t）、参数个数限制（-n）、自定义分隔符（-d）、占位符参数填充（-I）以及使用零字符（-0 / -print0）规避文件名空格风险的方案。
tags:
  - linux
  - bash
  - shell
  - command-line
  - xargs
aliases:
  - xargs-guide
  - shell-xargs
  - pipe-arguments
status: completed
---

<!-- toc -->

## 1. 简介

**xargs**（eXtended ARGuments）是 Linux 系统中给命令传递参数的一个过滤器。

- **核心功能**：它可以读取标准输入（stdin）、文件或管道输出，并将其转换为另一个命令的命令行参数。
- **解决痛点**：许多 Linux 命令（如 `echo`, `rm`, `mkdir` 等）本身 **不支持直接从管道接收参数**，xargs 充当了管道输出到命令参数的桥梁。

## 2. 常用参数及实例

### 2.1. `-t`：先打印命令后执行

启用调试输出模式，在执行命令之前，先在标准错误输出上打印出即将执行的完整命令。

```shell
echo "file1 file2" | xargs -t touch
# 输出：touch file1 file2
```

### 2.2. `-n`：指定每次执行的参数个数

限制每次命令调用时传递的参数最大数量。

假设 `test.txt` 内容如下：

```text
a b c d e f g
h i j k l m n
```

使用 `-n3` 限制每次仅传递 3 个参数：

```shell
cat test.txt | xargs -n3
```

输出结果：

```text
a b c
d e f
g h i
j k l
m n
```

### 2.3. `-d`：定义输入分隔符

xargs 默认以换行符和空格作为定界符。使用 `-d` 参数可以指定自定义的定界符。

```shell
echo "nameXnameXnameXname" | xargs -dX
```

输出结果（定界符 `X` 被替换为空格）：

```text
name name name name
```

### 2.4. `-I {}`：参数占位替换

使用指定的占位符（如 `{}`）在后续命令的特定位置进行参数替换。这允许你在命令的中间部位插入参数，而不仅仅是追加在尾部。

假设 `arg.txt` 内容如下：

```text
aaa
bbb
ccc
```

执行如下命令：

```shell
cat arg.txt | xargs -I {} echo "Prefix -> {} -> Suffix"
```

输出结果：

```text
Prefix -> aaa -> Suffix
Prefix -> bbb -> Suffix
Prefix -> ccc -> Suffix
```

### 2.5. `-0`：以 `\0` (Null) 作为定界符

当文件名包含空格、换行符或特殊字符时，默认的分隔符会导致 xargs 错误切割文件名。此时必须配合 `find` 命令的 `-print0` 参数使用。

```shell
find . -type f -name "*.log" -print0 | xargs -0 rm -f
```

> [!NOTE]
> `find -print0` 将输出的文件列表用空字符（null）进行分隔，而 `xargs -0` 则指示 xargs 仅以空字符作为分隔符。这是一种在脚本中处理未知文件名的安全最佳实践。

## 3. 参考资料

- [菜鸟教程 - Linux xargs 命令](https://www.runoob.com/linux/linux-comm-xargs.html)
