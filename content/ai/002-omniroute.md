---
Title: OmniRoute入门:连接第一个 AI 提供商
Date: 2026-07-01
Category: ai
Tags: omniroute
Series: OmniRoute入门
Series_index: 2
Author: 悠游
Summary: 从**免费提供商**开始，熟悉 OmniRoute 的配置流程后再添加付费 API
---

**从免费开始，逐步扩展你的 AI 连接**

---

## 推荐从哪里开始？

建议从**免费提供商**开始，熟悉 OmniRoute 的配置流程后再添加付费 API。

### 免费提供商推荐

| 提供商       | 描述                  | 标签 |
| ------------ | --------------------- | ---- |
| Kiro         | Claude 模型，完全免费 | 免费 |
| Pollinations | 多模型支持，无限制    | 免费 |
| Qoder        | GPT-4 免费使用        | 免费 |
| SiliconFlow  | 永久免费额度          | 免费 |

---

## 连接步骤

### 步骤 1：打开 OmniRoute Dashboard

访问 http://localhost:20128 ，使用默认账号登录（admin / admin）

### 步骤 2：进入「连接」或「Providers」页面

在侧边栏找到「Connections」或「Providers」选项

### 步骤 3：点击「添加连接」或「Add Connection」

选择你要添加的提供商（从免费开始，如 Kiro 或 Pollinations）

### 步骤 4：配置 API 密钥

某些免费提供商可能需要注册获取 API Key，某些则无需任何配置

### 步骤 5：验证连接

保存后 OmniRoute 会自动测试连接，显示连接状态

---

## 免费提供商配置详解

### Kiro（推荐新手）

完全免费，无需注册，直接使用。

**配置方式：**

```
Provider: Kiro
API Key: (留空，或者使用默认值)
Endpoint: (默认)
```

> 支持 Claude Sonnet 等模型

### Pollinations

多模型支持，包括 GPT-4、Claude、Llama 等。

**配置方式：**

```
Provider: Pollinations
API Key: (留空)
Endpoint: https://text.pollinations.ai
```

---

## 测试你的连接

连接成功后，使用 API 测试：

```bash
# 使用 cURL 测试
curl http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-secret" \
  -d '{
    "model": "kr/claude-sonnet-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

或者直接在 OmniRoute 的 **Playground** 页面测试。

---

## 常用免费 API 汇总

| 提供商       | 免费模型             | 限制                   | 需要注册 |
| ------------ | -------------------- | ---------------------- | -------- |
| Kiro         | Claude Sonnet, GPT-4 | 无明确限制             | 否       |
| Pollinations | GPT-4, Claude, Llama | 速率限制               | 否       |
| Qoder        | GPT-4o, Claude       | 每日请求限制           | 是       |
| SiliconFlow  | 多模型               | 每月固定额度           | 是       |
| Google AI    | Gemini               | 60 RPM, 1.5M tokens/月 | 是       |
| DeepSeek     | DeepSeek Chat        | R1/R2 有免费额度       | 是       |

---

## 常见问题

> ⚠️ **连接失败怎么办？**
>
> 1. 检查 API Key 是否正确
> 2. 确认网络可以访问该提供商
> 3. 查看 OmniRoute 日志中的错误信息
> 4. 尝试换一个提供商测试

---

> **有问题吗？**
>
> 如果连接遇到问题，告诉我你遇到的具体情况，我可以帮你排查。
