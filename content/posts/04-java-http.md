++
title = "Xây dựng HTTP client và server cơ bản bằng Java"
date = "2025-12-05"
tags = ["Java","HTTP"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop"
++

HTTP là giao thức nền tảng của web, được sử dụng để truyền tải dữ liệu giữa client và server. Trong Java, chúng ta có thể dễ dàng tạo HTTP client để gọi API và xây dựng HTTP server đơn giản cho mục đích học tập hoặc testing.

Bài viết này sẽ hướng dẫn sử dụng `HttpClient` (Java 11+) để thực hiện HTTP requests và tạo HTTP server cơ bản với `com.sun.net.httpserver.HttpServer`.

![HTTP Communication](https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&auto=format&fit=crop)
*Giao tiếp HTTP giữa client và server*

### 1. HTTP Client với Java 11+

Java 11 giới thiệu `java.net.http.HttpClient` - một API hiện đại để thực hiện HTTP requests.

#### GET Request

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.io.IOException;

public class HttpClientExample {
    public static void main(String[] args) {
        try {
            // Tạo HttpClient
            HttpClient client = HttpClient.newHttpClient();
            
            // Tạo HttpRequest
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://jsonplaceholder.typicode.com/posts/1"))
                .GET()
                .build();
            
            // Gửi request và nhận response
            HttpResponse<String> response = client.send(request, 
                HttpResponse.BodyHandlers.ofString());
            
            // Xử lý response
            System.out.println("Status Code: " + response.statusCode());
            System.out.println("Body: " + response.body());
            
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

#### POST Request với JSON

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class HttpPostExample {
    public static void main(String[] args) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            
            // Tạo JSON body
            String jsonBody = """{
                "title": "foo",
                "body": "bar",
                "userId": 1
            }""";
            
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://jsonplaceholder.typicode.com/posts"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();
            
            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            
            System.out.println("Status: " + response.statusCode());
            System.out.println("Response: " + response.body());
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### Asynchronous Request

```java
import java.net.http.*;
import java.net.URI;
import java.util.concurrent.CompletableFuture;

public class AsyncHttpExample {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://jsonplaceholder.typicode.com/posts/1"))
            .build();
        
        // Gửi request không đồng bộ
        CompletableFuture<HttpResponse<String>> responseFuture = 
            client.sendAsync(request, HttpResponse.BodyHandlers.ofString());
        
        responseFuture.thenApply(HttpResponse::body)
            .thenAccept(System.out::println)
            .join();
    }
}
```

### 2. Xây dựng HTTP Server

Java cung cấp `com.sun.net.httpserver.HttpServer` để tạo HTTP server đơn giản.

```java
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {
    public static void main(String[] args) throws IOException {
        // Tạo HTTP server trên port 8080
        HttpServer server = HttpServer.create(
            new InetSocketAddress(8080), 0);
        
        // Đăng ký handlers
        server.createContext("/", new RootHandler());
        server.createContext("/api/users", new UsersHandler());
        server.createContext("/api/posts", new PostsHandler());
        
        // Start server
        server.setExecutor(null); // Sử dụng default executor
        server.start();
        
        System.out.println("Server đang chạy trên http://localhost:8080");
    }
}

class RootHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String response = "Welcome to Simple HTTP Server!";
        exchange.sendResponseHeaders(200, response.length());
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}

class UsersHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        
        if ("GET".equals(method)) {
            handleGet(exchange);
        } else if ("POST".equals(method)) {
            handlePost(exchange);
        } else {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
        }
    }
    
    private void handleGet(HttpExchange exchange) throws IOException {
        String jsonResponse = """[
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Smith"}
        ]""";
        
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(200, jsonResponse.length());
        OutputStream os = exchange.getResponseBody();
        os.write(jsonResponse.getBytes());
        os.close();
    }
    
    private void handlePost(HttpExchange exchange) throws IOException {
        // Đọc request body
        String requestBody = new String(
            exchange.getRequestBody().readAllBytes());
        
        System.out.println("Received: " + requestBody);
        
        String response = "{\"message\": \"User created\"}";
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(201, response.length());
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}

class PostsHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String jsonResponse = """[
            {"id": 1, "title": "First Post", "body": "Content here"},
            {"id": 2, "title": "Second Post", "body": "More content"}
        ]""";
        
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(200, jsonResponse.length());
        OutputStream os = exchange.getResponseBody();
        os.write(jsonResponse.getBytes());
        os.close();
    }
}
```

### 3. Xử lý Headers và Query Parameters

```java
class AdvancedHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Lấy headers
        String userAgent = exchange.getRequestHeaders()
            .getFirst("User-Agent");
        
        // Lấy query parameters
        String query = exchange.getRequestURI().getQuery();
        Map<String, String> params = parseQuery(query);
        
        String response = "User-Agent: " + userAgent + "\n";
        response += "Params: " + params;
        
        exchange.sendResponseHeaders(200, response.length());
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
    
    private Map<String, String> parseQuery(String query) {
        Map<String, String> params = new HashMap<>();
        if (query != null) {
            String[] pairs = query.split("&");
            for (String pair : pairs) {
                String[] keyValue = pair.split("=");
                if (keyValue.length == 2) {
                    params.put(keyValue[0], keyValue[1]);
                }
            }
        }
        return params;
    }
}
```

### 4. Sử dụng Gson cho JSON

Để làm việc với JSON dễ dàng hơn, sử dụng thư viện Gson:

```java
import com.google.gson.Gson;

class User {
    private int id;
    private String name;
    private String email;
    
    // Constructor, getters, setters
}

class JsonHandler implements HttpHandler {
    private Gson gson = new Gson();
    
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if ("POST".equals(exchange.getRequestMethod())) {
            // Parse JSON từ request
            String requestBody = new String(
                exchange.getRequestBody().readAllBytes());
            User user = gson.fromJson(requestBody, User.class);
            
            // Xử lý user...
            
            // Trả về JSON response
            String jsonResponse = gson.toJson(user);
            exchange.getResponseHeaders()
                .add("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, jsonResponse.length());
            OutputStream os = exchange.getResponseBody();
            os.write(jsonResponse.getBytes());
            os.close();
        }
    }
}
```

`HttpClient` của Java 11+ cung cấp API hiện đại và mạnh mẽ để thực hiện HTTP requests, hỗ trợ cả synchronous và asynchronous operations. `HttpServer` là công cụ tuyệt vời cho mục đích học tập và testing, tuy nhiên trong production nên sử dụng các framework như Spring Boot hoặc Javalin.

Trong bài viết tiếp theo, chúng ta sẽ chuyển sang JavaScript và tìm hiểu về Fetch API cũng như WebSocket trên trình duyệt.

---

### Tài liệu tham khảo

- [Java HttpClient Documentation](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html)
- [Java HttpServer Documentation](https://docs.oracle.com/javase/8/docs/jre/api/net/httpserver/spec/com/sun/net/httpserver/HttpServer.html)
- [Guide to Java HttpClient](https://www.baeldung.com/java-9-http-client)
- [Building HTTP Server in Java](https://www.baeldung.com/java-http-server)
