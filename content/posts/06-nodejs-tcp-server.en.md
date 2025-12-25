++
title = "Node.js: TCP Server with the `net` Module"
date = "2025-12-09"
tags = ["JavaScript","Node.js","TCP"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&auto=format&fit=crop"
++

Node.js with its event-driven architecture and non-blocking I/O is an excellent platform for building high-performance network servers. The `net` module built into Node.js provides APIs to create TCP servers and clients simply.

Unlike the multithreading model in Java, Node.js uses a single-threaded event loop to handle thousands of concurrent connections, helping save resources and scale easily.

![Node.js TCP Server](https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=1200&auto=format&fit=crop)
*Node.js TCP Server with Event-Driven Architecture*

### 1. Creating a Basic TCP Server

```javascript
const net = require('net');

// Create TCP server
const server = net.createServer((socket) => {
  console.log('Client connected:', socket.remoteAddress, socket.remotePort);
  
  // Send welcome message
  socket.write('Welcome to TCP Server!\n');
  
  // Handle data from client
  socket.on('data', (data) => {
    console.log('Received from client:', data.toString());
    
    // Echo back to client
    socket.write(`Echo: ${data}`);
  });
  
  // Handle when client disconnects
  socket.on('end', () => {
    console.log('Client disconnected');
  });
  
  // Handle errors
  socket.on('error', (err) => {
    console.error('Socket error:', err.message);
  });
});

// Listen on port 8080
server.listen(8080, () => {
  console.log('TCP Server running on port 8080');
});

// Handle server errors
server.on('error', (err) => {
  console.error('Server error:', err.message);
});
```

### 2. TCP Client

```javascript
const net = require('net');

// Create TCP client
const client = net.createConnection({ port: 8080, host: 'localhost' }, () => {
  console.log('Connected to server');
  client.write('Hello server!');
});

// Receive data from server
client.on('data', (data) => {
  console.log('Received from server:', data.toString());
  // client.end(); // Close connection after receiving
});

// Handle when disconnected
client.on('end', () => {
  console.log('Disconnected');
});

// Handle errors
client.on('error', (err) => {
  console.error('Error:', err.message);
});
```

### 3. Echo Server with Multiple Client Management

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
      console.log(`Echo Server running on port ${this.port}`);
    });
    
    this.server.on('error', (err) => {
      console.error('Server error:', err);
    });
  }
  
  handleConnection(socket) {
    const clientId = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`[${clientId}] New connection`);
    
    // Add client to list
    this.clients.add(socket);
    
    // Send welcome message
    socket.write(`Welcome! Currently ${this.clients.size} clients online\n`);
    
    // Handle data
    socket.on('data', (data) => {
      const message = data.toString().trim();
      console.log(`[${clientId}] ${message}`);
      
      // Echo with timestamp
      const response = `[${new Date().toISOString()}] Echo: ${message}\n`;
      socket.write(response);
    });
    
    // Handle disconnection
    socket.on('end', () => {
      console.log(`[${clientId}] Disconnected`);
      this.clients.delete(socket);
    });
    
    // Handle errors
    socket.on('error', (err) => {
      console.error(`[${clientId}] Error:`, err.message);
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
    // Close all connections
    for (const client of this.clients) {
      client.end();
    }
    
    // Close server
    this.server.close(() => {
      console.log('Server closed');
    });
  }
}

// Usage
const server = new EchoServer(8080);
server.start();

// Broadcast message every 30 seconds
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
    // Request username
    socket.write('Enter your username: ');
    
    let username = null;
    
    socket.on('data', (data) => {
      const message = data.toString().trim();
      
      // If no username yet, set username
      if (!username) {
        username = message;
        this.clients.set(socket, username);
        
        socket.write(`Welcome ${username}!\n`);
        this.broadcast(`${username} joined the chat\n`, socket);
        
        console.log(`${username} joined`);
        return;
      }
      
      // Handle commands
      if (message.startsWith('/')) {
        this.handleCommand(socket, message);
        return;
      }
      
      // Broadcast message
      const chatMessage = `[${username}]: ${message}\n`;
      console.log(chatMessage.trim());
      this.broadcast(chatMessage);
    });
    
    socket.on('end', () => {
      if (username) {
        console.log(`${username} left`);
        this.broadcast(`${username} left the chat\n`, socket);
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
      socket.write('/users - View user list\n');
      socket.write('/help - Show help\n');
      socket.write('/quit - Exit chat\n');
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

// Start server
const chatServer = new ChatServer(8080);
chatServer.start();
```

### 5. Buffer and Encoding Handling

```javascript
const net = require('net');

const server = net.createServer((socket) => {
  // Set encoding to automatically convert buffer to string
  socket.setEncoding('utf8');
  
  socket.on('data', (data) => {
    // data is already a string, no need for toString()
    console.log('Received:', data);
  });
  
  // Or work directly with Buffer
  socket.on('data', (buffer) => {
    // buffer is a Buffer object
    console.log('Buffer length:', buffer.length);
    console.log('Hex:', buffer.toString('hex'));
    console.log('UTF-8:', buffer.toString('utf8'));
    console.log('Base64:', buffer.toString('base64'));
  });
});
```

### 6. Keep-alive and Timeout

```javascript
const server = net.createServer((socket) => {
  // Set 30 second timeout
  socket.setTimeout(30000);
  
  // Handle timeout
  socket.on('timeout', () => {
    console.log('Socket timeout');
    socket.end('Timeout - closing connection\n');
  });
  
  // Enable keep-alive
  socket.setKeepAlive(true, 60000); // 60 seconds
  
  socket.on('data', (data) => {
    // Reset timeout when data arrives
    socket.setTimeout(30000);
    // Process data...
  });
});
```

### 7. Comparison with Java Thread-based Model

**Node.js (Event-driven)**:
- Single-threaded event loop
- Non-blocking I/O
- Handle many connections with few resources
- Suitable for I/O-intensive applications

**Java (Thread-based)**:
- Each connection = one thread
- Blocking I/O (unless using NIO)
- Resource-intensive with many connections
- Suitable for CPU-intensive applications

Node.js's `net` module provides simple but powerful APIs to build TCP servers. With event-driven architecture, Node.js can efficiently handle thousands of concurrent connections, making it very suitable for realtime applications like chat, game servers, or IoT applications.

In the next article, we'll explore Socket.IO - a library built on WebSocket that makes developing realtime applications much easier.

---

### References

- [Node.js net Module Documentation](https://nodejs.org/api/net.html)
- [Node.js Stream API](https://nodejs.org/api/stream.html)
- [Building TCP Server with Node.js](https://nodejs.dev/learn/the-nodejs-net-module)
- [Node.js Network Programming](https://www.packtpub.com/product/nodejs-high-performance/9781785286148)
