# Blog Lập Trình Mạng — Hugo (Mẫu tối giản trắng-đen)

Hướng dẫn nhanh để chạy site này local với Hugo và deploy lên GitHub Pages.

Yêu cầu:
- Cài Hugo (https://gohugo.io/)
- Git và tài khoản GitHub

Chạy local:

```powershell
hugo server -D
```

Xây dựng tĩnh:

```powershell
hugo
```

Để deploy trên GitHub Pages, tạo repo, push nội dung `public/` (hoặc dùng actions). Thay `baseURL` trong `config.toml` trước khi build.
