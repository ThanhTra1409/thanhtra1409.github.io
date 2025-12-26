// Internationalization (i18n) Configuration
// Version: 1.1 - Updated language persistence
const translations = {
  vi: {
    // Header & Navigation
    'home': 'Trang chủ',
    'blog': 'Blog',
    'about': 'Giới thiệu',
    
    // Hero Section
    'site-title': 'Blog Lập Trình Mạng',
    'tagline': 'Chia sẻ kiến thức lập trình mạng — Java & JavaScript',
    'view-posts': 'Xem bài viết',
    'about-me': 'Về tôi',
    'hero-greeting': 'Xin chào, tôi là',
    
    // Hero Content
    'hero-name': 'Nguyễn Thanh Trà',
    'hero-role': 'Software Engineer | Backend Developer',
    'hero-intro-main': 'Tôi là sinh viên năm 4 yêu thích công nghệ phần mềm, hiện đang tìm hiểu các kiến thức cơ bản về lập trình và phát triển phần mềm. Có tinh thần học hỏi, chủ động rèn luyện tư duy logic và kỹ năng chuyên môn để phục vụ học tập và công việc trong tương lai.',
    'hero-intro-text': 'Tôi yêu thích công nghệ phần mềm, hiện đang tìm hiểu các kiến thức cơ bản về lập trình và phát triển phần mềm. Có tinh thần học hỏi, chủ động rèn luyện tư duy logic và kỹ năng chuyên môn để phục vụ học tập và công việc trong tương lai.',
    'backend-systems': 'Backend Systems',
    'network-programming': 'Network Programming',
    'database-design': 'Database Design',
    'api-development': 'API Development',
    'software-engineering': 'Công nghệ Phần mềm',
    
    // Latest Posts
    'latest-posts': 'Bài mới nhất',
    
    // Blog Page
    'blog-title': 'Blog',
    'blog-intro': 'Chia sẻ kiến thức và kinh nghiệm trong lập trình mạng với Java và JavaScript',
    
    // About Page
    'about-title': 'Thông Tin Cá Nhân',
    'personal-info': 'Thông tin cá nhân',
    'fullname-label': 'Họ và tên',
    'email-label': 'Email',
    'location-label': 'Địa chỉ',
    'location': 'TP. Hồ Chí Minh',
    'slogan': 'Công nghệ luôn thay đổi, tôi chọn cách học hỏi mỗi ngày để không bị bỏ lại phía sau.',
    'education': 'Học vấn',
    'university': 'Đại học Công nghệ TP.HCM (HUTECH)',
    'major-label': 'Ngành',
    'knowledge-title': 'Kiến thức chuyên môn',
    'knowledge-1': 'Lập trình hướng đối tượng (OOP)',
    'knowledge-2': 'Cấu trúc dữ liệu & Giải thuật',
    'knowledge-3': 'Lập trình mạng & Distributed Systems',
    'knowledge-4': 'Database Design & Management',
    'knowledge-5': 'Software Engineering & Design Patterns',
    'programming-skills': 'Kỹ năng lập trình',
    'backend-dev': 'Backend Development',
    'frontend-dev': 'Frontend Development',
    'responsive-design': 'Responsive Web Design',
    'tools-tech': 'Tools & Technologies',
    'projects-portfolio': 'Dự án & Portfolio',
    'blog-proof-text': 'Các bài viết trong phần',
    'blog-intro-text': 'Các bài viết trong blog là các kiến thức mà tôi đã được học',
    'project-1': 'Xây dựng TCP/UDP Server với Java',
    'project-2': 'Phát triển RESTful API với Node.js & Express',
    'project-3': 'Triển khai WebSocket real-time communication',
    'project-4': 'Security & CORS handling',
    'career-goals': 'Mục tiêu nghề nghiệp',
    'career-goal-text': 'Tìm kiếm vị trí',
    'career-position': 'Backend Developer Intern/Fresher',
    'career-or': 'hoặc',
    'career-position2': 'Junior Software Engineer',
    'career-at': 'tại các công ty công nghệ, nơi tôi có thể',
    'career-goal-1': 'Áp dụng kiến thức về Java & JavaScript vào dự án thực tế',
    'career-goal-2': 'Học hỏi từ đội ngũ senior developers',
    'career-goal-3': 'Đóng góp vào các hệ thống lớn, phức tạp',
    'career-goal-4': 'Phát triển kỹ năng system design & scalability',
    'contact': 'Liên hệ',
    'availability': 'Sẵn sàng làm việc full-time',
    
    // Post Titles
    'post-01': 'Socket cơ bản trong Java',
    'post-02': 'Multithreading và ServerSocket trong Java',
    'post-03': 'Java NIO — lập trình mạng hiệu năng cao',
    'post-04': 'Xây dựng HTTP client và server cơ bản bằng Java',
    'post-05': 'Fetch API và WebSocket trên trình duyệt',
    'post-06': 'Node.js: TCP server với module `net`',
    'post-07': 'WebSocket server với Socket.IO',
    'post-08': 'Xử lý REST API với Express (Node.js)',
    'post-09': 'Bảo mật cơ bản: CORS và chính sách cho API',
    
    // Post Excerpts
    'excerpt-01': 'Lập trình mạng là một phần quan trọng trong phát triển ứng dụng hiện đại. Socket là nền tảng cơ bản nhất để thiết lập kết nối mạng giữa các máy tính....',
    'excerpt-02': 'Trong bài trước, chúng ta đã tìm hiểu về Socket cơ bản trong Java. Tuy nhiên, một server đơn giản chỉ xử lý một client tại một thời điểm là chưa đủ ch...',
    'excerpt-03': 'Trong các bài trước, chúng ta đã tìm hiểu về Socket cơ bản và multithreading server. Tuy nhiên, với mô hình thread-per-connection, khi số lượng kết nố...',
    'excerpt-04': 'HTTP là giao thức nền tảng của web, được sử dụng để truyền tải dữ liệu giữa client và server. Trong Java, chúng ta có thể dễ dàng tạo HTTP client để g...',
    'excerpt-05': 'Trong phát triển web hiện đại, việc giao tiếp giữa client và server là thiết yếu. JavaScript cung cấp hai công cụ chính: Fetch API cho các yêu cầu HTT...',
    'excerpt-06': 'Node.js với kiến trúc event-driven và non-blocking I/O là nền tảng tuyệt vời để xây dựng server mạng hiệu năng cao. Module `net` được tích hợp sẵn tro...',
    'excerpt-07': 'WebSocket là công nghệ tuyệt vời cho giao tiếp realtime, nhưng việc implement từ đầu có thể phức tạp. Socket.IO là thư viện giúp đơn giản hóa quá trìn...',
    'excerpt-08': 'Express.js là framework web phổ biến nhất cho Node.js, cung cấp các công cụ đơn giản nhưng mạnh mẽ để xây dựng web server và REST API. Với cú pháp ngắ...',
    'excerpt-09': 'Khi xây dựng web API, bảo mật là mối quan tâm hàng đầu. Tuy nhiên, nhiều developer mới bắt đầu thường gặp phải lỗi CORS hoặc bỏ qua các vấn đề bảo mật...',
    
    // Certificates
    'certificates': 'Chứng chỉ và thành tựu',
    'achievements-title': 'Chứng Chỉ & Thành Tựu',
    'cert-1-title': 'Networking Basics',
    'cert-1-issuer': 'Nguyễn Thanh Trà',
    'cert-1-date': 'Nov 2025',
    'cert-2-title': 'JavaScript Essentials 1',
    'cert-2-issuer': 'Nguyễn Thanh Trà',
    'cert-2-date': 'Dec 2025',
    'cert-3-title': 'JavaScript Essentials 2',
    'cert-3-issuer': 'Nguyễn Thanh Trà',
    'cert-3-date': 'Dec 2025',
    
    // Profile Page
    'profile-intro': 'Sinh viên năm 4 ngành',
    'major': 'Công nghệ Phần mềm',
    'university-label': 'Trường',
    'university': 'Đại học Công nghệ TP.HCM (HUTECH)',
    'learned': 'Đã được học tập về',
    'tech-1': 'Java Backend Development',
    'tech-2': 'Network Programming',
    
    'main-skills': 'Kỹ năng chính:',
    'skill-1': 'Lập trình',
    'skill-1-detail': '(Socket, Multithreading, NIO, HTTP Server)',
    'skill-2': 'Phát triển',
    'skill-2-detail': 'với JavaScript, Node.js, Express.js',
    'skill-3': 'Xây dựng',
    'skill-3-detail': 'và',
    'skill-3-detail2': 'real-time',
    'skill-4': 'Quản lý',
    'skill-4-detail': '(SQL, NoSQL) và',
    'skill-4-detail2': '(Git)',
    
    'career-goals': 'Mục tiêu nghề nghiệp:',
    'goal-1-pre': 'Tìm kiếm cơ hội',
    'goal-1': 'Intern/Fresher Backend Developer',
    'goal-1-post': 'hoặc',
    'goal-2': 'Junior Software Engineer',
    'goal-3-pre': 'Mong muốn đóng góp vào các dự án',
    'goal-3': 'enterprise',
    'goal-3-post': 'và phát triển kỹ năng',
    'goal-4': 'system design',
    'goal-5': 'Sẵn sàng làm việc full-time',
    'goal-5-post': 'và cam kết',
    'goal-6': 'học hỏi không ngừng',
    
    // Footer
    'footer-copyright': '© 2025',
    'footer-tagline': 'Xây dựng giải pháp mở rộng với đam mê',
    'contact-info': 'Thông tin liên hệ',
    'rights': 'Bảo lưu mọi quyền.',
    'social-title': 'Mạng xã hội',
    'phone-label': 'SĐT',
    
    // Post sections
    'api-restful': 'API RESTful',
    'websocket': 'WebSocket',
    'web': 'Web',
    'database': 'Database',
    'version-control': 'Version Control',
    'java': 'Java'
  },
  en: {
    // Header & Navigation
    'home': 'Home',
    'blog': 'Blog',
    'about': 'About',
    
    // Hero Section
    'site-title': 'Network Programming Blog',
    'tagline': 'Sharing network programming knowledge — Java & JavaScript',
    'view-posts': 'View Posts',
    'about-me': 'About Me',
    'hero-greeting': 'Hello, I am',
    
    // Hero Content
    'hero-name': 'Nguyen Thanh Tra',
    'hero-role': 'Software Engineer | Backend Developer',
    'hero-intro-main': 'I am a final year student passionate about software technology and currently learning the fundamentals of programming and software development. I have a strong learning spirit, actively training logical thinking and professional skills to serve my studies and future career.',
    'hero-intro-text': 'I am passionate about software technology and currently learning the fundamentals of programming and software development. I have a strong learning spirit, actively training logical thinking and professional skills to serve my studies and future career.',
    'backend-systems': 'Backend Systems',
    'network-programming': 'Network Programming',
    'database-design': 'Database Design',
    'api-development': 'API Development',
    'software-engineering': 'Software Engineering',
    
    // Latest Posts
    'latest-posts': 'Latest Posts',
    
    // Blog Page
    'blog-title': 'Blog',
    'blog-intro': 'Sharing knowledge and experience in network programming with Java and JavaScript',
    
    // About Page
    'about-title': 'Personal Information',
    'personal-info': 'Personal Information',
    'fullname-label': 'Full Name',
    'email-label': 'Email',
    'location-label': 'Location',
    'location': 'Ho Chi Minh City',
    'slogan': 'Technology is always changing, I choose to learn every day to not be left behind.',
    'education': 'Education',
    'university': 'Ho Chi Minh City University of Technology (HUTECH)',
    'major-label': 'Major',
    'knowledge-title': 'Professional Knowledge',
    'knowledge-1': 'Object-Oriented Programming (OOP)',
    'knowledge-2': 'Data Structures & Algorithms',
    'knowledge-3': 'Network Programming & Distributed Systems',
    'knowledge-4': 'Database Design & Management',
    'knowledge-5': 'Software Engineering & Design Patterns',
    'programming-skills': 'Programming Skills',
    'backend-dev': 'Backend Development',
    'frontend-dev': 'Frontend Development',
    'responsive-design': 'Responsive Web Design',
    'tools-tech': 'Tools & Technologies',
    'projects-portfolio': 'Projects & Portfolio',
    'blog-proof-text': 'Articles in the',
    'blog-proof-text2': 'section demonstrate my knowledge and practical skills in',
    'project-1': 'Building TCP/UDP Server with Java',
    'project-2': 'Developing RESTful API with Node.js & Express',
    'project-3': 'Implementing WebSocket real-time communication',
    'project-4': 'Security & CORS handling',
    'career-goals': 'Career Goals',
    'career-goal-text': 'Looking for',
    'career-position': 'Backend Developer Intern/Fresher',
    'career-or': 'or',
    'career-position2': 'Junior Software Engineer',
    'career-at': 'position at tech companies where I can',
    'career-goal-1': 'Apply Java & JavaScript knowledge to real projects',
    'career-goal-2': 'Learn from senior developers',
    'career-goal-3': 'Contribute to large, complex systems',
    'career-goal-4': 'Develop system design & scalability skills',
    'contact': 'Contact',
    'availability': 'Available for full-time work',
    
    // Post Titles
    'post-01': 'Basic Socket in Java',
    'post-02': 'Multithreading and ServerSocket in Java',
    'post-03': 'Java NIO — High Performance Network Programming',
    'post-04': 'Building Basic HTTP Client and Server with Java',
    'post-05': 'Fetch API and WebSocket in Browser',
    'post-06': 'Node.js: TCP Server with `net` Module',
    'post-07': 'WebSocket Server with Socket.IO',
    'post-08': 'Handling REST API with Express (Node.js)',
    'post-09': 'Basic Security: CORS and API Policies',
    
    // Post Excerpts
    'excerpt-01': 'Network programming is an essential part of modern application development. Socket is the most fundamental foundation for establishing network connections between computers....',
    'excerpt-02': 'In the previous article, we learned about basic Socket in Java. However, a simple server that handles only one client at a time is not sufficient...',
    'excerpt-03': 'In previous articles, we learned about basic Socket and multithreading server. However, with the thread-per-connection model, when the number of connections...',
    'excerpt-04': 'HTTP is the foundational protocol of the web, used to transfer data between client and server. In Java, we can easily create HTTP clients to make requests...',
    'excerpt-05': 'In modern web development, communication between client and server is essential. JavaScript provides two main tools: Fetch API for HTTP requests...',
    'excerpt-06': 'Node.js with its event-driven architecture and non-blocking I/O is an excellent foundation for building high-performance network servers. The `net` module comes built-in...',
    'excerpt-07': 'WebSocket is great technology for realtime communication, but implementing it from scratch can be complex. Socket.IO is a library that simplifies the process...',
    'excerpt-08': 'Express.js is the most popular web framework for Node.js, providing simple yet powerful tools for building web servers and REST APIs. With concise syntax...',
    'excerpt-09': 'When building web APIs, security is a top concern. However, many beginner developers often encounter CORS errors or overlook security issues...',
    
    // Certificates
    'certificates': 'Certificates and Achievements',
    'achievements-title': 'Certificates & Achievements',
    'cert-1-title': 'Networking Basics',
    'cert-1-issuer': 'Nguyen Thanh Tra',
    'cert-1-date': 'Nov 2025',
    'cert-2-title': 'JavaScript Essentials 1',
    'cert-2-issuer': 'Nguyen Thanh Tra',
    'cert-2-date': 'Dec 2025',
    'cert-3-title': 'JavaScript Essentials 2',
    'cert-3-issuer': 'Nguyen Thanh Tra',
    'cert-3-date': 'Dec 2025',
    
    // Profile Page
    'profile-intro': 'Final year student majoring in',
    'major': 'Software Engineering',
    'university-label': 'University:',
    'university': 'Ho Chi Minh City University of Technology (HUTECH)',
    'learned': 'Learned about',
    'tech-1': 'Java Backend Development',
    'tech-2': 'Network Programming',
    
    'main-skills': 'Main Skills:',
    'skill-1': 'Programming',
    'skill-1-detail': '(Socket, Multithreading, NIO, HTTP Server)',
    'skill-2': 'Developing',
    'skill-2-detail': 'with JavaScript, Node.js, Express.js',
    'skill-3': 'Building',
    'skill-3-detail': 'and',
    'skill-3-detail2': 'real-time',
    'skill-4': 'Managing',
    'skill-4-detail': '(SQL, NoSQL) and',
    'skill-4-detail2': '(Git)',
    
    'career-goals': 'Career Goals:',
    'goal-1-pre': 'Looking for',
    'goal-1': 'Intern/Fresher Backend Developer',
    'goal-1-post': 'or',
    'goal-2': 'Junior Software Engineer',
    'goal-3-pre': 'Want to contribute to',
    'goal-3': 'enterprise',
    'goal-3-post': 'projects and develop',
    'goal-4': 'system design',
    'goal-5': 'Ready to work full-time',
    'goal-5-post': 'and committed to',
    'goal-6': 'continuous learning',
    
    // Footer
    'footer-copyright': '© 2025',
    'footer-tagline': 'Building scalable solutions with passion',
    'contact-info': 'Contact Information',
    'rights': 'All rights reserved.',
    'social-title': 'Social Network',
    'phone-label': 'Phone',
    
    // Post sections
    'api-restful': 'RESTful API',
    'websocket': 'WebSocket',
    'web': 'Web',
    'database': 'Database',
    'version-control': 'Version Control',
    'java': 'Java'
  }
};

