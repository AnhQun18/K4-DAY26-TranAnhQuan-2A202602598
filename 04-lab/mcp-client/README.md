# Weather Agent — ADK client

Hướng dẫn chạy đầy đủ: [Lab 04](../README.md).

Chạy các lệnh sau trong thư mục này sau khi MCP server đã khởi động:

```powershell
.\.venv\Scripts\python.exe verify_setup.py
.\.venv\Scripts\python.exe check_weather.py
.\.venv\Scripts\python.exe test_chat.py
.\.venv\Scripts\adk.exe web
```

Cấu hình: `GOOGLE_API_KEY` cho Gemini, `MCP_SERVER_URL=http://localhost:8085/mcp` cho MCP. Agent dùng model `gemini-3.5-flash-lite`. Có thể nạp từ environment, `.env` tại đây hoặc `.env` gốc. Các file mẫu không chứa khóa thật.

Agent chỉ khởi tạo cấu hình khi import; khám phá tool mới mở kết nối MCP. Không tự chuyển sang agent không có tool khi lỗi cấu hình. Lỗi runtime được báo ở ADK; không dùng câu trả lời thiếu dữ liệu làm minh chứng thành công.

`test_chat.py` yêu cầu đúng tool call, tool response và câu trả lời cuối cho cả thời tiết Hà Nội và forecast Đà Nẵng. Kiểm tra nội dung dữ liệu thật bằng `check_weather.py` trước khi chạy.
