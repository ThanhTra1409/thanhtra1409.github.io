++
title = "WebSocket server với Socket.IO"
date = "2025-12-11"
tags = ["JavaScript","Socket.IO","Realtime"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&auto=format&fit=crop"
++

WebSocket là công nghệ tuyệt vời cho giao tiếp realtime, nhưng việc implement từ đầu có thể phức tạp. Socket.IO là thư viện giúp đơn giản hóa quá trình này, cung cấp fallback mechanisms, automatic reconnection, và nhiều tính năng tiện lợi khác.

Socket.IO không chỉ là WebSocket wrapper - nó cung cấp thêm nhiều feature như rooms, namespaces, broadcasting, và tương thích với các trình duyệt cũ. Bài viết này sẽ hướng dẫn cách xây dựng ứng dụng realtime với Socket.IO.

![Socket.IO Realtime](https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&auto=format&fit=crop)
*Socket.IO cho ứng dụng realtime*

### 1. Cài đặt và Setup cơ bản

```bash
npm install socket.io express
```

#### Server cơ bản

```javascript
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Serve static files
app.use(express.static('public'));

// Socket.IO connection handler
io.on('connection', (socket) => {
  console.log('Client kết nối:', socket.id);
  
  // Nhận tin nhắn từ client
  socket.on('message', (data) => {
    console.log('Nhận message:', data);
    
    // Gửi lại cho client
    socket.emit('message', { text: 'Server nhận: ' + data.text });
  });
  
  // Xử lý disconnect
  socket.on('disconnect', () => {
    console.log('Client ngắt kết nối:', socket.id);
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server chạy trên http://localhost:${PORT}`);
});
```

#### Client HTML

```html
<!DOCTYPE html>
<html>
<head>
  <title>Socket.IO Chat</title>
  <script src="/socket.io/socket.io.js"></script>
</head>
<body>
  <div id="messages"></div>
  <input id="messageInput" type="text" placeholder="Nhập tin nhắn...">
  <button onclick="sendMessage()">Gửi</button>
  
  <script>
    // Kết nối tới server
    const socket = io();
    
    // Xử lý khi kết nối
    socket.on('connect', () => {
      console.log('Đã kết nối:', socket.id);
    });
    
    // Nhận message từ server
    socket.on('message', (data) => {
      const div = document.createElement('div');
      div.textContent = data.text;
      document.getElementById('messages').appendChild(div);
    });
    
    // Gửi message
    function sendMessage() {
      const input = document.getElementById('messageInput');
      socket.emit('message', { text: input.value });
      input.value = '';
    }
    
    // Xử lý disconnect
    socket.on('disconnect', () => {
      console.log('Ngắt kết nối');
    });
  </script>
</body>
</html>
```

### 2. Ứng dụng Chat với Rooms

```javascript
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

app.use(express.static('public'));

// Lưu thông tin users
const users = new Map();

io.on('connection', (socket) => {
  console.log('New connection:', socket.id);
  
  // Join room
  socket.on('join-room', (data) => {
    const { username, room } = data;
    
    socket.join(room);
    users.set(socket.id, { username, room });
    
    // Thông báo cho user
    socket.emit('message', {
      username: 'System',
      text: `Chào mừng ${username} đến room ${room}!`,
      timestamp: new Date()
    });
    
    // Thông báo cho room (trừ chính user)
    socket.to(room).emit('message', {
      username: 'System',
      text: `${username} đã tham gia room`,
      timestamp: new Date()
    });
    
    // Gửi danh sách users trong room
    updateRoomUsers(room);
  });
  
  // Nhận chat message
  socket.on('chat-message', (data) => {
    const user = users.get(socket.id);
    if (!user) return;
    
    const messageData = {
      username: user.username,
      text: data.text,
      timestamp: new Date()
    };
    
    // Broadcast tới tất cả trong room
    io.to(user.room).emit('message', messageData);
  });
  
  // Typing indicator
  socket.on('typing', (isTyping) => {
    const user = users.get(socket.id);
    if (!user) return;
    
    socket.to(user.room).emit('user-typing', {
      username: user.username,
      isTyping: isTyping
    });
  });
  
  // Disconnect
  socket.on('disconnect', () => {
    const user = users.get(socket.id);
    if (user) {
      io.to(user.room).emit('message', {
        username: 'System',
        text: `${user.username} đã rời room`,
        timestamp: new Date()
      });
      
      users.delete(socket.id);
      updateRoomUsers(user.room);
    }
  });
});

