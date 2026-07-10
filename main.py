from appium import webdriver
from appium.options.common import AppiumOptions


options = AppiumOptions()
options.set_capability("platformName", "iOS")
options.set_capability("automationName", "XCUITest")
options.set_capability("deviceName", "iPhone 16 Pro Max")
options.set_capability("udid", "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A")
options.set_capability("bundleId", "com.xue.Demo01")


driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)


driver.save_screenshot(
    "screen.png"
)


driver.quit()