// Language toggle functionality
let currentLang = localStorage.getItem('language') || 'vi';

// Detect language from URL or body attribute on page load
function detectLanguageFromPage() {
  const currentPath = window.location.pathname;
  const bodyLang = document.body.getAttribute('data-lang');
  
  // If URL contains .en.html, set language to English
  if (currentPath.includes('.en.html') || bodyLang === 'en') {
    return 'en';
  }
  
  // Otherwise, check localStorage or default to Vietnamese
  return localStorage.getItem('language') || 'vi';
}

// Initialize current language based on page
currentLang = detectLanguageFromPage();

function toggleLanguage() {
  currentLang = currentLang === 'vi' ? 'en' : 'vi';
  localStorage.setItem('language', currentLang);
  updateContent();
  updateLangButton();
}

function updateContent(shouldRedirect = false) {
  // Add transitioning class for fade effect
  document.body.classList.add('lang-transitioning');
  
  setTimeout(() => {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(element => {
      const key = element.getAttribute('data-i18n');
      if (translations[currentLang][key]) {
        element.textContent = translations[currentLang][key];
      }
    });
    
    // Update HTML lang attribute
    document.documentElement.lang = currentLang;
    
    // Update body data-lang attribute
    document.body.setAttribute('data-lang', currentLang);
    
    // Handle URL change for blog posts - only when user switches language
    if (shouldRedirect) {
      const currentPath = window.location.pathname;
      if (currentPath.includes('/posts/')) {
        // Check if we're on a blog post or blog index page
        if (currentPath.endsWith('.html') && currentPath !== '/posts/index.html' && currentPath !== '/posts/index.en.html') {
          // Individual post page
          if (currentLang === 'en' && !currentPath.includes('.en.html')) {
            // Switch to English version
            const newPath = currentPath.replace('.html', '.en.html');
            window.location.href = newPath;
            return;
          } else if (currentLang === 'vi' && currentPath.includes('.en.html')) {
            // Switch to Vietnamese version
            const newPath = currentPath.replace('.en.html', '.html');
            window.location.href = newPath;
            return;
          }
        } else if (currentPath.endsWith('/posts/') || currentPath === '/posts' || currentPath.endsWith('/posts/index.html') || currentPath.endsWith('/posts/index.en.html')) {
          // Blog index page
          if (currentLang === 'en' && !currentPath.includes('index.en.html')) {
            window.location.href = '/posts/index.en.html';
            return;
          } else if (currentLang === 'vi' && currentPath.includes('index.en.html')) {
            window.location.href = '/posts/';
            return;
          }
        }
      }
      
      // Handle about page - just update content without redirect since there's only one about page
      if (currentPath.includes('/about')) {
        // About page uses i18n to switch languages, no redirect needed
        // Just let the updateContent function handle the translation
      }
    }
    
    // Remove transitioning class
    setTimeout(() => {
      document.body.classList.remove('lang-transitioning');
    }, 50);
  }, 100);
}

