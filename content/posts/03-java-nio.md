++
title = "Java NIO — lập trình mạng hiệu năng cao"
date = "2025-12-03"
tags = ["Java","NIO"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&auto=format&fit=crop"
++

Trong các bài trước, chúng ta đã tìm hiểu về Socket cơ bản và multithreading server. Tuy nhiên, với mô hình thread-per-connection, khi số lượng kết nối tăng lên hàng nghìn, hệ thống sẽ gặp vấn đề về hiệu suất và tài nguyên.

Java NIO (New I/O hoặc Non-blocking I/O) được giới thiệu từ Java 1.4 để giải quyết vấn đề này. NIO cho phép một thread xử lý nhiều kết nối đồng thời thông qua cơ chế non-blocking I/O, giúp xây dựng server có khả năng mở rộng cao.

![Java NIO Architecture](https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200&auto=format&fit=crop)
*Kiến trúc Java NIO với Selector và Channel*

### 1. Sự khác biệt giữa I/O và NIO

**Blocking I/O (java.io)**:
- Một thread chỉ xử lý một kết nối
- Thread bị block khi đọc/ghi dữ liệu
- Không hiệu quả với nhiều kết nối

**Non-blocking I/O (java.nio)**:
- Một thread có thể xử lý nhiều kết nối
- Không bị block khi không có dữ liệu
- Sử dụng Selector để giám sát nhiều Channel

### 2. Các thành phần chính của NIO

**Channel**: Kênh đọc/ghi dữ liệu, tương tự như Stream nhưng hỗ trợ cả đọc và ghi.

**Buffer**: Vùng nhớ để lưu trữ dữ liệu tạm thời. Phải đọc/ghi dữ liệu qua Buffer.

**Selector**: Cho phép một thread giám sát nhiều Channel và xử lý các sự kiện I/O.

![NIO Components](https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1000&auto=format&fit=crop)
*Các thành phần chính: Channel, Buffer, Selector*

### 3. Xây dựng NIO Server

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
            // Mở ServerSocketChannel
            ServerSocketChannel serverChannel = ServerSocketChannel.open();
            serverChannel.bind(new InetSocketAddress(PORT));
            serverChannel.configureBlocking(false);
            
            // Tạo Selector
            Selector selector = Selector.open();
            
            // Đăng ký ServerSocketChannel với Selector
            serverChannel.register(selector, SelectionKey.OP_ACCEPT);
            
            System.out.println("NIO Server đang chạy trên port " + PORT);
            
            ByteBuffer buffer = ByteBuffer.allocate(BUFFER_SIZE);
            
            while (true) {
                // Chờ sự kiện I/O
                selector.select();
                
                // Lấy các key đã sẵn sàng
                Set<SelectionKey> selectedKeys = selector.selectedKeys();
                Iterator<SelectionKey> iterator = selectedKeys.iterator();
                
                while (iterator.hasNext()) {
                    SelectionKey key = iterator.next();
                    iterator.remove();
                    
                    if (key.isAcceptable()) {
                        // Chấp nhận kết nối mới
                        handleAccept(serverChannel, selector);
                    } else if (key.isReadable()) {
                        // Đọc dữ liệu
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
        System.out.println("Client kết nối: " + clientChannel.getRemoteAddress());
    }
    
    private static void handleRead(SelectionKey key, ByteBuffer buffer) 
                                  throws IOException {
        SocketChannel clientChannel = (SocketChannel) key.channel();
        buffer.clear();
        
        int bytesRead = clientChannel.read(buffer);
        
        if (bytesRead == -1) {
            // Client đóng kết nối
            clientChannel.close();
            System.out.println("Client ngắt kết nối");
            return;
        }
        
        if (bytesRead > 0) {
            buffer.flip();
            byte[] data = new byte[buffer.remaining()];
            buffer.get(data);
            String message = new String(data);
            
            System.out.println("Nhận: " + message);
            
            // Echo về client
            buffer.rewind();
            clientChannel.write(buffer);
        }
    }
}
```

### 4. Làm việc với ByteBuffer

ByteBuffer có các thuộc tính quan trọng:

- **capacity**: Kích thước tối đa của buffer
- **position**: Vị trí hiện tại
- **limit**: Giới hạn đọc/ghi

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);

// Ghi dữ liệu vào buffer
buffer.put("Hello".getBytes());

// Chuyển từ write mode sang read mode
buffer.flip();

// Đọc dữ liệu từ buffer
while (buffer.hasRemaining()) {
    byte b = buffer.get();
}

// Xóa buffer để ghi lại
buffer.clear();

// Hoặc compact để giữ dữ liệu chưa đọc
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
            
            // Gửi dữ liệu
            String message = "Hello from NIO Client";
            ByteBuffer buffer = ByteBuffer.wrap(message.getBytes());
            socketChannel.write(buffer);
            
            // Nhận phản hồi
            buffer.clear();
            int bytesRead = socketChannel.read(buffer);
            
            if (bytesRead > 0) {
                buffer.flip();
                byte[] data = new byte[buffer.remaining()];
                buffer.get(data);
                System.out.println("Nhận: " + new String(data));
            }
            
            socketChannel.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 6. Ưu điểm và nhược điểm

**Ưu điểm**:
- Xử lý nhiều kết nối với ít thread
- Hiệu suất cao với nhiều kết nối đồng thời
- Tiết kiệm tài nguyên hệ thống

**Nhược điểm**:
- Code phức tạp hơn blocking I/O
- Khó debug và maintain
- Cần hiểu rõ về Buffer và Channel

### 7. Khi nào nên dùng NIO?

- Server cần xử lý hàng nghìn kết nối đồng thời
- Các kết nối có lưu lượng thấp (chat, notification)
- Cần tối ưu tài nguyên hệ thống

Không nên dùng NIO khi:
- Số lượng kết nối ít (dưới 100)
- Xử lý logic phức tạp cho mỗi kết nối
- Team thiếu kinh nghiệm với NIO

Java NIO là công cụ mạnh mẽ để xây dựng server hiệu năng cao, có khả năng xử lý hàng nghìn kết nối đồng thời. Tuy nhiên, với sự phức tạp của nó, bạn nên cân nhắc sử dụng các framework như Netty hoặc Vert.x, được xây dựng trên nền tảng NIO nhưng cung cấp API dễ sử dụng hơn.

Trong các bài tiếp theo, chúng ta sẽ chuyển sang JavaScript và Node.js, tìm hiểu cách xây dựng server với event-driven model tự nhiên của Node.

---

### Tài liệu tham khảo

- [Oracle Java NIO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/nio.html)
- [Java NIO Selector](https://docs.oracle.com/javase/8/docs/api/java/nio/channels/Selector.html)
- [Guide to Java NIO](https://www.baeldung.com/java-nio-selector)
- [Java NIO vs IO](https://jenkov.com/tutorials/java-nio/nio-vs-io.html)
