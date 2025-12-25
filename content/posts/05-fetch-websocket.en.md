++
title = "Fetch API and WebSocket in the Browser"
date = "2025-12-07"
tags = ["JavaScript","Browser","WebSocket"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
++

In modern web development, communication between client and server is essential. JavaScript provides two main tools: **Fetch API** for regular HTTP requests and **WebSocket** for bidirectional realtime communication.

This article will introduce both technologies, distinguish when to use which, and how to use them in real applications.

![Web Communication](https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&auto=format&fit=crop)
*Fetch API and WebSocket in web programming*

### 1. Fetch API - Modern HTTP Requests

Fetch API replaces the old XMLHttpRequest, providing simpler syntax and using Promises.

#### Basic GET Request

```javascript
// Simple GET request
fetch('https://jsonplaceholder.typicode.com/posts/1')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Using async/await
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
    console.error('Error:', error);
  }
}

fetchPost();
```

#### POST Request with JSON

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
          title: 'New Post',
          body: 'Post content',
          userId: 1
        })
      }
    );
    
    const data = await response.json();
    console.log('Created successfully:', data);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

#### Handling Headers and Authentication

```javascript
async function fetchWithAuth() {
  const response = await fetch('https://api.example.com/data', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    }
  });
  
  // Read headers from response
  console.log('Content-Type:', response.headers.get('Content-Type'));
  
  return await response.json();
}
```

#### File Upload

```javascript
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('description', 'File description');
  
  try {
    const response = await fetch('https://api.example.com/upload', {
      method: 'POST',
      body: formData
      // Don't set Content-Type, browser sets it automatically
    });
    
    const result = await response.json();
    console.log('Upload successful:', result);
  } catch (error) {
    console.error('Upload error:', error);
  }
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    uploadFile(file);
  }
});
```

### 2. WebSocket - Realtime Communication

WebSocket provides a bidirectional, full-duplex communication channel between client and server.

#### Basic WebSocket Connection

```javascript
// Create WebSocket connection
const ws = new WebSocket('ws://localhost:8080');

// Event when connection successful
ws.onopen = (event) => {
  console.log('WebSocket connection successful');
  ws.send('Hello server!');
};

// Event when receiving message
ws.onmessage = (event) => {
  console.log('Received message:', event.data);
};

// Event when error occurs
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Event when disconnected
ws.onclose = (event) => {
  console.log('Connection closed. Code:', event.code);
};

// Send message
function sendMessage(message) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(message);
  } else {
    console.error('WebSocket not ready');
  }
}

// Close connection
function closeConnection() {
  ws.close();
}
```

#### Simple Chat Application

```javascript
class ChatClient {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    this.ws.onopen = () => {
      console.log('Chat connection successful');
      this.updateStatus('online');
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.displayMessage(message);
    };
    
    this.ws.onerror = (error) => {
      console.error('Error:', error);
      this.updateStatus('error');
    };
    
    this.ws.onclose = () => {
      console.log('Disconnected');
      this.updateStatus('offline');
      // Auto reconnect after 5 seconds
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
    console.log('Reconnecting...');
    this.ws = new WebSocket(this.ws.url);
    this.setupEventHandlers();
  }
}

// Usage
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

#### Sending/Receiving Binary Data

```javascript
// Send binary data
const buffer = new ArrayBuffer(8);
const view = new DataView(buffer);
view.setInt32(0, 42);
ws.send(buffer);

// Receive binary data
ws.binaryType = 'arraybuffer';
ws.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    const view = new DataView(event.data);
    console.log('Received number:', view.getInt32(0));
  }
};
```

### 3. Comparing Fetch and WebSocket

| Feature | Fetch API | WebSocket |
|---------|-----------|----------|
| Protocol | HTTP/HTTPS | WS/WSS |
| Connection | Request-Response | Full-duplex |
| Realtime | No | Yes |
| Overhead | High (each request) | Low (one connection) |
| Used for | REST API, CRUD | Chat, Notification, Game |

### 4. When to Use What?

**Use Fetch API when**:
- Need to request/receive data on demand
- Interacting with REST APIs
- Don't need realtime updates

**Use WebSocket when**:
- Need bidirectional realtime communication
- Chat applications, live notifications
- Multiplayer games, live dashboards
- Need low latency

Fetch API and WebSocket are two important tools in web development. Fetch API is suitable for regular HTTP tasks, while WebSocket is essential for realtime applications. Understanding the pros and cons of each technology helps you choose correctly in each situation.

In the next article, we'll explore how to build a TCP server with Node.js, the foundation for server-side realtime applications.

---

### References

- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [JavaScript.info - Fetch](https://javascript.info/fetch)
- [JavaScript.info - WebSocket](https://javascript.info/websocket)
