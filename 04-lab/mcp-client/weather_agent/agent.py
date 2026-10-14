"""Weather agent using local MCP tools. Connections open on discovery."""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8085/mcp")
weather_tools = McpToolset(connection_params=StreamableHTTPConnectionParams(
    url=MCP_SERVER_URL, timeout=30.0))
root_agent = Agent(
    name="weather_agent",
    model="gemini-3.5-flash-lite",
    instruction=("Trả lời bằng tiếng Việt. Luôn dùng công cụ cho câu hỏi thời tiết. "
                 "Nếu công cụ lỗi hoặc không có dữ liệu, nói rõ không lấy được dữ liệu; "
                 "không tự tạo số liệu thời tiết."),
    tools=[weather_tools],
)
logging.getLogger(__name__).info("Agent configured; run verify_setup.py to verify MCP connectivity.")
