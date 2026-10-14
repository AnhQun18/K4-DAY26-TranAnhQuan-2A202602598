"""Regression checks for the MCP v1 lab; run with the server environment."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("weather", ROOT / "04-lab/mcp-server/weather.py")
weather = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weather)


class WeatherTests(unittest.IsolatedAsyncioTestCase):
    async def test_forecast_bounds(self):
        for supplied, expected in ((-1, "1"), (0, "1"), (1, "1"), (3, "3"), (10, "3")):
            with self.subTest(days=supplied):
                with patch.object(weather, "make_weather_request", new_callable=AsyncMock, return_value=None) as request:
                    await weather.get_forecast("Hanoi", supplied)
                    self.assertEqual(request.call_args.args[1]["days"], expected)

    async def test_missing_key_does_not_send_request(self):
        with patch.object(weather, "API_KEY", None), patch.object(weather.httpx, "AsyncClient") as client:
            result = await weather.get_current_weather("Hanoi")
            self.assertIn("not configured", result)
            client.assert_not_called()

    async def test_network_failure_is_handled(self):
        with patch.object(weather, "API_KEY", "test-only"), patch.object(weather.httpx, "AsyncClient") as client:
            client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=weather.httpx.ConnectError("offline"))
            self.assertIsNone(await weather.make_weather_request("current.json", {"q": "Hanoi"}))

    async def test_rejected_key_and_location_response(self):
        for status in (400, 403):
            with self.subTest(status=status):
                response = weather.httpx.Response(status, request=weather.httpx.Request("GET", "https://example.test"))
                with patch.object(weather, "API_KEY", "test-only"), patch.object(weather.httpx, "AsyncClient") as client:
                    client.return_value.__aenter__.return_value.get = AsyncMock(return_value=response)
                    self.assertIsNone(await weather.make_weather_request("current.json", {"q": "Hanoi"}))

    async def test_empty_city_does_not_send_request(self):
        with patch.object(weather, "make_weather_request", new_callable=AsyncMock) as request:
            self.assertIn("Invalid city", await weather.get_current_weather(" "))
            self.assertIn("Invalid city", await weather.get_forecast(""))
            request.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
