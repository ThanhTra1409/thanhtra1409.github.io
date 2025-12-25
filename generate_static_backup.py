# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime

ROOT = os.path.dirname(__file__)
CONTENT = os.path.join(ROOT, 'content')
STATIC = os.path.join(ROOT, 'static')
PUBLIC = os.path.join(ROOT, 'public')

def read_front_matter_and_body(path):
  text = open(path, encoding='utf-8').read()
  # Match front matter delimited by ++ or +++ (Hugo uses +++ but some files used ++)
  m = re.match(r"\+{2,3}[\s\S]*?\+{2,3}[ \t\r\n]*", text)
  fm = {}
  body = text
  if m:
    fm_text = m.group(0)
    body = text[m.end():].strip()
    for line in fm_text.splitlines():
      line = line.strip()
      if line.startswith('title'):
        fm['title'] = line.split('=',1)[1].strip().strip('"')
      if line.startswith('date'):
        fm['date'] = line.split('=',1)[1].strip().strip('"')
      if line.startswith('thumbnail'):
        fm['thumbnail'] = line.split('=',1)[1].strip().strip('"')
      if line.startswith('summary'):
        fm['summary'] = line.split('=',1)[1].strip().strip('"')
  return fm, body

def to_html_paragraphs(md):
    # Very small markdown -> HTML converter: paragraphs and inline `code`
    parts = re.split(r"\n\s*\n", md.strip())
    html = []
    for p in parts:
        p = p.strip()
        # Bold markdown
        p = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)
        # Italic markdown
        p = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', p)
        # Inline code
        p = re.sub(r'`([^`]+)`', r'<code>\1</code>', p)
        p = p.replace('\n', '<br/>')
        html.append(f'<p>{p}</p>')
    return '\n'.join(html)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_social_section_html():
    return '''<section class="social-section">
      <div class="social-container">
        <h2 data-i18n="social-title">X&#227; h&#7897;i</h2>
        <div class="social-grid">
          <a href="https://github.com/nttra204" target="_blank" class="social-card">
            <i class="fab fa-github social-icon"></i>
            <h3>GitHub</h3>
            <p>@nttra204</p>
          </a>
          <a href="https://www.facebook.com/nguyen.thanh.tra.970568?locale=vi_VN" target="_blank" class="social-card">
            <i class="fab fa-facebook social-icon"></i>
            <h3>Facebook</h3>
            <p>Nguy&#7877;n Thanh Tr&#224;</p>
          </a>
          <a href="https://www.instagram.com/nttra204_/?igsh=MXVlc3p1NG4zdnBidw%3D%3D&utm_source=qr" target="_blank" class="social-card">
            <i class="fab fa-instagram social-icon"></i>
            <h3>Instagram</h3>
            <p>@nttra204_</p>
          </a>
          <a href="https://www.linkedin.com/in/nttra204" target="_blank" class="social-card">
            <i class="fab fa-linkedin social-icon"></i>
            <h3>LinkedIn</h3>
            <p>Nguy&#7877;n Thanh Tr&#224;</p>
          </a>
        </div>
      </div>
    </section>'''

def get_footer_html(site_title):
    return f'''<footer>
    <div class="footer-content">
      <div class="footer-brand">
        <h3 data-i18n="site-title">{site_title}</h3>
        <p class="footer-tagline" data-i18n="footer-tagline">Building scalable solutions with passion</p>
      </div>
      <div class="footer-contact">
        <h4 data-i18n="contact-info">Th&#244;ng tin li&#234;n h&#7879;</h4>
        <div class="contact-info-grid">
          <div class="contact-info-item">
            <i class="fas fa-envelope"></i>
            <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
          </div>
          <div class="contact-info-item">
            <i class="fas fa-phone"></i>
            <a href="tel:0941779093">0941779093</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p><span data-i18n="footer-copyright">© {datetime.now().year}</span> <span data-i18n="site-title">{site_title}</span>. <span data-i18n="rights">All rights reserved.</span></p>
      </div>
    </div>
  </footer>'''

