# -*- coding: utf-8 -*-
# Script to recreate clean contact sections with Font Awesome icons

import codecs

# Read current file
with codecs.open('generate_static.py', 'r', 'utf-8') as f:
    lines = f.readlines()

# Find and replace contact sections
new_lines = []
in_contact = False
skip_until_section_end = False

contact_html = '''    <section class="contact-section">
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
'''

for line in lines:
    if 'class="contact-section"' in line:
        in_contact = True
        skip_until_section_end = True
        new_lines.append(contact_html)
        continue
    
    if skip_until_section_end:
        if '</section>' in line and in_contact:
            skip_until_section_end = False
            in_contact = False
        continue
    
    # Add Font Awesome to head if not present
    if '<link rel="stylesheet" href="/css/style.css">' in line and 'font-awesome' not in ''.join(new_lines[-5:]):
        new_lines.append(line)
        new_lines.append('  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">\n')
        continue
    
    new_lines.append(line)

# Write back
with codecs.open('generate_static.py', 'w', 'utf-8') as f:
    f.writelines(new_lines)

print('Recreated contact sections with Font Awesome icons!')
