++
title = "Basic Socket in Java"
date = "2025-12-01"
tags = ["Java","Socket"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&auto=format&fit=crop"
++

Network programming is an essential part of modern application development. Socket is the most fundamental foundation for establishing network connections between computers. In Java, the `java.net` package provides `Socket` and `ServerSocket` classes that help us easily build client-server applications.

This article will introduce how to use Socket in Java to create TCP/IP connections, transmit and receive data between client and server, along with important notes when working with Sockets.

![Socket Architecture](https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&auto=format&fit=crop)
*Client-Server architecture using Sockets*

### 1. What is a Socket?

A Socket is an endpoint of a two-way communication channel between two programs running on a network. In Java, there are two main types of sockets:

- **Socket**: Used on the client side to connect to a server
- **ServerSocket**: Used on the server side to listen for connections from clients

![TCP Connection Flow](https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1000&auto=format&fit=crop)
*TCP connection flow between client and server*

### 2. Creating a Server Socket

The server needs to create a `ServerSocket` to listen for incoming connections on a specific port:

```java
import java.io.*;
import java.net.*;

public class SimpleServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8080)) {
            System.out.println("Server is listening on port 8080...");
            
            // Accept connection from client
            Socket clientSocket = serverSocket.accept();
            System.out.println("Client connected: " + clientSocket.getInetAddress());
            
            // Create input/output streams
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            
            // Read data from client
            String message = in.readLine();
            System.out.println("Received from client: " + message);
            
            // Send response to client
            out.println("Server received: " + message);
            
            // Close connection
            clientSocket.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 3. Creating a Client Socket

The client uses `Socket` to connect to the server:

```java
import java.io.*;
import java.net.*;

public class SimpleClient {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 8080)) {
            System.out.println("Connected to server!");
            
            // Create input/output streams
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));
            
            // Send data to server
            out.println("Hello server!");
            
            // Receive response from server
            String response = in.readLine();
            System.out.println("Received from server: " + response);
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 4. Key Concepts

**TCP vs UDP:**
- **TCP (Transmission Control Protocol)**: Connection-oriented, ensures data delivery and order (used by Socket)
- **UDP (User Datagram Protocol)**: Connectionless, faster but doesn't guarantee delivery (used by DatagramSocket)

**Ports:**
- Port is a number (0-65535) identifying a specific service on a computer
- Well-known ports: HTTP (80), HTTPS (443), FTP (21)
- Custom applications typically use ports 1024-65535

### 5. Error Handling

Common errors when working with Sockets:

```java
try {
    Socket socket = new Socket("localhost", 8080);
    // ... work with socket
} catch (UnknownHostException e) {
    System.err.println("Cannot find host: " + e.getMessage());
} catch (IOException e) {
    System.err.println("I/O error: " + e.getMessage());
} finally {
    // Always close socket in finally block
    if (socket != null && !socket.isClosed()) {
        socket.close();
    }
}
```

**Important notes:**
- Always close Socket and streams after use to avoid resource leaks
- Use try-with-resources (Java 7+) for automatic resource management
- Handle exceptions properly, especially IOException and UnknownHostException
- Set appropriate timeout to avoid blocking indefinitely

### 6. Practical Applications

Sockets are used in many applications:
- **Chat applications**: Real-time messaging between users
- **File transfer**: Sending files between computers
- **Remote control**: Controlling a computer from another location
- **Online gaming**: Synchronizing game state between players
- **IoT devices**: Communication between smart devices

### Conclusion

Java Socket is a powerful tool for building network applications. Understanding the basics of Socket helps you create client-server applications, from simple chat programs to complex distributed systems.

In the next article, we'll explore multithreading with ServerSocket to handle multiple clients simultaneously, making our server more scalable and efficient.

### References

- [Java Socket Documentation](https://docs.oracle.com/javase/8/docs/api/java/net/Socket.html)
- [Java ServerSocket Documentation](https://docs.oracle.com/javase/8/docs/api/java/net/ServerSocket.html)
- [Oracle Java Networking Tutorial](https://docs.oracle.com/javase/tutorial/networking/)
