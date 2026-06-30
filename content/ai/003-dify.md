---
Title: 模型接入与配置实战
Date: 2026-06-28
Category: dify
Tags: dify
Series: dify入门
Series_index: 3
Author: 悠游
Summary: 在 Dify 控制台里完成至少 2 个模型的接入配置，并理解不同模型类型（系统推理 / 对话 / Embedding）的区别与用途
---

第三课

# 模型接入与配置实战

让 Dify 真正"有脑可动"——手把手配置大模型

⏱ 预计时间：10-15 分钟

🎯 本课目标

在 Dify 控制台里完成至少 2 个模型的接入配置，并理解不同模型类型（系统推理 / 对话 / Embedding）的区别与用途。

## 一、Dify 里的 4 种模型类型

在配置模型之前，先搞清楚 Dify 把模型分成哪几类——这关系到你该配置哪些模型：

| 模型类型           | 作用                                           | 举例                            | 必须？         |
| :----------------- | :--------------------------------------------- | :------------------------------ | :------------- |
| **系统推理模型**   | 平台核心大脑，用于工作流、Agent 等所有 AI 推理 | DeepSeek-V3、GPT-4o、Claude 3.5 | ✅ 必须         |
| **对话模型**       | 聊天应用的专用模型，支持多轮对话               | 同上（通常共用）                | ⚠️ 建议         |
| **Embedding 模型** | 把文本转成向量，用于知识库语义检索（RAG）      | text-embedding-3-small、bge-m3  | ✅ 用知识库必须 |
| **语音/图像模型**  | 语音转文字、图像生成等扩展能力                 | Whisper、Stable Diffusion       | ❌ 可选         |

**💡 最小配置方案**：至少配置 1 个系统推理模型 + 1 个 Embedding 模型，就能跑通"聊天 + 知识库问答"的完整流程。

## 二、推荐模型供应商对比

国内用户推荐以下 3 家，免费额度充足、中文支持好、接入简单：

⭐ 最推荐

#### DeepSeek

¥1 / 百万 Token（输入）

中文理解极佳，推理能力强，价格极低，新用户送 500 万 Token。

**接入步骤：**

1. 注册 platform.deepseek.com
2. API 密钥 → 新建 Key
3. Dify 设置 → 模型供应商 → DeepSeek → 输入 Key

免费额度

#### 通义千问（阿里）

有免费额度，按量计费

阿里系，国内访问稳定，与阿里云生态深度整合。

**接入步骤：**

1. 注册 dashscope.aliyun.com
2. API-KEY 管理 → 创建 Key
3. Dify 设置 → 模型供应商 → 通义千问 → 输入 Key

#### ChatGLM（智谱 AI）

有免费额度

国产大模型，中文能力强，GLM-4 系列表现优秀。

**接入步骤：**

1. 注册 open.bigmodel.cn
2. API 密钥 → 新建
3. Dify 设置 → 模型供应商 → ChatGLM → 输入 Key

#### Ollama（本地模型）

完全免费（本地运行）

在 Debian 虚拟机里跑本地模型，数据完全不出本机，适合高隐私场景。

**接入步骤：**

1. Debian 里安装 Ollama
2. 拉取模型：`ollama pull qwen2.5:7b`
3. Dify 设置 → 模型供应商 → Ollama → 配置地址

## 三、实战：配置 DeepSeek（推荐首选）

跟着步骤走，5 分钟完成：

**1** 

#### 获取 DeepSeek API Key

