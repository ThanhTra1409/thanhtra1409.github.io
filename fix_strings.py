with open('generate_static.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Use hex escapes to avoid encoding issues
text = text.replace('\u004c\u0069\u00c3\u00aa\u006e\u0020\u0068\u00e1\u00bb\u0087\u0020\u0076\u00e1\u00bb\u009b\u0069\u0020\u0074\u00c3\u00b4\u0069', 'Liên hệ với tôi')
text = text.replace('\u00f0\u009f\u0093\u00a7', '\U0001f4e7')
text = text.replace('\u00f0\u009f\u0093\u00b1', '\U0001f4f1')
text = text.replace('\u0053\u00c4\u0054', 'SĐT')
text = text.replace('\u00f0\u009f\u0093\u008d', '\U0001f4cd')
text = text.replace('\u00c4\u0111\u00e1\u00bb\u008b\u0061\u0020\u0063\u0068\u00e1\u00bb\u0089', 'Địa chỉ')
text = text.replace('\u0048\u00e1\u00bb\u0093', 'Hồ')
text = text.replace('\u0043\u0068\u00c3\u00ad', 'Chí')
text = text.replace('\u00f0\u009f\u0094\u0097', '\U0001f517')

with open('generate_static.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print('Fixed all strings!')
