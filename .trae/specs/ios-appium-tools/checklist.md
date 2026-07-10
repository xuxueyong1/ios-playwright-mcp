# iOS Appium Tools - Verification Checklist

- [ ] Checkpoint 1: 共享会话管理器创建成功，多次调用返回同一 driver 实例
- [ ] Checkpoint 2: dump_ui_element 函数返回非空的 XML 格式字符串
- [ ] Checkpoint 3: element_click 函数能正确执行 accessibility_id 点击操作
- [ ] Checkpoint 4: element_click 函数能处理不存在的 accessibility_id 并返回错误信息
- [ ] Checkpoint 5: element_click 函数能处理空字符串参数并返回错误信息
- [ ] Checkpoint 6: MCP 服务器启动正常，三个工具均已注册
- [ ] Checkpoint 7: take_ios_screenshot 功能正常，使用共享会话
- [ ] Checkpoint 8: 代码风格一致，文档完整