def copy_static():
    # copy css
    src_css = os.path.join(STATIC, 'css', 'style.css')
    dst_css_dir = os.path.join(PUBLIC, 'css')
    ensure_dir(dst_css_dir)
    if os.path.exists(src_css):
        with open(src_css, 'rb') as fr, open(os.path.join(dst_css_dir, 'style.css'), 'wb') as fw:
            fw.write(fr.read())
    
    # copy js
    src_js = os.path.join(STATIC, 'js')
    dst_js_dir = os.path.join(PUBLIC, 'js')
    if os.path.exists(src_js):
        ensure_dir(dst_js_dir)
        for filename in os.listdir(src_js):
            src_file = os.path.join(src_js, filename)
            dst_file = os.path.join(dst_js_dir, filename)
            if os.path.isfile(src_file):
                with open(src_file, 'rb') as fr, open(dst_file, 'wb') as fw:
                    fw.write(fr.read())
    
    # copy images
    src_images = os.path.join(STATIC, 'images')
    dst_images = os.path.join(PUBLIC, 'images')
    if os.path.exists(src_images):
        ensure_dir(dst_images)
        for filename in os.listdir(src_images):
            src_file = os.path.join(src_images, filename)
            dst_file = os.path.join(dst_images, filename)
            if os.path.isfile(src_file):
                with open(src_file, 'rb') as fr, open(dst_file, 'wb') as fw:
                    fw.write(fr.read())

