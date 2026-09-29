# MCP

这里维护 MCP server 的“目录”和“可复用接入模板”。

## 不存什么

- token
- API key
- cookie
- private key
- 真实凭据文件

只提交环境变量名称或占位符。

## 建议

真正的启用配置由各 Agent runtime 单独生成：

- Claude Code
- Codex
- OpenCode
- Cursor
- 其他支持 MCP 的客户端

本仓库保持 vendor-neutral。
