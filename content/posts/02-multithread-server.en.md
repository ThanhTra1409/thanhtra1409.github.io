++
title = "Multithreading and ServerSocket in Java"
date = "2025-12-02"
tags = ["Java","Concurrency"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=800&auto=format&fit=crop"
++

In the previous article, we learned about basic Sockets in Java. However, a simple server that only handles one client at a time is not sufficient for real-world applications. When multiple clients connect simultaneously, we need to use multithreading to handle connections in parallel.

This article will guide you through building a multithreaded server in Java, using Thread Pool with `ExecutorService` to efficiently manage client connections.

![Multithreading Concept](https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1200&auto=format&fit=crop)
*Multithreading server architecture*

### 1. The Problem with Single-Threaded Server

A single-threaded server can only handle one client at a time. While processing one client, the server cannot accept new connections, leading to:

- Clients having to wait a long time
- Poor performance with multiple connections
- Inability to utilize system resources

### 2. Thread-Per-Connection Pattern

The simplest approach is to create a new thread for each connecting client:

```java
import java.io.*;
import java.net.*;

public class MultiThreadedServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8080)) {
            System.out.println("Server running on port 8080...");
            
            while (true) {
                // Accept new connection
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connected: " + clientSocket.getInetAddress());
                
                // Create new thread for each client
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
                System.out.println("Received: " + message);
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

### 3. Using Thread Pool with ExecutorService

Creating a new thread for each connection can waste resources when there are too many clients. Thread Pool helps limit the number of threads and reuse them:

![Thread Pool Architecture](https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1000&auto=format&fit=crop)
*Thread Pool architecture managing multiple connections*

```java
import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class ThreadPoolServer {
    private static final int PORT = 8080;
    private static final int THREAD_POOL_SIZE = 10;
    
    public static void main(String[] args) {
        // Create thread pool with 10 threads
        ExecutorService executor = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
        
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server with Thread Pool running...");
            
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connected: " + clientSocket.getInetAddress());
                
                // Submit task to thread pool
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

### 4. Exception Handling and Resource Closing

It's important to handle exceptions properly and ensure resources are closed:

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
            System.err.println("Error handling client: " + e.getMessage());
        }
    }
    
    private void processMessage(String message, PrintWriter out) {
        System.out.println("Processing: " + message);
        out.println("Server received: " + message);
    }
}
```

### 5. Graceful Shutdown

When shutting down the server, ensure all threads have completed:

```java
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
    System.out.println("Shutting down server...");
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

### 6. Notes on Synchronization

When multiple threads access shared data, synchronization is needed:

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

Multithreading is an important technique for building servers capable of handling multiple clients simultaneously. Using Thread Pool with `ExecutorService` helps manage resources more efficiently compared to creating a new thread for each connection.

However, with extremely large numbers of connections (thousands), thread-based models may hit limits. In the next article, we'll explore Java NIO - a non-blocking approach that handles thousands of connections with minimal threads.

---

### References

- [Java Concurrency Tutorial](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [ExecutorService Documentation](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ExecutorService.html)
- [Java Thread Pool Best Practices](https://www.baeldung.com/thread-pool-java-and-guava)
- [Multithreaded Server Socket Programming](https://www.geeksforgeeks.org/multithreaded-servers-in-java/)
