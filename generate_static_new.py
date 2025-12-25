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
    site_title = 'Blog Láº­p TrÃ¬nh Máº¡ng'
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
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>
    </nav>
  </header>
  <main>
    <section class="hero">
      <div class="hero-content">
        <p class="hero-greeting" data-i18n="hero-greeting">Xin chÃ o, mÃ¬nh lÃ </p>
        <h1 data-i18n="hero-name">Nguyá»…n Thanh TrÃ </h1>
        <div class="hero-intro">
          <p><strong data-i18n="hero-role">Software Engineer | Backend Developer</strong></p>
          <p><strong data-i18n="software-engineering">CÃ´ng nghá»‡ Pháº§n má»m</strong> <span data-i18n="hero-intro-1">lÃ  lÄ©nh vá»±c á»©ng dá»¥ng kiáº¿n thá»©c khoa há»c mÃ¡y tÃ­nh Ä‘á»ƒ thiáº¿t káº¿, phÃ¡t triá»ƒn vÃ  duy trÃ¬ cÃ¡c há»‡ thá»‘ng pháº§n má»m cháº¥t lÆ°á»£ng cao.</span></p>
          <p><span data-i18n="hero-intro-2-pre">Tá»«</span> <strong data-i18n="backend-systems">Backend Systems</strong> <span data-i18n="hero-intro-2-post">Ä‘áº¿n</span> <strong data-i18n="network-programming">Network Programming</strong>, <span data-i18n="hero-intro-2-post">tá»«</span> <strong data-i18n="database-design">Database Design</strong> <span data-i18n="hero-intro-2-post">Ä‘áº¿n</span> <strong data-i18n="api-development">API Development</strong> <span data-i18n="hero-intro-2-end">â€” má»—i dá»± Ã¡n lÃ  má»™t thá»­ thÃ¡ch giáº£i quyáº¿t váº¥n Ä‘á» thá»±c táº¿ báº±ng cÃ´ng nghá»‡.</span></p>
          <p><span data-i18n="hero-intro-3-pre">ChuyÃªn vá»</span> <strong>Java</strong> <span data-i18n="hero-intro-3-mid">vÃ </span> <strong>JavaScript</strong><span data-i18n="hero-intro-3-post">, tÃ´i táº­p trung xÃ¢y dá»±ng cÃ¡c giáº£i phÃ¡p backend hiá»‡u quáº£, scalable vÃ  báº£o máº­t.</span></p>
        </div>
        <div class="cta">
          <a class="btn primary" href="/posts/" data-i18n="view-posts">Xem portfolio</a>
          <a class="btn ghost" href="/about/" data-i18n="about-me">LiÃªn há»‡</a>
        </div>
      </div>
      <div class="hero-image-wrapper">
        <img src="/images/profile-photo.jpg" alt="Nguyá»…n Thanh TrÃ " class="hero-avatar">
      </div>
    </section>
    <section class="intro">
      {home_body}
    </section>
    <section class="contact-section">
      <div class="contact-container">
        <h2 data-i18n="contact-title">LiÃªn há»‡ vá»›i tÃ´i</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <span class="contact-icon">ðŸ“§</span>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“±</span>
            <div>
              <h3 data-i18n="phone-label">SÄT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“</span>
            <div>
              <h3 data-i18n="location-label">Äá»‹a chá»‰</h3>
              <p data-i18n="location">TP. Há»“ ChÃ­ Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ”—</span>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>GitHub â€¢ Facebook</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer>
    <p><span data-i18n="site-title">{site_title}</span> â€¢ <span data-i18n="footer-copyright">Â© {datetime.now().year}</span></p>
  </footer>
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
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>About - {site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
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
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>
    </nav>
  </header>
  <main>
    <article class="post about-content">
      <section class="about-section">
        <h2 data-i18n="personal-info">ThÃ´ng tin cÃ¡ nhÃ¢n</h2>
        <p class="personal-info-line">
          <span><strong data-i18n="fullname-label">Há» vÃ  tÃªn</strong>: Nguyá»…n Thanh TrÃ </span>
          <span>|</span>
          <span><strong data-i18n="phone-label">SÄT</strong>: 0941779093</span>
          <span>|</span>
          <span><strong data-i18n="email-label">Email</strong>: ntra140924@gmail.com</span>
          <span>|</span>
          <span><strong data-i18n="location-label">Äá»‹a chá»‰</strong>: <span data-i18n="location">TP. Há»“ ChÃ­ Minh</span></span>
        </p>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="education">Há»c váº¥n</h2>
        <p><strong data-i18n="university">Äáº¡i há»c CÃ´ng nghá»‡ TP.HCM (HUTECH)</strong> | 2021 - 2025</p>
        <p><span data-i18n="major-label">NgÃ nh</span>: <strong data-i18n="major">CÃ´ng nghá»‡ Pháº§n má»m</strong></p>
        
        <p><strong data-i18n="knowledge-title">Kiáº¿n thá»©c chuyÃªn mÃ´n</strong>:</p>
        <ul>
          <li data-i18n="knowledge-1">Láº­p trÃ¬nh hÆ°á»›ng Ä‘á»‘i tÆ°á»£ng (OOP)</li>
          <li data-i18n="knowledge-2">Cáº¥u trÃºc dá»¯ liá»‡u & Giáº£i thuáº­t</li>
          <li data-i18n="knowledge-3">Láº­p trÃ¬nh máº¡ng & Distributed Systems</li>
          <li data-i18n="knowledge-4">Database Design & Management</li>
          <li data-i18n="knowledge-5">Software Engineering & Design Patterns</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="programming-skills">Ká»¹ nÄƒng láº­p trÃ¬nh</h2>
        
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
        <h2 data-i18n="projects-portfolio">Dá»± Ã¡n & Portfolio</h2>
        <p><span data-i18n="blog-proof-text">CÃ¡c bÃ i viáº¿t trong pháº§n</span> <strong data-i18n="blog">Blog</strong> <span data-i18n="blog-proof-text2">lÃ  minh chá»©ng cho kiáº¿n thá»©c vÃ  ká»¹ nÄƒng thá»±c táº¿ cá»§a mÃ¬nh trong</span>:</p>
        <ul>
          <li data-i18n="project-1">XÃ¢y dá»±ng TCP/UDP Server vá»›i Java</li>
          <li data-i18n="project-2">PhÃ¡t triá»ƒn RESTful API vá»›i Node.js & Express</li>
          <li data-i18n="project-3">Triá»ƒn khai WebSocket real-time communication</li>
          <li data-i18n="project-4">Security & CORS handling</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="career-goals">Má»¥c tiÃªu nghá» nghiá»‡p</h2>
        <p><span data-i18n="career-goal-text">TÃ¬m kiáº¿m vá»‹ trÃ­</span> <strong data-i18n="career-position">Backend Developer Intern/Fresher</strong> <span data-i18n="career-or">hoáº·c</span> <strong data-i18n="career-position2">Junior Software Engineer</strong> <span data-i18n="career-at">táº¡i cÃ¡c cÃ´ng ty cÃ´ng nghá»‡, nÆ¡i mÃ¬nh cÃ³ thá»ƒ</span>:</p>
        <ul>
          <li data-i18n="career-goal-1">Ãp dá»¥ng kiáº¿n thá»©c vá» Java & JavaScript vÃ o dá»± Ã¡n thá»±c táº¿</li>
          <li data-i18n="career-goal-2">Há»c há»i tá»« Ä‘á»™i ngÅ© senior developers</li>
          <li data-i18n="career-goal-3">ÄÃ³ng gÃ³p vÃ o cÃ¡c há»‡ thá»‘ng lá»›n, phá»©c táº¡p</li>
          <li data-i18n="career-goal-4">PhÃ¡t triá»ƒn ká»¹ nÄƒng system design & scalability</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2 data-i18n="contact">LiÃªn há»‡</h2>
        <p>ðŸ“§ <strong data-i18n="email-label">Email</strong>: ntra140924@gmail.com</p>
        <p>ðŸ“± <strong data-i18n="phone-label">SÄT</strong>: 0941779093</p>
        <p>ðŸ‘¥ <strong>Facebook</strong>: [facebook.com/yourprofile]</p>
        <p>ðŸ”— <strong>GitHub</strong>: [github.com/yourprofile]</p>
        <p><strong data-i18n="availability">Sáºµn sÃ ng lÃ m viá»‡c full-time</strong></p>
      </section>
    </article>
    <section class="contact-section">
      <div class="contact-container">
        <h2 data-i18n="contact-title">LiÃªn há»‡ vá»›i tÃ´i</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <span class="contact-icon">ðŸ“§</span>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“±</span>
            <div>
              <h3 data-i18n="phone-label">SÄT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“</span>
            <div>
              <h3 data-i18n="location-label">Äá»‹a chá»‰</h3>
              <p data-i18n="location">TP. Há»“ ChÃ­ Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ”—</span>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>GitHub â€¢ Facebook</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer>
    <p><span data-i18n="site-title">{site_title}</span> â€¢ <span data-i18n="footer-copyright">Â© {datetime.now().year}</span></p>
  </footer>
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
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} - {site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
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
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>
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
        <h2 data-i18n="contact-title">LiÃªn há»‡ vá»›i tÃ´i</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <span class="contact-icon">ðŸ“§</span>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“±</span>
            <div>
              <h3 data-i18n="phone-label">SÄT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“</span>
            <div>
              <h3 data-i18n="location-label">Äá»‹a chá»‰</h3>
              <p data-i18n="location">TP. Há»“ ChÃ­ Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ”—</span>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>GitHub â€¢ Facebook</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer>
    <p><span data-i18n="site-title">{site_title}</span> â€¢ <span data-i18n="footer-copyright">Â© {datetime.now().year}</span></p>
  </footer>
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
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Blog - {site_title}</title>
  <link rel="stylesheet" href="/css/style.css">
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
            <button id="lang-vn" class="lang-btn">ðŸ‡»ðŸ‡³ VN</button>
            <button id="lang-en" class="lang-btn">ðŸ‡¬ðŸ‡§ EN</button>
          </div>
        </li>
      </ul>
      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>
    </nav>
  </header>
  <main>
    <h1 data-i18n="blog-title">Blog</h1>
    <p class="blog-intro" data-i18n="blog-intro">Chia sáº» kiáº¿n thá»©c vÃ  kinh nghiá»‡m trong láº­p trÃ¬nh máº¡ng vá»›i Java vÃ  JavaScript</p>
    <ul class="posts">
      {''.join(items)}
    </ul>
    <section class="contact-section">
      <div class="contact-container">
        <h2 data-i18n="contact-title">LiÃªn há»‡ vá»›i tÃ´i</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <span class="contact-icon">ðŸ“§</span>
            <div>
              <h3 data-i18n="email-label">Email</h3>
              <a href="mailto:ntra140924@gmail.com">ntra140924@gmail.com</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“±</span>
            <div>
              <h3 data-i18n="phone-label">SÄT</h3>
              <a href="tel:0941779093">0941779093</a>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ“</span>
            <div>
              <h3 data-i18n="location-label">Äá»‹a chá»‰</h3>
              <p data-i18n="location">TP. Há»“ ChÃ­ Minh</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="contact-icon">ðŸ”—</span>
            <div>
              <h3 data-i18n="social-label">Social</h3>
              <p>GitHub â€¢ Facebook</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer>
    <p><span data-i18n="site-title">{site_title}</span> â€¢ <span data-i18n="footer-copyright">Â© {datetime.now().year}</span></p>
  </footer>
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

