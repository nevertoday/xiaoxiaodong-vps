# 小小东 VPS

一套可复用的 VPS 部署蓝图，用于配置 3x-ui / Xray 节点、OpenClash 与 Shadowrocket 订阅、AI 分流、CLIProxyAPI、自动升级、SSH 密钥登录、备份和安全加固。

## 内容

- [3x-ui + CLIProxyAPI 多服务器部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md)

蓝图包含完整的部署顺序、端口规划、节点逻辑、Gemini / Grok / Muse / OpenAI / Claude 分流、CLIProxyAPI 管理中心、自动升级与回滚、验收清单和常见故障处理。

## 安全说明

本项目只发布通用架构和占位符，不包含任何真实服务器的：

- SSH 私钥
- 面板密码
- 订阅密钥
- Reality 私钥
- OAuth 文件
- CLIProxyAPI 管理密钥或 API Key

部署时必须为每台服务器重新生成凭据，并通过本机安全文件或密钥管理器注入，不要把真实密钥提交到 Git。

## 适用范围

这是一份部署和运维参考方案，不保证所有服务商线路、运营商网络、客户端版本或上游 AI 账号都能直接工作。完成部署后必须按文档中的验收清单进行实际连接测试。