function updateRoomUsers(room) {
  const roomUsers = Array.from(users.values())
    .filter(user => user.room === room)
    .map(user => user.username);
  
  io.to(room).emit('room-users', roomUsers);
}

server.listen(3000, () => {
  console.log('Chat server running on port 3000');
});
```

### 3. Broadcasting và Namespaces

```javascript
// Broadcasting
io.on('connection', (socket) => {
  // Gửi cho chính socket
  socket.emit('message', 'Chỉ gửi cho bạn');
  
  // Gửi cho tất cả trừ chính socket
  socket.broadcast.emit('message', 'Gửi cho tất cả trừ sender');
  
  // Gửi cho tất cả
  io.emit('message', 'Gửi cho tất cả');
  
  // Gửi cho room
  io.to('room1').emit('message', 'Gửi cho room1');
  
  // Gửi cho nhiều rooms
  io.to('room1').to('room2').emit('message', 'Gửi cho 2 rooms');
  
  // Gửi cho tất cả trong room trừ sender
  socket.to('room1').emit('message', 'Gửi cho room1 trừ sender');
});

// Namespaces
const adminNamespace = io.of('/admin');
const chatNamespace = io.of('/chat');

adminNamespace.on('connection', (socket) => {
  console.log('Admin connected');
  socket.emit('admin-message', 'Welcome admin');
});

chatNamespace.on('connection', (socket) => {
  console.log('Chat user connected');
  socket.emit('chat-message', 'Welcome to chat');
});
```

### 4. Authentication và Middleware

```javascript
const jwt = require('jsonwebtoken');

// Middleware cho authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  
  if (!token) {
    return next(new Error('Authentication error'));
  }
  
  try {
    const decoded = jwt.verify(token, 'secret-key');
    socket.userId = decoded.userId;
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

io.on('connection', (socket) => {
  console.log('Authenticated user:', socket.userId);
});

// Client
const socket = io({
  auth: {
    token: 'your-jwt-token'
  }
});
```

### 5. Acknowledgments (Callbacks)

```javascript
// Server
io.on('connection', (socket) => {
  socket.on('send-message', (data, callback) => {
    console.log('Received:', data);
    
    // Xử lý message...
    
    // Gọi callback để xác nhận
    callback({
      status: 'ok',
      messageId: generateId()
    });
  });
});

// Client
socket.emit('send-message', { text: 'Hello' }, (response) => {
  console.log('Server response:', response);
});
```

### 6. Error Handling và Reconnection

```javascript
// Client
const socket = io({
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 5
});

socket.on('connect', () => {
  console.log('Connected');
});

socket.on('connect_error', (error) => {
  console.error('Connection error:', error);
});

socket.on('disconnect', (reason) => {
  console.log('Disconnected:', reason);
  
  if (reason === 'io server disconnect') {
    // Server chủ động disconnect, cần reconnect manual
    socket.connect();
  }
});

socket.on('reconnect', (attemptNumber) => {
  console.log('Reconnected after', attemptNumber, 'attempts');
});

socket.on('reconnect_attempt', (attemptNumber) => {
  console.log('Reconnection attempt', attemptNumber);
});

socket.on('reconnect_failed', () => {
  console.log('Reconnection failed');
});
```

### 7. Performance và Scaling

#### Sử dụng Redis Adapter cho multiple servers

```javascript
const redis = require('socket.io-redis');

io.adapter(redis({ 
  host: 'localhost', 
  port: 6379 
}));

// Giờ có thể scale horizontally với nhiều server instances
```

#### Compression

```javascript
const io = socketIO(server, {
  perMessageDeflate: {
    threshold: 1024 // Compress nếu message > 1KB
  }
});
```

Socket.IO là lựa chọn tuyệt vời để xây dựng ứng dụng realtime với JavaScript. Với các tính năng như rooms, namespaces, automatic reconnection và fallback mechanisms, Socket.IO giúp developer tập trung vào business logic thay vì lo lắng về các vấn đề low-level.

Tuy nhiên, cần lưu ý rằng Socket.IO không phải là WebSocket thuần túy - nó có overhead lớn hơn. Với ứng dụng đơn giản chỉ cần WebSocket cơ bản, có thể cân nhắc sử dụng ws library hoặc WebSocket native.

---

### Tài liệu tham khảo

- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [Socket.IO Server API](https://socket.io/docs/v4/server-api/)
- [Socket.IO Client API](https://socket.io/docs/v4/client-api/)
- [Building Realtime Apps with Socket.IO](https://socket.io/get-started/chat)
