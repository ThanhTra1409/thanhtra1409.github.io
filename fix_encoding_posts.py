# -*- coding: utf-8 -*-
"""
Script to fix encoding for all markdown files in content/posts/
Reads as latin-1, writes as utf-8, and applies common Vietnamese corrections.
"""
import os

# Corrections for common encoding errors
corrections = {
    'LiÃªn há»‡ vá»›i tÃ´i': 'Liên hệ với tôi',
    'ðŸ"§': '📧',
    'ðŸ"±': '📱',
    'SÄT': 'SĐT',
    'ðŸ"': '📍',
    'Äá»‹a chá»‰': 'Địa chỉ',
    'Há»"': 'Hồ',
    'ChÃ­': 'Chí',
    'ðŸ"—': '🔗',
    'â€¢': '•',
    'Â©': '©',
    'Nguyá»…n': 'Nguyễn',
    'CÃ´ng nghá»‡': 'Công nghệ',
    'pháº§n má»m': 'phần mềm',
    'lÃ  lÄ©nh vá»±c': 'là lĩnh vực',
    'kiáº¿n thá»©c': 'kiến thức',
    'phÃ¡t triá»ƒn': 'phát triển',
    'vÃ ': 'và',
    'má»—i dá»± Ã¡n': 'mỗi dự án',
    'thá»­ thÃ¡ch': 'thử thách',
    'giáº£i quyáº¿t váº¥n Ä'á» ': 'giải quyết vấn đề',
    'thá»±c táº¿': 'thực tế',
    'báº±ng cÃ´ng nghá»‡': 'bằng công nghệ',
    'ChuyÃªn vá»': 'Chuyên về',
    ', tÃ´i táº­p trung': ', tôi tập trung',
    'xÃ¢y dá»±ng': 'xây dựng',
    'giáº£i phÃ¡p': 'giải pháp',
    'hiá»‡u quáº£': 'hiệu quả',
    'scalable vÃ  báº£o máº­t': 'scalable và bảo mật',
    'Sinh viÃªn': 'Sinh viên',
    'TrÆ°á»ng': 'Trường',
    'Ä'áº¿n': 'đến',
    'Tá»«': 'Từ',
    'â€"': '—',
}

md_dir = os.path.join('content', 'posts')
for fname in os.listdir(md_dir):
    if fname.endswith('.md'):
        fpath = os.path.join(md_dir, fname)
        with open(fpath, 'rb') as f:
            raw = f.read()
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('latin-1')
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
print('Đã sửa encoding cho tất cả file markdown trong content/posts/')
