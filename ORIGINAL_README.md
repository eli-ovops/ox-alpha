# Ox Alpha Local Client

这是一个隔离的本地调用客户端，不是本地模型权重或本地推理部署。
模型实际运行在 OpenRouter 远程服务；本地只保存调用脚本和独立 Codex 配置。

模型固定为 `stealth/ox-alpha`。每次调用前都会实时检查模型存在且 prompt/completion 价格均为 0；价格变化或模型消失时启动器会拒绝调用。

## 使用

```bash
cd ~/Documents/ox-alpha-local
./bin/check-ox
./bin/ask-ox
./bin/ask-ox "Reply with exactly: OX_ALPHA_OK"
./bin/run-ox-codex
```

API Key 只在当前进程中通过 `OPENROUTER_API_KEY` 或终端隐藏输入提供，不写入本目录、`.env`、Codex 配置或命令参数。不要发送客户源码、私有项目、生产凭据或隐私数据。

Codex 入口使用本目录的隔离 `CODEX_HOME`，不会修改原有 `~/.codex`。当前 Provider 配置使用 Responses API；如果 Codex 版本与该模型不兼容，`bin/ask-ox` 仍可作为独立 API 入口。

常见状态：401 表示密钥无效；402 表示账户余额或免费政策变化；404/Unknown model 表示模型不可用；429/5xx 表示服务暂时失败；Provider incompatibility 表示 Codex 入口不兼容。
