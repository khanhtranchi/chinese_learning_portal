# Tổng Kết Dự Án - Chinese Docusaurus

## 📋 Mô Tả Dự Án

Dự án website học tiếng Trung sử dụng Docusaurus, với các tính năng:
- Hiển thị bài học từ file JSON
- Tự động tạo audio với giọng đọc riêng cho từng nhân vật
- Hướng dẫn viết chữ Hán bằng animation (Hanzi Writer)
- Phương pháp chiết tự để nhớ mặt chữ

## 📁 Cấu Trúc Dự Án

```
chinese_docusaurus/
├── docs/                          # Tài liệu bài học
│   └── hsk1/
│       ├── _category_.json        # Category config cho sidebar
│       └── lesson-1.md            # Bài học mẫu
│
├── lessons/                       # Dữ liệu bài học (JSON)
│   └── hsk/
│       └── hsk1/
│           └── lesson1.json       # File JSON bài học
│
├── scripts/                       # Scripts tự động hóa
│   ├── generate_lesson_md.py      # Tạo markdown từ JSON
│   ├── generate_lesson_audio.py   # Tạo audio từ JSON
│   ├── generate_lesson.py        # Script tổng hợp
│   ├── update_components.py      # Cập nhật components trong markdown
│   └── README.md                  # Hướng dẫn sử dụng scripts
│
├── src/
│   └── components/
│       ├── AudioPlayButton.tsx           # Nút play audio
│       ├── AudioPlayButton.module.css
│       ├── ClickableCharacter.tsx        # Chữ Hán có thể click
│       ├── ClickableCharacter.module.css
│       ├── HanziWriterModal.tsx          # Modal hướng dẫn viết chữ
│       └── HanziWriterModal.module.css
│
├── static/
│   └── audio/                    # File audio
│       └── hsk1/
│           └── lesson-1/
│               ├── line-01.mp3
│               ├── line-02.mp3
│               └── ... (15 files)
│
├── docusaurus.config.ts          # Config Docusaurus
├── sidebars.ts                   # Sidebar config
├── package.json
└── PROJECT_SUMMARY.md            # File này
```

## 🎯 Cấu Trúc JSON Bài Học

File JSON bài học (`lessons/hsk/hsk1/lesson1.json`) có cấu trúc:

```json
{
  "id": "lesson_001_greetings",
  "title": "Bài 1: Chào hỏi cơ bản & Hỏi tên",
  "category": "Giao tiếp xã giao",
  "level": "HSK 1 (Sơ cấp)",
  "description": "Mô tả bài học...",
  "audio_url": null,
  "conversation": [
    {
      "id": 1,
      "speaker": "A",
      "text_cn": "你好！",
      "text_pinyin": "Nǐ hǎo!",
      "text_en": "Hello!"
    }
  ],
  "analysis": [
    {
      "chunk_cn": "你好",
      "chunk_pinyin": "Nǐ hǎo",
      "chunk_meaning": "Xin chào...",
      "characters": [
        {
          "char": "你",
          "pinyin": "Nǐ",
          "meaning": "Bạn",
          "mnemonic": "Mnemonic để nhớ...",
          "components": [
            {
              "part": "亻",
              "name": "Nhân đứng",
              "pinyin": "rén",
              "meaning": "Người"
            }
          ]
        }
      ]
    }
  ]
}
```

Xem chi tiết trong `json-structure.md`.

## 🔧 Components React

### 1. AudioPlayButton
**File:** `src/components/AudioPlayButton.tsx`

**Chức năng:**
- Hiển thị nút play (▶️) đơn giản, không có progress bar
- Phát audio ngay trong trang, không mở tab mới
- Tự động dừng audio khác khi phát audio mới

**Sử dụng:**
```md
<AudioPlayButton src="/audio/hsk1/lesson-1/line-01.mp3" />
```

### 2. ClickableCharacter
**File:** `src/components/ClickableCharacter.tsx`

**Chức năng:**
- Wrap chữ Hán, khi click sẽ mở modal hướng dẫn viết
- Hiển thị với style underline, có hover effect

**Sử dụng:**
```md
<ClickableCharacter char="你">你</ClickableCharacter>
```

### 3. HanziWriterModal
**File:** `src/components/HanziWriterModal.tsx`

**Chức năng:**
- Modal popup hiển thị animation thứ tự nét viết chữ Hán
- Sử dụng thư viện `hanzi-writer`
- Có nút "Xem lại" và "Luyện viết"

**Dependencies:**
- `hanzi-writer` (đã cài: `npm install hanzi-writer`)

## 📝 Scripts Tự Động Hóa

### 1. generate_lesson_md.py
**Mục đích:** Tạo file markdown từ JSON

**Cách dùng:**
```bash
python scripts/generate_lesson_md.py lessons/hsk/hsk1/lesson1.json
python scripts/generate_lesson_md.py lessons/hsk/hsk1/lesson1.json --output docs/hsk1/lesson-1.md
```

**Tính năng:**
- Tự động tạo front matter (id, title, description, sidebar_label)
- Tự động import components (AudioPlayButton, ClickableCharacter)
- Tạo bảng hội thoại với AudioPlayButton
- Tạo phần chiết tự với ClickableCharacter
- Format: Character → Components → Mnemonic
- Tự động extract số bài học từ JSON id hoặc filename

