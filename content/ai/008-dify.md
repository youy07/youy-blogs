---
Title: dify入门:自定义插件与二次开发
Date: 2026-07-02
Category: dify
Tags: dify
Series: dify入门
Series_index: 8
Author: 悠游
Summary: 了解 Dify 二次开发的 4 条路径，并根据你的技术能力选择合适的定制方案。学完后你能判断：哪些需求可以不用改代码，哪些必须改源码
---

深度定制 Dify，让它完全适配你的业务——从"能用"到"好用"

⏱ 预计时间：25-30 分钟

🎯 本课目标

了解 Dify 二次开发的 4 条路径，并根据你的技术能力选择合适的定制方案。学完后你能判断：哪些需求可以不用改代码，哪些必须改源码。

## 一、Dify 二次开发的 4 条路径

不是所有定制都需要改源码！根据你的需求和技术能力，选择最合适的路径：

⭐ 推荐

#### ① 自定义工具（Tool）

难度：⭐ 简单 | 无需改源码

通过 HTTP API 接入你们的私有接口，Agent 就能调用。90% 的定制需求用这个就够了。

#### ② 自定义工作流节点

难度：⭐⭐ 中等 | 需改源码

在 Dify 画布上添加新的节点类型（如"发送短信"节点）。需要写 Python + React。

#### ③ 修改前端界面

难度：⭐⭐⭐ 较难 | 需改源码

定制 Dify 控制台界面、聊天窗口样式、增加企业品牌元素等。

高级

#### ④ Fork 改源码

难度：⭐⭐⭐⭐ 很难 | 需深度掌握

完全修改 Dify 核心逻辑（如换掉向量数据库、改推理引擎）。维护成本高，慎选。

**💡 选择建议**：先看能不能用 ① 自定义工具解决；不行再看 ②；③ 和 ④ 建议等有专职开发团队再考虑。

## 二、深度：自定义工具（最实用！）

这是投入产出比最高的定制方式。详细步骤：

**1** 

#### 设计你们的 API 接口

先确保你们的后端有一个 HTTP API 可供调用。例如"查询订单"接口：

```
# 你们的 API 设计示例 POST https://api.your-company.com/order/query # 请求 {  "order_id": "SO-2024-001",  "user_id": "U123" } # 响应（Dify 要求固定格式） {  "result": "success",  "data": {    "order_id": "SO-2024-001",    "status": "已发货",    "tracking_no": "SF123456"  } } 
```

**2** 

#### 在 Dify 里注册自定义工具

Dify 控制台 → 设置 → 工具 → **自定义工具** → 创建工具

- **工具名称**：如 `查询订单`
- **工具描述**：如 `根据用户ID或订单号查询订单状态和物流信息`（AI 靠这个决定是否调用）
- **API 地址**：`https://api.your-company.com/order/query`
- **请求方法**：POST
- **参数定义**：添加 `order_id`（必填）、`user_id`（可选）

**3** 

#### 在工作流/Agent 里使用

添加工具节点 → 选择"查询订单" → 映射变量 → 测试

**💡 工具描述写作公式**：
"当用户需要【场景】时，调用此工具。【需要的参数】是必填的。"
例："当用户需要查询订单状态或物流信息时，调用此工具。order_id（订单号）是必填参数。"

## 三、进阶：开发自定义工作流节点

如果你们需要在工作流画布上出现一个全新的节点（而不只是调用 API），需要修改 Dify 源码。以下是核心步骤概览：

⚠️ 前置要求

- 熟悉 Python（后端）和 TypeScript/React（前端）
- 理解 Dify 的 `api/core/workflow/nodes/` 目录结构
- 有能力维护一个 Fork 版本的 Dify（跟进官方更新）

### 核心目录结构

