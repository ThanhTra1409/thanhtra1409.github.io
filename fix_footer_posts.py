# -*- coding: utf-8 -*-
"""
Replace old contact-section and footer with new social-section and footer
"""
import os
import glob

# Template social-section và footer mới
new_section = '''    <section class="social-section">
      <div class="social-container">
        <h2 data-i18n="social-title">Mạng xã hội</h2>
        <div class="social-grid">
          <a href="https://github.com/ThanhTra1409" target="_blank" class="social-card">
            <i class="fab fa-github social-icon"></i>
            <h3>GitHub</h3>
            <p>@ThanhTra1409</p>
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
          <a href="https://www.linkedin.com/in/thanh-tra-nguyen-84a46833a" target="_blank" class="social-card">
            <i class="fab fa-linkedin social-icon"></i>
            <h3>LinkedIn</h3>
            <p>Nguyễn Thanh Trà</p>
          </a>
        </div>
      </div>
    </section>
  </main>
  <footer>
    <div class="footer-content">
      <div class="footer-brand">
        <h3 data-i18n="site-title">Blog Lập Trình Mạng</h3>
        <p class="footer-tagline" data-i18n="footer-tagline">Xây dựng giải pháp mở rộng với đam mê</p>
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
        <p><span data-i18n="footer-copyright">© 2025</span> <span data-i18n="site-title">Blog Lập Trình Mạng</span>. <span data-i18n="rights">All rights reserved.</span></p>
      </div>
    </div>
  </footer>'''

# Tìm tất cả file HTML trong public/posts/ (không bao gồm index)
files = glob.glob(os.path.join('public', 'posts', '*.html'))
files = [f for f in files if 'index' not in os.path.basename(f)]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm vị trí bắt đầu contact-section
    start_marker = '<section class="contact-section">'
    end_marker = '</footer>'
    
    if start_marker in content and end_marker in content:
        # Tìm vị trí
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker, start_idx) + len(end_marker)
        
        # Thay thế
        new_content = content[:start_idx] + new_section + content[end_idx:]
        
        # Ghi lại file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'✓ Đã sửa: {os.path.basename(filepath)}')
    else:
        print(f'⚠ Bỏ qua (không tìm thấy contact-section): {os.path.basename(filepath)}')

print('\nHoàn thành!')