### 2. generate_lesson_audio.py
**Mục đích:** Tạo file audio từ JSON

**Cách dùng:**
```bash
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --rate=-20% --force
```

**Tính năng:**
- Tự động phát hiện tất cả speakers (A, B, C, D...)
- Tự động gán giọng cho từng nhân vật:
  - A → `zh-CN-XiaoxiaoNeural` (nữ)
  - B → `zh-CN-YunxiNeural` (nam)
  - C, D... → tự động gán theo round-robin
- Hỗ trợ `--rate` để điều chỉnh tốc độ đọc (mặc định: -20%)
- Tạo file audio riêng lẻ: `line-01.mp3`, `line-02.mp3`, ...

**Dependencies:**
- `edge-tts` (đã cài: `pip install edge-tts`)

### 3. generate_lesson.py
**Mục đích:** Script tổng hợp - tạo cả markdown và audio

**Cách dùng:**
```bash
# Tạo cả markdown và audio
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json

# Với tùy chọn
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --rate=-30% --force
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --skip-audio  # Chỉ tạo markdown
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --skip-md    # Chỉ tạo audio
```

## 🎨 Cấu Trúc Markdown Bài Học

File markdown có cấu trúc:

```markdown
---
id: lesson-1
title: "Bài 1: Chào hỏi cơ bản & Hỏi tên"
description: "..."
sidebar_label: "Bài 1"
---

import AudioPlayButton from '@site/src/components/AudioPlayButton';
import ClickableCharacter from '@site/src/components/ClickableCharacter';

## Giới thiệu nhanh
- **Chủ đề:** ...
- **Cấp độ:** ...
- **Mục tiêu:** ...

## Hội thoại mẫu
| # | Nhân vật | Tiếng Trung | Audio | Pinyin | Nghĩa |
| ... | ... | ... | <AudioPlayButton src="..." /> | ... | ... |

## Ghi chú sử dụng
- ...

## Chiết tự & ghi nhớ
### 你好 — Nǐ hǎo
> Mô tả...

- <ClickableCharacter char="你">你</ClickableCharacter> (Nǐ) – Bạn.
  - Thành phần:
    - 亻 Nhân đứng (rén) - Người
    - 尔 Nhĩ (ěr) - Ngươi/Bạn
  - Mnemonic: ...
```

## 🔄 Workflow Tạo Bài Học Mới

1. **Tạo file JSON** theo cấu trúc trong `json-structure.md`
   - Đặt trong `lessons/hsk/hsk1/lesson2.json`

2. **Chạy script tổng hợp:**
   ```bash
   python scripts/generate_lesson.py lessons/hsk/hsk1/lesson2.json
   ```
   - Tự động tạo `docs/hsk1/lesson-2.md`
   - Tự động tạo `static/audio/hsk1/lesson-2/line-*.mp3`

3. **Kiểm tra và chỉnh sửa:**
   - Xem file markdown đã tạo
   - Chỉnh sửa "Ghi chú sử dụng" nếu cần
   - Test audio và Hanzi Writer

## ⚙️ Cấu Hình Docusaurus

### docusaurus.config.ts
- Đã xóa blog plugin
- Đã xóa tutorials menu
- Có menu HSK1 trong navbar
- Docs plugin vẫn hoạt động

### sidebars.ts
- Tự động generate từ cấu trúc thư mục `docs/`

## 📦 Dependencies

### Node.js packages:
- `@docusaurus/core`: 3.9.2
- `@docusaurus/preset-classic`: 3.9.2
- `hanzi-writer`: 3.7.3 (cho animation viết chữ)

### Python packages:
- `edge-tts`: 7.2.3 (cho tạo audio)

## 🚀 Lệnh Thường Dùng

```bash
# Start dev server
npm start

# Build production
npm run build

# Tạo bài học mới
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson2.json

# Tạo lại audio với tốc độ khác
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --rate=-30% --force
```

## 📝 Lưu Ý Quan Trọng

1. **File markdown:** Docusaurus hỗ trợ MDX, có thể dùng JSX components trực tiếp
2. **Audio paths:** Phải bắt đầu với `/` để trỏ đến `static/audio/`
3. **Giọng đọc:** Script tự động gán, có thể chỉnh trong `KNOWN_SPEAKER_VOICES`
4. **Tốc độ đọc:** Mặc định -20%, có thể điều chỉnh bằng `--rate`
5. **Hanzi Writer:** Cần cài `hanzi-writer`, component đã xử lý type với `@ts-ignore`

## 🔗 Tài Liệu Tham Khảo

- [Docusaurus Docs](https://docusaurus.io/)
- [Hanzi Writer](https://github.com/chanind/hanzi-writer)
- [Edge TTS](https://github.com/rany2/edge-tts)
- Cấu trúc JSON: `json-structure.md`
- Hướng dẫn scripts: `scripts/README.md`

---

**Cập nhật lần cuối:** Session hiện tại
**Trạng thái:** ✅ Hoàn thành và sẵn sàng sử dụng

