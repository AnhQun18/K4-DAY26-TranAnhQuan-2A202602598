"""Regression checks for the MCP v2 demos; run with the root environment."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch, Mock
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DemoTests(unittest.TestCase):
    def function_module(self):
        with patch.dict("os.environ", {"GOOGLE_API_KEY": "test-only", "GEMINI_API_KEY": "test-only"}):
            return load("function_demo", "01-function-calling/weather_function_calling.py")

    def test_city_aliases(self):
        module = self.function_module()
        for city, temperature in (("Ha Noi", "29°C"), ("Hanoi", "29°C"), ("Da Nang", "30°C"), ("Đà Nẵng", "30°C")):
            self.assertEqual(json.loads(module.get_weather(city))["nhiệt_độ"], temperature)

    def test_invalid_tool_is_rejected(self):
        module = self.function_module()
        response = SimpleNamespace(function_calls=[SimpleNamespace(name="unknown", args={"city": "Hanoi"})],
                                   candidates=[SimpleNamespace(content=Mock())])
        with patch.object(module.client.models, "generate_content", return_value=response):
            with self.assertRaises(ValueError):
                module.run("test")

    def test_tool_loop_is_bounded(self):
        module = self.function_module()
        response = SimpleNamespace(function_calls=[SimpleNamespace(name="get_weather", args={"city": "Hanoi"})],
                                   candidates=[SimpleNamespace(content=Mock())])
        with patch.object(module.client.models, "generate_content", return_value=response) as generate:
            with self.assertRaisesRegex(RuntimeError, "8 tool rounds"):
                module.run("test")
            self.assertEqual(generate.call_count, 9)

    def test_registry_utf8_and_selection(self):
        module = load("registry", "03-production/registry_client.py")
        registry = module.ToolRegistry()
        self.assertIn("thời tiết", registry.tools["get_weather"]["description"])
        self.assertEqual(registry.best_match(tag="weather")["tool"], "get_weather_v2")
        registry.tools["get_weather"]["version"] = "10.0.0"
        self.assertEqual(registry.best_match(tag="weather")["tool"], "get_weather")
        registry.tools["get_weather"]["deprecated"] = True
        self.assertEqual(registry.best_match(tag="weather")["tool"], "get_weather_v2")

    def test_versioning_and_units(self):
        module = load("versioned", "03-production/versioned_server.py")
        self.assertIn("29°C", module.get_weather("Hanoi"))
        data = json.loads(module.get_weather_v2("Hanoi", True, "fahrenheit"))
        self.assertEqual(data["temp"], 84.2)
        self.assertEqual([item["temp"] for item in data["forecast"]], [80.6, 87.8])
        self.assertIn("error", json.loads(module.get_weather_v2("Hanoi", units="kelvin")))
        self.assertIn("error", json.loads(module.get_weather_v2("Unknown")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
