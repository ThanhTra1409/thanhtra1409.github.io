++
title = "Java NIO — High Performance Network Programming"
date = "2025-12-03"
tags = ["Java","NIO"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&auto=format&fit=crop"
++

In previous articles, we learned about basic Sockets and multithreaded servers. However, with the thread-per-connection model, when the number of connections increases to thousands, the system will face performance and resource issues.

Java NIO (New I/O or Non-blocking I/O) was introduced in Java 1.4 to solve this problem. NIO allows a thread to handle multiple connections simultaneously through non-blocking I/O mechanisms, helping build highly scalable servers.

![Java NIO Architecture](https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200&auto=format&fit=crop)
*Java NIO architecture with Selector and Channel*

### 1. Differences Between I/O and NIO

**Blocking I/O (java.io)**:
- One thread handles one connection only
- Thread blocks when reading/writing data
- Not efficient with many connections

**Non-blocking I/O (java.nio)**:
- One thread can handle multiple connections
- Not blocked when no data available
- Uses Selector to monitor multiple Channels

### 2. Main Components of NIO

**Channel**: Channel for reading/writing data, similar to Stream but supports both reading and writing.

**Buffer**: Memory area for temporarily storing data. Must read/write data through Buffer.

**Selector**: Allows a thread to monitor multiple Channels and handle I/O events.

![NIO Components](https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1000&auto=format&fit=crop)
*Main components: Channel, Buffer, Selector*

### 3. Building an NIO Server

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;
import java.util.Set;

public class NIOServer {
    private static final int PORT = 8080;
    private static final int BUFFER_SIZE = 256;
    
    public static void main(String[] args) {
        try {
            // Open ServerSocketChannel
            ServerSocketChannel serverChannel = ServerSocketChannel.open();
            serverChannel.bind(new InetSocketAddress(PORT));
            serverChannel.configureBlocking(false);
            
            // Create Selector
            Selector selector = Selector.open();
            
            // Register ServerSocketChannel with Selector
            serverChannel.register(selector, SelectionKey.OP_ACCEPT);
            
            System.out.println("NIO Server running on port " + PORT);
            
            ByteBuffer buffer = ByteBuffer.allocate(BUFFER_SIZE);
            
            while (true) {
                // Wait for I/O events
                selector.select();
                
                // Get ready keys
                Set<SelectionKey> selectedKeys = selector.selectedKeys();
                Iterator<SelectionKey> iterator = selectedKeys.iterator();
                
                while (iterator.hasNext()) {
                    SelectionKey key = iterator.next();
                    iterator.remove();
                    
                    if (key.isAcceptable()) {
                        // Accept new connection
                        handleAccept(serverChannel, selector);
                    } else if (key.isReadable()) {
                        // Read data
                        handleRead(key, buffer);
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private static void handleAccept(ServerSocketChannel serverChannel, 
                                    Selector selector) throws IOException {
        SocketChannel clientChannel = serverChannel.accept();
        clientChannel.configureBlocking(false);
        clientChannel.register(selector, SelectionKey.OP_READ);
        System.out.println("Client connected: " + clientChannel.getRemoteAddress());
    }
    
    private static void handleRead(SelectionKey key, ByteBuffer buffer) 
                                  throws IOException {
        SocketChannel clientChannel = (SocketChannel) key.channel();
        buffer.clear();
        
        int bytesRead = clientChannel.read(buffer);
        
        if (bytesRead == -1) {
            // Client closed connection
            clientChannel.close();
            System.out.println("Client disconnected");
            return;
        }
        
        if (bytesRead > 0) {
            buffer.flip();
            byte[] data = new byte[buffer.remaining()];
            buffer.get(data);
            String message = new String(data);
            
            System.out.println("Received: " + message);
            
            // Echo back to client
            buffer.rewind();
            clientChannel.write(buffer);
        }
    }
}
```

### 4. Working with ByteBuffer

ByteBuffer has important properties:

- **capacity**: Maximum size of buffer
- **position**: Current position
- **limit**: Read/write limit

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);

// Write data to buffer
buffer.put("Hello".getBytes());

// Switch from write mode to read mode
buffer.flip();

// Read data from buffer
while (buffer.hasRemaining()) {
    byte b = buffer.get();
}

// Clear buffer to write again
buffer.clear();

// Or compact to keep unread data
buffer.compact();
```

### 5. NIO Client

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public class NIOClient {
    public static void main(String[] args) {
        try {
            SocketChannel socketChannel = SocketChannel.open();
            socketChannel.connect(new InetSocketAddress("localhost", 8080));
            
            // Send data
            String message = "Hello from NIO Client";
            ByteBuffer buffer = ByteBuffer.wrap(message.getBytes());
            socketChannel.write(buffer);
            
            // Receive response
            buffer.clear();
            int bytesRead = socketChannel.read(buffer);
            
            if (bytesRead > 0) {
                buffer.flip();
                byte[] data = new byte[buffer.remaining()];
                buffer.get(data);
                System.out.println("Received: " + new String(data));
            }
            
            socketChannel.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 6. Advantages and Disadvantages

**Advantages**:
- Handle many connections with few threads
- High performance with many concurrent connections
- Save system resources

**Disadvantages**:
- More complex code than blocking I/O
- Difficult to debug and maintain
- Need deep understanding of Buffer and Channel

### 7. When to Use NIO?

- Server needs to handle thousands of concurrent connections
- Connections have low traffic (chat, notifications)
- Need to optimize system resources

Don't use NIO when:
- Few connections (under 100)
- Complex processing logic for each connection
- Team lacks experience with NIO

Java NIO is a powerful tool for building high-performance servers capable of handling thousands of concurrent connections. However, with its complexity, you should consider using frameworks like Netty or Vert.x, built on NIO foundation but providing easier-to-use APIs.

In the next articles, we'll move to JavaScript and Node.js, exploring how to build servers with Node's natural event-driven model.

---

### References

- [Oracle Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/nio.html)
- [Java NIO Selector](https://docs.oracle.com/javase/8/docs/api/java/nio/channels/Selector.html)
- [Guide to Java NIO](https://www.baeldung.com/java-nio-selector)
- [Java NIO vs IO](https://jenkov.com/tutorials/java-nio/nio-vs-io.html)
