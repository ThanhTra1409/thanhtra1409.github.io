# -*- coding: utf-8 -*-
"""Fix all encoding issues in generate_static.py"""

with open('generate_static.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix all Vietnamese characters that are showing incorrectly
replacements = {
    'Nguy�n': 'Nguyễn',
    'Công ngh�': 'Công nghệ',
    '��': 'để',
    'phát tri�n': 'phát triển',
    'h� th�ng': 'hệ thống',
    '�ến': 'đến',
    '� m�i': '— mỗi',
    'm�t': 'một',
    '�ề': 'đề',
    'hi�u': 'hiệu',
    'Liên h�': 'Liên hệ',
    'K�': 'Kỹ',
    'n�ng': 'năng',
    'Xây d�ng': 'Xây dựng',
    'v�i': 'với',
    'Phát tri�n': 'Phát triển',
    'Tri�n khai': 'Triển khai',
    '�ã': 'Đã',
    'H�': 'Hồ',
    'Ch�': 'Chí',
    'Đ�Địa chỉ�': 'Địa chỉ',
    'SĐT': 'SĐT',
    'SĐTATIC': 'STATIC',
    'RESĐTful': 'RESTful',
    'RESĐT API': 'REST API',
    'hư�ng ��i tượng': 'hướng đối tượng',
    'dữ li�u': 'dữ liệu',
    '�ại': 'Đại',
    'metĐịa chỉarset': 'charset',
    '☰': '☰',
    '�': '☰',
    'công ngh☰': 'công nghệ',
    'v☰ trí': 'vị trí',
    'có th☰': 'có thể',
    'l☰n': 'lớn',
    'nghi☰p': 'nghiệp',
    'đểi ngũ': 'đội ngũ',
}

for wrong, correct in replacements.items():
    text = text.replace(wrong, correct)

with open('generate_static.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('✓ Fixed all encoding issues in generate_static.py')
