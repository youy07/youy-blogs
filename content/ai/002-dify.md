---
Title: 在 Debian 虚拟机上部署 Dify
Date: 2026-06-27
Category: dify
Tags: dify
Series: dify入门
Series_index: 2
Author: 悠游
Summary: 在你的 Debian 虚拟机上，用 Docker Compose 一键部署 Dify，并完成初始化设置，看到 Dify 的登录页面
---

第二课

# 在 Debian 虚拟机上部署 Dify

跟着步骤走，5 分钟让你的第一个 AI 平台跑起来

⏱ 预计时间：15-20 分钟（不含镜像下载等待时间）

🎯 本课目标

在你的 Debian 虚拟机上，用 Docker Compose 一键部署 Dify，并完成初始化设置，看到 Dify 的登录页面。

## 一、前置检查

在动手之前，先确认你的 Debian 虚拟机已经准备好：

✅ 你需要有的

- 一台运行中的 Debian 虚拟机（推荐 Debian 12）
- 已安装 Docker Engine（如果没装，下面有步骤）
- 虚拟机网络可访问外网
- Windows 宿主机能 ping 通虚拟机 IP（桥接模式最佳）
- 虚拟机至少 4GB 内存 + 20GB 空闲磁盘

### 检查 Docker 是否已安装

debian-vm ~

$ docker --version Docker version 27.5.1, build 9f9e405 $ docker compose version Docker Compose version v2.32.4

Docker 已有，直接跳到第 2 步

没有 Docker？→ 往下看"安装 Docker"

### 如果没装 Docker，先装它

```
# 1. 安装依赖 sudo apt update sudo apt install -y ca-certificates curl gnupg lsb-release # 2. 添加 Docker 官方源 sudo install -m 0755 -d /etc/apt/keyrings curl -fsSL https://download.docker.com/linux/debian/gpg | \  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg echo \  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \  https://download.docker.com/linux/debian $(lsb_release -cs) stable" | \  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null # 3. 安装 Docker sudo apt update sudo apt install -y docker-ce docker-ce-cli containerd.io \  docker-buildx-plugin docker-compose-plugin # 4. 将当前用户加入 docker 组（避免每次输 sudo） sudo usermod -aG docker $USER # ⚠️ 然后注销重新登录（或执行 newgrp docker）
```

**⚠️ 国内镜像加速** —— 如果不配置，拉取 Dify 镜像可能很慢（有时会超时）。强烈建议执行下面这步：

```
sudo mkdir -p /etc/docker sudo tee /etc/docker/daemon.json <<-'EOF' {  "registry-mirrors": [    "https://docker.m.daocloud.io",    "https://hub-mirror.c.163.com",    "https://mirror.baidubce.com"  ],  "log-driver": "json-file",  "log-opts": {    "max-size": "10m",    "max-file": "3"  } } EOF sudo systemctl daemon-reload sudo systemctl restart docker
```

## 二、部署 Dify

### Step 1：克隆 Dify 仓库

```
git clone https://github.com/langgenius/dify.git cd dify/docker
```

成功后会看到`dify/docker/`目录，里面有`docker-compose.yml`和`.env.example`

### Step 2：创建配置文件

```
cp .env.example .env
```

默认配置已经可以直接使用。如果你后续需要调整模型密钥、数据库密码等，后续再修改 `.env` 文件。

### Step 3：启动 Dify

```
# 启动所有服务（后台运行） docker compose up -d # 查看启动状态 docker compose ps
```

首次启动会拉取镜像，需要等待几分钟（取决于网络速度）。**这是最耗时的步骤，耐心等待。**

debian-vm ~/dify/docker

$ docker compose up -d [+] Running 6/6 ✔ Container dify-nginx-1       Started ✔ Container dify-api-1         Started ✔ Container dify-worker-1      Started ✔ Container dify-web-1         Started ✔ Container db-1               Started ✔ Container redis-1            Started

看到所有容器都是 **Up** 状态，就说明启动成功了。

### Step 4：检查日志（可选）

```
# 查看 Dify API 的启动日志 docker compose logs dify-api --tail=50 # 如果某服务挂了，查看具体错误 docker compose logs [服务名] --tail=100
```

## 三、初始化设置

### Step 5：访问 Dify

在 **Windows 浏览器**（而非虚拟机内）访问：

访问地址

http://你的虚拟机IP

💡 如何查看虚拟机 IP？在 Debian 里执行 `ip addr show | grep 'inet '`

桥接模式 vs NAT 模式

**桥接模式**：虚拟机有独立 IP（如 192.168.1.105），可直接访问
**NAT 模式**：需要在 VirtualBox 设置端口转发（主机 80 → 子系统 80）

