---
Title: OmniRoute入门:OmniRoute 简介与快速部署
Date: 2026-07-01
Category: ai
Tags: omniroute
Series: OmniRoute入门
Series_index: 1
Author: 悠游
Summary: 了解 免费 AI 网关：237 个提供商、其中 **90+ 个完全免费**,一个入口、永不限速
---

**免费 AI 网关：237 个提供商、一个入口、永不限速**

---

## 什么是 OmniRoute？

OmniRoute 是一个开源的 **AI 网关（AI Gateway）**，让你通过一个统一的端点访问 **237 个 AI 提供商**，其中 **90+ 个完全免费**。

| 统计           | 数值 |
| -------------- | ---- |
| AI 提供商      | 237  |
| 免费提供商     | 90+  |
| 免费 Tokens/月 | 1.6B |
| 路由策略       | 17   |

### 核心能力

- **智能路由** — 17 种路由策略，自动选择最佳提供商
- **自动故障转移** — 一个提供商失败，秒级切换到下一个
- **Token 压缩** — RTK + Caveman 压缩，节省 15-95% Tokens
- **MCP 服务** — 95 个内置工具，支持 3 种传输协议
- **统一 API** — OpenAI ↔ Claude ↔ Gemini 格式自动转换

### 功能特点

- **编程代理支持** — Claude Code、Codex、Cursor、Cline、Copilot 等 24+ 工具，一个配置全部搞定
- **生产级特性** — 熔断器、TLS 伪装、MCP、A2A、Guardrails、评估工具
- **成本优化** — 自动路由到最便宜的可用模型，支持配额共享
- **隐私优先** — 本地优先运行，完全开源，可自托管

---

## 快速部署

OmniRoute 支持多种安装方式。选择最适合你的一种：

### 方式一：Docker（推荐）

```bash
docker run -d \
  --name omniroute \
  -p 20128:20128 \
  -v omniroute-data:/app/data \
  -e API_SECRET=your-secret-key \
  diegosouzapw/omniroute
```

### 方式二：Docker Compose

```yaml
# 创建 docker-compose.yml
version: '3.8'
services:
  omniroute:
    image: diegosouzapw/omniroute
    container_name: omniroute
    ports:
      - "20128:20128"
    volumes:
      - ./data:/app/data
    environment:
      - API_SECRET=your-secret-key
    restart: unless-stopped
```

### 方式三：NPM

```bash
npm install -g omniroute
# 或使用 npx
npx omniroute
```

### 方式四：从源码

```bash
git clone https://github.com/diegosouzapw/OmniRoute.git
cd OmniRoute
pnpm install
pnpm build
pnpm start
```

### 验证安装

部署完成后，打开浏览器访问：

```
http://localhost:20128
```

> **注意**：默认管理员账号密码：`admin` / `admin`（请立即修改）

---

## 工作原理

OmniRoute 充当你所有 AI 请求的智能路由器：

```
┌──────────────────────────────────────────────────────────────┐
│         你的应用 / IDE（Claude Code、Cursor、Cline）            │
└───────────────────────────┬──────────────────────────────────┘
                            │ 请求发送到 http://localhost:20128/v1
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    OmniRoute — 智能路由器                      │
│                                                              │
│   • 格式转换（OpenAI ↔ Claude ↔ Gemini）                      │
│   • Token 压缩（RTK + Caveman）                               │
│   • 路由策略选择（17 种策略）                                  │
│   • 故障转移（自动切换到备用提供商）                            │
└───────────────────────────┬──────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┬────────────────┐
        ▼                   ▼                   ▼                ▼
   ┌─────────┐        ┌─────────┐         ┌─────────┐      ┌─────────┐
   │订阅配额 │        │ API 密钥│         │ 廉价方案 │      │ 免费方案 │
   │Claude   │        │DeepSeek │         │  GLM    │      │  Kiro   │
   │Code     │        │  Groq   │         │ MiniMax │      │ Pollin. │
   └─────────┘        └─────────┘         └─────────┘      └─────────┘
```

当一个提供商配额用完或出错时，OmniRoute 会自动切换到下一个提供商，全程无感知。

---

## 支持的编程代理

OmniRoute 专为各种 AI 编程工具设计：

| 工具           | 类型         | 配置难度 |
| -------------- | ------------ | -------- |
| Claude Code    | 命令行       | ⭐⭐       |
| GitHub Copilot | IDE 插件     | ⭐⭐⭐      |
| Cursor         | IDE          | ⭐⭐       |
| Cline          | VS Code 插件 | ⭐        |
| Codex (Pro)    | 命令行       | ⭐⭐       |
| Continue       | IDE 插件     | ⭐⭐       |
| Roo Code       | VS Code 插件 | ⭐        |
| Aider          | 命令行       | ⭐⭐       |
| OpenCode       | 命令行       | ⭐        |

---

## 下一步

现在你已经了解了 OmniRoute 的基本概念。接下来我们将学习：

- 连接你的第一个 AI 提供商
- 配置智能路由策略
- 设置自动故障转移

---

> **有什么问题吗？**
>
> 如果任何内容不清晰，随时问我。我是你的老师，可以帮助你理解任何概念或解决遇到的问题。

---

