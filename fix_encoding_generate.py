# -*- coding: utf-8 -*-
import codecs

# Read the file with potential encoding issues
with codecs.open('generate_static.py', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix common encoding issues
replacements = {
    'Xã hội': 'Xã hội',
    'Nguyễn Thanh Trà': 'Nguyễn Thanh Trà',
    'Thông tin liên hệ': 'Thông tin liên hệ',
    'Xin chào, mình là': 'Xin chào, mình là',
    'Công nghệ Phần mềm': 'Công nghệ Phần mềm',
    'là lĩnh vực ứng dụng kiến thức khoa học máy tính để thiết kế, phát triển và duy trì các hệ thống phần mềm chất lượng cao.': 'là lĩnh vực ứng dụng kiến thức khoa học máy tính để thiết kế, phát triển và duy trì các hệ thống phần mềm chất lượng cao.',
    'Từ': 'Từ',
    'đến': 'đến',
    '— mỗi dự án là một thử thách giải quyết vấn đề thực tế bằng công nghệ.': '— mỗi dự án là một thử thách giải quyết vấn đề thực tế bằng công nghệ.',
    'Chuyên về': 'Chuyên về',
    'và': 'và',
    ', tôi tập trung xây dựng các giải pháp backend hiệu quả, scalable và bảo mật.': ', tôi tập trung xây dựng các giải pháp backend hiệu quả, scalable và bảo mật.',
    'Xem portfolio': 'Xem portfolio',
    'Liên hệ': 'Liên hệ',
}

for old, new in replacements.items():
    if old != new:
        content = content.replace(old, new)

# Write back with correct encoding
with codecs.open('generate_static.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed encoding in generate_static.py")
