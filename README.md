# iOS Screenshot MCP Server

基于 Appium 的 iOS 设备屏幕截图 MCP Server，可用于 Trae 等支持 MCP 协议的 AI 客户端。

## 安装依赖

```bash
uv sync
```

## 运行方式

### 方式一：Stdio 模式（推荐用于 Trae）

```bash
uv run python mcp_server.py --stdio
```

### 方式二：SSE 模式（用于远程连接）

```bash
uv run python mcp_server.py
```

服务器将在 `http://localhost:8000` 运行。

## Trae MCP 配置

### Stdio 模式（推荐）

将以下 JSON 配置添加到 Trae 的 MCP Servers 配置中：

```json
{
  "name": "iOS Screenshot MCP",
  "type": "stdio",
  "command": "uv run python mcp_server.py --stdio",
  "cwd": "/Users/xuxueyong/Desktop/Python/练习/AppuimDemo",
  "enabled": true
}
```

### SSE 模式

先启动服务器：

```bash
cd /Users/xuxueyong/Desktop/Python/练习/AppuimDemo
uv run python mcp_server.py
```

将以下 JSON 配置添加到 Trae 的 MCP Servers 配置中：

```json
{
  "name": "iOS Screenshot MCP",
  "type": "sse",
  "url": "http://localhost:8000/mcp/sse",
  "enabled": true
}
```

## 工具说明

### take_ios_screenshot_tool

截取 iOS 设备屏幕并保存为图片文件。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| platform_name | str | iOS | 平台名称 |
| automation_name | str | XCUITest | 自动化框架名称 |
| device_name | str | iPhone 16 Pro Max | 设备名称 |
| udid | str | 32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A | 设备唯一标识符 |
| bundle_id | str | com.xue.Demo01 | 应用 Bundle ID |
| appium_server_url | str | http://127.0.0.1:4723 | Appium 服务器地址 |
| output_path | str | screen.png | 截图保存路径 |

**返回值：**

截图文件的完整路径。

## 前置条件

调用截图工具前需要确保：

1. **Appium Server** 已启动在 `http://127.0.0.1:4723`
2. **目标设备/模拟器**已连接
3. **指定的应用**（`bundle_id`）已安装在设备上

## 文件结构

```
.
├── mcp_server.py          # MCP Server 主文件
├── screenshot_service.py  # 截图逻辑服务模块
├── main.py                # 原始截图脚本
├── pyproject.toml         # 项目配置
└── README.md              # 项目说明
```
