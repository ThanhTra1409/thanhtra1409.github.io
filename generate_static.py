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

  # Remove BOM if present

  if text.startswith('\ufeff'):

    text = text[1:]

  

  # Match front matter delimited by ++ or +++ (Hugo uses +++ but some files used ++)

  m = re.match(r"\+{2,3}([\s\S]*?)\+{2,3}[ \t\r\n]*", text)

  fm = {}

  body = text

  if m:

    fm_text = m.group(1)  # Get content between ++ markers

    body = text[m.end():].strip()

    for line in fm_text.splitlines():

      line = line.strip()

      if not line or line.startswith('++'):

        continue

      if '=' in line:

        key, value = line.split('=', 1)

        key = key.strip()

        value = value.strip().strip('"')

        fm[key] = value

  

  # Generate summary if not provided - extract first paragraph from body

  if not fm.get('summary') and body:

    # Remove markdown headings, code blocks, and images for summary

    summary_text = re.sub(r'```[\s\S]*?```', '', body)  # Remove code blocks

    summary_text = re.sub(r'^#{1,6}\s+.*$', '', summary_text, flags=re.MULTILINE)  # Remove headings

    summary_text = re.sub(r'!\[.*?\]\(.*?\)', '', summary_text)  # Remove images

    summary_text = re.sub(r'\*[^\*]*\*', '', summary_text)  # Remove image captions

    # Get first paragraph

    first_para = summary_text.strip().split('\n\n')[0] if summary_text.strip() else ''

    # Take first 150 chars

    fm['summary'] = first_para[:150].strip() + ('...' if len(first_para) > 150 else '')

  

  return fm, body



