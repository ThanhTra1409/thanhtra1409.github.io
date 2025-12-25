++
title = "Xử lý REST API với Express (Node.js)"
date = "2025-12-14"
tags = ["JavaScript","Express","REST"]
draft = false
thumbnail = "https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800&auto=format&fit=crop"
++

Express.js là framework web phổ biến nhất cho Node.js, cung cấp các công cụ đơn giản nhưng mạnh mẽ để xây dựng web server và REST API. Với cú pháp ngắn gọn và hệ sinh thái middleware phong phú, Express giúp developer tạo API nhanh chóng và hiệu quả.

Bài viết này sẽ hướng dẫn xây dựng REST API hoàn chỉnh với Express, bao gồm routing, middleware, error handling, và các best practices.

![REST API Development](https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=1200&auto=format&fit=crop)
*Xây dựng REST API với Express.js*

### 1. Cài đặt và Setup cơ bản

```bash
npm init -y
npm install express
```

#### Server cơ bản

```javascript
const express = require('express');
const app = express();

// Middleware để parse JSON
app.use(express.json());

// Middleware để parse URL-encoded data
app.use(express.urlencoded({ extended: true }));

// Basic route
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to API' });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

### 2. CRUD REST API

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// In-memory database
let users = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
];

let nextId = 3;

// GET all users
app.get('/api/users', (req, res) => {
  res.json(users);
});

// GET user by ID
app.get('/api/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.find(u => u.id === id);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json(user);
});

// POST create new user
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  
  const newUser = {
    id: nextId++,
    name,
    email
  };
  
  users.push(newUser);
  res.status(201).json(newUser);
});

// PUT update user
app.put('/api/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { name, email } = req.body;
  
  const userIndex = users.findIndex(u => u.id === id);
  
  if (userIndex === -1) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  users[userIndex] = { id, name, email };
  res.json(users[userIndex]);
});

// PATCH partial update
app.patch('/api/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const user = users.find(u => u.id === id);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  Object.assign(user, req.body);
  res.json(user);
});

// DELETE user
app.delete('/api/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const userIndex = users.findIndex(u => u.id === id);
  
  if (userIndex === -1) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  users.splice(userIndex, 1);
  res.status(204).send();
});

app.listen(3000, () => {
  console.log('API server running on port 3000');
});
```

### 3. Middleware

```javascript
// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  next();
});

// Authentication middleware
function authenticate(req, res, next) {
  const token = req.headers['authorization'];
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  // Verify token (giả sử)
  if (token === 'Bearer valid-token') {
    req.userId = 1; // Set user info
    next();
  } else {
    res.status(403).json({ error: 'Invalid token' });
  }
}

// Sử dụng middleware cho specific routes
app.get('/api/protected', authenticate, (req, res) => {
  res.json({ message: 'This is protected', userId: req.userId });
});

// Validation middleware
function validateUser(req, res, next) {
  const { name, email } = req.body;
  
  if (!name || name.length < 3) {
    return res.status(400).json({ error: 'Name must be at least 3 characters' });
  }
  
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Valid email is required' });
  }
  
  next();
}

app.post('/api/users', validateUser, (req, res) => {
  // Tạo user...
});
```

### 4. Router và Cấu trúc dự án

#### routes/users.js
```javascript
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json({ message: 'Get all users' });
});

router.get('/:id', (req, res) => {
  res.json({ message: `Get user ${req.params.id}` });
});

router.post('/', (req, res) => {
  res.json({ message: 'Create user' });
});

router.put('/:id', (req, res) => {
  res.json({ message: `Update user ${req.params.id}` });
});

router.delete('/:id', (req, res) => {
  res.json({ message: `Delete user ${req.params.id}` });
});

module.exports = router;
```

#### routes/posts.js
```javascript
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json({ message: 'Get all posts' });
});

router.post('/', (req, res) => {
  res.json({ message: 'Create post' });
});

module.exports = router;
```

#### app.js
```javascript
const express = require('express');
const userRoutes = require('./routes/users');
const postRoutes = require('./routes/posts');

const app = express();

app.use(express.json());

// Mount routers
app.use('/api/users', userRoutes);
app.use('/api/posts', postRoutes);

app.listen(3000, () => {
  console.log('Server running');
});
```

### 5. Error Handling

```javascript
// Custom error class
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

// Async error handler wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Route với error handling
app.get('/api/users/:id', asyncHandler(async (req, res, next) => {
  const user = await getUserById(req.params.id);
  
  if (!user) {
    throw new AppError('User not found', 404);
  }
  
  res.json(user);
}));

// 404 handler
app.use((req, res, next) => {
  res.status(404).json({ error: 'Route not found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  
  const statusCode = err.statusCode || 500;
  const message = err.isOperational ? err.message : 'Internal server error';
  
  res.status(statusCode).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});
```

### 6. Query Parameters và Pagination

```javascript
app.get('/api/users', (req, res) => {
  // Query parameters: /api/users?page=1&limit=10&sort=name
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const sort = req.query.sort || 'id';
  
  const startIndex = (page - 1) * limit;
  const endIndex = page * limit;
  
  let result = [...users];
  
  // Sorting
  result.sort((a, b) => a[sort] > b[sort] ? 1 : -1);
  
  // Pagination
  const paginatedUsers = result.slice(startIndex, endIndex);
  
  res.json({
    data: paginatedUsers,
    page: page,
    limit: limit,
    total: users.length,
    totalPages: Math.ceil(users.length / limit)
  });
});
```

### 7. CORS và Security

```javascript
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// CORS
app.use(cors({
  origin: 'http://localhost:3001',
  credentials: true
}));

// Security headers
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

Express.js là framework mạnh mẽ và linh hoạt để xây dựng REST API. Với các khái niệm cơ bản như routing, middleware, error handling, bạn có thể tạo API chuyên nghiệp và scalable.

Các best practices bao gồm: sử dụng Router để tổ chức code, implement error handling đầy đủ, validation dữ liệu, và bảo mật API với CORS, helmet, và rate limiting.

---

### Tài liệu tham khảo

- [Express.js Official Documentation](https://expressjs.com/)
- [Express.js API Reference](https://expressjs.com/en/4x/api.html)
- [REST API Design Best Practices](https://www.freecodecamp.org/news/rest-api-best-practices-rest-endpoint-design-examples/)
- [Building RESTful APIs with Express](https://www.toptal.com/nodejs/secure-rest-api-in-nodejs)
