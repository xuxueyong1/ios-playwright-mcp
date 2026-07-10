# iOS Appium Tools - Implementation Plan

## [ ] Task 1: 创建共享 Appium 会话管理器
- **Priority**: high
- **Depends On**: None
- **Description**: 
  - 创建一个会话管理器类，支持懒加载创建 Appium 会话
  - 提供获取和关闭会话的方法
  - 确保线程安全
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-1.1: 多次调用获取会话方法返回同一个 driver 实例
  - `programmatic` TR-1.2: 调用关闭方法后，再次获取会创建新会话
- **Notes**: 参考现有的 screenshot_service.py 中的 capability 配置

## [ ] Task 2: 实现 dump_ui_element 服务函数
- **Priority**: high
- **Depends On**: Task 1
- **Description**: 
  - 在 service 文件中实现 `dump_ui_element` 函数
  - 使用共享会话获取页面 source（XML 格式）
  - 返回 UI 元素树字符串
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-2.1: 调用函数返回非空字符串
  - `programmatic` TR-2.2: 返回字符串为有效的 XML 格式（包含 `<XCUIElementTypeApplication>` 根节点）
- **Notes**: 使用 driver.page_source 获取完整的 UI 树

## [ ] Task 3: 实现 element_click 服务函数
- **Priority**: high
- **Depends On**: Task 1
- **Description**: 
  - 在 service 文件中实现 `element_click` 函数
  - 接收 accessibility_id 参数
  - 使用 driver.find_element(AppiumBy.ACCESSIBILITY_ID, id).click() 执行点击
  - 添加参数校验（非空检查）
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: 传入有效 accessibility_id 返回成功消息
  - `programmatic` TR-3.2: 传入不存在的 accessibility_id 返回错误
  - `programmatic` TR-3.3: 传入空字符串返回错误
- **Notes**: 使用 AppiumBy.ACCESSIBILITY_ID 进行元素查找

## [ ] Task 4: 注册 MCP 工具
- **Priority**: high
- **Depends On**: Task 2, Task 3
- **Description**: 
  - 在 mcp_server.py 中注册 `element_click_tool` 和 `dump_ui_element_tool`
  - 添加完整的参数说明和文档字符串
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3
- **Test Requirements**:
  - `human-judgment` TR-4.1: 工具注册代码符合现有代码风格
  - `human-judgment` TR-4.2: 文档字符串完整清晰
- **Notes**: 参考现有的 take_ios_screenshot_tool 注册方式

## [ ] Task 5: 更新 take_ios_screenshot 使用共享会话
- **Priority**: medium
- **Depends On**: Task 1
- **Description**: 
  - 修改 `take_ios_screenshot` 函数使用共享会话管理器
  - 移除每次调用创建和销毁会话的逻辑
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-5.1: 截图功能正常工作，返回正确的文件路径
- **Notes**: 需要添加可选的关闭会话参数，以保持向后兼容