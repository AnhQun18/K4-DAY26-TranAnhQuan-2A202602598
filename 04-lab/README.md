# Lab 04 — Weather Agent local

Luồng: người dùng → ADK/Gemini → MCP HTTP → WeatherAPI → câu trả lời.
Server cung cấp `get_current_weather(city)`, `get_forecast(city, days)` và `health_check()`.
Forecast giới hạn đầu vào về 1–3 ngày; health chỉ xác nhận MCP hoạt động, không xác thực WeatherAPI.

## Chuẩn bị trên Windows / PowerShell

Dùng Python 3.12 và hai môi trường riêng cho server/client. Bài 01–03 dùng môi trường gốc với MCP v2; lab dùng MCP v1 theo lockfile. Không cài chồng hai bộ dependency.

Từ gốc repo, nếu chưa có cấu hình:

```powershell
Copy-Item .env.example .env
```

Điền `GOOGLE_API_KEY` và `WEATHERAPI_KEY` trong `.env` bằng trình soạn thảo; dùng cùng một khóa nếu đặt thêm `GEMINI_API_KEY`. Biến môi trường của terminal được ưu tiên, tiếp theo là `.env` của từng thành phần rồi `.env` gốc. Không commit khóa.

Cài dependency một lần trong từng thư mục:

```powershell
Set-Location .\04-lab\mcp-server
uv sync --locked --python 3.12
Set-Location ..\mcp-client
uv sync --locked --python 3.12
```

## Chạy theo thứ tự

Terminal 1, từ gốc repo:

```powershell
Set-Location .\04-lab\mcp-server
.\.venv\Scripts\python.exe weather.py
```

Server mặc định HTTP tại `http://localhost:8085/mcp`; đặt `PORT` nếu cần đổi cổng. Chỉ dùng `--stdio` khi kết nối bằng client stdio.

Terminal 2 mới, từ gốc repo:

```powershell
Set-Location .\04-lab\mcp-client
.\.venv\Scripts\python.exe verify_setup.py
.\.venv\Scripts\python.exe check_weather.py
.\.venv\Scripts\python.exe test_chat.py
.\.venv\Scripts\adk.exe web
```

Mở http://localhost:8000, chọn `weather_agent`, hỏi thời tiết Hà Nội và dự báo Đà Nẵng ba ngày. Kiểm tra Events có tool call, tool response và câu trả lời cuối. Model hiện cấu hình `gemini-3.5-flash-lite`.

`verify_setup.py` kiểm tra cấu hình, dependency, MCP initialize/list_tools/health_check và khám phá tool qua ADK. Chỉ `check_weather.py` kiểm chứng WeatherAPI thật; `test_chat.py` kiểm chứng thêm Gemini. Import agent thành công chưa chứng minh kết nối mạng.

## Kiểm tra lỗi

Trong terminal client riêng:

```powershell
$env:MCP_SERVER_URL='http://localhost:8085/wrong-path'
.\.venv\Scripts\python.exe verify_setup.py
# Phải exit 1
Remove-Item Env:MCP_SERVER_URL
```

Dừng server bằng Ctrl+C và chạy verify lần nữa: phải exit 1. Khởi động lại server, verify phải exit 0. Biến trong terminal cũ không tự xuất hiện ở terminal mới.

404 thường là sai endpoint; lỗi kết nối thường do server dừng/sai cổng. Không suy ra trạng thái MCP từ một HTTP GET đơn lẻ. Dừng auth demo trước khi mở ADK vì cùng dùng cổng 8000.

Nếu import `pydantic_core` thất bại, kiểm tra `python --version` và tái đồng bộ môi trường bằng Python 3.12. Không dùng môi trường Python 3.14 chứa wheel cp312.

## Minh chứng và phạm vi

Ảnh đã lưu ở `screenshots/`, log kiểm chứng ở `evidence/`; xem `PLAN.md` và `evidence/RESULTS.md` tại gốc repo.
Docker/Cloud Run thuộc phần mở rộng và không thực hiện trong lần bàn giao này.