\# Dify 源码关键目录 dify/ ├── api/core/workflow/nodes/ # 后端节点逻辑 │ ├── base/ # 节点基类 │ ├── llm/ # LLM 节点示例 │ └── your_custom_node/ # 你的自定义节点 ├── web/app/components/workflow/nodes/ # 前端节点组件 │ ├── llm/ # LLM 节点前端 │ └── your_custom_node/ # 你的节点前端 └── web/app/components/workflow/types.ts # 节点类型定义

### 开发步骤概览

**1** 

#### Fork Dify 仓库

`git clone https://github.com/langgenius/dify.git` → 创建你的分支

**2** 

#### 后端：创建节点类

在 `api/core/workflow/nodes/your_custom_node/` 下创建：

- `node.py`：继承 `BaseNode`，实现 `run()` 方法
- `entities.py`：定义节点的数据 schema
- 在 `node_mapping.py` 里注册新节点类型

**3** 

#### 前端：创建节点组件

在 `web/app/components/workflow/nodes/your_custom_node/` 下创建 React 组件，定义节点在画布上的外观和配置面板。

**4** 

#### 构建并部署你的定制版

`cd web && npm run build` → 重新构建 Docker 镜像 → 部署

**⚠️ 维护警告**：修改 Dify 源码后，每次官方发布新版本你都需要合并代码。如果定制需求不深，优先考虑用 ① 自定义工具 或 ② 外部系统调用 Dify API 的方式实现。

## 四、Dify 插件系统（2025+ 新架构）

Dify 正在逐步推出**插件系统**（Plugin System），目标是让定制不需要改源码。截至 2026 年中，插件系统还在完善中。

✅ 插件系统能做什么（将来）

- 不修改源码，通过安装插件扩展 Dify 能力
- 插件可以包含：自定义工具、自定义模型接入、自定义工作流节点
- 插件可发布到 Dify Marketplace 供他人使用

### 如何使用 Dify Marketplace

**1** 

#### 浏览 Marketplace

