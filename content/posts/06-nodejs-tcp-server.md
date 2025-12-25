++
title = "Node.js: TCP server với module `net`"
date = "2025-12-09"
tags = ["JavaScript","Node.js","TCP"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&auto=format&fit=crop"
++

Node.js với kiến trúc event-driven và non-blocking I/O là nền tảng tuyệt vời để xây dựng server mạng hiệu năng cao. Module `net` được tích hợp sẵn trong Node.js, cung cấp API để tạo TCP server và client một cách đơn giản.

Khác với mô hình multithreading trong Java, Node.js sử dụng single-threaded event loop để xử lý hàng nghìn kết nối đồng thời, giúp tiết kiệm tài nguyên và dễ dàng scale.

![Node.js TCP Server](https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=1200&auto=format&fit=crop)
*Node.js TCP Server với Event-Driven Architecture*

### 1. Tạo TCP Server cơ bản

```javascript
const net = require('net');

// Tạo TCP server
const server = net.createServer((socket) => {
  console.log('Client kết nối:', socket.remoteAddress, socket.remotePort);
  
  // Gửi welcome message
  socket.write('Chào mừng đến TCP Server!\n');
  
  // Xử lý dữ liệu từ client
  socket.on('data', (data) => {
    console.log('Nhận từ client:', data.toString());
    
    // Echo lại cho client
    socket.write(`Echo: ${data}`);
  });
  
  // Xử lý khi client ngắt kết nối
  socket.on('end', () => {
    console.log('Client ngắt kết nối');
  });
  
  // Xử lý lỗi
  socket.on('error', (err) => {
    console.error('Lỗi socket:', err.message);
  });
});

// Lắng nghe trên port 8080
server.listen(8080, () => {
  console.log('TCP Server đang chạy trên port 8080');
});

// Xử lý lỗi server
server.on('error', (err) => {
  console.error('Lỗi server:', err.message);
});
```

### 2. TCP Client

```javascript
const net = require('net');

// Tạo TCP client
const client = net.createConnection({ port: 8080, host: 'localhost' }, () => {
  console.log('Đã kết nối tới server');
  client.write('Xin chào server!');
});

// Nhận dữ liệu từ server
client.on('data', (data) => {
  console.log('Nhận từ server:', data.toString());
  // client.end(); // Đóng kết nối sau khi nhận
});

// Xử lý khi ngắt kết nối
client.on('end', () => {
  console.log('Đã ngắt kết nối');
});

// Xử lý lỗi
client.on('error', (err) => {
  console.error('Lỗi:', err.message);
});
```

### 3. Echo Server với quản lý nhiều client

```javascript
const net = require('net');

class EchoServer {
  constructor(port) {
    this.port = port;
    this.clients = new Set();
    this.server = null;
  }
  
  start() {
    this.server = net.createServer((socket) => {
      this.handleConnection(socket);
    });
    
    this.server.listen(this.port, () => {
      console.log(`Echo Server chạy trên port ${this.port}`);
    });
    
    this.server.on('error', (err) => {
      console.error('Server error:', err);
    });
  }
  
  handleConnection(socket) {
    const clientId = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`[${clientId}] Kết nối mới`);
    
    // Thêm client vào danh sách
    this.clients.add(socket);
    
    // Gửi welcome message
    socket.write(`Chào mừng! Hiện có ${this.clients.size} clients online\n`);
    
    // Xử lý dữ liệu
    socket.on('data', (data) => {
      const message = data.toString().trim();
      console.log(`[${clientId}] ${message}`);
      
      // Echo với timestamp
      const response = `[${new Date().toISOString()}] Echo: ${message}\n`;
      socket.write(response);
    });
    
    // Xử lý ngắt kết nối
    socket.on('end', () => {
      console.log(`[${clientId}] Ngắt kết nối`);
      this.clients.delete(socket);
    });
    
    // Xử lý lỗi
    socket.on('error', (err) => {
      console.error(`[${clientId}] Lỗi:`, err.message);
      this.clients.delete(socket);
    });
  }
  
  broadcast(message) {
    const data = `[Broadcast] ${message}\n`;
    for (const client of this.clients) {
      client.write(data);
    }
  }
  
  stop() {
    // Đóng tất cả kết nối
    for (const client of this.clients) {
      client.end();
    }
    
    // Đóng server
    this.server.close(() => {
      console.log('Server đã đóng');
    });
  }
}

// Sử dụng
const server = new EchoServer(8080);
server.start();

// Broadcast message mỗi 30 giây
setInterval(() => {
  server.broadcast(`Server uptime: ${process.uptime()}s`);
}, 30000);
```

### 4. Chat Server

```javascript
const net = require('net');

class ChatServer {
  constructor(port) {
    this.port = port;
    this.clients = new Map(); // Map<socket, username>
    this.server = null;
  }
  
  start() {
    this.server = net.createServer((socket) => {
      this.handleClient(socket);
    });
    
    this.server.listen(this.port, () => {
      console.log(`Chat Server running on port ${this.port}`);
    });
  }
  
  handleClient(socket) {
    // Yêu cầu username
    socket.write('Nhập username của bạn: ');
    
    let username = null;
    
    socket.on('data', (data) => {
      const message = data.toString().trim();
      
      // Nếu chưa có username, set username
      if (!username) {
        username = message;
        this.clients.set(socket, username);
        
        socket.write(`Chào mừng ${username}!\n`);
        this.broadcast(`${username} đã tham gia chat\n`, socket);
        
        console.log(`${username} đã tham gia`);
        return;
      }
      
      // Xử lý commands
      if (message.startsWith('/')) {
        this.handleCommand(socket, message);
        return;
      }
      
      // Broadcast tin nhắn
      const chatMessage = `[${username}]: ${message}\n`;
      console.log(chatMessage.trim());
      this.broadcast(chatMessage);
    });
    
    socket.on('end', () => {
      if (username) {
        console.log(`${username} đã rời đi`);
        this.broadcast(`${username} đã rời chat\n`, socket);
        this.clients.delete(socket);
      }
    });
    
    socket.on('error', (err) => {
      console.error('Socket error:', err.message);
      this.clients.delete(socket);
    });
  }
  
  handleCommand(socket, command) {
    const username = this.clients.get(socket);
    
    if (command === '/users') {
      const userList = Array.from(this.clients.values()).join(', ');
      socket.write(`Online users: ${userList}\n`);
    } else if (command === '/help') {
      socket.write('Commands:\n');
      socket.write('/users - Xem danh sách users\n');
      socket.write('/help - Hiển thị trợ giúp\n');
      socket.write('/quit - Thoát chat\n');
    } else if (command === '/quit') {
      socket.end();
    } else {
      socket.write('Unknown command. Type /help for help\n');
    }
  }
  
  broadcast(message, excludeSocket = null) {
    for (const [socket, username] of this.clients) {
      if (socket !== excludeSocket) {
        socket.write(message);
      }
    }
  }
}

// Khởi động server
const chatServer = new ChatServer(8080);
chatServer.start();
```

### 5. Xử lý Buffer và Encoding

```javascript
const net = require('net');

const server = net.createServer((socket) => {
  // Set encoding để tự động chuyển buffer sang string
  socket.setEncoding('utf8');
  
  socket.on('data', (data) => {
    // data đã là string, không cần toString()
    console.log('Received:', data);
  });
  
  // Hoặc làm việc trực tiếp với Buffer
  socket.on('data', (buffer) => {
    // buffer là Buffer object
    console.log('Buffer length:', buffer.length);
    console.log('Hex:', buffer.toString('hex'));
    console.log('UTF-8:', buffer.toString('utf8'));
    console.log('Base64:', buffer.toString('base64'));
  });
});
```

### 6. Keep-alive và Timeout

```javascript
const server = net.createServer((socket) => {
  // Set timeout 30 giây
  socket.setTimeout(30000);
  
  // Xử lý timeout
  socket.on('timeout', () => {
    console.log('Socket timeout');
    socket.end('Timeout - closing connection\n');
  });
  
  // Enable keep-alive
  socket.setKeepAlive(true, 60000); // 60 seconds
  
  socket.on('data', (data) => {
    // Reset timeout khi có data
    socket.setTimeout(30000);
    // Xử lý data...
  });
});
```

### 7. So sánh với Java Thread-based Model

**Node.js (Event-driven)**:
- Single-threaded event loop
- Non-blocking I/O
- Xử lý nhiều kết nối với ít tài nguyên
- Phù hợp với I/O-intensive applications

**Java (Thread-based)**:
- Mỗi connection = một thread
- Blocking I/O (trừ khi dùng NIO)
- Tốn nhiều tài nguyên với nhiều kết nối
- Phù hợp với CPU-intensive applications

Module `net` của Node.js cung cấp API đơn giản nhưng mạnh mẽ để xây dựng TCP server. Với event-driven architecture, Node.js có thể xử lý hàng nghìn kết nối đồng thời một cách hiệu quả, rất phù hợp cho các ứng dụng realtime như chat, game server, hay IoT applications.

Trong bài viết tiếp theo, chúng ta sẽ tìm hiểu về Socket.IO - một thư viện xây dựng trên WebSocket, giúp việc phát triển ứng dụng realtime trở nên dễ dàng hơn nhiều.

---

### Tài liệu tham khảo

- [Node.js net Module Documentation](https://nodejs.org/api/net.html)
- [Node.js Stream API](https://nodejs.org/api/stream.html)
- [Building TCP Server with Node.js](https://nodejs.dev/learn/the-nodejs-net-module)
- [Node.js Network Programming](https://www.packtpub.com/product/nodejs-high-performance/9781785286148)
