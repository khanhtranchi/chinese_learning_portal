# Hướng Dẫn Deploy Lên GitHub Pages

## Bước 1: Tạo Repository trên GitHub

1. Đăng nhập vào GitHub
2. Tạo repository mới:
   - Vào https://github.com/new
   - Đặt tên repository (ví dụ: `chinese-docusaurus`)
   - Chọn **Public** (để dùng GitHub Pages miễn phí)
   - **KHÔNG** tích "Initialize with README" (nếu bạn đã có code)
   - Click "Create repository"

### ⚠️ Lưu ý về Public vs Private:

- **Public Repository**: 
  - ✅ GitHub Pages miễn phí
  - ✅ Ai cũng có thể xem code và website
  - ✅ Phù hợp cho project open source hoặc tài liệu công khai

- **Private Repository**:
  - ❌ GitHub Pages miễn phí KHÔNG hỗ trợ private repo
  - ✅ Cần GitHub Pro ($4/tháng) hoặc Team/Enterprise để dùng GitHub Pages
  - ✅ Hoặc dùng dịch vụ khác: Vercel, Netlify (hỗ trợ private repo miễn phí)

## Bước 2: Cấu hình docusaurus.config.ts

Cập nhật file `docusaurus.config.ts` với thông tin GitHub của bạn:

```typescript
const config: Config = {
  title: 'Học Tiếng Trung', // Tên website
  tagline: 'Website học tiếng Trung với Docusaurus',
  url: 'https://YOUR_USERNAME.github.io', // Thay YOUR_USERNAME
  baseUrl: '/chinese-docusaurus/', // Thay bằng tên repository của bạn
  
  organizationName: 'YOUR_USERNAME', // Thay YOUR_USERNAME
  projectName: 'chinese-docusaurus', // Thay bằng tên repository
  
  // ... rest of config
}
```

**Lưu ý:**
- Nếu repository là `username.github.io`, thì `baseUrl` phải là `/`
- Nếu repository có tên khác, thì `baseUrl` phải là `/repository-name/`

## Bước 3: Khởi tạo Git và Push Code

```bash
# Khởi tạo git (nếu chưa có)
git init

# Thêm remote
git remote add origin https://github.com/YOUR_USERNAME/chinese-docusaurus.git

# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit: Chinese learning website with Docusaurus"

# Push lên GitHub
git branch -M main
git push -u origin main
```

## Bước 4: Cấu hình GitHub Pages

### Sử dụng GitHub Actions (Khuyến nghị)

1. File `.github/workflows/deploy.yml` đã được tạo sẵn trong project
2. Push code lên GitHub (file workflow sẽ tự động được thêm)
3. Bật GitHub Pages:
   - Vào repository → Settings → Pages
   - Source: chọn "GitHub Actions"
   - Save

### Cách 2: Sử dụng gh-pages branch (Cách cũ)

```bash
# Cài đặt gh-pages (nếu chưa có)
npm install --save-dev gh-pages

# Deploy
npm run deploy
```

Sau đó vào Settings → Pages → Source: chọn branch `gh-pages`

## Bước 5: Kiểm tra Website

Sau khi deploy thành công, website sẽ có tại:
- `https://YOUR_USERNAME.github.io/chinese-docusaurus/` (nếu repository có tên)
- `https://YOUR_USERNAME.github.io/` (nếu repository là `username.github.io`)

## Bước 6: Cập nhật Code và Deploy Tự Động

Sau khi setup GitHub Actions, mỗi khi bạn push code lên branch `main`, website sẽ tự động được build và deploy.

```bash
# Làm việc bình thường
git add .
git commit -m "Update content"
git push origin main

# GitHub Actions sẽ tự động deploy
```

## Lưu Ý Quan Trọng

1. **File .gitignore**: Đảm bảo không commit các file không cần thiết:
   - `node_modules/`
   - `.docusaurus/`
   - `build/`
   - `.env`

2. **Audio Files**: Các file audio trong `static/audio/` sẽ được deploy cùng website. Đảm bảo kích thước repository không quá lớn (GitHub có giới hạn).

3. **Environment Variables**: Nếu có API keys hoặc secrets, không commit vào repository. Sử dụng GitHub Secrets.

4. **Custom Domain** (Tùy chọn):
   - Vào Settings → Pages → Custom domain
   - Thêm domain của bạn
   - Thêm file `CNAME` vào thư mục `static/`

## Alternatives: Deploy Private Repository

Nếu bạn muốn dùng **Private Repository** nhưng không muốn trả phí GitHub Pro, có thể dùng:

### Option 1: Vercel (Miễn phí, hỗ trợ private repo)

1. Đăng ký tại https://vercel.com (dùng GitHub account)
2. Import repository từ GitHub
3. Vercel tự động detect Docusaurus và deploy
4. Website sẽ có tại: `https://your-project.vercel.app`

**Ưu điểm:**
- ✅ Miễn phí cho private repo
- ✅ Tự động deploy khi push code
- ✅ Custom domain miễn phí
- ✅ SSL tự động

### Option 2: Netlify (Miễn phí, hỗ trợ private repo)

1. Đăng ký tại https://www.netlify.com (dùng GitHub account)
2. New site from Git → Chọn repository
3. Build settings:
   - Build command: `npm run build`
   - Publish directory: `build`
4. Deploy site

**Ưu điểm:**
- ✅ Miễn phí cho private repo
- ✅ Tự động deploy khi push code
- ✅ Custom domain miễn phí
- ✅ Form handling, Functions

### Option 3: GitHub Pro ($4/tháng)

Nếu muốn tiếp tục dùng GitHub Pages với private repo:
- Upgrade lên GitHub Pro
- Private repo sẽ có thể dùng GitHub Pages

## Troubleshooting

### Lỗi 404 khi truy cập website
- Kiểm tra `baseUrl` trong `docusaurus.config.ts` có đúng không
- Đảm bảo GitHub Pages đã được bật

### Build failed trên GitHub Actions
- Kiểm tra Node version trong workflow (phải >= 20)
- Xem logs trong tab Actions để biết lỗi cụ thể

### Website không cập nhật
- Đợi vài phút (GitHub Actions cần thời gian build)
- Kiểm tra tab Actions xem có lỗi không
- Clear cache trình duyệt (Ctrl+Shift+R)

