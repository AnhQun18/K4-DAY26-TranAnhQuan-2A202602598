"""Verify local configuration, ADK discovery and a real MCP health call."""
import asyncio
import importlib
import os
from pathlib import Path
import sys

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
EXPECTED_TOOLS = {"get_current_weather", "get_forecast", "health_check"}


def load_configuration():
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
    load_dotenv(BASE_DIR.parent.parent / ".env")


def check_environment():
    load_configuration()
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    configured = bool(key and not key.startswith("your_") and key.strip())
    print(f"{'PASS' if configured else 'FAIL'} API key configured (API validity checked by test_chat.py)")
    return configured


def check_dependencies():
    ok = True
    for package in ("google.adk", "google.genai", "mcp", "dotenv", "httpx"):
        try:
            importlib.import_module(package)
            print(f"PASS import {package}")
        except ImportError:
            print(f"FAIL import {package}; run uv sync --locked --python 3.12")
            ok = False
    return ok


def check_agent_structure():
    ok = all((BASE_DIR / path).is_file() for path in (
        "weather_agent/agent.py", "weather_agent/__init__.py"))
    print(f"{'PASS' if ok else 'FAIL'} agent files")
    return ok


async def verify_mcp(server_url):
    import httpx
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

    async with httpx.AsyncClient(timeout=10) as client:
        async with streamable_http_client(server_url, http_client=client) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                names = {tool.name for tool in (await session.list_tools()).tools}
                if not EXPECTED_TOOLS <= names:
                    raise ValueError(f"Missing tools: {sorted(EXPECTED_TOOLS - names)}")
                result = await session.call_tool("health_check", {})
                if result.isError or not any(getattr(item, "text", "").strip() for item in result.content):
                    raise ValueError("health_check failed or returned no text")
                print("PASS MCP initialize, required tools and health_check")

    toolset = McpToolset(connection_params=StreamableHTTPConnectionParams(url=server_url, timeout=10))
    try:
        names = {tool.name for tool in await toolset.get_tools()}
        if not EXPECTED_TOOLS <= names:
            raise ValueError("ADK discovery missing required tools")
        print("PASS ADK tool discovery: " + ", ".join(sorted(names)))
    finally:
        await toolset.close()


def check_mcp_server():
    load_configuration()
    try:
        asyncio.run(asyncio.wait_for(verify_mcp(os.getenv("MCP_SERVER_URL", "http://localhost:8085/mcp")), 35))
        return True
    except Exception as error:
        print(f"FAIL MCP connection/handshake/health ({type(error).__name__})")
        return False


def check_agent_import():
    try:
        from weather_agent import root_agent
        if not root_agent.tools:
            raise ValueError("Agent has no tools")
        print(f"PASS agent configuration: {root_agent.name}, model={root_agent.model}")
        return True
    except Exception as error:
        print(f"FAIL agent configuration ({type(error).__name__})")
        return False


def main():
    checks = []
    for check in (check_dependencies, check_environment, check_agent_structure,
                  check_mcp_server, check_agent_import):
        try:
            checks.append(check())
        except Exception as error:
            print(f"FAIL {check.__name__} ({type(error).__name__})")
            checks.append(False)
    print("All checks passed!" if all(checks) else "Some checks failed")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
