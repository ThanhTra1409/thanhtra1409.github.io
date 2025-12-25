++
title = "Fetch API và WebSocket trên trình duyệt"
date = "2025-12-07"
tags = ["JavaScript","Browser","WebSocket"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
++

Trong phát triển web hiện đại, việc giao tiếp giữa client và server là thiết yếu. JavaScript cung cấp hai công cụ chính: **Fetch API** cho các yêu cầu HTTP thông thường và **WebSocket** cho giao tiếp hai chiều realtime.

Bài viết này sẽ giới thiệu cả hai công nghệ, phân biệt khi nào nên dùng cái nào, và cách sử dụng chúng trong ứng dụng thực tế.

![Web Communication](https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&auto=format&fit=crop)
*Fetch API và WebSocket trong lập trình web*

### 1. Fetch API - HTTP Request Hiện Đại

Fetch API thay thế XMLHttpRequest cũ, cung cấp cú pháp đơn giản hơn và sử dụng Promise.

#### GET Request cơ bản

```javascript
// GET request đơn giản
fetch('https://jsonplaceholder.typicode.com/posts/1')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Lỗi:', error));

// Sử dụng async/await
async function fetchPost() {
  try {
    const response = await fetch(
      'https://jsonplaceholder.typicode.com/posts/1'
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Lỗi:', error);
  }
}

fetchPost();
```

#### POST Request với JSON

```javascript
async function createPost() {
  try {
    const response = await fetch(
      'https://jsonplaceholder.typicode.com/posts',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'Bài viết mới',
          body: 'Nội dung bài viết',
          userId: 1
        })
      }
    );
    
    const data = await response.json();
    console.log('Tạo thành công:', data);
  } catch (error) {
    console.error('Lỗi:', error);
  }
}
```

#### Xử lý Headers và Authentication

```javascript
async function fetchWithAuth() {
  const response = await fetch('https://api.example.com/data', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    }
  });
  
  // Đọc headers từ response
  console.log('Content-Type:', response.headers.get('Content-Type'));
  
  return await response.json();
}
```

#### Upload File

```javascript
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('description', 'Mô tả file');
  
  try {
    const response = await fetch('https://api.example.com/upload', {
      method: 'POST',
      body: formData
      // Không set Content-Type, browser tự động set
    });
    
    const result = await response.json();
    console.log('Upload thành công:', result);
  } catch (error) {
    console.error('Lỗi upload:', error);
  }
}

// Sử dụng
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    uploadFile(file);
  }
});
```

### 2. WebSocket - Giao tiếp Realtime

WebSocket cung cấp kênh giao tiếp hai chiều, full-duplex giữa client và server.

#### Kết nối WebSocket cơ bản

```javascript
// Tạo kết nối WebSocket
const ws = new WebSocket('ws://localhost:8080');

// Sự kiện khi kết nối thành công
ws.onopen = (event) => {
  console.log('Kết nối WebSocket thành công');
  ws.send('Xin chào server!');
};

// Sự kiện khi nhận tin nhắn
ws.onmessage = (event) => {
  console.log('Nhận tin nhắn:', event.data);
};

// Sự kiện khi có lỗi
ws.onerror = (error) => {
  console.error('Lỗi WebSocket:', error);
};

// Sự kiện khi ngắt kết nối
ws.onclose = (event) => {
  console.log('Kết nối đóng. Code:', event.code);
};

// Gửi tin nhắn
function sendMessage(message) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(message);
  } else {
    console.error('WebSocket chưa sẵn sàng');
  }
}

// Đóng kết nối
function closeConnection() {
  ws.close();
}
```

#### Ứng dụng Chat đơn giản

```javascript
class ChatClient {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    this.ws.onopen = () => {
      console.log('Kết nối chat thành công');
      this.updateStatus('online');
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.displayMessage(message);
    };
    
    this.ws.onerror = (error) => {
      console.error('Lỗi:', error);
      this.updateStatus('error');
    };
    
    this.ws.onclose = () => {
      console.log('Đã ngắt kết nối');
      this.updateStatus('offline');
      // Tự động kết nối lại sau 5 giây
      setTimeout(() => this.reconnect(), 5000);
    };
  }
  
  sendMessage(text, username) {
    const message = {
      type: 'message',
      username: username,
      text: text,
      timestamp: new Date().toISOString()
    };
    
    this.ws.send(JSON.stringify(message));
  }
  
  displayMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.innerHTML = `
      <strong>${message.username}</strong>: ${message.text}
      <span class="time">${new Date(message.timestamp).toLocaleTimeString()}</span>
    `;
    
    document.getElementById('messages').appendChild(messageDiv);
  }
  
  updateStatus(status) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = status;
    statusEl.className = `status-${status}`;
  }
  
  reconnect() {
    console.log('Đang kết nối lại...');
    this.ws = new WebSocket(this.ws.url);
    this.setupEventHandlers();
  }
}

// Sử dụng
const chat = new ChatClient('ws://localhost:8080');

document.getElementById('sendBtn').addEventListener('click', () => {
  const input = document.getElementById('messageInput');
  const username = document.getElementById('username').value;
  
  if (input.value.trim()) {
    chat.sendMessage(input.value, username);
    input.value = '';
  }
});
```

#### Gửi/Nhận Binary Data

```javascript
// Gửi binary data
const buffer = new ArrayBuffer(8);
const view = new DataView(buffer);
view.setInt32(0, 42);
ws.send(buffer);

// Nhận binary data
ws.binaryType = 'arraybuffer';
ws.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    const view = new DataView(event.data);
    console.log('Nhận số:', view.getInt32(0));
  }
};
```

### 3. So sánh Fetch và WebSocket

| Tính năng | Fetch API | WebSocket |
|---------|-----------|----------|
| Giao thức | HTTP/HTTPS | WS/WSS |
| Kết nối | Request-Response | Full-duplex |
| Realtime | Không | Có |
| Overhead | Cao (mỗi request) | Thấp (một kết nối) |
| Sử dụng cho | REST API, CRUD | Chat, Notification, Game |

### 4. Khi nào dùng gì?

**Dùng Fetch API khi**:
- Cần gọi/nhận dữ liệu theo yêu cầu
- Tương tác với REST API
- Không cần realtime updates

**Dùng WebSocket khi**:
- Cần giao tiếp hai chiều realtime
- Ứng dụng chat, live notifications
- Game multiplayer, live dashboard
- Cần latency thấp

Fetch API và WebSocket là hai công cụ quan trọng trong web development. Fetch API phù hợp cho các tác vụ HTTP thông thường, trong khi WebSocket thiết yếu cho ứng dụng realtime. Hiểu rõ ưu nhược điểm của mỗi công nghệ giúp bạn lựa chọn đúng trong từng tình huống.

Trong bài tiếp theo, chúng ta sẽ tìm hiểu cách xây dựng TCP server với Node.js, nền tảng cho các ứng dụng realtime phia server.

---

### Tài liệu tham khảo

- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [JavaScript.info - Fetch](https://javascript.info/fetch)
- [JavaScript.info - WebSocket](https://javascript.info/websocket)
