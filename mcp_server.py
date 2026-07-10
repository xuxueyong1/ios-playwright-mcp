from mcp.server import FastMCP
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import argparse
from screenshot_service import take_ios_screenshot


server = FastMCP(
    name="iOS Screenshot MCP Server",
    instructions="提供 iOS 设备屏幕截图功能"
)


@server.tool()
def take_ios_screenshot_tool(
    platform_name: str = "iOS",
    automation_name: str = "XCUITest",
    device_name: str = "iPhone 16 Pro Max",
    udid: str = "32EFED52-E30A-4CC8-AAE9-525B5A3A5B6A",
    bundle_id: str = "com.xue.Demo01",
    appium_server_url: str = "http://127.0.0.1:4723",
    output_path: str = "screen.png"
) -> str:
    """
    截取 iOS 设备屏幕并保存为图片文件

    Args:
        platform_name: 平台名称，默认为 iOS
        automation_name: 自动化框架名称，默认为 XCUITest
        device_name: 设备名称，默认为 iPhone 16 Pro Max
        udid: 设备唯一标识符
        bundle_id: 应用 Bundle ID
        appium_server_url: Appium 服务器地址
        output_path: 截图保存路径

    Returns:
        截图文件的完整路径
    """
    return take_ios_screenshot(
        platform_name=platform_name,
        automation_name=automation_name,
        device_name=device_name,
        udid=udid,
        bundle_id=bundle_id,
        appium_server_url=appium_server_url,
        output_path=output_path
    )


app = FastAPI(title="iOS Screenshot MCP Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.mount("/mcp", server.sse_app())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="iOS Screenshot MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Run in stdio mode for Trae MCP")
    parser.add_argument("--port", type=int, default=8000, help="Server port (HTTP mode)")
    args = parser.parse_args()
    
    if args.stdio:
        server.run()
    else:
        uvicorn.run(
            "mcp_server:app",
            host="0.0.0.0",
            port=args.port,
            reload=False
        )
