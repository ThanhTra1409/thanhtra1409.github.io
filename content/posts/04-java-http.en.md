++
title = "Building Basic HTTP Client and Server with Java"
date = "2025-12-05"
tags = ["Java","HTTP"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop"
++

HTTP is the foundational protocol of the web, used to transmit data between client and server. In Java, we can easily create HTTP clients to call APIs and build simple HTTP servers for learning or testing purposes.

This article will guide you through using `HttpClient` (Java 11+) to make HTTP requests and create a basic HTTP server with `com.sun.net.httpserver.HttpServer`.

![HTTP Communication](https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&auto=format&fit=crop)
*HTTP communication between client and server*

### 1. HTTP Client with Java 11+

Java 11 introduced `java.net.http.HttpClient` - a modern API for making HTTP requests.

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
            // Create HttpClient
            HttpClient client = HttpClient.newHttpClient();
            
            // Create HttpRequest
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://jsonplaceholder.typicode.com/posts/1"))
                .GET()
                .build();
            
            // Send request and receive response
            HttpResponse<String> response = client.send(request, 
                HttpResponse.BodyHandlers.ofString());
            
            // Process response
            System.out.println("Status Code: " + response.statusCode());
            System.out.println("Body: " + response.body());
            
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

#### POST Request with JSON

```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;

public class HttpPostExample {
    public static void main(String[] args) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            
            // Create JSON body
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
        
        // Send async request
        CompletableFuture<HttpResponse<String>> responseFuture = 
            client.sendAsync(request, HttpResponse.BodyHandlers.ofString());
        
        responseFuture.thenApply(HttpResponse::body)
            .thenAccept(System.out::println)
            .join();
    }
}
```

### 2. Building an HTTP Server

Java provides `com.sun.net.httpserver.HttpServer` to create simple HTTP servers.

```java
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {
    public static void main(String[] args) throws IOException {
        // Create HTTP server on port 8080
        HttpServer server = HttpServer.create(
            new InetSocketAddress(8080), 0);
        
        // Register handlers
        server.createContext("/", new RootHandler());
        server.createContext("/api/users", new UsersHandler());
        server.createContext("/api/posts", new PostsHandler());
        
        // Start server
        server.setExecutor(null); // Use default executor
        server.start();
        
        System.out.println("Server running on http://localhost:8080");
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
        // Read request body
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

### 3. Handling Headers and Query Parameters

```java
class AdvancedHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Get headers
        String userAgent = exchange.getRequestHeaders()
            .getFirst("User-Agent");
        
        // Get query parameters
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

### 4. Using Gson for JSON

To work with JSON more easily, use the Gson library:

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
            // Parse JSON from request
            String requestBody = new String(
                exchange.getRequestBody().readAllBytes());
            User user = gson.fromJson(requestBody, User.class);
            
            // Process user...
            
            // Return JSON response
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

Java 11+'s `HttpClient` provides a modern and powerful API for making HTTP requests, supporting both synchronous and asynchronous operations. `HttpServer` is a great tool for learning and testing purposes, however in production you should use frameworks like Spring Boot or Javalin.

In the next article, we'll move to JavaScript and explore the Fetch API as well as WebSocket in the browser.

---

### References

- [Java HttpClient Documentation](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html)
- [Java HttpServer Documentation](https://docs.oracle.com/javase/8/docs/jre/api/net/httpserver/spec/com/sun/net/httpserver/HttpServer.html)
- [Guide to Java HttpClient](https://www.baeldung.com/java-9-http-client)
- [Building HTTP Server in Java](https://www.baeldung.com/java-http-server)
