---
Title: dify入门:API 集成与发布
Date: 2026-07-02
Category: dify
Tags: dify
Series: dify入门
Series_index: 7
Author: 悠游
Summary: 获取 Dify 应用的 API 密钥，学会用 API 调用 Dify 应用，并了解将应用嵌入网站和接入企业微信/飞书的方案。
---

把 Dify 应用接入你的网站/系统——让 AI 真正为用户服务

⏱ 预计时间：15-20 分钟

🎯 本课目标

获取 Dify 应用的 API 密钥，学会用 API 调用 Dify 应用，并了解将应用嵌入网站和接入企业微信/飞书的方案。

## 一、为什么需要 API 集成？

在 Dify 控制台里测试完应用，下一步就是让它真正为用户服务。有几种方式：

#### 🌐 嵌入网站

在公司官网嵌入聊天窗口，访客直接对话

难度：⭐ 简单

#### 📱 接入企业微信

员工在企业微信里直接问 AI 助手

难度：⭐⭐ 中等

#### 🖥️ 集成自有系统

在 OA / CRM 里调用 Dify API

难度：⭐⭐ 中等

#### 🤖 公众号 / 小程序

在微信生态里提供服务

难度：⭐⭐⭐ 较难

## 二、Dify 的 3 种 API

不同应用类型对应不同的 API 接口，先搞清楚用哪个：

| API 类型           | 适用应用        | 特点                   | 端点示例               |
| :----------------- | :-------------- | :--------------------- | :--------------------- |
| **Chatflow API**   | 聊天助手、Agent | 支持多轮对话、流式返回 | `/chat-messages`       |
| **Workflow API**   | 工作流应用      | 一次性执行，无对话历史 | `/workflows/run`       |
| **Completion API** | 文本生成应用    | 单轮文本生成           | `/completion-messages` |

## 三、获取 API 密钥

**1** 

#### 进入应用 API 设置

在 Dify 控制台 → 选择你的应用 → 右上角"发布"旁 → 点击**"..." → "访问 API 密钥"**

**2** 

#### 创建 API 密钥

- 点击"创建密钥"
- 填写备注（如"官网嵌入用"）
- **复制密钥并保存**（只显示一次！）

**3** 

#### 查看 API 文档

在同一个页面，可以看到完整的 API 文档链接和示例代码，建议打开参考。

**⚠️ API 密钥安全！**
API 密钥等同于你的账号权限，不要前端代码里硬编码，不要提交到 GitHub，不要分享给他人。

## 四、API 调用实战（curl + Python）

### 方式 1：用 curl 测试（最快）

```
# 替换 YOUR_API_KEY 和 YOUR_APP_ID curl -X POST https://你的Dify域名/v1/chat-messages \  -H "Authorization: Bearer YOUR_API_KEY" \  -H "Content-Type: application/json" \  -d '{    "inputs": {},    "query": "公司年假怎么申请？",    "response_mode": "blocking",    "user": "user-123"  }' 
```

### 方式 2：用 Python 调用（推荐）

```
# 安装依赖：pip install requests import requests import json # 配置 API_URL = "http://你的虚拟机IP/v1/chat-messages" API_KEY = "YOUR_API_KEY" # 发送请求 headers = {    "Authorization": f"Bearer {API_KEY}",    "Content-Type": "application/json" } payload = {    "inputs": {},    "query": "公司年假怎么申请？",    "response_mode": "blocking",    "user": "user-123" } resp = requests.post(API_URL, headers=headers, json=payload) result = resp.json() # 解析返回 print("AI 回答：", result["answer"]) 
```

📋 返回格式说明

- `answer`：AI 的回答文本
- `conversation_id`：会话 ID，多轮对话需要传回
- `message_id`：消息 ID，用于反馈点赞/点踩
- `metadata`：附加信息（如知识库来源）

## 进阶：流式输出 (Streaming) 与 Webhook 回调

前面用的是 `"response_mode": "blocking"`（阻塞模式）——等 AI 全部生成完毕后才一次性返回。但生产级应用几乎都用**流式输出**（Streaming），让用户看到逐字生成的过程，体验好得多。

### 什么是 Streaming？

流式输出使用 **SSE（Server-Sent Events）** 协议：AI 每生成一个 token 就立刻推送给客户端，客户端逐字显示。
效果类似 ChatGPT——看到文字"打"出来的过程，而不是黑屏等 20 秒再全部出现。

### Python 调用 Streaming API

```
import requests import json url = "http://192.168.1.100/v1/chat-messages" headers = {    "Authorization": "Bearer YOUR_API_KEY",    "Content-Type": "application/json", } payload = {    "inputs": {},    "query": "如何申请报销？",    "response_mode": "streaming",          # 关键：streaming 模式    "user": "user-001", } # streaming 方式：stream=True，逐行解析 SSE with requests.post(url, json=payload, headers=headers, stream=True) as resp:    for line in resp.iter_lines():        if line:            line_str = line.decode("utf-8")            # SSE 格式：data: {"event": "message", "answer": "..."}            if line_str.startswith("data: "):                data = json.loads(line_str[6:])                answer = data.get("answer", "")                print(answer, end="", flush=True)
```

✅ Streaming 返回的 SSE 事件类型

- `message`：AI 生成的文本增量（`answer` 字段逐 token 更新）
- `message_end`：生成完毕，包含完整 `metadata`（Token 消耗、知识库来源等）
- `agent_thought`（仅 Agent 模式）：Agent 的思考过程和工具调用日志
- `error`：发生错误时的中断事件

