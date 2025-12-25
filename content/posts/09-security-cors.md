++
title = "Bảo mật cơ bản: CORS và chính sách cho API"
date = "2025-12-16"
tags = ["Security","JavaScript","Web"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&auto=format&fit=crop"
++

Khi xây dựng web API, bảo mật là mối quan tâm hàng đầu. Tuy nhiên, nhiều developer mới bắt đầu thường gặp phải lỗi CORS hoặc bỏ qua các vấn đề bảo mật cơ bản, dẫn đến ứng dụng dễ bị tấn công.

Bài viết này sẽ giải thích CORS là gì, tại sao cần nó, cách cấu hình đúng, và các best practices bảo mật khác cho web API.

![Security Concept](https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&auto=format&fit=crop)
*Bảo mật API với CORS và authentication*

### 1. CORS là gì?

**CORS (Cross-Origin Resource Sharing)** là cơ chế bảo mật của trình duyệt, ngăn chặn các request từ một origin (domain) khác gọi đến API của bạn.

**Origin** bao gồm:
- Protocol (http/https)
- Domain (example.com)
- Port (3000, 8080)

Ví dụ:
- `http://localhost:3000` và `http://localhost:8080` là khác origin
- `http://example.com` và `https://example.com` là khác origin

### 2. Tại sao cần CORS?

Không có CORS, một website độc hại có thể:
- Đọc dữ liệu nhạy cảm từ API của bạn
- Gửi request với credentials của user
- Thực hiện các thao tác trái phép

### 3. Cấu hình CORS trong Express

#### Cơ bản - Cho phép tất cả

```javascript
const express = require('express');
const cors = require('cors');

const app = express();

// Cho phép tất cả origins (KHÔNG nên dùng trong production)
app.use(cors());

app.get('/api/data', (req, res) => {
  res.json({ message: 'Data' });
});
```

#### Giới hạn origins cụ thể

```javascript
const corsOptions = {
  origin: 'http://localhost:3001', // Chỉ cho phép origin này
  credentials: true, // Cho phép gửi cookies
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

#### Nhiều origins

```javascript
const allowedOrigins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'https://myapp.com'
];

const corsOptions = {
  origin: function (origin, callback) {
    // Cho phép requests không có origin (như mobile apps, Postman)
    if (!origin) return callback(null, true);
    
    if (allowedOrigins.indexOf(origin) === -1) {
      const msg = 'The CORS policy does not allow access from this origin.';
      return callback(new Error(msg), false);
    }
    return callback(null, true);
  },
  credentials: true
};

app.use(cors(corsOptions));
```

#### Chỉ cho phép một số methods

```javascript
const corsOptions = {
  origin: 'http://localhost:3001',
  methods: ['GET', 'POST'], // Chỉ cho phép GET và POST
  allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));
```

### 4. Cấu hình CORS trong Java

```java
import javax.servlet.*;
import javax.servlet.http.*;

public class CorsFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        
        HttpServletResponse response = (HttpServletResponse) res;
        HttpServletRequest request = (HttpServletRequest) req;
        
        response.setHeader("Access-Control-Allow-Origin", "http://localhost:3001");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
        response.setHeader("Access-Control-Allow-Credentials", "true");
        
        if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
            response.setStatus(HttpServletResponse.SC_OK);
        } else {
            chain.doFilter(req, res);
        }
    }
}
```

### 5. Xác thực với JWT

```javascript
const jwt = require('jsonwebtoken');
const SECRET_KEY = 'your-secret-key';

// Tạo token
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  
  // Verify credentials (giả sử)
  if (username === 'user' && password === 'pass') {
    const token = jwt.sign(
      { userId: 1, username: username },
      SECRET_KEY,
      { expiresIn: '1h' }
    );
    
    res.json({ token: token });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Middleware xác thực
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    
    req.user = user;
    next();
  });
}

// Sử dụng middleware
app.get('/api/protected', authenticateToken, (req, res) => {
  res.json({ message: 'Protected data', user: req.user });
});
```

### 6. Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

// Giới hạn requests chung
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 phút
  max: 100, // 100 requests mỗi IP
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Giới hạn login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts
  skipSuccessfulRequests: true,
  message: 'Too many login attempts'
});

app.post('/api/login', loginLimiter, (req, res) => {
  // Login logic...
});
```

### 7. Helmet - Security Headers

```javascript
const helmet = require('helmet');

// Sử dụng tất cả protections
app.use(helmet());

// Hoặc tùy chỉnh
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", "data:", "https:"],
      },
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    }
  })
);
```

### 8. Input Validation

```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  // Validation rules
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  body('name').trim().isLength({ min: 3 }),
  
  // Handler
  (req, res) => {
    const errors = validationResult(req);
    
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    // Tạo user...
    res.json({ message: 'User created' });
  }
);
```

### 9. SQL Injection Prevention

```javascript
// Sử dụng parameterized queries
const mysql = require('mysql2/promise');

// KHÔNG BAO GIỞ làm như thế này:
// const query = `SELECT * FROM users WHERE email = '${email}'`;

// ĐÚNG:
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE email = ?',
  [email]
);

// Với ORM (Sequelize)
const user = await User.findOne({
  where: { email: email }
});
```

### 10. HTTPS và Best Practices

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};

https.createServer(options, app).listen(443);

// Redirect HTTP to HTTPS
const http = require('http');
http.createServer((req, res) => {
  res.writeHead(301, { Location: `https://${req.headers.host}${req.url}` });
  res.end();
}).listen(80);
```

### 11. Security Checklist

☑️ Sử dụng HTTPS trong production  
☑️ Cấu hình CORS đúng  
☑️ Implement authentication & authorization  
☑️ Sử dụng Helmet cho security headers  
☑️ Rate limiting cho API  
☑️ Validate và sanitize inputs  
☑️ Sử dỡng parameterized queries  
☑️ Không expose sensitive data trong errors  
☑️ Keep dependencies updated  
☑️ Sử dụng environment variables cho secrets  
☑️ Log security events  

Bảo mật API là một quá trình liên tục, không phải một task một lần. CORS chỉ là một phần nhỏ trong hệ thống bảo mật toàn diện. Kết hợp CORS với authentication, rate limiting, input validation, và các best practices khác để xây dựng API an toàn.

Luôn cập nhật kiến thức về bảo mật, theo dõi các lỗ hổng mới, và kiểm tra bảo mật thường xuyên. An toàn là ưu tiên hàng đầu, không phải lựa chọn thứ yếu!

---

### Tài liệu tham khảo

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [JWT.io - JSON Web Tokens](https://jwt.io/)
