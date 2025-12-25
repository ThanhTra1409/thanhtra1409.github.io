++
title = "WebSocket Server with Socket.IO"
date = "2025-12-11"
tags = ["JavaScript","Socket.IO","Realtime"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&auto=format&fit=crop"
++

WebSocket is a great technology for realtime communication, but implementing it from scratch can be complex. Socket.IO is a library that simplifies this process, providing fallback mechanisms, automatic reconnection, and many other convenient features.

Socket.IO is not just a WebSocket wrapper - it provides additional features like rooms, namespaces, broadcasting, and compatibility with older browsers. This article will guide you through building realtime applications with Socket.IO.

![Socket.IO Realtime](https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&auto=format&fit=crop)
*Socket.IO for realtime applications*

### 1. Installation and Basic Setup

```bash
npm install socket.io express
```

#### Basic Server

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
  console.log('Client connected:', socket.id);
  
  // Receive message from client
  socket.on('message', (data) => {
    console.log('Received message:', data);
    
    // Send back to client
    socket.emit('message', { text: 'Server received: ' + data.text });
  });
  
  // Handle disconnect
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
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
  <input id="messageInput" type="text" placeholder="Enter message...">
  <button onclick="sendMessage()">Send</button>
  
  <script>
    // Connect to server
    const socket = io();
    
    // Handle when connected
    socket.on('connect', () => {
      console.log('Connected:', socket.id);
    });
    
    // Receive message from server
    socket.on('message', (data) => {
      const div = document.createElement('div');
      div.textContent = data.text;
      document.getElementById('messages').appendChild(div);
    });
    
    // Send message
    function sendMessage() {
      const input = document.getElementById('messageInput');
      socket.emit('message', { text: input.value });
      input.value = '';
    }
    
    // Handle disconnect
    socket.on('disconnect', () => {
      console.log('Disconnected');
    });
  </script>
</body>
</html>
```

### 2. Chat Application with Rooms

```javascript
const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

app.use(express.static('public'));

// Store user information
const users = new Map();

io.on('connection', (socket) => {
  console.log('New connection:', socket.id);
  
  // Join room
  socket.on('join-room', (data) => {
    const { username, room } = data;
    
    socket.join(room);
    users.set(socket.id, { username, room });
    
    // Notify user
    socket.emit('message', {
      username: 'System',
      text: `Welcome ${username} to room ${room}!`,
      timestamp: new Date()
    });
    
    // Notify room (except user)
    socket.to(room).emit('message', {
      username: 'System',
      text: `${username} joined the room`,
      timestamp: new Date()
    });
    
    // Send list of users in room
    updateRoomUsers(room);
  });
  
  // Receive chat message
  socket.on('chat-message', (data) => {
    const user = users.get(socket.id);
    if (!user) return;
    
    const messageData = {
      username: user.username,
      text: data.text,
      timestamp: new Date()
    };
    
    // Broadcast to all in room
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
        text: `${user.username} left the room`,
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

### 3. Broadcasting and Namespaces

```javascript
// Broadcasting
io.on('connection', (socket) => {
  // Send to this socket only
  socket.emit('message', 'Only for you');
  
  // Send to all except this socket
  socket.broadcast.emit('message', 'Send to all except sender');
  
  // Send to all
  io.emit('message', 'Send to everyone');
  
  // Send to room
  io.to('room1').emit('message', 'Send to room1');
  
  // Send to multiple rooms
  io.to('room1').to('room2').emit('message', 'Send to 2 rooms');
  
  // Send to all in room except sender
  socket.to('room1').emit('message', 'Send to room1 except sender');
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

### 4. Authentication and Middleware

```javascript
const jwt = require('jsonwebtoken');

// Middleware for authentication
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
    
    // Process message...
    
    // Call callback to acknowledge
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

### 6. Error Handling and Reconnection

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
    // Server actively disconnected, need manual reconnect
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

### 7. Performance and Scaling

#### Using Redis Adapter for Multiple Servers

```javascript
const redis = require('socket.io-redis');

io.adapter(redis({ 
  host: 'localhost', 
  port: 6379 
}));

// Now can scale horizontally with multiple server instances
```

#### Compression

```javascript
const io = socketIO(server, {
  perMessageDeflate: {
    threshold: 1024 // Compress if message > 1KB
  }
});
```

Socket.IO is a great choice for building realtime applications with JavaScript. With features like rooms, namespaces, automatic reconnection, and fallback mechanisms, Socket.IO helps developers focus on business logic instead of worrying about low-level issues.

However, note that Socket.IO is not pure WebSocket - it has more overhead. For simple applications that only need basic WebSocket, consider using the ws library or native WebSocket.

---

### References

- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [Socket.IO Server API](https://socket.io/docs/v4/server-api/)
- [Socket.IO Client API](https://socket.io/docs/v4/client-api/)
- [Building Realtime Apps with Socket.IO](https://socket.io/get-started/chat)
