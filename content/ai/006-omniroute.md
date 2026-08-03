---
Title: OmniRoute入门:Token 压缩（RTK + Caveman）
Date: 2026-07-11
Category: ai
Tags: omniroute
Series: OmniRoute入门
Series_index: 6
Author: 悠游
Summary: AI 编程工具会产生大量「噪音」：git diff、grep 输出、文件列表……这些内容消耗大量 Tokens，但 AI 真正需要理解的信息很少。
---

**节省 15-95% Tokens，自动压缩，无感知**

---

## 为什么需要压缩？

AI 编程工具会产生大量「噪音」：git diff、grep 输出、文件列表……这些内容消耗大量 Tokens，但 AI 真正需要理解的信息很少。

### 节省效果

**15-95%** 平均节省 Tokens（工具密集型会话可达 89%）

| 压缩方式       | 压缩率 |
| -------------- | ------ |
| RTK 压缩率     | 15-40% |
| Caveman 压缩率 | 30-60% |
| 叠加效果       | 89%    |

---

## 压缩效果示例

### 原始 git diff 输出

```diff
diff --git a/src/index.ts b/src/index.ts
index 8a2b1c3..d4e5f6a 100644
--- a/src/index.ts
+++ b/src/index.ts
@@ -12,7 +12,8 @@ export function processData(data: any) {
-    const result = oldLogic(data);
+    const result = newLogic(data);
     return result;
 }
@@ -45,1 +46,2 @@ export function processData
+    const newLogic = (data: any) => {
+        return data.map(item => item.value);
     };
```

### 压缩后

```yaml
# src/index.ts:12
- oldLogic → + newLogic

# src/index.ts:45
+ 新增: data.map(item => item.value)
```

> 压缩后的 diff 从 **~850 Tokens** 降至 **~85 Tokens**，节省 **90%**，AI 仍然能准确理解变更内容。

---

## 两大压缩引擎

### ⚡ RTK（Rapid Toolkit）

**基于规则的快速压缩**

使用预定义模板处理结构化输出，如 git diff、grep、build logs。速度快，适合高频场景。

**适用场景：**

- git diff / status 输出
- grep / find 搜索结果
- 编译错误和日志
- ls / tree 文件列表

### 🗿 Caveman

**智能语义压缩**

通过去重、缩写、模式识别等智能规则压缩自然语言和代码注释。更高的压缩率，但需要更多处理时间。

**适用场景：**

- 长代码注释
- 重复的错误信息
- 冗长的文档内容
- 调试输出

---

## 堆叠压缩效果

OmniRoute 可以同时使用 RTK + Caveman，叠加压缩效果：

```
原始输入 → RTK 压缩 → Caveman 压缩 → 最终输出

输入: 2,400 Tokens → RTK: 1,680 (-30%) → Caveman: 1,008 (-40%) → 最终: 360 Tokens (-85%)
```

> **质量保护**
>
> OmniRoute 内置**膨胀保护**机制：当压缩后内容反而变长时，自动使用原始内容。
>
> 另有多语言支持：英语语法（dedup + ultra）、德语、法语、日语、中文（文言/白话）规则包。

---

## 启用压缩

> **默认启用**
>
> 压缩功能默认开启，无需额外配置即可享受 Token 节省。

如需手动控制：

```yaml
# 启用压缩（默认）
x-omniroute-compression: true

# 禁用压缩
x-omniroute-compression: false

# 指定压缩级别
x-omniroute-compression: ultra   # 最高压缩
x-omniroute-compression: balanced # 平衡
x-omniroute-compression: minimal # 最低压缩，保留更多细节
```

---

## 压缩控制头

使用 `X-OmniRoute-Compression` 请求头控制压缩行为：

```bash
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer your-secret" \
  -H "x-omniroute-compression: true" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "..."}]
  }'
```

---

> **有问题吗？**
>
> 如果对压缩效果有疑问，或者想了解更多高级配置，告诉我。
