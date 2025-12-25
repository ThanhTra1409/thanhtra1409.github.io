++
title = "Multithreading và ServerSocket trong Java"
date = "2025-12-02"
tags = ["Java","Concurrency"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&auto=format&fit=crop"
++

Trong bài trước, chúng ta đã tìm hiểu về Socket cơ bản trong Java. Tuy nhiên, một server đơn giản chỉ xử lý một client tại một thời điểm là chưa đủ cho ứng dụng thực tế. Khi có nhiều client kết nối đồng thời, chúng ta cần sử dụng multithreading để xử lý song song các kết nối.

Bài viết này sẽ hướng dẫn cách xây dựng server đa luồng (multithreaded server) trong Java, sử dụng Thread Pool với `ExecutorService` để quản lý hiệu quả các kết nối client.

![Multithreading Concept](https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1200&auto=format&fit=crop)
*Kiến trúc multithreading server*

### 1. Vấn đề với Single-Threaded Server

Server đơn luồng chỉ xử lý một client tại một thời điểm. Khi đang xử lý một client, server không thể chấp nhận kết nối mới, dẫn đến:

- Client phải chờ đợi lâu
- Hiệu suất thấp với nhiều kết nối
- Không tận dụng được tài nguyên hệ thống

### 2. Thread-Per-Connection Pattern

Cách đơn giản nhất là tạo một thread mới cho mỗi client kết nối:

```java
import java.io.*;
import java.net.*;

public class MultiThreadedServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8080)) {
            System.out.println("Server đang chạy trên port 8080...");
            
            while (true) {
                // Chấp nhận kết nối mới
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client kết nối: " + clientSocket.getInetAddress());
                
                // Tạo thread mới cho mỗi client
                Thread clientThread = new Thread(new ClientHandler(clientSocket));
                clientThread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;
    
    public ClientHandler(Socket socket) {
        this.clientSocket = socket;
    }
    
    @Override
    public void run() {
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream()));
             PrintWriter out = new PrintWriter(
                clientSocket.getOutputStream(), true)) {
            
            String message;
            while ((message = in.readLine()) != null) {
                System.out.println("Nhận: " + message);
                out.println("Echo: " + message);
                
                if ("bye".equalsIgnoreCase(message)) {
                    break;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
```

### 3. Sử dụng Thread Pool với ExecutorService

Tạo thread mới cho mỗi kết nối có thể gây lãng phí tài nguyên khi có quá nhiều client. Thread Pool giúp giới hạn số lượng thread và tái sử dụng chúng:

![Thread Pool Architecture](https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1000&auto=format&fit=crop)
*Kiến trúc Thread Pool quản lý nhiều kết nối*

```java
import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class ThreadPoolServer {
    private static final int PORT = 8080;
    private static final int THREAD_POOL_SIZE = 10;
    
    public static void main(String[] args) {
        // Tạo thread pool với 10 threads
        ExecutorService executor = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
        
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server với Thread Pool đang chạy...");
            
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client kết nối: " + clientSocket.getInetAddress());
                
                // Submit task vào thread pool
                executor.submit(new ClientHandler(clientSocket));
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
    }
}
```

### 4. Xử lý Exception và Đóng Tài Nguyên

Quan trọng là phải xử lý exception đúng cách và đảm bảo đóng tài nguyên:

```java
class ClientHandler implements Runnable {
    private Socket clientSocket;
    
    public ClientHandler(Socket socket) {
        this.clientSocket = socket;
    }
    
    @Override
    public void run() {
        try (Socket socket = clientSocket;
             BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(
                socket.getOutputStream(), true)) {
            
            String message;
            while ((message = in.readLine()) != null) {
                processMessage(message, out);
                
                if ("exit".equalsIgnoreCase(message)) {
                    break;
                }
            }
            
        } catch (IOException e) {
            System.err.println("Lỗi xử lý client: " + e.getMessage());
        }
    }
    
    private void processMessage(String message, PrintWriter out) {
        System.out.println("Xử lý: " + message);
        out.println("Server nhận: " + message);
    }
}
```

### 5. Graceful Shutdown

Khi tắt server, cần đảm bảo tất cả thread đã hoàn thành:

```java
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
    System.out.println("Đang tắt server...");
    executor.shutdown();
    try {
        if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
            executor.shutdownNow();
        }
    } catch (InterruptedException e) {
        executor.shutdownNow();
    }
}));
```

### 6. Lưu ý về Đồng Bộ

Khi nhiều thread truy cập shared data, cần sử dụng synchronization:

```java
class ClientRegistry {
    private final Set<Socket> clients = Collections.synchronizedSet(new HashSet<>());
    
    public void addClient(Socket socket) {
        clients.add(socket);
    }
    
    public void removeClient(Socket socket) {
        clients.remove(socket);
    }
    
    public void broadcast(String message) {
        synchronized (clients) {
            for (Socket client : clients) {
                try {
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                    out.println(message);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

Multithreading là kỹ thuật quan trọng để xây dựng server có khả năng xử lý nhiều client đồng thời. Sử dụng Thread Pool với `ExecutorService` giúp quản lý tài nguyên hiệu quả hơn so với việc tạo thread mới cho mỗi kết nối.

Tuy nhiên, với số lượng kết nối cực lớn (hàng nghìn), thread-based model có thể gặp giới hạn. Trong bài viết tiếp theo, chúng ta sẽ tìm hiểu về Java NIO - một cách tiếp cận non-blocking giúp xử lý hàng nghìn kết nối với số lượng thread tối thiểu.

---

### Tài liệu tham khảo

- [Java Concurrency Tutorial](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [ExecutorService Documentation](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ExecutorService.html)
- [Java Thread Pool Best Practices](https://www.baeldung.com/thread-pool-java-and-guava)
- [Multithreaded Server Socket Programming](https://www.geeksforgeeks.org/multithreaded-servers-in-java/)