访问 [marketplace.dify.ai](https://marketplace.dify.ai/)，可以浏览社区贡献的插件。分类包括：工具（Tools）、模型接入（Model Providers）、Agent 策略等。

**2** 

#### 安装插件

在 Dify 管理后台 → 插件 → 粘贴 Marketplace 上提供的安装 URL 或上传 `.difypkg` 文件。

**3** 

#### 在工作流/Agent 中使用

安装后的工具和模型接入自动出现在工作流节点的工具列表里，和内置工具使用方式完全一样。

⚠️ 插件系统现状（2026 年中）

- **已可用**：Marketplace 上的第三方工具插件、社区模型接入插件
- **待完善**：自定义工作流节点插件、主题定制插件
- **建议**：优先使用 Marketplace 现成插件，自定义插件开发等官方 SDK 文档更完善后再深入

## 五、定制版 Dify 的维护策略

✅ 推荐维护策略

- **尽量不改源码**：用自定义工具 + API 调用解决 90% 需求
- **必须改源码时**：把改动控制在最少文件里，方便合并更新
- **追踪官方版本**：Star Dify GitHub，关注 Release Notes
- **测试更新**：官方发新版本后，先在测试环境验证再更新生产
- **备份！**：更新前备份数据库（PostgreSQL）和向量库数据

## 六、生产运维：CI/CD、监控与备份

如果你决定长期用 Dify，下面是你需要了解的生产环境运维要点。

### 6.1 Docker 镜像构建与 CI/CD

如果你改了 Dify 源码或定制了 Docker Compose 配置，需要一个自动化构建流程：

```
# Dockerfile 示例：基于 Dify 官方镜像，打补丁/加定制 FROM langgenius/dify-api:1.1.3 # 复制你的定制文件（如果有的话） COPY custom-nodes/ /app/api/core/workflow/nodes/custom/ COPY custom-frontend/ /app/web/ # 安装额外依赖 RUN pip install your-extra-package
```

✅ 推荐的 CI/CD 流程

1. **代码托管**：Fork Dify 到你的私有 GitLab/GitHub
2. **自动构建**（GitHub Actions / Jenkins）：push 代码 → build Docker 镜像 → 推送到私有 Registry（如 Harbor）
3. **测试环境部署**：用 docker compose 拉起测试实例，运行冒泡测试
4. **生产滚动更新**：`docker compose pull` + `docker compose up -d`（Docker Compose 默认会最小化停机）

### 6.2 数据库备份（必须！）

Dify 有两类数据必须备份：

💾 备份命令

- **PostgreSQL 数据库**（应用配置、用户、应用定义）：

  `# 备份 docker exec -t dify-db-1 pg_dump -U postgres dify > dify_backup_$(date +%Y%m%d).sql # 恢复 docker exec -i dify-db-1 psql -U postgres dify < dify_backup_20260613.sql`

- **向量数据库**（知识库 Embedding）：

  - Weaviate/Qdrant 通常有内置的备份命令或 snapshot 功能
  - Milvus 用 `milvus-backup` 工具

- **.env 配置文件**和**自定义工作流节点代码**——这些也一起备份

**💡 自动化建议**：用 `cron` 每天凌晨自动执行 pg_dump + tar 压缩 + 上传到对象存储（MinIO/S3/阿里云OSS）。保留最近 7 天的备份。

### 6.3 监控与告警

📊 需要监控的指标

- **服务健康**：Docker 容器是否在运行（`docker ps` + 健康检查）
- **资源使用**：CPU、内存、磁盘（Dify API + Worker + PostgreSQL 最吃内存）
- **API 错误率**：Dify API 返回的 5xx 错误数量和频率
- **Token 消耗**：通过 Dify 日志查询各应用的 Token 使用趋势，控制成本

推荐方案：

- **轻量级**：Docker Stats + `uptime-kuma`（开源状态监控 + Webhook 告警）
- **企业级**：Prometheus（指标采集） + Grafana（可视化仪表盘） + AlertManager（告警通知）

### 6.4 多环境配置

生产部署建议至少维护 **dev（开发）** 和 **prod（生产）** 两套 docker-compose 配置。
dev 用于测试升级和新功能，确认没问题后再操作 prod。
两套环境可以用同一个 Docker 宿主机（不同端口 + 不同 .env 文件），或分两台机器。

## 七、本节课重点回顾

- ✅ 4 条定制路径：自定义工具（推荐）→ 自定义节点 → 改前端 → Fork 改源码
- ✅ 自定义工具：设计 API → Dify 注册 → 工作流/Agent 里使用
- ✅ 工具描述要清晰：说明使用场景和必填参数
- ✅ 自定义节点需改源码：后端 Python + 前端 React，维护成本高
- ✅ 插件系统还在完善中，现阶段优先用自定义工具方案
- ✅ 维护策略：尽量不改源码、追踪官方版本、及时合并、定期备份数据库
- ✅ 生产运维：CI/CD 自动构建镜像、pg_dump 备份数据库、监控资源与 API 健康

🎓

## 课程完成！

恭喜你完成了《Dify 应用和开发》全套 8 节课程！

你现在已经具备了从部署、配置、应用搭建到二次开发的完整知识体系。
接下来就是在真实业务中实践、迭代、创造价值了。

**🚀 下一步行动建议**

1. 在 Debian 虚拟机上把 Dify 部署起来（第 2 课）
2. 用你们公司的真实文档创建一个知识库（第 4 课）
3. 搭建第一个工作流应用解决一个真实业务问题（第 5 课）

遇到问题随时问我，陪你一起把 Dify 用起来！

------

## 参考资料

- [Dify GitHub 仓库](https://github.com/langgenius/dify) — Fork 并定制源码的出发点
- [Dify 官方文档 - 工具](https://docs.dify.ai/zh/use-dify/tools) — 自定义工具配置参考
- [Dify Marketplace](https://marketplace.dify.ai/) — 现成插件和工具模板
- [Dify 开发文档](https://docs.dify.ai/zh/development) — 二次开发官方指南（如有更新）

学完所有课程了！接下来就是在实战中深化理解 🔧
