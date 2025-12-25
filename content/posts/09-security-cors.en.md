++
title = "Basic Security: CORS and API Policies"
date = "2025-12-16"
tags = ["Security","JavaScript","Web"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&auto=format&fit=crop"
++

When building web APIs, security is a top concern. However, many developers starting out often encounter CORS errors or overlook basic security issues, leading to applications vulnerable to attacks.

This article will explain what CORS is, why we need it, how to configure it properly, and other security best practices for web APIs.

![Security Concept](https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&auto=format&fit=crop)
*API security with CORS and authentication*

### 1. What is CORS?

**CORS (Cross-Origin Resource Sharing)** is a browser security mechanism that prevents requests from a different origin (domain) from calling your API.

**Origin** includes:
- Protocol (http/https)
- Domain (example.com)
- Port (3000, 8080)

Examples:
- `http://localhost:3000` and `http://localhost:8080` are different origins
- `http://example.com` and `https://example.com` are different origins

### 2. Why Do We Need CORS?

Without CORS, a malicious website could:
- Read sensitive data from your API
- Send requests with user credentials
- Perform unauthorized operations

### 3. Configuring CORS in Express

#### Basic - Allow All

```javascript
const express = require('express');
const cors = require('cors');

const app = express();

// Allow all origins (SHOULD NOT use in production)
app.use(cors());

app.get('/api/data', (req, res) => {
  res.json({ message: 'Data' });
});
```

#### Restrict to Specific Origins

```javascript
const corsOptions = {
  origin: 'http://localhost:3001', // Only allow this origin
  credentials: true, // Allow sending cookies
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
```

#### Multiple Origins

```javascript
const allowedOrigins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'https://myapp.com'
];

const corsOptions = {
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps, Postman)
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

#### Allow Only Specific Methods

```javascript
const corsOptions = {
  origin: 'http://localhost:3001',
  methods: ['GET', 'POST'], // Only allow GET and POST
  allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));
```

### 4. Configuring CORS in Java

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

### 5. Authentication with JWT

```javascript
const jwt = require('jsonwebtoken');
const SECRET_KEY = 'your-secret-key';

// Create token
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  
  // Verify credentials (assumed)
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

// Authentication middleware
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

// Use middleware
app.get('/api/protected', authenticateToken, (req, res) => {
  res.json({ message: 'Protected data', user: req.user });
});
```

### 6. Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

// General request limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per IP
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Login attempt limit
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

// Use all protections
app.use(helmet());

// Or customize
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
    
    // Create user...
    res.json({ message: 'User created' });
  }
);
```

### 9. SQL Injection Prevention

```javascript
// Use parameterized queries
const mysql = require('mysql2/promise');

// NEVER do this:
// const query = `SELECT * FROM users WHERE email = '${email}'`;

// CORRECT:
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE email = ?',
  [email]
);

// With ORM (Sequelize)
const user = await User.findOne({
  where: { email: email }
});
```

### 10. HTTPS and Best Practices

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

☑️ Use HTTPS in production  
☑️ Configure CORS properly  
☑️ Implement authentication & authorization  
☑️ Use Helmet for security headers  
☑️ Rate limiting for APIs  
☑️ Validate and sanitize inputs  
☑️ Use parameterized queries  
☑️ Don't expose sensitive data in errors  
☑️ Keep dependencies updated  
☑️ Use environment variables for secrets  
☑️ Log security events  

API security is an ongoing process, not a one-time task. CORS is just a small part of a comprehensive security system. Combine CORS with authentication, rate limiting, input validation, and other best practices to build secure APIs.

Always update your security knowledge, follow new vulnerabilities, and regularly check security. Security is a top priority, not a secondary choice!

---

### References

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [JWT.io - JSON Web Tokens](https://jwt.io/)
