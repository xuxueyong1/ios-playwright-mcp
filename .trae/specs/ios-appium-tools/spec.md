# iOS Appium Tools - Product Requirement Document

## Overview
- **Summary**: 在现有的 iOS Screenshot MCP Server 基础上，新增两个工具：`element_click`（通过 accessibility_id 点击元素）和 `dump_ui_element`（获取 UI 元素树）
- **Purpose**: 提供完整的 iOS 自动化测试能力，支持截图、点击和 UI 树获取，便于测试人员进行自动化操作
- **Target Users**: 测试工程师、自动化测试脚本开发者

## Goals
- 实现 `element_click` 工具，通过 accessibility_id 点击元素
- 实现 `dump_ui_element` 工具，获取当前屏幕的完整 UI 元素树（XML 格式）
- 优化 Appium 会话管理，支持跨工具调用共享会话

## Non-Goals (Out of Scope)
- 不实现独立的元素查找（find_element）工具（element_click 内部已集成）
- 不实现滑动、长按等复杂手势操作
- 不实现多设备并发支持
- 不实现会话持久化存储

## Background & Context
- 现有项目使用 Appium Python Client 和 FastMCP 框架
- 当前 `take_ios_screenshot` 每次调用创建并销毁 Appium 会话
- 新增工具需要共享会话以确保操作的一致性和有效性

## Functional Requirements
- **FR-1**: `element_click` 工具接收 accessibility_id 参数，通过元素的 accessibility identifier 执行点击操作
- **FR-2**: `dump_ui_element` 工具返回当前屏幕的完整 UI 元素树（XML 格式）
- **FR-3**: 所有工具共享同一个 Appium 会话，避免重复创建连接

## Non-Functional Requirements
- **NFR-1**: 工具调用响应时间 < 5 秒（网络延迟除外）
- **NFR-2**: 会话管理线程安全，避免并发冲突
- **NFR-3**: 错误处理完善，提供清晰的错误信息

## Constraints
- **Technical**: Python 3.11+, Appium Python Client 5.3.1+, FastMCP 3.4.4+
- **Dependencies**: 需要运行 Appium 服务器（默认端口 4723）

## Assumptions
- Appium 服务器已在本地运行（http://127.0.0.1:4723）
- iOS 设备已配置好并可通过 Appium 访问
- 用户提供的 accessibility_id 对应屏幕上存在的元素

## Acceptance Criteria

### AC-1: element_click 工具 accessibility_id 点击成功
- **Given**: Appium 服务器运行正常，设备连接正常，目标元素存在
- **When**: 调用 `element_click` 工具，传入有效的 accessibility_id
- **Then**: 对应元素被点击，返回成功消息
- **Verification**: `programmatic`

### AC-2: element_click 工具处理无效参数
- **Given**: Appium 服务器运行正常，设备连接正常
- **When**: 调用 `element_click` 工具，传入不存在的 accessibility_id 或空字符串
- **Then**: 返回错误信息，说明参数无效
- **Verification**: `programmatic`

### AC-3: dump_ui_element 工具返回 UI 树
- **Given**: Appium 服务器运行正常，设备连接正常，应用已启动
- **When**: 调用 `dump_ui_element` 工具
- **Then**: 返回包含完整 UI 元素信息的 XML 字符串
- **Verification**: `programmatic`

### AC-4: 工具共享会话
- **Given**: 已调用过截图或 dump 工具建立会话
- **When**: 连续调用多个工具
- **Then**: 使用同一个 Appium 会话，无需重复建立连接
- **Verification**: `human-judgment`

## Open Questions
- [ ] 是否需要添加显式的会话断开工具？