在浏览器打开的页面应该是这样的：

首次访问会自动跳转到**初始化管理员账号页面**

### Step 6：创建管理员账号

1. 填写邮箱、姓名、密码
2. 点击"创建管理员"
3. 登录进入 Dify 控制台

**💡 建议**：使用真实邮箱，后续找回密码、邮件通知等功能会用到。密码用强密码（大小写 + 数字 + 特殊字符）。

### Step 7：接入大模型（关键一步！）

Dify 本身不包含大模型，需要你自己配置 API Key。进入控制台后：

```
设置 → 模型供应商 → 添加模型
```

如果是国内用户，推荐以下两种方式：

#### 🅰️ DeepSeek（推荐）

- 注册：platform.deepseek.com
- 新用户送 500 万 Token
- 便宜、中文好、速度快

#### 🅱️ 通义千问

- 注册：dashscope.aliyun.com
- 有免费额度赠送
- 阿里生态，国内访问稳定

配置完成后，你就可以创建你的第一个 AI 应用了！

## 四、常见问题排查

❌ 浏览器打不开页面

- 确认虚拟机 IP 正确：`ip addr show`
- 检查防火墙：`sudo iptables -L -n`，必要时关掉：`sudo iptables -F`
- 确认容器在运行：`docker compose ps`
- NAT 模式需配置端口转发

❌ 容器启动后不断重启（Restarting）

- 查看日志：`docker compose logs 容器名`
- 常见原因：端口被占用、.env 配置错误、内存不足
- 尝试重启整个服务：`docker compose restart`

❌ 拉取镜像超时

- 检查 Docker 镜像加速是否配置正确（参照前面的国内镜像配置）
- 尝试单独拉取：`docker pull nginx:latest` 测试网络
- 挂梯子或换用国内镜像源

❌ 权限不足（Permission denied）

- 执行 `sudo usermod -aG docker $USER` 后记得**注销重新登录**
- 或用 `newgrp docker` 立即生效
- 临时方案：所有命令前加 `sudo`

## 五、验证部署成功

按照以下清单确认一切正常：

☑️ 部署完成检查清单

- ✅ 浏览器能打开 Dify 初始化页面
- ✅ 成功创建管理员账号并登录
- ✅ 成功配置至少一个模型供应商（DeepSeek / 通义千问）
- ✅ 能看到 Dify 主控制台（工作台页面）

debian-vm ~/dify/docker

$ docker compose ps NAME                IMAGE                           STATUS       PORTS dify-api            langgenius/dify-api:1.1.3         Up 2 hours   5001/tcp dify-web            langgenius/dify-web:1.1.3         Up 2 hours   3000/tcp dify-worker         langgenius/dify-worker:1.1.3     Up 2 hours   5001/tcp dify-nginx          nginx:latest                      Up 2 hours   0.0.0.0:80->80/tcp db                  postgres:15-alpine                 Up 2 hours   5432/tcp redis               redis:7-alpine                     Up 2 hours   6379/tcp

## 六、日常管理命令

部署完成后，记住这几个常用命令就够了：

```
# 启动 / 停止 / 重启 docker compose start docker compose stop docker compose restart # 查看实时日志（按 Ctrl+C 退出） docker compose logs -f # 更新 Dify（备份后执行） docker compose pull docker compose up -d # 彻底卸载 docker compose down -v
```

**⚠️ docker compose down -v 会删除所有数据（包括数据库和向量库）**，生产环境千万别乱用！

## 七、本节课重点回顾

- ✅ 确认 Docker 环境已就绪（需 Docker + Docker Compose）
- ✅ 配置国内镜像加速，避免拉取超时
- ✅ `git clone` → `cp .env.example .env` → `docker compose up -d` 三步搞定部署
- ✅ 通过 **Windows 浏览器 → 虚拟机 IP** 访问 Dify
- ✅ 创建管理员账号 → 配置大模型 API Key → 开始使用
- ✅ 记住日常管理命令（启动/停止/日志）

**▶ 下一课预告**

第 3 课：模型接入与配置实战——DeepSeek 通义千问任你挑

部署已完成，下一步就是让你的 Dify 真正"有脑可动"——配置大模型！

------

## 参考资料

- [Dify 官方文档 - 快速开始](https://docs.dify.ai/zh/use-dify/getting-started/introduction)
- [Dify 官方文档 - 服务器安装](https://docs.dify.ai/zh/use-dify/installation/install-server)
- [Dify GitHub 仓库](https://github.com/langgenius/dify)
- [Docker 官方文档 - Debian 安装指南](https://docs.docker.com/engine/install/debian/)

部署遇到问题随时问我！发一下你的报错信息，我帮你排查 🚀
