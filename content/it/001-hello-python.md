---
Title: Hello Python — 你的第一个Python程序
Date: 2026-06-24
Category: python
Tags: python
Series: python入门
Series_index: 2
Author: 悠游
Summary: 欢迎来到Python的世界！这节课我们将了解Python是什么、写出第一行代码。
---


第一阶段：基础语法

## 第一课：Hello Python — 你的第一个Python程序

欢迎来到Python的世界！这节课我们将了解Python是什么、写出第一行代码。

## 一、理论知识

### 1.1 什么是Python？

Python是一种**高级、解释型、通用编程语言**，由Guido van Rossum于1991年发布。它的设计哲学强调代码可读性和简洁的语法。

为什么选择Python？

- **简单易学**：语法接近自然语言，零基础也能快速上手
- **应用广泛**：Web开发、数据分析、人工智能、自动化脚本、游戏开发……
- **生态丰富**：拥有超过40万个第三方库（PyPI）
- **跨平台**：Windows、macOS、Linux都能运行

### 1.2 Python如何工作？

Python是**解释型语言**。这意味着代码不是像C语言那样预先编译成机器码，而是由Python解释器逐行读取并执行。

```
# 工作流程：
你写的代码  →  Python解释器  →  计算机执行
```

### 1.3 两种运行方式

Python有两种主要使用方式：

| 方式               | 说明                            | 适用场景               |
| :----------------- | :------------------------------ | :--------------------- |
| **交互式（REPL）** | 逐行输入，立即看到结果          | 测试小段代码、学习探索 |
| **脚本模式**       | 把代码写入 .py 文件，一次性运行 | 实际项目、复杂程序     |

### 1.4 print() 函数

`print()` 是Python最常用的内置函数，用于在屏幕上输出内容。

```
print("Hello, World!")
print("你好", "世界")
print(42)
```

Hello, World! 你好 世界 42

## 二、实操演示

### 2.1 使用交互式Python

打开终端（命令提示符），输入 `python`（Windows）或 `python3`（macOS/Linux），进入交互模式：

```
$ python
Python 3.12.0
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello, Python!")
Hello, Python!
>>> exit()
```

### 2.2 编写Python脚本

创建一个名为 `hello.py` 的文件，写入以下内容：

```
# hello.py - 我的第一个Python程序
print("Hello, World!")
print("我正在学习Python")
print("Python真有趣！")
```

在终端中运行：

```
$ python hello.py
Hello, World!
我正在学习Python
Python真有趣！
```

### 2.3 使用注释

`#` 后面的文字是注释，Python不会执行它们。注释用来解释代码的目的。

```
# 这是单行注释
print("注释不影响程序运行")

# 下面计算 2 的 10 次方
print(2 ** 10)  # 输出 1024
```

## 三、动手练习

练习 1.1：自我介绍 简单

创建一个名为 `intro.py` 的文件，让它输出以下三行内容：

1. 你的名字（可以用任意字符串代替）
2. 一句话介绍你为什么学Python
3. 一句鼓励自己的话

**提示**：每行用一个 `print()` 函数。

练习 1.2：数学计算器 简单

在Python交互模式中，直接输入以下表达式，观察输出结果：

- `100 + 250`
- `17 * 23`
- `1000 / 7`
- `2 ** 10`
- `100 % 7`

想一想：哪个运算符表示"取余数"？哪个表示"幂运算"？

练习 1.3：趣味输出 中等

编写一个脚本 `fun.py`，输出如下图案：

   ^__^  (o__o)\  (__)  )\_______     ((    /\      ||--w |      ||    ||

**提示**：每一行用单独的 `print()`。

## 四、本课要点

- Python是解释型语言，代码由解释器逐行执行
- 有两种运行方式：交互式（REPL）和脚本模式（.py文件）
- `print()` 用于输出内容到屏幕
- `#` 开头的文字是注释，不会被执行
- 每个Python脚本保存为 `.py` 后缀的文件

📚 推荐阅读

[Python官方教程 - 引言](https://docs.python.org/zh-cn/3/tutorial/index.html) — 官方文档的入门章节，权威且详细。

💡 学习建议

不要只是阅读代码，一定要亲手敲一遍！肌肉记忆对编程学习非常重要。如果练习中遇到问题，随时向AI助手提问。
