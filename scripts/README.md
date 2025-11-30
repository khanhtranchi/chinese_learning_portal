# Scripts Tự Động Hóa

Các script này giúp tự động tạo file markdown và audio từ file JSON bài học.

## Cài đặt và Thiết lập

Project này sử dụng [uv](https://github.com/astral-sh/uv) để quản lý môi trường Python và dependencies.

### Cài đặt uv (nếu chưa có)

```bash
# Trên WSL2/Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Hoặc với pip
pip install uv
```

### Thiết lập môi trường

```bash
# Tự động tạo virtual environment và cài đặt dependencies
uv sync

# Hoặc chỉ cài đặt dependencies vào môi trường hiện tại
uv pip install -e .
```

### Chạy scripts với uv

**Cách 1: Dùng `uv run` (khuyến nghị - không cần activate)**

```bash
# Chạy trực tiếp với uv run
uv run python3 scripts/generate_lesson.py lessons/hsk/hsk1/stories-2.json

# Hoặc với các script khác
uv run python3 scripts/generate_lesson_audio.py lessons/hsk/hsk1/stories-2.json
uv run python3 scripts/generate_lesson_md.py lessons/hsk/hsk1/stories-2.json
```

**Cách 2: Kích hoạt virtual environment trước**

```bash
# Kích hoạt virtual environment
source .venv/bin/activate  # Linux/WSL2/macOS
# hoặc
.venv\Scripts\activate  # Windows PowerShell

# Sau đó chạy script bình thường
python3 scripts/generate_lesson.py lessons/hsk/hsk1/stories-2.json
```

**Lưu ý:** `uv sync` sẽ tự động tạo virtual environment tại `.venv/` và cài đặt tất cả dependencies từ `pyproject.toml`.

## Cấu trúc

- `generate_lesson_md.py` - Tạo file markdown từ JSON
- `generate_lesson_audio.py` - Tạo file audio từ JSON
- `generate_lesson_exercise.py` - Sinh section **Bài Tập** vào markdown
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

# Chỉ tạo audio cho conversation (bỏ qua characters/chunks/components)
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --skip-characters

# Tạo lại audio dùng chung (characters + components)
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --hard-force-shared

# Chỉ in thông tin Bài Tập (dry-run)
python scripts/generate_lesson_exercise.py lessons/hsk/hsk1/lesson1.json --dry-run
```

### 4. Tạo/ghi đè section “Bài Tập”

```bash
# Append khối ExerciseSection vào docs/{category}/{code}.md
python scripts/generate_lesson_exercise.py lessons/hsk/hsk1/lesson1.json

# Ghi rõ docs root (nếu không nằm trong docs/)
python scripts/generate_lesson_exercise.py lessons/hsk/hsk1/lesson1.json --docs-root custom_docs/
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

Bỏ qua hoặc chỉ tạo audio cho characters/chunks/components (chỉ dùng với `generate_lesson_audio.py`).

### `--hard-force-shared`

Tạo lại audio dùng chung (character + component). Mặc định script **không** ghi đè những file này kể cả khi dùng `--force`.

## Ví dụ

```bash
# Tạo bài học mới từ JSON
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson2.json

# Tạo lại audio với tốc độ chậm hơn
python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --rate=-30% --force

# Bổ sung section Bài Tập
python scripts/generate_lesson_exercise.py lessons/hsk/hsk1/lesson1.json
```

## Cấu trúc file tự động

Script sẽ tự động tạo cấu trúc file dựa trên **category** và **code** từ JSON:

- JSON với `category: "HSK1"`, `code: "lesson-1"` → `docs/HSK1/lesson-1.md`
- JSON với `category: "HSK1"`, `code: "lesson-1"` → `static/audio/HSK1/lesson-1/line-*.mp3` (conversation)
- JSON với `category: "HSK1"`, `code: "lesson-1"` → `static/audio/HSK1/lesson-1/chunk-*.mp3` (chunks - **riêng cho từng bài học**)
- Tất cả bài học → `static/audio/characters/char-*.mp3` (characters - **dùng chung cho TẤT CẢ bài học**)
- Tất cả bài học → `static/audio/components/component-*.mp3` (radicals/parts - **dùng chung cho TẤT CẢ bài học**)

**Lưu ý quan trọng:**

- **category** trong JSON → dùng làm parent folder (ví dụ: `HSK1`, `HSK2`, `Grammar`, ...)
- **code** trong JSON → dùng làm tên file markdown và folder audio (ví dụ: `lesson-1`, `lesson-2`, ...)
- Audio cho conversation được lưu riêng cho từng bài học: `static/audio/{category}/{code}/line-*.mp3`
- Audio cho chunks (chunk_cn) được lưu riêng cho từng bài học: `static/audio/{category}/{code}/chunk-*.mp3`
- Audio cho characters được lưu **chung cho TẤT CẢ bài học** (không phân category): `static/audio/characters/char-*.mp3`
- Audio cho components (radical/parts) cũng lưu **chung cho TẤT CẢ bài học**: `static/audio/components/component-*.mp3`
- Mỗi character/component có tên file dựa trên Unicode code point (ví dụ: `char-4F60.mp3`, `component-4EBB.mp3`)
- Mỗi chunk sẽ có một file audio riêng với tên theo thứ tự: `chunk-01.mp3`, `chunk-02.mp3`, ...
- Khi tạo bài học mới, script sẽ tự động kiểm tra và dùng lại audio character/component đã có (`--hard-force-shared` mới ghi đè)
- Audio cho chunks KHÔNG dùng chung, mỗi bài học có audio riêng cho các chunks của nó

## Lưu ý

- **Dependencies được quản lý bằng uv**: Chạy `uv sync` để cài đặt `edge-tts` và các dependencies khác
- File JSON phải tuân theo cấu trúc trong `json-structure.md`
- File JSON **bắt buộc** phải có 2 trường: `category` (parent folder) và `code` (tên file/folder)
- Script sẽ tự động gán giọng cho các nhân vật mới
- Audio cho characters/components/chunks được tạo với tốc độ chậm hơn (mặc định -40%) để dễ học phát âm
- Mỗi character và component trong markdown sẽ có nút play kế bên để nghe phát âm
- Mỗi chunk (phần header của section) sẽ có nút play kèm theo
- **Audio character/component được dùng chung cho TẤT CẢ bài học**: chỉ khi chạy `--hard-force-shared` mới ghi đè
- **Audio chunk riêng cho từng bài học**: mỗi bài học có audio riêng cho các chunks của nó, không dùng chung
- `generate_lesson_exercise.py` luôn chèn block Bài Tập ngay sau “Giới thiệu nhanh” và thêm anchor ở cuối file để nhảy ngược lại
