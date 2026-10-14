"""HTTP rejection checks; run while the demo auth server occupies port 8000."""
import httpx

for label, headers in (("missing", {}), ("invalid", {"Authorization": "Bearer deliberately-invalid"})):
    result = httpx.post("http://localhost:8000/mcp", headers=headers,
                        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, timeout=10)
    assert result.status_code == 401, f"Unexpected status: {result.status_code}"
    print(f"PASS {label} token -> HTTP {result.status_code}")