function updateLangButton() {
  const langSwitch = document.getElementById('lang-switch');
  
  if (langSwitch) {
    langSwitch.setAttribute('data-lang', currentLang);
    
    // Add ripple effect
    langSwitch.classList.add('ripple');
    setTimeout(() => {
      langSwitch.classList.remove('ripple');
    }, 600);
  }
}

function switchToLanguage(lang) {
  if (currentLang !== lang) {
    currentLang = lang;
    localStorage.setItem('language', currentLang);
    updateContent(true); // Pass true to enable redirect
    updateLangButton();
  }
}

function toggleLanguage() {
  switchToLanguage(currentLang === 'vi' ? 'en' : 'vi');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  updateContent(false); // Pass false to prevent redirect on initial load
  updateLangButton();
  
  // Add event listeners to language switch with drag support
  const langSwitch = document.getElementById('lang-switch');
  const slider = langSwitch?.querySelector('.lang-switch-slider');
  
  if (langSwitch && slider) {
    let isDragging = false;
    let startX = 0;
    let currentX = 0;
    
    // Mouse/Touch events for dragging
    const handleStart = (e) => {
      isDragging = true;
      startX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
      langSwitch.classList.add('dragging');
    };
    
    const handleMove = (e) => {
      if (!isDragging) return;
      currentX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
      const diff = currentX - startX;
      
      // Trigger language change based on drag direction
      if (Math.abs(diff) > 20) {
        if (diff > 0 && currentLang === 'vi') {
          switchToLanguage('en');
          isDragging = false;
        } else if (diff < 0 && currentLang === 'en') {
          switchToLanguage('vi');
          isDragging = false;
        }
      }
    };
    
    const handleEnd = () => {
      if (isDragging) {
        langSwitch.classList.remove('dragging');
        isDragging = false;
      }
    };
    
    // Click to toggle
    langSwitch.addEventListener('click', (e) => {
      if (!isDragging) {
        toggleLanguage();
      }
    });
    
    // Drag events
    slider.addEventListener('mousedown', handleStart);
    slider.addEventListener('touchstart', handleStart, { passive: true });
    
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('touchmove', handleMove, { passive: true });
    
    document.addEventListener('mouseup', handleEnd);
    document.addEventListener('touchend', handleEnd);
  }
});
