import threading
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException


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
                    if key != "appium_server_url":
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