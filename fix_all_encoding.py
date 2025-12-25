# -*- coding: utf-8 -*-
# This script will fix all encoding issues in generate_static.py

with open('generate_static.py', 'rb') as f:
    data = f.read()

# The file was saved with wrong encoding - strings are actually Latin-1 encoded UTF-8
# We need to decode as Latin-1, then re-encode to UTF-8
text = data.decode('latin-1')

# Now fix the double-encoded strings
corrections = {
    'Xin chÃ o, mÃ¬nh lÃ ': 'Xin chào, mình là',
    'Nguyá»…n Thanh TrÃ ': 'Nguyễn Thanh Trà',
    'CÃ´ng nghá»‡ Pháº§n má»m': 'Công nghệ Phần mềm',
    'lÃ  lÄ©nh vá»±c á»©ng dá»¥ng kiáº¿n thá»©c khoa há»c mÃ¡y tÃ­nh Ä'á»ƒ thiáº¿t káº¿, phÃ¡t triá»ƒn vÃ  duy trÃ¬ cÃ¡c há»‡ thá»'ng pháº§n má»m cháº¥t lÆ°á»£ng cao.': 'là lĩnh vực ứng dụng kiến thức khoa học máy tính để thiết kế, phát triển và duy trì các hệ thống phần mềm chất lượng cao.',
    'Tá»«': 'Từ',
    'Ä'áº¿n': 'đến',
    'â€"': '—',
    'má»—i dá»± Ã¡n lÃ  má»™t thá»­ thÃ¡ch giáº£i quyáº¿t váº¥n Ä'á» thá»±c táº¿ báº±ng cÃ´ng nghá»‡.': 'mỗi dự án là một thử thách giải quyết vấn đề thực tế bằng công nghệ.',
    'ChuyÃªn vá»': 'Chuyên về',
    'vÃ ': 'và',
    ', tÃ´i táº­p trung xÃ¢y dá»±ng cÃ¡c giáº£i phÃ¡p backend hiá»‡u quáº£, scalable vÃ  báº£o máº­t.': ', tôi tập trung xây dựng các giải pháp backend hiệu quả, scalable và bảo mật.',
    'â˜°': '☰',
    'â€¢': '•',
    'Â©': '©',
    'ðŸ"§': '📧',
    'ðŸ"±': '📱',
    'SÄT': 'SĐT',
    'ðŸ"': '📍',
    'Äá»‹a chá»‰': 'Địa chỉ',
    'Há»"': 'Hồ',
    'ChÃ­': 'Chí',
    'ðŸ"—': '🔗',
    'LiÃªn há»‡ vá»›i tÃ´i': 'Liên hệ với tôi',
}

for wrong, correct in corrections.items():
    text = text.replace(wrong, correct)

# Write with proper UTF-8
with open('generate_static.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed all encoding issues!')