- 访问 [platform.deepseek.com](https://platform.deepseek.com)，注册/登录
- 左侧菜单 → **API 密钥**
- 点击"创建密钥"，名称随意（如 `dify-test`）
- **复制 Key 并保存**（只显示一次！）

**2** 

#### 在 Dify 里添加 DeepSeek

- 打开 Dify 控制台（http://你的虚拟机IP）
- 右上角头像 → **设置**
- 左侧 → **模型供应商**
- 找到 **DeepSeek**，点击"+"或"添加模型"
- 填入 API Key，模型类型选"LLM"，模型名称选 `deepseek-chat`
- 点击"保存"

**3** 

#### 添加 Embedding 模型（知识库必备）

- 在同一个 DeepSeek 供应商页面，继续添加模型
- 模型类型选 **"Text Embedding"**
- 模型名称选 `deepseek-embedder`（如果 DeepSeek 没有 Embedding 模型，改用下面的备选方案）

⚠️ DeepSeek 没有 Embedding 模型！

DeepSeek 目前只提供对话/推理模型，**不提供 Embedding 模型**。配置知识库需要单独接入一个 Embedding 模型，推荐用 **OpenAI（text-embedding-3-small）** 或 **本地 Ollama + bge-m3**。

**✅ 推荐组合（国内用户）**
系统推理：DeepSeek-V3（便宜、中文好）
Embedding：Ollama 本地跑 `bge-m3`（完全免费，数据不出本机）

## 四、进阶：在 Debian 里跑本地模型（Ollama）

如果不想依赖任何第三方 API，可以在 Debian 虚拟机里直接跑模型。这样数据完全不出本机，适合对隐私要求高的场景。

### 安装 Ollama

```
# 在 Debian 虚拟机里执行 curl -fsSL https://ollama.com/install.sh | sh # 安装完成后，Ollama 会自动以服务运行 # 验证 ollama --version
```

### 拉取并运行 Embedding 模型

```
# 拉取 bge-m3（中文 Embedding 效果最好） ollama pull bge-m3 # 拉取一个对话模型（可选，完全离线运行） ollama pull qwen2.5:7b # 查看已安装的模型 ollama list
```

### 在 Dify 里配置 Ollama

⚠️ 网络配置关键点

Dify 的容器里访问 `localhost` 指的是**容器自己**，不是 Debian 宿主机。需要在 Dify 的 Ollama 配置里填 Debian 的**内网 IP**（如 `http://192.168.1.105:11434`），而不是 `localhost:11434`。

- Dify 控制台 → 设置 → 模型供应商 → 找到 **Ollama**
- 模型类型：Text Embedding，模型名称：`bge-m3`
- Base URL：填 `http://你的DebianIP:11434`
- 点击保存

## 五、验证模型配置成功

✅ 验证清单

- ✅ 设置 → 模型供应商 页面能看到已添加的模型，状态为"已启用"
- ✅ 创建一个"聊天助手"应用，能正常对话
- ✅ 创建一个知识库，能成功上传文档并完成向量化

**快速测试对话：**

1. 工作台 → 创建应用 → 聊天助手
2. 应用名称随意（如"测试助手"）
3. 提示词：简单写一句，如"你是一个有帮助的 AI 助手"
4. 选择你刚配置的模型（如 DeepSeek-V3）
5. 点击"预览"，输入一句话测试

📷 提示：第一次对话会稍慢（模型冷启动），之后就快了
如果报错，检查 API Key 是否正确、账户是否有余额

## 六、费用控制与最佳实践

💰 费用参考（2026 年价格）

- **DeepSeek-V3**：输入 ¥1/百万 Token，输出 ¥2/百万 Token
- **DeepSeek-R1（推理模型）**：输入 ¥4/百万 Token，输出 ¥16/百万 Token
- **一次普通对话**：约消耗 500-2000 Token，成本约 ¥0.001-¥0.004
- **结论**：个人/小团队测试，¥10 能用很久

### 最佳实践

- **分开配置多个模型**：轻量任务用便宜模型（DeepSeek-V3），复杂推理用强模型（Claude/GPT-4o）
- **设置 Token 限制**：在 Dify 应用设置里限制最大 Token 数，防止异常消耗
- **本地 Embedding**：用 Ollama 跑 bge-m3，知识库检索不花 API 钱
- **定期检查用量**：Dify 控制台 → 观测 → 日志，可以看到每次对话的 Token 消耗

## 七、常见问题排查

❌ 报错："模型供应商 API 请求失败"

- 检查 API Key 是否正确（注意前后空格）
- 检查账户是否有余额（DeepSeek 新用户有免费额度，但也会用完）
- 检查 Debian 虚拟机能否访问外网（`curl https://api.deepseek.com`）

❌ Ollama 模型在 Dify 里连不上

- 确认 Ollama 服务在运行：`systemctl status ollama`
- 确认 Dify 里填的是 Debian **内网 IP**，不是 localhost
- 确认防火墙放行 11434 端口：`sudo ufw allow 11434`

❌ 知识库上传文档后向量化失败

- 检查是否配置了 Embedding 模型
- 检查 Embedding 模型的 API Key / 连接是否正常
- 文档格式是否支持（PDF/Word/TXT/Markdown 都支持）

## 八、本节课重点回顾

- ✅ Dify 有 4 种模型类型，最小配置需要"系统推理 + Embedding"
- ✅ 推荐组合：DeepSeek-V3（推理）+ Ollama/bge-m3（Embedding，免费）
- ✅ DeepSeek 接入：获取 API Key → Dify 设置 → 模型供应商 → 添加
- ✅ Ollama 本地模型：数据不出本机，适合高隐私场景
- ✅ 验证方法：创建聊天助手应用，发一条消息测试
- ✅ 费用极低：个人测试 ¥10 能用很久

**▶ 下一课预告**

第 4 课：知识库构建与 RAG 实战——上传你的第一份文档，搭建专属问答系统

模型已配好，下一步就是让 AI "读懂"你的私有资料！

------

## 参考资料

- [DeepSeek 开放平台](https://platform.deepseek.com) — 注册获取 API Key
- [Ollama - bge-m3 模型](https://ollama.com/library/bge-m3) — 中文 Embedding 最佳选择
- [Dify 官方文档 - 模型供应商配置](https://docs.dify.ai/zh/use-dify/model-providers)
- [Dify 官方文档 - 知识库](https://docs.dify.ai/zh/use-dify/knowledge-base) — 第 4 课预习

配置过程中遇到问题，把报错截图或文字发给我，我帮你排查 🔧
