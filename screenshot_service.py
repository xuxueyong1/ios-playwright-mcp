from appium import webdriver
from appium.options.common import AppiumOptions


def take_ios_screenshot(
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723",
    output_path: str = "screen.png"
) -> str:
    options = AppiumOptions()
    options.set_capability("platformName", platform_name)
    options.set_capability("automationName", automation_name)
    options.set_capability("deviceName", device_name)
    options.set_capability("udid", udid)
    options.set_capability("bundleId", bundle_id)

    driver = webdriver.Remote(
        appium_server_url,
        options=options
    )

    driver.save_screenshot(output_path)
    driver.quit()

    return output_path