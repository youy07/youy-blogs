---
Title: OmniRoute入门:MCP 工具集成
Date: 2026-07-11
Category: ai
Tags: omniroute
Series: OmniRoute入门
Series_index: 7
Author: 悠游
Summary: MCP（Model Context Protocol）是 Anthropic 推出的开放协议，让 AI 模型可以调用外部工具和服务。
---

**95 个内置工具，让 AI 连接真实世界**

---

## 什么是 MCP？

MCP（Model Context Protocol）是 Anthropic 推出的开放协议，让 AI 模型可以调用外部工具和服务。

> **OmniRoute 内置 MCP**
>
> OmniRoute 提供 **95 个内置 MCP 工具**，支持 **3 种传输协议** 和 **30 个作用域**。

### 功能特点

- **文件系统** — 读写文件、执行命令
- **搜索工具** — grep、find、web search
- **Git 操作** — diff、status、log、branch
- **网络工具** — curl、fetch、API 调用
- **包管理** — npm、pnpm、docker
- **安全工具** — guardrails、PII 检测

---

## 支持的传输协议

| 协议    | 说明               | 适用场景           |
| ------- | ------------------ | ------------------ |
| `stdio` | 标准输入输出       | 本地工具、本地开发 |
| `sse`   | Server-Sent Events | Web 应用、远程服务 |
| `http`  | HTTP/WebSocket     | 微服务、API 集成   |

---

## 常用 MCP 工具一览

| 工具         | 功能         |
| ------------ | ------------ |
| 📁 read_file  | 读取文件内容 |
| ✏️ write_file | 写入文件内容 |
| 🔍 grep       | 搜索文件内容 |
| 🌳 list_dir   | 列出目录内容 |
| 📝 edit_file  | 编辑文件     |
| 🐚 bash       | 执行命令     |
| 🔀 git_diff   | 查看代码变更 |
| 🌐 web_search | 网络搜索     |

---

## 配置 MCP 工具

### 方式一：使用 OmniRoute Dashboard

**步骤 1：打开 MCP 设置**

在 Dashboard 中找到「MCP」或「Tools」选项

**步骤 2：启用内置工具**

打开你要使用的工具开关

**步骤 3：保存配置**

OmniRoute 自动重启 MCP 服务

### 方式二：配置文件

```json
# config/mcp.json
{
  "mcpServers": {
    "filesystem": {
      "enabled": true,
      "tools": ["read_file", "write_file", "list_dir"]
    },
    "git": {
      "enabled": true,
      "tools": ["git_diff", "git_status", "git_log"]
    },
    "web": {
      "enabled": true,
      "tools": ["web_search", "fetch"]
    }
  }
}
```

---

## 使用 MCP 工具

配置完成后，AI 模型可以自动发现并使用这些工具：

> **对话示例**
>
> **用户:** 查看 src 目录下所有 TypeScript 文件
>
> **AI:** 我来帮你列出 src 目录下的 TypeScript 文件。
>
> **调用工具: list_dir** `{"path": "src", "pattern": "*.ts"}`
>
> **工具结果:** `["src/index.ts", "src/utils.ts", "src/components/App.tsx"]`

---

## 创建自定义 MCP 工具

你也可以创建自己的 MCP 工具：

```javascript
// 创建自定义 MCP 服务器
// my-mcp-server.js
const { Server } = require('@modelcontextprotocol/sdk');

const server = new Server({
  name: 'my-tools',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {},
  },
});

server.setRequestHandler('tools/list', async () => {
  return {
    tools: [{
      name: 'my_custom_tool',
      description: '我的自定义工具',
      inputSchema: {
        type: 'object',
        properties: {
          param1: { type: 'string' }
        }
      }
    }]
  };
});

server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'my_custom_tool') {
    return {
      content: [{ type: 'text', text: `处理: ${args.param1}` }]
    };
  }
});
```

> ⚠️ **注意**
>
> 自定义 MCP 工具需要连接到 OmniRoute 的 MCP 端点。请参考官方文档了解详细的配置方法。

---

> **有问题吗？**
>
> 如果对 MCP 工具配置有疑问，或者想了解特定工具的使用方法，告诉我。