**💡 什么时候用 blocking，什么时候用 streaming？**
• **blocking**：后台批处理任务（如批量生成报告）、自动化脚本、无需交互的场景
• **streaming**：任何面向终端用户的交互场景——对话助手、客服、搜索增强
Dify 的网页嵌入（第 5 节）默认使用 streaming，无需额外配置。

### 多轮对话（conversation_id）管理

blocking 和 streaming 两种模式都支持多轮对话。核心操作：

1. **第 1 轮**：调用 API 前不带 `conversation_id`，API 首次调用会自动创建
2. **保存 ID**：从第 1 轮的返回值中获取 `conversation_id`
3. **后续轮次**：每次调用 API 时把上一轮的 `conversation_id` 传回，API 就知道这是同一个会话
4. **Streaming 模式获取 ID**：在 `message_end` 事件的 metadata 中拿 `conversation_id`

### Webhook 回调（异步触发工作流）

除了主动调用 API，Dify 还支持 **Webhook**——外部系统可以触发 Dify 工作流执行，并接收异步结果。

🔄 Webhook 的典型场景

- **表单提交触发 AI 分析**：用户在网站填表 → Webhook 发数据到 Dify → 工作流处理 → 结果回填/通知
- **定时任务触发**：企业微信/钉钉机器人 → 用户发消息 → 群机器人 Webhook → Dify 生成回复 → 发回群聊
- **第三方系统联动**：ERP/WMS 数据变更 → Webhook → Dify 提取关键信息 → 通知相关负责人

```
# Webhook 调用：外部系统 POST 请求触发工作流 curl -X POST "http://192.168.1.100/v1/workflows/run" \  -H "Authorization: Bearer YOUR_API_KEY" \  -H "Content-Type: application/json" \  -d '{    "inputs": {"order_id": "ORD-20260613"},    "response_mode": "blocking",    "user": "system-webhook"  }'
```

**💡 注意**：Dify 本身不提供 Webhook "接收端点"，你需要在自己的服务端接收外部 Webhook 回调，然后再调用 Dify API。所以 Webhook 集成的典型架构是：
`外部系统 → 你的服务端 → Dify API → 处理结果 → 你的服务端 → （可选）通知用户`

## 六、嵌入网站（最简单的方式）

Dify 提供了官方的 Web 嵌入功能，无需写代码：

**1** 

#### 获取嵌入代码

应用编辑页面 → 右上角"发布" → **"嵌入网站"** → 复制代码

**2** 

#### 放入你的网页

把复制的代码粘贴到网页的 `<body>` 标签内任意位置，刷新页面即可看到聊天窗口。

```
<!-- 嵌入代码示例 --> <script  src="http://你的虚拟机IP/embed.js"  data-app-id="YOUR_APP_ID"  data-mode="chat"  data-button-position="bottom-right"> </script> 
```

**💡 自定义样式**
嵌入代码支持多个 data 属性：button-position（位置）、theme（主题）、initial-message（欢迎语）等，详见嵌入配置页面。

## 七、接入企业微信 / 飞书（概览）

让 AI 助手出现在员工日常使用的工具里，是使用率最高的方式。目前 Dify 官方暂未直接支持，但社区有成熟方案：

⚠️ 企业微信接入方案

- **方案 A**：用企业微信"自建应用" + 服务器接收消息 → 转发给 Dify API
- **方案 B**：使用社区插件（GitHub 搜索 "dify wecom"）
- **难度**：需要一台有公网 IP 的服务器（接收企业微信回调）

✅ 飞书接入方案

- 飞书开放平台 → 创建企业自建应用
- 配置事件订阅（接收用户消息）
- 服务端收到消息 → 调用 Dify API → 回复用户
- 社区有开源项目可直接用（搜索 "dify feishu bot"）

## 八、API 安全最佳实践

🔐 安全检查清单

- ✅ API 密钥存在服务端环境变量，不写在前端代码里
- ✅ 设置 API 调用频率限制（防止被刷）
- ✅ 为不同用途创建不同 API 密钥（便于管理和撤销）
- ✅ 定期检查 Dify 日志，发现异常调用
- ✅ 生产环境建议配置 HTTPS（用 Nginx 反代 + Let's Encrypt 证书）

## 九、本节课重点回顾

- ✅ 3 种 API：Chatflow API（对话）/ Workflow API（工作流）/ Completion API（文本生成）
- ✅ 流式输出 (Streaming)：用 SSE 协议逐 token 返回，提升用户体验
- ✅ 获取 API 密钥：应用 → 访问 API 密钥 → 创建并保存
- ✅ 多轮对话：保存 conversation_id 传回，维持上下文
- ✅ API 调用：用 curl 快速测试，用 Python 集成到自有系统
- ✅ 嵌入网站：复制嵌入代码，粘贴到网页即可，无需写代码
- ✅ 企业微信/飞书接入：通过服务端转发消息到 Dify API
- ✅ API 安全：密钥存服务端、限频、定期检查日志

**▶ 下一课预告（最终课）**

第 8 课：自定义插件与二次开发——深度定制 Dify，让它完全适配你的业务

API 已打通，下一步就是让 Dify "长"出你们公司独有的能力！

------

## 参考资料

- [Dify 官方文档 - 发布与集成](https://docs.dify.ai/zh/use-dify/publish) — 嵌入网站、API 调用详细说明
- [Dify 官方文档 - API 扩展](https://docs.dify.ai/zh/use-dify/publish/API-based-extension) — API 完整参数说明
- [Dify GitHub Issues](https://github.com/langgenius/dify/issues) — 搜索企业微信/飞书接入相关问题

用 Python 跑通一次 API 调用，成就感满满！🔗🔗
