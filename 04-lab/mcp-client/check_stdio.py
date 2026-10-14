"""Verify lab stdio transport is free of stdout logging pollution."""
import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server = Path(__file__).resolve().parent.parent / "mcp-server"
    params = StdioServerParameters(command=str(server / ".venv/Scripts/python.exe"),
                                   args=[str(server / "weather.py"), "--stdio"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = {tool.name for tool in (await session.list_tools()).tools}
            assert names == {"get_current_weather", "get_forecast", "health_check"}
            assert not (await session.call_tool("health_check", {})).isError
            print("PASS lab stdio initialize/list_tools/health_check without stdout pollution")


if __name__ == "__main__":
    asyncio.run(main())
