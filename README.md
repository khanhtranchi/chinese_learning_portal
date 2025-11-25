# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Python Scripts và Audio Generation

Project này sử dụng [uv](https://github.com/astral-sh/uv) để quản lý môi trường Python và dependencies.

### Thiết lập Python Environment

```bash
# Cài đặt uv (nếu chưa có)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Thiết lập môi trường và cài đặt dependencies
uv sync
```

### Tạo Audio cho Bài Học

Scripts có thể tạo audio cho các bài học từ file JSON sử dụng [edge-tts](https://github.com/rany2/edge-tts):

```bash
# Sử dụng uv run để chạy script
uv run python scripts/generate_lesson.py lessons/hsk/hsk1/lesson-1.json

# Hoặc kích hoạt virtual environment trước
source .venv/bin/activate  # Linux/WSL2/macOS
python scripts/generate_lesson.py lessons/hsk/hsk1/lesson-1.json
```

Xem thêm chi tiết trong [scripts/README.md](scripts/README.md).

**Lưu ý:** Restart `yarn start` nếu dev server đang chạy để serve các file audio mới.
