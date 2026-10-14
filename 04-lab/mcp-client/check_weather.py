"""Exercise real weather tools over MCP HTTP, without a model call."""
import asyncio
import os
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from verify_setup import load_configuration


async def main():
    load_configuration()
    async with httpx.AsyncClient(timeout=45) as client:
        async with streamable_http_client(os.getenv("MCP_SERVER_URL", "http://localhost:8085/mcp"), http_client=client) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                for name, args, marker in (
                    ("get_current_weather", {"city": "Hanoi"}, "Current Weather for"),
                    ("get_forecast", {"city": "Danang", "days": 1}, "Weather Forecast for"),
                    ("get_forecast", {"city": "Danang", "days": 3}, "Weather Forecast for"),
                    ("get_current_weather", {"city": " "}, "Invalid city"),
                ):
                    result = await session.call_tool(name, args)
                    text = "\n".join(getattr(item, "text", "") for item in result.content)
                    if result.isError or marker not in text:
                        print(f"FAIL {name}: {text}")
                        raise AssertionError(f"Unexpected result for {name}")
                    if name == "get_forecast":
                        assert text.count("High:") == args["days"], "Wrong forecast length"
                    print(f"PASS {name} {args}\n{text}")


if __name__ == "__main__":
    asyncio.run(main())
