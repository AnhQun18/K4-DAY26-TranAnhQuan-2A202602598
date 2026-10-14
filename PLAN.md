# Tiến độ bài lab — Function Calling, MCP và Weather Agent

Cập nhật ngày 14/10/2026, Windows / PowerShell. Phạm vi bàn giao: bài 01–03 và lab 04 chạy local. Docker/Cloud Run và các mở rộng production không thực hiện theo yêu cầu.

## Kết quả hoàn thành

- [x] Dùng môi trường gốc cho demo MCP v2; server/client lab dùng Python 3.12 và MCP v1 theo lockfile.
- [x] Sửa môi trường server bị trộn interpreter 3.14 với wheel cp312; kiểm tra import và `pip check` đạt.
- [x] Cấu hình Gemini và WeatherAPI qua environment hoặc `.env`; các `.env.example` chỉ giữ placeholder.
- [x] MCP cơ bản: initialize, khám phá tool và gọi dữ liệu mock ba thành phố.
- [x] Function Calling: Gemini yêu cầu tool, app thực thi, model tổng hợp; hỗ trợ tên thành phố không dấu; kiểm tra tên/args, giới hạn 8 vòng và phản hồi rỗng.
- [x] Registry: JSON UTF-8, đường dẫn độc lập cwd, chọn semantic version và ưu tiên tool chưa deprecated.
- [x] Versioning: v1 còn hoạt động; v2 chuyển đúng nhiệt độ hiện tại và forecast sang Fahrenheit, từ chối units sai.
- [x] Auth HTTP: token hợp lệ gọi được tool; thiếu/sai token bị từ chối HTTP 401.
- [x] Server lab mặc định HTTP trên cổng 8085; stdio được chọn bằng `--stdio`, không ghi log ứng dụng ra stdout.
- [x] Forecast giới hạn days về 1–3; city rỗng được từ chối trước khi gọi API.
- [x] Xác minh MCP thật: initialize, đủ ba tool, gọi health_check và ADK khám phá tool; đóng session/toolset sau khi dùng.
- [x] Kiểm chứng WeatherAPI thật: Hanoi hiện tại, Danang forecast 1 và 3 ngày qua MCP.
- [x] Kiểm chứng hai câu hỏi ADK: đúng tool call, tool response và câu trả lời cuối.
- [x] Endpoint sai và server dừng đều làm verify exit 1; cấu hình đúng exit 0.
- [x] Có 9 ảnh minh chứng bài 01–04; bổ sung log chạy cuối và log lỗi trong `evidence/`.
- [x] 10 kiểm tra hồi quy đạt, bao gồm đơn vị forecast, encoding, tên thành phố, vòng gọi tool, miền days, key thiếu/bị từ chối, lỗi mạng và city rỗng.
- [x] README đã cập nhật PowerShell, model thực dùng, thứ tự khởi động, môi trường riêng, cổng và dữ liệu mock/thật.
- [x] Kiểm tra minh chứng dạng văn bản không chứa khóa cấu hình; chặn httpx INFO log chứa query key; runtime log được bỏ qua trong Git.

## Cách chạy lại

Theo [README gốc](README.md), [bài 03](03-production/README.md) và [lab 04](04-lab/README.md).
Dùng `.venv/Scripts/python.exe` trong môi trường tương ứng; không bắt buộc activate.

Thứ tự: MCP cơ bản → Function Calling → registry/versioning → auth → dừng auth → MCP server lab → verify → check_weather → test_chat → ADK Web.

Kiểm tra hồi quy từ gốc repo:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_demo.py -v
.\04-lab\mcp-server\.venv\Scripts\python.exe -m unittest discover -s tests -p test_weather.py -v
```

## Giới hạn diễn giải kết quả

Health check chỉ xác nhận server hoạt động; không chứng minh khóa WeatherAPI hợp lệ. Kiểm chứng dữ liệu thật nằm ở `weather-live.log` và luồng ADK.

Thiếu khóa, HTTP 400/403 và lỗi mạng được kiểm tra hồi quy bằng phản hồi giả lập; không thay đổi khóa thật để tạo lỗi. Endpoint sai/server dừng và auth HTTP 401 được kiểm tra bằng dịch vụ local thật.

WeatherAPI có thể khớp gần đúng tên địa điểm lạ; không dùng một chuỗi ngẫu nhiên để khẳng định provider luôn từ chối thành phố sai. City rỗng được từ chối tại server; các lỗi HTTP từ provider được xử lý rõ.

Một số SDK in cảnh báo experimental hoặc ADC/mTLS, nhưng đường API-key local vẫn chạy đạt. Không cần thiết lập Cloud ADC cho phạm vi này. Gemini có thể gặp ngắt kết nối mạng tạm thời; log ADK bàn giao là lần chạy hoàn tất.

## Bàn giao

Xem [bảng kết quả](evidence/RESULTS.md) để đối chiếu log và ảnh. Các dịch vụ local được khởi động phục vụ kiểm tra; khi chạy lại ở phiên mới, khởi động theo README.
