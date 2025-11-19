# Scripts Tự Động Hóa

Các script này giúp tự động tạo file markdown và audio từ file JSON bài học.

## Cấu trúc

- `generate_lesson_md.py` - Tạo file markdown từ JSON
- `generate_lesson_audio.py` - Tạo file audio từ JSON
- `generate_lesson.py` - Script tổng hợp (tạo cả markdown và audio)

## Cách sử dụng

### 1. Tạo cả markdown và audio (Khuyến nghị)

```bash
# Tạo cả markdown và audio (bao gồm cả audio cho từng character)
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json

# Với tốc độ đọc tùy chỉnh
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --rate=-30% --char-rate=-50%

# Tạo lại tất cả (force)
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --force

# Bỏ qua audio cho characters (chỉ tạo audio cho conversation)
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --skip-characters
```

### 2. Chỉ tạo markdown

```bash
python scripts/generate_lesson_md.py lessons/hsk/hsk1/lesson1.json

# Chỉ định output path
python scripts/generate_lesson_md.py lessons/hsk/hsk1/lesson1.json --output docs/hsk1/lesson-1.md
```

### 3. Chỉ tạo audio

```bash
# Tạo cả audio cho conversation và characters
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json

# Với tốc độ đọc tùy chỉnh
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --rate=-25% --char-rate=-45%

# Tạo lại tất cả audio
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --force

# Chỉ tạo audio cho characters (bỏ qua conversation)
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --only-characters

# Chỉ tạo audio cho conversation (bỏ qua characters)
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --skip-characters
```

## Tùy chọn

### `--rate`
Điều chỉnh tốc độ đọc audio cho conversation:
- `-20%` (mặc định) - Chậm hơn 20%
- `-30%` - Chậm hơn 30%
- `-10%` - Chậm hơn 10%
- `+10%` - Nhanh hơn 10%

### `--char-rate`
Điều chỉnh tốc độ đọc audio cho từng character (chậm hơn để dễ học):
- `-40%` (mặc định) - Chậm hơn 40%
- `-50%` - Chậm hơn 50%
- `-30%` - Chậm hơn 30%

### `--force`
Tạo lại tất cả file, bỏ qua file đã tồn tại.

### `--skip-audio` / `--skip-md`
Bỏ qua việc tạo audio hoặc markdown (chỉ dùng với `generate_lesson.py`).

### `--skip-characters` / `--only-characters`
Bỏ qua hoặc chỉ tạo audio cho characters (chỉ dùng với `generate_lesson_audio.py`).

## Ví dụ

```bash
# Tạo bài học mới từ JSON
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson2.json

# Tạo lại audio với tốc độ chậm hơn
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --rate=-30% --force
```

## Cấu trúc file tự động

Script sẽ tự động tạo cấu trúc file dựa trên **category** và **code** từ JSON:

- JSON với `category: "HSK1"`, `code: "lesson-1"` → `docs/HSK1/lesson-1.md`
- JSON với `category: "HSK1"`, `code: "lesson-1"` → `static/audio/HSK1/lesson-1/line-*.mp3` (conversation)
- JSON với `category: "HSK1"`, `code: "lesson-1"` → `static/audio/HSK1/lesson-1/chunk-*.mp3` (chunks - **riêng cho từng bài học**)
- Tất cả bài học → `static/audio/characters/char-*.mp3` (characters - **dùng chung cho TẤT CẢ bài học**)

**Lưu ý quan trọng:**
- **category** trong JSON → dùng làm parent folder (ví dụ: `HSK1`, `HSK2`, `Grammar`, ...)
- **code** trong JSON → dùng làm tên file markdown và folder audio (ví dụ: `lesson-1`, `lesson-2`, ...)
- Audio cho conversation được lưu riêng cho từng bài học: `static/audio/{category}/{code}/line-*.mp3`
- Audio cho chunks (chunk_cn) được lưu riêng cho từng bài học: `static/audio/{category}/{code}/chunk-*.mp3`
- Audio cho characters được lưu **chung cho TẤT CẢ bài học** (không phân category): `static/audio/characters/char-*.mp3`
- Mỗi character sẽ có một file audio riêng với tên dựa trên Unicode code point (ví dụ: `char-4F60.mp3` cho chữ "你")
- Mỗi chunk sẽ có một file audio riêng với tên theo thứ tự: `chunk-01.mp3`, `chunk-02.mp3`, ...
- Khi tạo bài học mới, script sẽ tự động kiểm tra và dùng lại audio character đã có (trừ khi dùng `--force`)
- Cùng một chữ Hán sẽ chỉ tạo audio một lần duy nhất, tất cả các bài học đều dùng chung file đó
- Audio cho chunks KHÔNG dùng chung, mỗi bài học có audio riêng cho các chunks của nó

## Lưu ý

- Đảm bảo đã cài đặt `edge-tts`: `pip install edge-tts`
- File JSON phải tuân theo cấu trúc trong `json-structure.md`
- File JSON **bắt buộc** phải có 2 trường: `category` (parent folder) và `code` (tên file/folder)
- Script sẽ tự động gán giọng cho các nhân vật mới
- Audio cho characters và chunks được tạo với tốc độ chậm hơn (mặc định -40%) để dễ học phát âm
- Mỗi character trong markdown sẽ có nút play kế bên để nghe phát âm
- Mỗi chunk (phần header của section) sẽ có nút play kế bên để nghe phát âm
- **Audio character được dùng chung cho TẤT CẢ bài học**: cùng một chữ Hán sẽ chỉ tạo audio một lần duy nhất, tất cả các bài học (không phân level) sẽ tự động dùng lại
- **Audio chunk riêng cho từng bài học**: mỗi bài học có audio riêng cho các chunks của nó, không dùng chung

