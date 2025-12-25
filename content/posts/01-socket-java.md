++
title = "Socket cơ bản trong Java"
date = "2025-12-01"
tags = ["Java","Socket"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&auto=format&fit=crop"
++

Lập trình mạng là một phần quan trọng trong phát triển ứng dụng hiện đại. Socket là nền tảng cơ bản nhất để thiết lập kết nối mạng giữa các máy tính. Trong Java, package `java.net` cung cấp các class `Socket` và `ServerSocket` giúp chúng ta dễ dàng xây dựng ứng dụng client-server.

Bài viết này sẽ giới thiệu cách sử dụng Socket trong Java để tạo kết nối TCP/IP, truyền nhận dữ liệu giữa client và server, cùng với những lưu ý quan trọng khi làm việc với Socket.

![Socket Architecture](https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&auto=format&fit=crop)
*Kiến trúc client-server sử dụng Socket*

### 1. Socket là gì?

Socket là điểm cuối (endpoint) của một kênh giao tiếp hai chiều giữa hai chương trình chạy trên mạng. Trong Java, có hai loại socket chính:

- **Socket**: Dùng cho phía client để kết nối tới server
- **ServerSocket**: Dùng cho phía server để lắng nghe kết nối từ client

![TCP Connection Flow](https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1000&auto=format&fit=crop)
*Luồng kết nối TCP giữa client và server*

### 2. Tạo Server Socket

Server cần tạo một `ServerSocket` để lắng nghe các kết nối đến trên một cổng (port) cụ thể:

```java
import java.io.*;
import java.net.*;

public class SimpleServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8080)) {
            System.out.println("Server đang lắng nghe trên port 8080...");
            
            // Chấp nhận kết nối từ client
            Socket clientSocket = serverSocket.accept();
            System.out.println("Client đã kết nối: " + clientSocket.getInetAddress());
            
            // Tạo input/output streams
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            
            // Đọc dữ liệu từ client
            String message = in.readLine();
            System.out.println("Nhận từ client: " + message);
            
            // Gửi phản hồi về client
            out.println("Server đã nhận: " + message);
            
            // Đóng kết nối
            clientSocket.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 3. Tạo Client Socket

Client sử dụng `Socket` để kết nối tới server:

```java
import java.io.*;
import java.net.*;

public class SimpleClient {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 8080)) {
            System.out.println("Đã kết nối tới server!");
            
            // Tạo input/output streams
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));
            
            // Gửi dữ liệu tới server
            out.println("Xin chào server!");
            
            // Nhận phản hồi từ server
            String response = in.readLine();
            System.out.println("Nhận từ server: " + response);
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 4. Xử lý Streams

Khi làm việc với Socket, chúng ta cần hiểu về Input/Output Streams:

- **InputStream**: Đọc dữ liệu từ socket
- **OutputStream**: Ghi dữ liệu vào socket

Thường sử dụng các wrapper class như `BufferedReader`, `PrintWriter` để làm việc với text, hoặc `DataInputStream`, `DataOutputStream` để làm việc với dữ liệu nhị phân.

### 5. Lưu ý quan trọng

**Đóng tài nguyên**: Luôn đóng Socket và Streams sau khi sử dụng để tránh rò rỉ tài nguyên. Sử dụng try-with-resources để tự động đóng:

```java
try (Socket socket = new Socket("localhost", 8080);
     PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
     BufferedReader in = new BufferedReader(
         new InputStreamReader(socket.getInputStream()))) {
    // Xử lý logic
}
```

**Xử lý ngoại lệ**: Cần xử lý các exception như `IOException`, `UnknownHostException` khi làm việc với Socket.

**Timeout**: Có thể set timeout cho Socket để tránh chờ đợi vô thời hạn:

```java
socket.setSoTimeout(5000); // 5 giây
```

Socket là công cụ cơ bản và mạnh mẽ để xây dựng ứng dụng mạng trong Java. Hiểu rõ cách hoạt động của `Socket` và `ServerSocket` là nền tảng để phát triển các ứng dụng phức tạp hơn như chat application, file transfer, hoặc multiplayer games.

Trong các bài viết tiếp theo, chúng ta sẽ tìm hiểu về cách xử lý nhiều client đồng thời sử dụng multithreading, và các kỹ thuật lập trình mạng nâng cao hơn với Java NIO.

---

### Tài liệu tham khảo

- [Oracle Java Documentation - Socket](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html)
- [Oracle Java Documentation - ServerSocket](https://docs.oracle.com/javase/8/docs/api/java/net/ServerSocket.html)
- [Java Network Programming Tutorial](https://www.baeldung.com/a-guide-to-java-sockets)
- [Java Socket Programming Examples](https://www.geeksforgeeks.org/socket-programming-in-java/)
