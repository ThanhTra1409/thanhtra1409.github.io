# Fix encoding issues in generate_static.py
with open('generate_static.py', 'rb') as f:
    raw_data = f.read()

# Decode as latin-1 and fix
text = raw_data.decode('latin-1')

replacements = [
    ('LiÃªn há»‡ vá»›i tÃ´i', 'Liên hệ với tôi'),
    ('ðŸ"§', '📧'),
    ('ðŸ"±', '📱'),
    ('SÄT', 'SĐT'),
    ('ðŸ"', '📍'),
    ('Äá»‹a chá»‰', 'Địa chỉ'),
    ('Há»"', 'Hồ'),
    ('ChÃ­', 'Chí'),
    ('ðŸ"—', '🔗'),
    ('â€¢', '•'),
    ('Â©', '©'),
]

for old, new in replacements:
    text = text.replace(old, new)

# Write back with UTF-8
with open('generate_static.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("Fixed encoding!")
