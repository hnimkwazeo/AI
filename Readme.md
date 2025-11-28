# AI Chatbot tích hợp Giọng nói

## Tổng quan dự án

Dự án này là một ứng dụng chatbot AI dựa trên web tích hợp Google Gemini AI với các khả năng giọng nói nâng cao. Nó cho phép người dùng tương tác với AI bằng cả văn bản và giọng nói (Speech-to-Text) và nghe phản hồi của AI (Text-to-Speech). Ứng dụng được xây dựng bằng FastAPI cho backend và JavaScript thuần cho frontend, được đóng gói với Docker để dễ dàng triển khai.

## Tính năng

- **Trò chuyện văn bản**: Giao diện trò chuyện tương tác với hỗ trợ markdown để định dạng văn bản phong phú.
- **Nhập liệu bằng giọng nói (Speech-to-Text)**: Ghi âm thời gian thực thông qua Web Audio API của trình duyệt, chuyển đổi thành văn bản bằng Google Speech Recognition. Hỗ trợ tiếng Việt và tiếng Anh.
- **Đầu ra giọng nói (Text-to-Speech)**: Chuyển đổi phản hồi của AI thành giọng nói tiếng Việt tự nhiên bằng Google Text-to-Speech (gTTS).
- **Giao diện hiện đại**: Thiết kế đáp ứng (responsive) với giao diện sạch sẽ, phản hồi trực quan cho trạng thái ghi âm và điều khiển phát lại âm thanh.
- **Hỗ trợ Docker**: Ứng dụng được đóng gói hoàn toàn bằng Docker và Docker Compose.

## Kiến trúc hệ thống

Ứng dụng tuân theo kiến trúc Client-Server tiêu chuẩn:

1.  **Frontend (Client)**:
    -   HTML5/CSS3 cho cấu trúc và kiểu dáng.
    -   JavaScript (ES6+) cho logic.
    -   Web Audio API để thu tín hiệu micro và xử lý dữ liệu âm thanh.
    -   Fetch API để giao tiếp bất đồng bộ với backend.

2.  **Backend (Server)**:
    -   **FastAPI**: Framework web hiệu năng cao để xử lý các yêu cầu HTTP.
    -   **Google Gemini API**: Mô hình AI tạo sinh để xử lý lời nhắc và tạo phản hồi.
    -   **SpeechRecognition**: Thư viện chuyển đổi tệp âm thanh WAV thành văn bản.
    -   **gTTS**: Thư viện chuyển đổi phản hồi văn bản thành âm thanh MP3.

## Công nghệ sử dụng

### Backend
-   **Python 3.11**
-   **FastAPI**: Web framework.
-   **Uvicorn**: ASGI server.
-   **Google Generative AI (Gemini 2.0)**: Nhà cung cấp LLM.
-   **SpeechRecognition**: Xử lý âm thanh.
-   **gTTS**: Công cụ chuyển văn bản thành giọng nói.
-   **Jinja2**: Template engine.

### Frontend
-   **HTML5 / CSS3**
-   **JavaScript (Vanilla)**
-   **Web Audio API**

### DevOps
-   **Docker**
-   **Docker Compose**

## Cấu trúc dự án

```text
chatbot/
├── main.py                 # Điểm vào ứng dụng chính và các API endpoint
├── requirements.txt        # Các phụ thuộc Python
├── Dockerfile              # Cấu hình Docker image
├── docker-compose.yml      # Cấu hình dịch vụ Docker
├── .env                    # Biến môi trường (API Keys)
├── .dockerignore           # Các tệp bị loại trừ khỏi bản build Docker
├── templates/
│   └── index.html          # Giao diện người dùng Frontend
└── README.md               # Tài liệu dự án
```

## Yêu cầu tiên quyết

-   Python 3.11 trở lên (để phát triển cục bộ)
-   Docker và Docker Compose (để triển khai container)
-   Google Gemini API Key

## Cài đặt và Thiết lập

### 1. Cấu hình môi trường

Tạo tệp `.env` trong thư mục gốc và thêm khóa API Google Gemini của bạn:

```env
GEMINI_API_KEY=your_api_key_here
```

### 2. Chạy với Docker (Khuyên dùng)

Xây dựng và khởi động container:

```bash
docker-compose up --build
```

