---
Title: Python安装与环境搭建
Date: 2026-06-24
Category: python
Tags: python
Series: python入门
Series_index: 1
Author: 悠游
Summary: python之路，万里长征第一步，纪念一下。
---

# 预备课：Python安装与环境搭建

在开始写代码之前，我们需要先准备好Python的运行环境。这节课会手把手带你完成安装和配置。

## 一、检查是否已安装

### Windows

按 `Win + R`，输入 `cmd` 打开命令提示符，然后输入：

```
python --version
```

如果显示 `Python 3.x.x`，说明已安装。如果显示"不是内部或外部命令"，则需要安装。

### macOS

打开"终端"（Spotlight搜索"Terminal"），输入：

```
python3 --version
```

macOS通常自带Python 2.7（已废弃），我们需要安装Python 3。

### Linux

```
python3 --version
```

## 二、Windows 安装Python

### 步骤1：下载安装包

打开浏览器，访问 Python 官网：

https://www.python.org/downloads/windows/

点击页面中央的大按钮 **"Download Python 3.x.x"**（最新版）。

### 步骤2：运行安装程序

1. 双击下载的 `python-3.x.x-amd64.exe`
2. **务必勾选** `✅ Add Python to PATH`（这一步非常重要！）
3. 点击 **"Install Now"**

⚠️ 重要提醒

安装时如果不勾选 **"Add Python to PATH"**，后续很多操作都会出问题。如果忘了勾选，需要卸载后重新安装。

### 步骤3：验证安装

关闭之前的命令提示符，重新打开一个新的，输入：

```
python --version
```

Python 3.12.x

看到版本号就说明安装成功了！

### 步骤4：验证 pip

pip 是Python的包管理工具，用来安装第三方库：

```
pip --version
```

pip 24.x.x from ... (python 3.12)

## 三、macOS 安装Python

### 方法1：用 Homebrew（推荐）

如果你已经安装了Homebrew（macOS最常用的包管理器）：

```
brew install python3
```

### 方法2：从官网下载

1. 访问 [python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/)
2. 下载 macOS 安装包
3. 双击安装，按提示操作

### 验证安装

```
python3 --version
pip3 --version
```

## 四、Linux 安装Python

### Ubuntu/Debian

```
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### CentOS/RHEL

```
sudo yum install python3 python3-pip
```

### 验证安装

```
python3 --version
pip3 --version
```

## 五、选择代码编辑器

安装好Python后，你需要一个写代码的工具。推荐以下两种：

### VS Code（强烈推荐）

微软出品，免费、轻量、功能强大，支持Python智能提示和调试。

1. 下载：[code.visualstudio.com](https://code.visualstudio.com/)
2. 安装后，点击左侧扩展图标（方块图标）
3. 搜索 **"Python"**，安装 Microsoft 官方的 Python 扩展

### PyCharm（备选）

JetBrains出品，专业的Python IDE，功能更全面但较重。

1. 下载：[jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download/)
2. 免费版（Community）足够初学者使用

## 六、虚拟环境（重要概念）

虚拟环境让你可以为每个项目创建独立的Python环境，避免不同项目的依赖冲突。

### 创建虚拟环境

```
# Windows
python -m venv myproject_env

# macOS / Linux
python3 -m venv myproject_env
```

### 激活虚拟环境

```
# Windows（CMD）
myproject_env\Scripts\activate

# Windows（PowerShell）
myproject_env\Scripts\Activate.ps1

# macOS / Linux
source myproject_env/bin/activate
```

激活成功后，命令行前面会出现 `(myproject_env)` 标记。

### 退出虚拟环境

```
deactivate
```

## 七、第一次运行Python

### 方法1：交互式模式（REPL）

在终端中输入 `python`（Windows）或 `python3`（macOS/Linux）：

```
$ python
>>> print("Hello, Python!")
Hello, Python!
>>> exit()
```

### 方法2：用VS Code运行

1. 打开VS Code
2. 文件 → 新建文件 → 保存为 `hello.py`
3. 输入：`print("Hello, World!")`
4. 右键 → "Run Python File in Terminal"

## 八、动手练习

练习 0.1：验证安装 简单

在终端中依次输入以下命令，确认都能正常运行：

1. `python --version` 或 `python3 --version`
2. `pip --version` 或 `pip3 --version`
3. 进入交互模式，计算 `2 ** 10`
4. 退出交互模式

练习 0.2：创建虚拟环境 简单

在你的项目目录下创建一个名为 `python_course` 的虚拟环境，并激活它。

**验证**：激活后，命令行提示符前面应该显示 `(python_course)`。

练习 0.3：安装第一个第三方库 简单

在激活的虚拟环境中，安装 requests 库：

```
pip install requests
```

然后在Python交互模式中验证：

```
>>> import requests
>>> requests.__version__
```

## 九、本课要点

- Windows安装时务必勾选 **"Add Python to PATH"**
- macOS使用 `python3` 和 `pip3`
- 推荐安装 VS Code + Python 扩展作为开发环境
- 虚拟环境是每个Python项目的标配
- REPL（交互式模式）是学习和测试代码的好工具

💡 常见问题排查

- **"python不是内部命令"**：没有勾选PATH，重新安装
- **pip装不上**：尝试 `python -m pip install xxx`
- **VS Code不识别Python**：检查是否安装了Python扩展