def to_html_paragraphs(md):

    # Very small markdown -> HTML converter: paragraphs, inline `code`, images, and headings

    parts = re.split(r"\n\s*\n", md.strip())

    html = []

    for p in parts:

        p = p.strip()

        

        # Check if this is a heading (starts with #)

        if p.startswith('#'):

            heading_match = re.match(r'^(#{1,6})\s+(.+)$', p)

            if heading_match:

                level = len(heading_match.group(1))

                heading_text = heading_match.group(2)

                html.append(f'<h{level}>{heading_text}</h{level}>')

                continue

        

        # Check if this is an image line (starts with ![)

        if p.startswith('!['):

            # Image markdown: ![alt](url)

            img_match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', p)

            if img_match:

                alt_text = img_match.group(1)

                img_url = img_match.group(2)

                html.append(f'<img src="{img_url}" alt="{alt_text}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0;">')

                continue

        

        # Bold markdown

        p = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)

        # Italic markdown (but not for image caption lines starting with *)

        if not p.startswith('*'):

            p = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', p)

        else:

            # This is likely an image caption

            p = '<em>' + p[1:] + '</em>'

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

        <h2 data-i18n="social-title">Xã hội</h2>

        <div class="social-grid">

          <a href="https://github.com/ThanhTra1409" target="_blank" class="social-card">

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

          <a href="https://www.linkedin.com/in/thanh-tra-nguyen-84a46833a" target="_blank" class="social-card">

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

        <h4 data-i18n="contact-info">Thông tin liên hệ</h4>

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

        <p><span data-i18n="footer-copyright">Â© {datetime.now().year}</span> <span data-i18n="site-title">{site_title}</span></p>

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

    site_title = 'Nguyễn Thanh Trà'

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

  <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>ðŸ‘¨â€ðŸ’»</text></svg>">

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

      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>

    </nav>

  </header>

  <main>

    <section class="hero">

      <div class="hero-content">

        <p class="hero-greeting" data-i18n="hero-greeting">Xin chào, tôi là</p>

        <h1 data-i18n="hero-name">Nguyễn Thanh Trà</h1>

        <div class="hero-intro">

          <p><strong data-i18n="hero-role">Software Engineer | Backend Developer</strong></p>

          <p data-i18n="hero-intro-main">Tôi là sinh viên năm 4 yêu thích công nghệ phần mềm, hiện đang tìm hiểu các kiến thức cơ bản về lập trình và phát triển phần mềm. Có tinh thần học hỏi, chủ động rèn luyện tư duy logic và kỹ năng chuyên môn để phục vụ học tập và công việc trong tương lai.</p>

        </div>

        <div class="cta">

          <a class="btn primary" href="/posts/" data-i18n="view-posts">Xem portfolio</a>

          <a class="btn ghost" href="/about/" data-i18n="about-me">Liên hệ</a>

        </div>

      </div>

      <div class="hero-image-wrapper">

        <img src="/images/133.jpg" alt="Nguyễn Thanh Trà" class="hero-avatar">

      </div>

    </section>

    <section class="intro">

      {home_body}

    </section>

    

    <section class="certificates-section" style="max-width: 1200px; margin: 4rem auto; padding: 0 2rem;">

      <h2 style="text-align: center; font-size: 2rem; margin-bottom: 3rem;" data-i18n="certificates">Chá»©ng chá»‰ vÃ  thÃ nh tá»±u</h2>

      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem;">

        <div class="certificate-card" style="cursor: pointer; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.3s; background: white;" onclick="openImageModal('/images/cert-networking-basics.jpg')">

          <img src="/images/cert-networking-basics.jpg" alt="Networking Basics Certificate" style="width: 100%; height: auto; object-fit: contain;">

          <div style="padding: 1.5rem; text-align: center;">

            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; color: #5b6fce;">Networking Basics</h3>

            <p style="margin: 0.5rem 0; color: #666; font-size: 0.95rem;">Nguyễn Thanh Trà</p>

            <p style="margin: 0.5rem 0; color: #999; font-size: 0.9rem;">Nov 2025</p>

          </div>

        </div>

        

        <div class="certificate-card" style="cursor: pointer; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.3s; background: white;" onclick="openImageModal('/images/cert-js-essentials-1.jpg')">

          <img src="/images/cert-js-essentials-1.jpg" alt="JavaScript Essentials 1 Certificate" style="width: 100%; height: auto; object-fit: contain;">

          <div style="padding: 1.5rem; text-align: center;">

            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; color: #5b6fce;">JavaScript Essentials 1</h3>

            <p style="margin: 0.5rem 0; color: #666; font-size: 0.95rem;">Nguyễn Thanh Trà</p>

            <p style="margin: 0.5rem 0; color: #999; font-size: 0.9rem;">Dec 2025</p>

          </div>

        </div>

        

        <div class="certificate-card" style="cursor: pointer; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.3s; background: white;" onclick="openImageModal('/images/cert-js-essentials-2.jpg')">

          <img src="/images/cert-js-essentials-2.jpg" alt="JavaScript Essentials 2 Certificate" style="width: 100%; height: auto; object-fit: contain;">

          <div style="padding: 1.5rem; text-align: center;">

            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; color: #5b6fce;">JavaScript Essentials 2</h3>

            <p style="margin: 0.5rem 0; color: #666; font-size: 0.95rem;">Nguyễn Thanh Trà</p>

            <p style="margin: 0.5rem 0; color: #999; font-size: 0.9rem;">Dec 2025</p>

          </div>

        </div>

      </div>

    </section>

    

    <!-- Image Modal -->

    <div id="imageModal" style="display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); justify-content: center; align-items: center;" onclick="closeImageModal()">

      <span style="position: absolute; top: 20px; right: 40px; color: white; font-size: 40px; font-weight: bold; cursor: pointer;">&times;</span>

      <img id="modalImage" style="max-width: 90%; max-height: 90%; object-fit: contain;">

    </div>

    

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

  <script src="/js/i18n.js?v=1.1"></script>

  <script>

  function toggleMenu(){{

    document.body.classList.toggle('menu-open');

  }}

  

  function openImageModal(imageSrc) {{

    document.getElementById('imageModal').style.display = 'flex';

    document.getElementById('modalImage').src = imageSrc;

  }}

  

  function closeImageModal() {{

    document.getElementById('imageModal').style.display = 'none';

  }}

  

  // Hover effect for certificate cards

  document.addEventListener('DOMContentLoaded', function() {{

    const cards = document.querySelectorAll('.certificate-card');

    cards.forEach(card => {{

      card.addEventListener('mouseenter', function() {{

        this.style.transform = 'translateY(-5px)';

      }});

      card.addEventListener('mouseleave', function() {{

        this.style.transform = 'translateY(0)';

      }});

    }});

  }});

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

  <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>ðŸ‘¨â€ðŸ’»</text></svg>">

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

      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>

    </nav>

  </header>

  <main style="padding: 0; max-width: 100%;">

    <article class="post about-content" style="max-width: 100%;">

      <section class="about-section personal-info-section" style="max-width: 100%; padding: 3rem 0; margin: 0; display: flex; justify-content: center;">

        <div style="width: 85%; max-width: 1200px;">

          <div style="background: white; padding: 3rem 4rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 12px; display: flex; flex-direction: column;">

            <h2 data-i18n="personal-info" style="text-align: center; margin-bottom: 3rem; margin-top: 0; font-size: 2.5rem; font-weight: 700; margin-right: -114px;">ThÃ´ng tin cÃ¡ nhÃ¢n</h2>

            <div style="display: flex; align-items: flex-start; justify-content: flex-start; gap: 4rem; max-width: 100%; margin: 0 auto;">

              <div style="flex-shrink: 0; margin-left: -114px; margin-top: -76px;">

                <img src="/images/133.jpg" alt="Nguyễn Thanh Trà" style="width: 280px; height: 380px; border-radius: 16px; object-fit: cover; border: 4px solid rgba(107, 114, 128, 0.2); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);">

              </div>

              <div style="flex: 1;">

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem 4rem; max-width: 600px; margin-bottom: 2rem;">

                  <div>

                    <strong data-i18n="fullname-label" style="color: #6b7280; font-size: 1rem; display: block; margin-bottom: 0.5rem;">Họ và tên</strong>

                    <span style="font-size: 1.1rem; color: #2d3748; font-weight: 500;">Nguyễn Thanh Trà</span>

                  </div>

                  

                  <div>

                    <strong data-i18n="phone-label" style="color: #6b7280; font-size: 1rem; display: block; margin-bottom: 0.5rem;">SÄT</strong>

                    <span style="font-size: 1.1rem; color: #2d3748; font-weight: 500;">0941779093</span>

                  </div>

                  

                  <div>

                    <strong data-i18n="email-label" style="color: #6b7280; font-size: 1rem; display: block; margin-bottom: 0.5rem;">Email</strong>

                    <span style="font-size: 1.1rem; color: #2d3748; font-weight: 500;">ntra140924@gmail.com</span>

                  </div>

                  

                  <div>

                    <strong data-i18n="location-label" style="color: #6b7280; font-size: 1rem; display: block; margin-bottom: 0.5rem;">Äá»‹a chá»‰</strong>

                    <span data-i18n="location" style="font-size: 1.1rem; color: #2d3748; font-weight: 500;">TP. Há»“ ChÃ­ Minh</span>

                  </div>

                </div>

                <div style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; border-radius: 8px; font-style: italic; color: #4b5563; font-size: 1.05rem; line-height: 1.6; max-width: 600px;">

                  "<span data-i18n="slogan">CÃ´ng nghá»‡ luÃ´n thay Ä‘á»•i, tÃ´i chá»n cÃ¡ch há»c há»i má»—i ngÃ y Ä‘á»ƒ khÃ´ng bá»‹ bá» láº¡i phÃ­a sau.</span>"

                </div>

              </div>

            </div>

          </div>

        </div>

      </section>

      

      <section class="about-section" style="max-width: 90%; margin: 2rem auto; padding: 0 2rem;">

        <h2 data-i18n="education" style="text-align: center; margin-bottom: 3rem; font-size: 2rem;">Há»c váº¥n</h2>

        

        <div class="education-card" style="background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer; border: 2px solid transparent; max-width: 900px; margin: 0 auto; position: relative; overflow: hidden;">

          <div style="position: relative; z-index: 1;">

            <h3 style="color: #4b5563; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">

              <span data-i18n="university">Äáº¡i há»c CÃ´ng nghá»‡ TP.HCM (HUTECH)</span> | 2022 - 2026

            </h3>

            <p style="color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;">

              <span data-i18n="major-label">NgÃ nh</span>: <strong data-i18n="major" style="color: #4b5563;">CÃ´ng nghá»‡ Pháº§n má»m</strong>

            </p>

            

            <h4 data-i18n="knowledge-title" style="color: #4b5563; font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">Kiáº¿n thá»©c chuyÃªn mÃ´n:</h4>

            <ul style="list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 0.8rem;">

              <li data-i18n="knowledge-1" style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem; transition: all 0.3s ease;">âœ“ Láº­p trÃ¬nh hÆ°á»›ng Ä‘á»‘i tÆ°á»£ng (OOP)</li>

              <li data-i18n="knowledge-2" style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem; transition: all 0.3s ease;">âœ“ Cáº¥u trÃºc dá»¯ liá»‡u & Giáº£i thuáº­t</li>

              <li data-i18n="knowledge-3" style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem; transition: all 0.3s ease;">âœ“ Láº­p trÃ¬nh máº¡ng & Distributed Systems</li>

              <li data-i18n="knowledge-4" style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem; transition: all 0.3s ease;">âœ“ Database Design & Management</li>

              <li data-i18n="knowledge-5" style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem; transition: all 0.3s ease;">âœ“ Software Engineering & Design Patterns</li>

            </ul>

          </div>

        </div>

      </section>

      

      <section class="about-section" style="max-width: 90%; margin: 2rem auto; padding: 0 2rem;">

        <h2 data-i18n="programming-skills" style="text-align: center; margin-bottom: 3rem; font-size: 2rem;">Ká»¹ nÄƒng láº­p trÃ¬nh Ä‘Ã£ há»c</h2>

        

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; max-width: 1200px; margin: 0 auto;">

          <!-- Backend Card -->

          <div class="skill-card" style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer; border: 2px solid transparent;">

            <h3 data-i18n="backend-dev" style="color: #4b5563; margin-bottom: 1.5rem; font-size: 1.5rem; font-weight: 700;">Backend Development</h3>

            <ul style="list-style: none; padding: 0; margin: 0;">

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Java (Spring Boot, Socket Programming, Multithreading, NIO)</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Node.js (Express.js, Socket.IO, REST API)</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Database: MySQL, PostgreSQL, MongoDB</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ API Design (RESTful, WebSocket)</li>

            </ul>

          </div>

          

          <!-- Frontend Card -->

          <div class="skill-card" style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer; border: 2px solid transparent;">

            <h3 data-i18n="frontend-dev" style="color: #4b5563; margin-bottom: 1.5rem; font-size: 1.5rem; font-weight: 700;">Frontend Development</h3>

            <ul style="list-style: none; padding: 0; margin: 0;">

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ HTML5, CSS3, JavaScript (ES6+)</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ React/Vue.js basics</li>

              <li data-i18n="responsive-design" style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Responsive Web Design</li>

            </ul>

          </div>

          

          <!-- Tools Card -->

          <div class="skill-card" style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer; border: 2px solid transparent;">

            <h3 data-i18n="tools-tech" style="color: #4b5563; margin-bottom: 1.5rem; font-size: 1.5rem; font-weight: 700;">Tools & Technologies</h3>

            <ul style="list-style: none; padding: 0; margin: 0;">

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Git/GitHub</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Docker basics</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Postman, VS Code</li>

              <li style="padding: 0.5rem 0; color: #6b7280; font-size: 1rem;">âœ“ Linux command line</li>

            </ul>

          </div>

        </div>

      </section>

      

      <section class="about-section" style="max-width: 90%; margin: 2rem auto; padding: 0 2rem;">

        <h2 data-i18n="projects-portfolio" style="text-align: center; margin-bottom: 3rem; font-size: 2rem;">Dá»± Ã¡n & Portfolio</h2>

        

        <div class="projects-card" style="background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer; border: 2px solid transparent; max-width: 900px; margin: 0 auto; position: relative; overflow: hidden;">

          <div style="position: relative; z-index: 1;">

            <p data-i18n="blog-intro-text" style="color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem; text-align: center;">CÃ¡c bÃ i viáº¿t trong blog lÃ  cÃ¡c kiáº¿n thá»©c mÃ  tÃ´i Ä‘Ã£ Ä‘Æ°á»£c há»c:</p>

            <ul style="list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">

              <li data-i18n="project-1" style="padding: 0.8rem; color: #6b7280; font-size: 1rem; transition: all 0.3s ease; border-left: 3px solid #d1d5db;">âœ“ XÃ¢y dá»±ng TCP/UDP Server vá»›i Java</li>

              <li data-i18n="project-2" style="padding: 0.8rem; color: #6b7280; font-size: 1rem; transition: all 0.3s ease; border-left: 3px solid #d1d5db;">âœ“ PhÃ¡t triá»ƒn RESTful API vá»›i Node.js & Express</li>

              <li data-i18n="project-3" style="padding: 0.8rem; color: #6b7280; font-size: 1rem; transition: all 0.3s ease; border-left: 3px solid #d1d5db;">âœ“ Triá»ƒn khai WebSocket real-time communication</li>

              <li data-i18n="project-4" style="padding: 0.8rem; color: #6b7280; font-size: 1rem; transition: all 0.3s ease; border-left: 3px solid #d1d5db;">âœ“ Security & CORS handling</li>

            </ul>

          </div>

        </div>

      </section>

      

      {get_social_section_html()}

  </main>

  {get_footer_html(site_title)}

  <script src="/js/i18n.js?v=1.1"></script>

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

    posts_en = []

    posts_src = os.path.join(CONTENT, 'posts')

    

    # Process Vietnamese and English posts

    for fn in sorted(os.listdir(posts_src)):

        if not fn.endswith('.md'):

            continue

        

        # Skip .en.md files in the first pass

        if fn.endswith('.en.md'):

            continue

            

        # Process Vietnamese post

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

  <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>ðŸ‘¨â€ðŸ’»</text></svg>">

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

    {get_social_section_html()}

  </main>

  {get_footer_html(site_title)}

  <script src="/js/i18n.js?v=1.1"></script>

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

        posts.append({'title': title, 'slug': slug, 'date': date, 'summary': fm.get('summary', ''), 'thumbnail': fm.get('thumbnail','')})

        

        # Process English version if exists

        en_fn = slug + '.en.md'

        en_path = os.path.join(posts_src, en_fn)

        if os.path.exists(en_path):

            fm_en, body_en = read_front_matter_and_body(en_path)

            title_en = fm_en.get('title', title)

            html_body_en = to_html_paragraphs(body_en)

            

            # Generate English HTML

            post_html_en = f'''<!doctype html>

<html lang="en">

<head>

  <meta charset="utf-8">

  <meta name="viewport" content="width=device-width,initial-scale=1">

  <title>{title_en} - {site_title}</title>

  <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>ðŸ‘¨â€ðŸ’»</text></svg>">

  <link rel="stylesheet" href="/css/style.css">

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

</head>

<body data-lang="en">

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

          <div id="lang-switch" class="lang-switch" data-lang="en">

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

      <h1>{title_en}</h1>

      <p class="meta">{date}</p>

      {featured_image_html}

      {html_body_en}

    </article>

    {get_social_section_html()}

  </main>

  {get_footer_html(site_title)}

  <script src="/js/i18n.js?v=1.1"></script>

  <script>

  function toggleMenu(){{

    document.body.classList.toggle('menu-open');

  }}

  </script>

</body>

</html>'''

            outpath_en = os.path.join(posts_out, f'{slug}.en.html')

            with open(outpath_en, 'w', encoding='utf-8') as f:

                f.write(post_html_en)

            posts_en.append({'title': title_en, 'slug': slug, 'date': date, 'summary': fm_en.get('summary', ''), 'thumbnail': thumbnail})



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

          thumb_html = f'<div class="thumb-wrap"><img src="{src}" alt="{p["title"]}" loading="lazy"></div>'

        

        # Add data-i18n attribute for post titles (extract number from slug like '01-socket-java' -> 'post-01')

        post_num = p['slug'].split('-')[0]  # Get '01', '02', etc.

        post_i18n_key = f"post-{post_num}"

        excerpt_i18n_key = f"excerpt-{post_num}"

        

        # Create structured card HTML

        card_content = f'''

        {thumb_html}

        <div class="post-card-content">

          <a href="/posts/{p['slug']}.html" data-i18n="{post_i18n_key}">{p['title']}</a>

          <p class="excerpt" data-i18n="{excerpt_i18n_key}">{p['summary']}</p>

          <div class="post-meta">

            <span class="post-date">{p['date']}</span>

          </div>

        </div>

        '''

        items.append(f'<li>{card_content}</li>')

    posts_index = f'''<!doctype html>

<html lang="vi">

<head>

  <meta charset="utf-8">

  <meta name="viewport" content="width=device-width,initial-scale=1">

  <title>Blog - {site_title}</title>

  <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>ðŸ‘¨â€ðŸ’»</text></svg>">

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

      <div class="menu-toggle" onclick="toggleMenu()" aria-label="menu">â˜°</div>

    </nav>

  </header>

  <main>

    <h1 data-i18n="blog-title">Blog</h1>

    <p class="blog-intro" data-i18n="blog-intro">Chia sáº» kiáº¿n thá»©c vÃ  kinh nghiá»‡m trong láº­p trÃ¬nh máº¡ng vá»›i Java vÃ  JavaScript</p>

    <ul class="posts">

      {''.join(items)}

    </ul>

    {get_social_section_html()}

  </main>

  {get_footer_html(site_title)}

  <script src="/js/i18n.js?v=1.1"></script>

    <script>

      function toggleMenu(){{

        document.body.classList.toggle('menu-open');

      }}

      </script>

</body>

</html>'''

    with open(os.path.join(posts_out, 'index.html'), 'w', encoding='utf-8') as f:

        f.write(posts_index)

    

    # Generate English posts index

    items_en = []

    for p in posts_en:

        thumb_html = ''

        if p.get('thumbnail'):

          tn = p['thumbnail']

          if tn.startswith('http://') or tn.startswith('https://') or tn.startswith('/'):

            src = tn

          else:

            src = '/images/' + tn

          thumb_html = f'<div class="thumb-wrap"><img src="{src}" alt="{p["title"]}" loading="lazy"></div>'

        

        post_num = p['slug'].split('-')[0]

        post_i18n_key = f"post-{post_num}"

        excerpt_i18n_key = f"excerpt-{post_num}"

        

        # Create structured card HTML

        card_content = f'''

        {thumb_html}

        <div class="post-card-content">

          <a href="/posts/{p['slug']}.en.html" data-i18n="{post_i18n_key}">{p['title']}</a>

          <p class="excerpt" data-i18n="{excerpt_i18n_key}">{p['summary']}</p>

          <div class="post-meta">

            <span class="post-date">{p['date']}</span>

          </div>

        </div>

        '''

        items_en.append(f'<li>{card_content}</li>')

    

    posts_index_en = f'''<!doctype html>

<html lang="en">

<head>

  <meta charset="utf-8">

  <meta name="viewport" content="width=device-width,initial-scale=1">

  <title>Blog - {site_title}</title>  <link rel="icon" type="image/x-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>ðŸ‘¨â€ðŸ’»</text></svg>">  <link rel="stylesheet" href="/css/style.css">

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

</head>

<body data-lang="en">

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

          <div id="lang-switch" class="lang-switch" data-lang="en">

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

    <h1 data-i18n="blog-title">Blog</h1>

    <p class="blog-intro" data-i18n="blog-intro">Sharing knowledge and experience in network programming with Java and JavaScript</p>

    <ul class="posts">

      {''.join(items_en)}

    </ul>

    {get_social_section_html()}

  </main>

  {get_footer_html(site_title)}

  <script src="/js/i18n.js?v=1.1"></script>

    <script>

      function toggleMenu(){{

        document.body.classList.toggle('menu-open');

      }}

      </script>

</body>

</html>'''

    with open(os.path.join(posts_out, 'index.en.html'), 'w', encoding='utf-8') as f:

        f.write(posts_index_en)



    print('Generated static site in', PUBLIC)



if __name__ == '__main__':

    build()