def build():
    ensure_dir(PUBLIC)
    copy_static()

    # read config title
    site_title = 'Blog Lập Trình Mạng'
    tagline = ''
    cfg = os.path.join(ROOT, 'config.toml')
    if os.path.exists(cfg):
        for line in open(cfg, encoding='utf-8'):
            if line.strip().startswith('title'):
                site_title = line.split('=',1)[1].strip().strip('"')
            if 'tagline' in line:
                tagline = line.split('=',1)[1].strip().strip('"')

    # Home
    home_fm, home_body = read_front_matter_and_body(os.path.join(CONTENT, '_index.md'))
    home_html = f'''<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script>
    function toggleMenu(){{
      document.body.classList.toggle('menu-open');
    }}
    </script>
</head>
<body>
  <div class="overlay" id="overlay">
    <ul class="menu">
      <li><a href="/" data-i18n="home">Home</a></li>
      <li><a href="/posts/" data-i18n="blog">Blog</a></li>
      <li><a href="/about/" data-i18n="about">About</a></li>
    </ul>
  </div>
  <header>
    <nav>
      <div class="brand"><a href="/" data-i18n="site-title">{site_title}</a></div>
      <ul>
        <li><a href="/" data-i18n="home">Home</a></li>
        <li><a href="/posts/" data-i18n="blog">Blog</a></li>
        <li><a href="/about/" data-i18n="about">About</a></li>
        <li class="lang-toggle-wrapper">
          <div id="lang-switch" class="lang-switch" data-lang="vi">
            <div class="lang-switch-slider"></div>
            <button id="lang-vn" class="lang-btn">VN</button>
            <button id="lang-en" class="lang-btn">EN</button>
          </div>
        </li>
      </ul>
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">☰</div>
    </nav>
  </header>
  <main>
    <section class="hero">
      <div class="hero-content">
        <p class="hero-greeting" data-i18n="hero-greeting">Xin chào, mình là</p>
        <h1 data-i18n="hero-name">Nguyễn Thanh Trà</h1>
        <div class="hero-intro">
          <p><strong data-i18n="hero-role">Software Engineer | Backend Developer</strong></p>
          <p><strong data-i18n="software-engineering">Công nghệ Phần mềm</strong> <span data-i18n="hero-intro-1">là lĩnh vực ứng dụng kiến thức khoa học máy tính để thiết kế, phát triển và duy trì các hệ thống phần mềm chất lượng cao.</span></p>
          <p><span data-i18n="hero-intro-2-pre">Từ</span> <strong data-i18n="backend-systems">Backend Systems</strong> <span data-i18n="hero-intro-2-post">đến</span> <strong data-i18n="network-programming">Network Programming</strong>, <span data-i18n="hero-intro-2-post">từ</span> <strong data-i18n="database-design">Database Design</strong> <span data-i18n="hero-intro-2-post">đến</span> <strong data-i18n="api-development">API Development</strong> <span data-i18n="hero-intro-2-end">— mỗi dự án là một thử thách giải quyết vấn đề thực tế bằng công nghệ.</span></p>
          <p><span data-i18n="hero-intro-3-pre">Chuyên về</span> <strong>Java</strong> <span data-i18n="hero-intro-3-mid">và</span> <strong>JavaScript</strong><span data-i18n="hero-intro-3-post">, tôi tập trung xây dựng các giải pháp backend hiệu quả, scalable và bảo mật.</span></p>
        </div>
        <div class="cta">
          <a class="btn primary" href="/posts/" data-i18n="view-posts">Xem portfolio</a>
          <a class="btn ghost" href="/about/" data-i18n="about-me">Liên hệ</a>
        </div>
      </div>
      <div class="hero-image-wrapper">
        <img src="/images/profile-photo.jpg" alt="Nguyễn Thanh Trà" class="hero-avatar">
      </div>
    </section>
    <section class="intro">
      {home_body}
    </section>
    <section class="social-section">
      <div class="social-container">
        <h2 data-i18n="social-title">Xã hội</h2>
        <div class="social-grid">
          <a href="https://github.com/nttra204" target="_blank" class="social-card">
            <i class="fab fa-github social-icon"></i>
            <h3>GitHub</h3>
            <p>@nttra204</p>
          </a>
          <a href="https://www.facebook.com/nguyen.thanh.tra.970568?locale=vi_VN" target="_blank" class="social-card">
            <i class="fab fa-facebook social-icon"></i>
            <h3>Facebook</h3>
            <p>Nguyễn Thanh Trà</p>
          </a>
          <a href="https://www.instagram.com/nttra204_/?igsh=MXVlc3p1NG4zdnBidw%3D%3D&utm_source=qr" target="_blank" class="social-card">
            <i class="fab fa-instagram social-icon"></i>
            <h3>Instagram</h3>
            <p>@nttra204_</p>
          </a>
          <a href="https://www.linkedin.com/in/nttra204" target="_blank" class="social-card">
            <i class="fab fa-linkedin social-icon"></i>
            <h3>LinkedIn</h3>
            <p>Nguyễn Thanh Trà</p>
          </a>
        </div>
      </div>
    </section>
  </main>
  {get_footer_html(site_title)}
  <script src="/js/i18n.js"></script>
  <script>
  function toggleMenu(){{
    document.body.classList.toggle('menu-open');
  }}
  </script>
</body>
</html>'''
    with open(os.path.join(PUBLIC, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(home_html)

    # About
    about_dir = os.path.join(PUBLIC, 'about')
    ensure_dir(about_dir)
    about_fm, about_body = read_front_matter_and_body(os.path.join(CONTENT, 'about', '_index.md'))
    
    # About page with i18n-ready content
    about_html = f'''<!doctype html>
<html lang="vi">
<head>
  <charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>About - {site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
  <div class="overlay" id="overlay">
    <ul class="menu">
      <li><a href="/" data-i18n="home">Home</a></li>
      <li><a href="/posts/" data-i18n="blog">Blog</a></li>
      <li><a href="/about/" data-i18n="about">About</a></li>
    </ul>
  </div>
  <header>
    <nav>
      <div class="brand"><a href="/" data-i18n="site-title">{site_title}</a></div>
      <ul>
        <li><a href="/" data-i18n="home">Home</a></li>
        <li><a href="/posts/" data-i18n="blog">Blog</a></li>
        <li><a href="/about/" data-i18n="about">About</a></li>
        <li class="lang-toggle-wrapper">
          <div id="lang-switch" class="lang-switch" data-lang="vi">
            <div class="lang-switch-slider"></div>
            <button id="lang-vn" class="lang-btn">VN</button>
            <button id="lang-en" class="lang-btn">EN</button>
          </div>
        </li>
      </ul>
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">☰</div>
    </nav>
  </header>
  <main>
    <article class="post about-content">
      <section class="about-section">
        <h2 data-i18n="personal-info">Thông tin cá nhân</h2>
        <p class="personal-info-line">
          <span><strong data-i18n="fullname-label">Họ và tên</strong>: Nguyễn Thanh Trà</span>
          <span>|</span>
          <span><strong data-i18n="phone-label">SĐT</strong>: 0941779093</span>
          <span>|</span>
          <span><strong data-i18n="email-label">Email</strong>: ntra140924@gmail.com</span>
          <span>|</span>
          <span><strong data-i18n="location-label">Địa chỉ</strong>: <span data-i18n="location">TP. Hồ Chí Minh</span></span>
        </p>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="education">Học vấn</h2>
        <p><strong data-i18n="university">Đại học Công nghệ TP.HCM (HUTECH)</strong> | 2021 - 2025</p>
        <p><span data-i18n="major-label">Ngành</span>: <strong data-i18n="major">Công nghệ Phần mềm</strong></p>
        
        <p><strong data-i18n="knowledge-title">Kiến thức chuyên môn</strong>:</p>
        <ul>
          <li data-i18n="knowledge-1">Lập trình hư☰ng đểi tượng (OOP)</li>
          <li data-i18n="knowledge-2">Cấu trúc dữ liệu & Giải thuật</li>
          <li data-i18n="knowledge-3">Lập trình mạng & Distributed Systems</li>
          <li data-i18n="knowledge-4">Database Design & Management</li>
          <li data-i18n="knowledge-5">Software Engineering & Design Patterns</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="programming-skills">Kỹ năng lập trình</h2>
        
        <p><strong data-i18n="backend-dev">Backend Development</strong>:</p>
        <ul>
          <li>Java (Spring Boot, Socket Programming, Multithreading, NIO)</li>
          <li>Node.js (Express.js, Socket.IO, REST API)</li>
          <li>Database: MySQL, PostgreSQL, MongoDB</li>
          <li>API Design (RESTful, WebSocket)</li>
        </ul>
        
        <p><strong data-i18n="frontend-dev">Frontend Development</strong>:</p>
        <ul>
          <li>HTML5, CSS3, JavaScript (ES6+)</li>
          <li>React/Vue.js basics</li>
          <li data-i18n="responsive-design">Responsive Web Design</li>
        </ul>
        
        <p><strong data-i18n="tools-tech">Tools & Technologies</strong>:</p>
        <ul>
          <li>Git/GitHub</li>
          <li>Docker basics</li>
          <li>Postman, VS Code</li>
          <li>Linux command line</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="projects-portfolio">Dự án & Portfolio</h2>
        <p><span data-i18n="blog-proof-text">Các bài viết trong phần</span> <strong data-i18n="blog">Blog</strong> <span data-i18n="blog-proof-text2">là minh chứng cho kiến thức và kỹ năng thực tế của mình trong</span>:</p>
        <ul>
          <li data-i18n="project-1">Xây dựng TCP/UDP Server với Java</li>
          <li data-i18n="project-2">Phát triển RESTful API với Node.js & Express</li>
          <li data-i18n="project-3">Triển khai WebSocket real-time communication</li>
          <li data-i18n="project-4">Security & CORS handling</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="career-goals">Mục tiêu nghề nghiệp</h2>
        <p><span data-i18n="career-goal-text">Tìm kiếm vị trí</span> <strong data-i18n="career-position">Backend Developer Intern/Fresher</strong> <span data-i18n="career-or">hoặc</span> <strong data-i18n="career-position2">Junior Software Engineer</strong> <span data-i18n="career-at">tại các công ty công nghệ, nơi mình có thể</span>:</p>
        <ul>
          <li data-i18n="career-goal-1">Áp dụng kiến thức về Java & JavaScript vào dự án thực tế</li>
          <li data-i18n="career-goal-2">Học hỏi từ đội ngũ senior developers</li>
          <li data-i18n="career-goal-3">Đóng góp vào các hệ thống lớn, phức tạp</li>
          <li data-i18n="career-goal-4">Phát triển kỹ năng system design & scalability</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="contact">Liên hệ</h2>
        <p> <strong data-i18n="email-label">Email</strong>: ntra140924@gmail.com</p>
        <p> <strong data-i18n="phone-label">SĐT</strong>: 0941779093</p>
        <p>☰ <strong>Facebook</strong>: [facebook.com/yourprofile]</p>
        <p>☰ <strong>GitHub</strong>: [github.com/yourprofile]</p>
        <p><strong data-i18n="availability">Sẵn sàng làm việc full-time</strong></p>
      </section>
    </article>
    <section class="contact-section">
      <div class="contact-container">
        <h2 data-i18n="contact-title">Liên hệ với tôi</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <i class="fas fa-envelope contact-icon"></i>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-phone contact-icon"></i>
            <div>
              <h3 data-i18n="phone-label">SĐT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-map-marker-alt contact-icon"></i>
            <div>
              <h3 data-i18n="location-label">Địa chỉ</h3>
              <p data-i18n="location">TP. Hồ Chí Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-share-alt contact-icon"></i>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>
                <a href="https://www.instagram.com/nttra204_/?igsh=MXVlc3p1NG4zdnBidw%3D%3D&utm_source=qr" target="_blank"><i class="fab fa-instagram"></i> Instagram</a> • 
                <a href="https://www.facebook.com/nguyen.thanh.tra.970568?locale=vi_VN" target="_blank"><i class="fab fa-facebook"></i> Facebook</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    {get_social_section_html()}
  </main>
  {get_footer_html(site_title)}
  <script src="/js/i18n.js"></script>
  <script>
  function toggleMenu(){{
    document.body.classList.toggle('menu-open');
  }}
  </script>
</body>
</html>'''
    with open(os.path.join(about_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(about_html)

    # Posts
    posts_out = os.path.join(PUBLIC, 'posts')
    ensure_dir(posts_out)
    posts = []
    posts_src = os.path.join(CONTENT, 'posts')
    for fn in sorted(os.listdir(posts_src)):
        if not fn.endswith('.md'):
            continue
        path = os.path.join(posts_src, fn)
        fm, body = read_front_matter_and_body(path)
        title = fm.get('title', fn)
        date = fm.get('date', '')
        slug = os.path.splitext(fn)[0]
        thumbnail = fm.get('thumbnail', '')
        html_body = to_html_paragraphs(body)
        
        # Add featured image if thumbnail exists
        featured_image_html = ''
        if thumbnail:
            if thumbnail.startswith('http://') or thumbnail.startswith('https://') or thumbnail.startswith('/'):
                src = thumbnail
            else:
                src = '/images/' + thumbnail
            featured_image_html = f'<div class="featured-image"><img src="{src}" alt="{title}"></div>'
        
        post_html = f'''<!doctype html>
<html lang="vi">
<head>
  <charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} - {site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
  <div class="overlay" id="overlay">
    <ul class="menu">
      <li><a href="/" data-i18n="home">Home</a></li>
      <li><a href="/posts/" data-i18n="blog">Blog</a></li>
      <li><a href="/about/" data-i18n="about">About</a></li>
    </ul>
  </div>
  <header>
    <nav>
      <div class="brand"><a href="/" data-i18n="site-title">{site_title}</a></div>
      <ul>
        <li><a href="/" data-i18n="home">Home</a></li>
        <li><a href="/posts/" data-i18n="blog">Blog</a></li>
        <li><a href="/about/" data-i18n="about">About</a></li>
        <li class="lang-toggle-wrapper">
          <div id="lang-switch" class="lang-switch" data-lang="vi">
            <div class="lang-switch-slider"></div>
            <button id="lang-vn" class="lang-btn">VN</button>
            <button id="lang-en" class="lang-btn">EN</button>
          </div>
        </li>
      </ul>
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">☰</div>
    </nav>
  </header>
  <main>
    <article class="post">
      <h1>{title}</h1>
      <p class="meta">{date}</p>
      {featured_image_html}
      {html_body}
    </article>
    <section class="contact-section">
      <div class="contact-container">
        <h2 data-i18n="contact-title">Liên hệ với tôi</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <i class="fas fa-envelope contact-icon"></i>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-phone contact-icon"></i>
            <div>
              <h3 data-i18n="phone-label">SĐT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-map-marker-alt contact-icon"></i>
            <div>
              <h3 data-i18n="location-label">Địa chỉ</h3>
              <p data-i18n="location">TP. Hồ Chí Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-share-alt contact-icon"></i>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>
                <a href="https://www.instagram.com/nttra204_/?igsh=MXVlc3p1NG4zdnBidw%3D%3D&utm_source=qr" target="_blank"><i class="fab fa-instagram"></i> Instagram</a> • 
                <a href="https://www.facebook.com/nguyen.thanh.tra.970568?locale=vi_VN" target="_blank"><i class="fab fa-facebook"></i> Facebook</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    {get_social_section_html()}
  </main>
  {get_footer_html(site_title)}
  <script src="/js/i18n.js"></script>
  <script>
  function toggleMenu(){{
    document.body.classList.toggle('menu-open');
  }}
  </script>
</body>
</html>'''
        outpath = os.path.join(posts_out, f'{slug}.html')
        with open(outpath, 'w', encoding='utf-8') as f:
          f.write(post_html)
        posts.append({'title': title, 'slug': slug, 'date': date, 'summary': fm.get('summary', body[:160]), 'thumbnail': fm.get('thumbnail','')})

    # posts index
    items = []
    for p in posts:
        thumb_html = ''
        if p.get('thumbnail'):
          tn = p['thumbnail']
          if tn.startswith('http://') or tn.startswith('https://') or tn.startswith('/'):
            src = tn
          else:
            # assume images placed in /images/
            src = '/images/' + tn
          thumb_html = f"<div class=\"thumb-wrap reveal\"><img src=\"{src}\" alt=\"{p['title']}\"></div>"
        
        # Add data-i18n attribute for post titles (extract number from slug like '01-socket-java' -> 'post-01')
        post_num = p['slug'].split('-')[0]  # Get '01', '02', etc.
        post_i18n_key = f"post-{post_num}"
        items.append(f"<li>{thumb_html}<a href=\"/{'posts'}/{p['slug']}.html\" data-i18n=\"{post_i18n_key}\">{p['title']}</a><p class=\"excerpt\">{p['summary']}</p></li>")
    posts_index = f'''<!doctype html>
<html lang="vi">
<head>
  <charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Blog - {site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
  <div class="overlay" id="overlay">
    <ul class="menu">
      <li><a href="/" data-i18n="home">Home</a></li>
      <li><a href="/posts/" data-i18n="blog">Blog</a></li>
      <li><a href="/about/" data-i18n="about">About</a></li>
    </ul>
  </div>
  <header>
    <nav>
      <div class="brand"><a href="/" data-i18n="site-title">{site_title}</a></div>
      <ul>
        <li><a href="/" data-i18n="home">Home</a></li>
        <li><a href="/posts/" data-i18n="blog">Blog</a></li>
        <li><a href="/about/" data-i18n="about">About</a></li>
        <li class="lang-toggle-wrapper">
          <div id="lang-switch" class="lang-switch" data-lang="vi">
            <div class="lang-switch-slider"></div>
            <button id="lang-vn" class="lang-btn">VN</button>
            <button id="lang-en" class="lang-btn">EN</button>
          </div>
        </li>
      </ul>
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">☰</div>
    </nav>
  </header>
  <main>
    <h1 data-i18n="blog-title">Blog</h1>
    <p class="blog-intro" data-i18n="blog-intro">Chia sẻ kiến thức và kinh nghiệm trong lập trình mạng với Java và JavaScript</p>
    <ul class="posts">
      {''.join(items)}
    </ul>
    <section class="contact-section">
      <div class="contact-container">
        <h2 data-i18n="contact-title">Liên hệ với tôi</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <i class="fas fa-envelope contact-icon"></i>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-phone contact-icon"></i>
            <div>
              <h3 data-i18n="phone-label">SĐT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-map-marker-alt contact-icon"></i>
            <div>
              <h3 data-i18n="location-label">Địa chỉ</h3>
              <p data-i18n="location">TP. Hồ Chí Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <i class="fas fa-share-alt contact-icon"></i>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>
                <a href="https://www.instagram.com/nttra204_/?igsh=MXVlc3p1NG4zdnBidw%3D%3D&utm_source=qr" target="_blank"><i class="fab fa-instagram"></i> Instagram</a> • 
                <a href="https://www.facebook.com/nguyen.thanh.tra.970568?locale=vi_VN" target="_blank"><i class="fab fa-facebook"></i> Facebook</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    {get_social_section_html()}
  </main>
  {get_footer_html(site_title)}
  <script src="/js/i18n.js"></script>
    <script>
      function toggleMenu(){{
        document.body.classList.toggle('menu-open');
      }}
      </script>
</body>
</html>'''
    with open(os.path.join(posts_out, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(posts_index)

    print('Generated static site in', PUBLIC)

if __name__ == '__main__':
    build()