Ứng dụng sẽ có sẵn tại `http://localhost:8000`.

Để dừng ứng dụng:

```bash
docker-compose down
```

### 3. Chạy cục bộ

1.  Tạo môi trường ảo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

2.  Cài đặt các phụ thuộc:
    ```bash
    pip install -r requirements.txt
    ```

    *Lưu ý: Bạn có thể cần cài đặt các phụ thuộc cấp hệ thống cho PyAudio (ví dụ: `portaudio19-dev` trên Linux) nếu gặp lỗi cài đặt.*

3.  Chạy máy chủ:
    ```bash
    python -m uvicorn main:app --reload
    ```

4.  Truy cập ứng dụng tại `http://localhost:8000`.

## Hướng dẫn sử dụng

### Trò chuyện văn bản
1.  Nhập tin nhắn của bạn vào trường nhập liệu ở cuối màn hình.
2.  Nhấn Enter hoặc nhấp vào nút "Gui".
3.  Phản hồi của AI sẽ xuất hiện trong cửa sổ trò chuyện.

### Nhập liệu bằng giọng nói
1.  Nhấp vào nút "MIC".
2.  Cấp quyền truy cập micro nếu trình duyệt yêu cầu.
3.  Nói câu hỏi của bạn. Nút sẽ thay đổi giao diện để báo hiệu đang ghi âm.
4.  Nhấp vào nút một lần nữa (có nhãn "STOP") để kết thúc ghi âm.
5.  Hệ thống sẽ xử lý âm thanh và điền văn bản đã chuyển đổi vào trường nhập liệu.
6.  Bạn có thể chỉnh sửa văn bản nếu cần trước khi gửi.

### Đầu ra giọng nói
1.  Sau khi nhận được phản hồi từ AI, nút "Nghe" sẽ xuất hiện bên dưới tin nhắn.
2.  Nhấp vào nút để nghe phản hồi được đọc to.
3.  Nút sẽ hiển thị "Dang phat..." trong khi âm thanh đang phát.

## Các API Endpoint

### `GET /`
Hiển thị giao diện trò chuyện chính.

### `POST /chat`
Xử lý các lời nhắc văn bản.
-   **Input**: Form data `prompt` (chuỗi).
-   **Output**: HTML template với lịch sử trò chuyện đã cập nhật.

### `POST /transcribe`
Chuyển đổi tệp âm thanh thành văn bản.
-   **Input**: Multipart form data `audio` (tệp WAV).
-   **Output**: JSON `{"text": "văn bản đã chuyển đổi"}`.

### `POST /text-to-speech`
Chuyển đổi văn bản thành âm thanh.
-   **Input**: JSON `{"text": "văn bản cần đọc"}`.
-   **Output**: JSON `{"audio": "base64_encoded_mp3"}`.

## Các vấn đề bảo mật

-   **API Keys**: Không bao giờ commit tệp `.env` vào version control. Đảm bảo `GEMINI_API_KEY` được giữ bí mật.
-   **Tệp tạm thời**: Ứng dụng tạo các tệp WAV và MP3 tạm thời để xử lý. Các tệp này sẽ tự động bị xóa sau khi sử dụng để tránh đầy bộ nhớ và rò rỉ dữ liệu.
-   **Xác thực đầu vào**: Xác thực cơ bản được thực hiện để đảm bảo lời nhắc không bị trống.

## Khắc phục sự cố

-   **Truy cập Micro**: Đảm bảo trình duyệt của bạn cho phép truy cập micro cho trang web. Điều này thường yêu cầu trang web phải được phục vụ qua HTTPS hoặc `localhost`.
-   **Lỗi định dạng âm thanh**: Frontend được cấu hình để ghi âm ở tần số 16kHz mono. Nếu bạn gặp lỗi định dạng, hãy đảm bảo trình duyệt của bạn hỗ trợ các ràng buộc Web Audio API được sử dụng trong `index.html`.
-   **Vấn đề phụ thuộc**: Nếu `pyaudio` không cài đặt được cục bộ, hãy đảm bảo bạn đã cài đặt các công cụ build C++ và header phát triển PortAudio cần thiết trên hệ thống của mình.

## Giấy phép

Dự án này là mã nguồn mở và có sẵn để sửa đổi và phân phối.

