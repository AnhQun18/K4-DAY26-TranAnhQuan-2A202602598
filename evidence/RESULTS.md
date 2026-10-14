# Kết quả kiểm chứng — 14/10/2026

Phạm vi: local; không thực hiện Docker/Cloud Run.

| Kiểm tra | Kết quả | Minh chứng |
|---|---|---|
| MCP cơ bản stdio | Đạt, đủ ba thành phố mock | [mcp-basic.log](mcp-basic.log) |
| Function Calling Gemini | Đạt, tool thực thi và câu trả lời; Hanoi 29°C, Danang 30°C mock | [function-calling.log](function-calling.log) |
| Registry | Đạt, chọn get_weather_v2 | [registry.log](registry.log) |
| Versioning | Đạt v1/v2 và metadata | [versioning.log](versioning.log) |
| Auth hợp lệ | Đạt, gọi get_weather | [auth-valid.log](auth-valid.log) |
| Auth thiếu/sai | Đạt, đều HTTP 401 | [auth-rejected.log](auth-rejected.log) |
| MCP + ADK discovery | Đạt initialize, đủ 3 tool, health_check, đóng session | [verify-success.log](verify-success.log) |
| Endpoint sai | Từ chối đúng, exit 1 | [verify-wrong-path.log](verify-wrong-path.log) |
| MCP server dừng | Từ chối đúng, exit 1 | [verify-server-off.log](verify-server-off.log) |
| WeatherAPI qua MCP | Đạt Hanoi hiện tại, Danang 1/3 ngày và city rỗng bị từ chối | [weather-live.log](weather-live.log) |
| ADK + Gemini | Đạt cả current và forecast, có tool call/response và câu trả lời cuối | [adk-chat.log](adk-chat.log) |
| Hồi quy demo | 5/5 đạt | [tests-demo.log](tests-demo.log) |
| Hồi quy lab | 5/5 đạt | [tests-weather.log](tests-weather.log) |
| Lab stdio | Đạt initialize/list_tools/health_check, không bị log stdout phá giao thức | [lab-stdio.log](lab-stdio.log) |
| ADK Web | Khởi động trên cổng 8000 | [adk-web.log](adk-web.log) |

Ảnh giao diện và demo đã có trong [screenshots](../screenshots): Function Calling, MCP client, auth thành công/thất bại, registry, versioning, ADK current/forecast và verify setup (9 ảnh). Ảnh được giữ từ phiên chạy trước; các log ở đây kiểm chứng phiên mã nguồn bàn giao.

`environment.log` ghi interpreter, phiên bản package và kiểm tra dependency của ba môi trường. Các phép thử key sai/thiếu và lỗi mạng trong hồi quy dùng mock; phép thử WeatherAPI thành công dùng dịch vụ thật. Thời tiết thay đổi theo thời điểm chạy.

Log runtime mới được lưu trong `.runtime/` và không đưa vào Git. Không mở hoặc xuất nội dung `.env` khi bàn giao.
