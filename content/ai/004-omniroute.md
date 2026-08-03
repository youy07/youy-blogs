---
Title: OmniRoute入门:Combo 组合配置
Date: 2026-07-11
Category: ai
Tags: omniroute
Series: OmniRoute入门
Series_index: 4
Author: 悠游
Summary: Combo（组合）是一系列按优先级排列的 AI 模型列表。当当前模型不可用时，OmniRoute 自动切换到下一个，实现**零停机**
---

**构建永不宕机的 AI 请求链**

---

## 什么是 Combo？

Combo（组合）是一系列按优先级排列的 AI 模型列表。当当前模型不可用时，OmniRoute 自动切换到下一个，实现**零停机**。

```
┌──────────────────────────────────────────────────────────────┐
│ Tier 1  │ cc/claude-opus-4-7        │ 订阅配额 (Claude Code) │
├─────────┼────────────────────────────┼───────────────────────┤
│ Tier 2  │ cx/gpt-5.5                 │ 第二订阅             │
├─────────┼────────────────────────────┼───────────────────────┤
│ Tier 3  │ glm/glm-5.1                 │ 廉价 API ($0.5/1M)   │
├─────────┼────────────────────────────┼───────────────────────┤
│ Tier 4  │ kr/claude-sonnet-4.5       │ 免费，无限           │
└─────────┴────────────────────────────┴───────────────────────┘

4 层故障转移 = 永不停机
```

---

## 快速创建 Combo

### 步骤 1：进入 Combo 配置页面

在 OmniRoute Dashboard 找到「Combos」或「路由」设置

### 步骤 2：添加模型

点击「Add Model」或「+」，按优先级添加模型（从高到低）

### 步骤 3：设置策略

选择路由策略（推荐 auto 或 priority）

### 步骤 4：保存并测试

保存后使用 Playground 测试故障转移是否正常

---

## Combo 配置示例

### 编程专用 Combo（推荐）

```yaml
combo: coding-elite
strategy: auto/coding
models:
  - cc/claude-opus-4        # Claude Code 订阅
  - cx/gpt-5                # ChatGPT Plus
  - ds/deepseek-coder       # DeepSeek 便宜
  - kr/claude-sonnet-4      # 免费备用
```

### 预算优先 Combo

```yaml
combo: budget-friend
strategy: cost-optimized
models:
  - gl/gemini-flash         # Google 免费
  - ds/deepseek-chat       # DeepSeek 便宜
  - pl/gpt-4o-mini          # Pollinations 免费
```

### 速度优先 Combo

```yaml
combo: speed-demon
strategy: auto/fast
models:
  - gl/gemini-flash         # Google 快
  - gr/groq-llama           # Groq 超快
  - ds/deepseek-chat        # DeepSeek
```

---

## 使用 Combo

创建 Combo 后，在请求中使用：

```bash
# 在 API 请求中使用 Combo
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer your-secret" \
  -d '{
    "model": "coding-elite",    # 使用你定义的 Combo 名称
    "messages": [{"role": "user", "content": "写一个排序算法"}]
  }'

# 或者使用 OmniRoute 内置的 auto 模型
{
  "model": "auto",             # OmniRoute 自动选择最佳模型
  "messages": [...]
}
```

---

## 内置自动模型

除了自定义 Combo，OmniRoute 还提供内置的自动模型：

| 模型 ID        | 优化目标                   |
| -------------- | -------------------------- |
| `auto`         | 均衡默认（使用 LKGP 粘性） |
| `auto/coding`  | 编程质量优先               |
| `auto/fast`    | 最低延迟优先               |
| `auto/cheap`   | 最便宜优先                 |
| `auto/offline` | 最多余量优先               |
| `auto/smart`   | 质量优先 + 10% 探索        |

---

## 故障转移演示

> **故障转移流程**
>
> 1. **请求发送** → OmniRoute 尝试 Tier 1（Claude Code）
> 2. **配额用完** → OmniRoute 毫秒级切换到 Tier 2（GPT）
> 3. **API 超时** → 继续切换到 Tier 3（廉价 API）
> 4. **全部失败** → 最终切换到 Tier 4（免费）
> 5. **全部成功** → 你收到 AI 回复，完全无感知

---

> **有问题吗？**
>
> 如果配置 Combo 遇到问题，或者想要我帮你设计一个适合你场景的 Combo，告诉我。
