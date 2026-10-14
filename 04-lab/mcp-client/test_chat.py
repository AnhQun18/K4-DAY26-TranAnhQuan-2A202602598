import asyncio
import os
import sys
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
load_dotenv()

from google.adk import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from weather_agent.agent import root_agent, weather_tools

async def ask(question: str, expected_tool: str):
    print(f"\n==================================================")
    print(f"User: {question}")
    print(f"==================================================")

    session_service = InMemorySessionService()
    runner = Runner(
        app_name="weather_agent_app",
        agent=root_agent,
        session_service=session_service,
        auto_create_session=True,
    )

    msg = types.Content(
        role="user",
        parts=[types.Part.from_text(text=question)],
    )

    calls, responses, final_text = set(), set(), []
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=msg,
    ):
        # Look for function calls or model text in event
        content = getattr(event, "content", None)
        if content and getattr(content, "parts", None):
            for part in content.parts:
                fn_call = getattr(part, "function_call", None)
                if fn_call:
                    calls.add(fn_call.name)
                    print(f"  [ADK Tool Call] -> {fn_call.name}({fn_call.args})")
                fn_resp = getattr(part, "function_response", None)
                if fn_resp:
                    responses.add(fn_resp.name)
                    print(f"  [MCP Server Response] -> {str(fn_resp.response)[:150]}...")
                text = getattr(part, "text", None)
                if text:
                    print(f"\nAgent: {text}")
                    if event.is_final_response():
                        final_text.append(text)
    if expected_tool not in calls or expected_tool not in responses or not final_text:
        raise AssertionError("Missing expected tool call, tool response or final answer")
    print(f"PASS end-to-end: {expected_tool}")

async def main():
    try:
        await ask("Thời tiết Hà Nội hiện tại thế nào?", "get_current_weather")
        await ask("Dự báo thời tiết Đà Nẵng 3 ngày tới", "get_forecast")
    finally:
        await weather_tools.close()

if __name__ == "__main__":
    asyncio.run(main())
