# iOS Appium Tools 实现计划

## 仓库调研结论

**现有代码结构：**
- [mcp_server.py](file:///Users/xuxueyong/Desktop/mcp-servers/ios-playwright-mcp/mcp_server.py) - MCP 服务器主文件，注册了 `take_ios_screenshot_tool`
- [screenshot_service.py](file:///Users/xuxueyong/Desktop/mcp-servers/ios-playwright-mcp/screenshot_service.py) - 截图服务函数，每次调用创建并销毁 Appium 会话
- [main.py](file:///Users/xuxueyong/Desktop/mcp-servers/ios-playwright-mcp/main.py) - 测试脚本
- [pyproject.toml](file:///Users/xuxueyong/Desktop/mcp-servers/ios-playwright-mcp/pyproject.toml) - 依赖配置（Appium Python Client 5.3.1+, FastMCP 3.4.4+）

**核心问题：**
当前 `take_ios_screenshot` 每次调用都创建新的 Appium 会话，新工具需要共享会话。

## 需要编辑的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `screenshot_service.py` | 修改 | 添加会话管理器、`dump_ui_element` 和 `element_click` 函数 |
| `mcp_server.py` | 修改 | 注册新工具 `element_click_tool` 和 `dump_ui_element_tool` |

## 实施步骤

### 步骤 1：创建共享会话管理器

**目标：** 在 `screenshot_service.py` 中添加会话管理器类

**实现方案：**
- 创建 `AppiumSessionManager` 类，使用单例模式
- 提供 `get_driver()` 方法，懒加载创建会话
- 提供 `quit_driver()` 方法，关闭会话
- 添加线程锁确保线程安全
- 使用 `threading.Lock()` 保护 driver 实例

**修改内容：**
```python
import threading
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

class AppiumSessionManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._driver = None
                cls._instance._driver_lock = threading.Lock()
                cls._instance._capabilities = {}
        return cls._instance
    
    def get_driver(self, **capabilities):
        with self._driver_lock:
            if self._driver is None:
                self._capabilities = capabilities
                options = AppiumOptions()
                for key, value in capabilities.items():
                    options.set_capability(key, value)
                self._driver = webdriver.Remote(
                    capabilities.get("appium_server_url", "http://127.0.0.1:4723"),
                    options=options
                )
            return self._driver
    
    def quit_driver(self):
        with self._driver_lock:
            if self._driver is not None:
                self._driver.quit()
                self._driver = None
```

### 步骤 2：实现 dump_ui_element 函数

**目标：** 在 `screenshot_service.py` 中添加 `dump_ui_element` 函数

**实现方案：**
- 使用会话管理器获取 driver
- 调用 `driver.page_source` 获取 XML 格式的 UI 树
- 返回 XML 字符串

**修改内容：**
```python
def dump_ui_element(
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723"
) -> str:
    manager = AppiumSessionManager()
    driver = manager.get_driver(
        platformName=platform_name,
        automationName=automation_name,
        deviceName=device_name,
        udid=udid,
        bundleId=bundle_id,
        appium_server_url=appium_server_url
    )
    return driver.page_source
```

### 步骤 3：实现 element_click 函数

**目标：** 在 `screenshot_service.py` 中添加 `element_click` 函数

**实现方案：**
- 接收 `accessibility_id` 参数
- 添加参数校验（非空检查）
- 使用 `driver.find_element(AppiumBy.ACCESSIBILITY_ID, id).click()` 执行点击
- 捕获 `NoSuchElementException` 并返回错误信息

**修改内容：**
```python
from selenium.common.exceptions import NoSuchElementException

def element_click(
    accessibility_id: str,
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723"
) -> str:
    if not accessibility_id or not accessibility_id.strip():
        raise ValueError("accessibility_id cannot be empty")
    
    manager = AppiumSessionManager()
    driver = manager.get_driver(
        platformName=platform_name,
        automationName=automation_name,
        deviceName=device_name,
        udid=udid,
        bundleId=bundle_id,
        appium_server_url=appium_server_url
    )
    
    try:
        element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)
        element.click()
        return f"Successfully clicked element with accessibility_id: {accessibility_id}"
    except NoSuchElementException:
        raise ValueError(f"Element with accessibility_id '{accessibility_id}' not found")
```

### 步骤 4：更新 take_ios_screenshot 使用共享会话

**目标：** 修改 `take_ios_screenshot` 函数使用共享会话

**实现方案：**
- 使用会话管理器获取 driver
- 移除 `driver.quit()` 调用
- 添加可选的 `close_session` 参数，默认 `False`

**修改内容：**
```python
def take_ios_screenshot(
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723",
    output_path: str = "screen.png",
    close_session: bool = False
) -> str:
    manager = AppiumSessionManager()
    driver = manager.get_driver(
        platformName=platform_name,
        automationName=automation_name,
        deviceName=device_name,
        udid=udid,
        bundleId=bundle_id,
        appium_server_url=appium_server_url
    )
    
    driver.save_screenshot(output_path)
    
    if close_session:
        manager.quit_driver()
    
    return output_path
```

### 步骤 5：注册 MCP 工具

**目标：** 在 `mcp_server.py` 中注册新工具

**实现方案：**
- 导入 `element_click` 和 `dump_ui_element` 函数
- 注册 `element_click_tool` 工具
- 注册 `dump_ui_element_tool` 工具
- 添加完整的参数说明和文档字符串

**修改内容：**
```python
from screenshot_service import take_ios_screenshot, element_click, dump_ui_element

@server.tool()
def element_click_tool(
    accessibility_id: str,
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723"
) -> str:
    """
    通过 accessibility_id 点击 iOS 设备上的元素
    
    Args:
        accessibility_id: 元素的 accessibility identifier
        platform_name: 平台名称，默认为 iOS
        automation_name: 自动化框架名称，默认为 XCUITest
        device_name: 设备名称，默认为 iPhone 16 Pro Max
        udid: 设备唯一标识符
        bundle_id: 应用 Bundle ID
        appium_server_url: Appium 服务器地址
    
    Returns:
        操作结果消息
    """
    return element_click(
        accessibility_id=accessibility_id,
        platform_name=platform_name,
        automation_name=automation_name,
        device_name=device_name,
        udid=udid,
        bundle_id=bundle_id,
        appium_server_url=appium_server_url
    )

@server.tool()
def dump_ui_element_tool(
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723"
) -> str:
    """
    获取 iOS 设备当前屏幕的完整 UI 元素树
    
    Args:
        platform_name: 平台名称，默认为 iOS
        automation_name: 自动化框架名称，默认为 XCUITest
        device_name: 设备名称，默认为 iPhone 16 Pro Max
        udid: 设备唯一标识符
        bundle_id: 应用 Bundle ID
        appium_server_url: Appium 服务器地址
    
    Returns:
        UI 元素树的 XML 字符串
    """
    return dump_ui_element(
        platform_name=platform_name,
        automation_name=automation_name,
        device_name=device_name,
        udid=udid,
        bundle_id=bundle_id,
        appium_server_url=appium_server_url
    )
```

## 潜在依赖与注意事项

**依赖：**
- Appium Python Client 已在 `pyproject.toml` 中声明（>=5.3.1）
- 需要 `AppiumBy` 类，从 `appium.webdriver.common.appiumby` 导入
- 需要 `NoSuchElementException`，从 `selenium.common.exceptions` 导入

**风险处理：**
- 会话管理器使用线程锁，避免并发问题
- `element_click` 捕获 `NoSuchElementException`，提供清晰的错误信息
- `element_click` 添加参数非空校验
- `take_ios_screenshot` 添加 `close_session` 参数，保持向后兼容

## 验证计划

1. **会话管理器验证**：多次调用获取 driver 返回同一实例
2. **dump_ui_element 验证**：返回非空的 XML 字符串，包含 `<XCUIElementTypeApplication>` 根节点
3. **element_click 验证**：
   - 传入有效 accessibility_id 返回成功消息
   - 传入不存在的 accessibility_id 返回错误
   - 传入空字符串返回错误
4. **MCP 服务器验证**：启动正常，三个工具均已注册
5. **截图功能验证**：截图功能正常工作

## 完成标准

- [ ] `screenshot_service.py` 包含会话管理器、`dump_ui_element` 和 `element_click` 函数
- [ ] `mcp_server.py` 注册了 `element_click_tool` 和 `dump_ui_element_tool` 工具
- [ ] MCP 服务器能正常启动
- [ ] 所有工具使用共享会话管理器