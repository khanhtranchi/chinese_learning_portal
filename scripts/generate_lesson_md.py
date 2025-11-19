#!/usr/bin/env python3
"""
Script để tạo file markdown cho bài học từ JSON.

Usage:
    python scripts/generate_lesson_md.py lessons/hsk/hsk1/lesson1.json
    python scripts/generate_lesson_md.py lessons/hsk/hsk1/lesson1.json --output docs/hsk1/lesson-1.md
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def format_component(comp: dict) -> str:
    """Format component với đầy đủ pinyin và meaning."""
    part = comp["part"]
    name = comp["name"]
    pinyin = comp.get("pinyin", "")
    meaning = comp.get("meaning", "")
    
    if pinyin and meaning:
        return f"    - {part} {name} ({pinyin}) - {meaning}"
    elif pinyin:
        return f"    - {part} {name} ({pinyin})"
    else:
        return f"    - {part} {name}"


def generate_markdown(json_path: Path, output_path: Path) -> None:
    """Generate markdown file từ JSON."""
    # Đọc JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extract metadata từ JSON
    title = data.get("title", "Bài học")
    description = data.get("description", "")
    category = data.get("category", "")  # Dùng làm parent folder
    code = data.get("code", "")  # Dùng làm tên file và folder
    level = data.get("level", "")
    
    # Tạo sidebar_label dựa trên code và title
    sidebar_label = None
    if code:
        # Xử lý các loại khác nhau
        if code.startswith("lesson-"):
            # lesson-1 → "Bài 1", lesson-2 → "Bài 2"
            num_match = re.search(r"lesson-(\d+)", code)
            if num_match:
                sidebar_label = f"Bài {num_match.group(1)}"
        elif code.startswith("stories-"):
            # stories-1 → "Stories 1", stories-2 → "Stories 2"
            num_match = re.search(r"stories-(\d+)", code)
            if num_match:
                sidebar_label = f"Stories {num_match.group(1)}"
        elif code.startswith("grammar-"):
            # grammar-1 → "Grammar 1"
            num_match = re.search(r"grammar-(\d+)", code)
            if num_match:
                sidebar_label = f"Grammar {num_match.group(1)}"
        elif code.startswith("vocab-"):
            # vocab-1 → "Vocab 1"
            num_match = re.search(r"vocab-(\d+)", code)
            if num_match:
                sidebar_label = f"Vocab {num_match.group(1)}"
    
    # Fallback: thử extract từ title nếu chưa có
    if not sidebar_label:
        sidebar_match = re.search(r"Bài\s+(\d+)", title)
        if sidebar_match:
            sidebar_label = f"Bài {sidebar_match.group(1)}"
        else:
            sidebar_label = "Bài học"  # Fallback cuối cùng
    
    # Dùng code từ JSON làm doc_id, fallback nếu không có
    doc_id = code if code else "lesson-1"
    
    # Tính sidebar_position dựa trên code để sắp xếp động
    # Mapping prefix → base position (có thể mở rộng cho nhiều loại)
    # Format: {prefix}-{number} → base_position + number
    POSITION_MAP = {
        "lesson": 0,      # lesson-1 → 1, lesson-2 → 2, ...
        "stories": 100,   # stories-1 → 101, stories-2 → 102, ...
        "grammar": 200,   # grammar-1 → 201, grammar-2 → 202, ...
        "vocab": 300,     # vocab-1 → 301, vocab-2 → 302, ...
        # Có thể thêm thêm các loại khác ở đây
    }
    
    sidebar_position = None
    if code:
        # Tìm prefix trong code (ví dụ: "lesson", "stories", "grammar", ...)
        for prefix, base_position in POSITION_MAP.items():
            if code.startswith(f"{prefix}-"):
                # Extract số từ code (ví dụ: lesson-1 → 1, stories-2 → 2)
                num_match = re.search(rf"{prefix}-(\d+)", code)
                if num_match:
                    number = int(num_match.group(1))
                    sidebar_position = base_position + number
                    break
    
    # Bắt đầu tạo markdown
    lines = []
    
    # Front matter
    lines.append("---")
    lines.append(f'id: {doc_id}')
    lines.append(f'title: "{title}"')
    lines.append(f'description: "{description}"')
    lines.append(f'sidebar_label: "{sidebar_label}"')
    if sidebar_position is not None:
        lines.append(f'sidebar_position: {sidebar_position}')
    lines.append("---")
    lines.append("")
    lines.append("import AudioPlayButton from '@site/src/components/AudioPlayButton';")
    lines.append("import ClickableCharacter from '@site/src/components/ClickableCharacter';")
    lines.append("")
    
    # Giới thiệu nhanh
    lines.append("## Giới thiệu nhanh")
    lines.append("")
    lines.append(f"- **Chủ đề:** {category}")
    lines.append(f"- **Cấp độ:** {level}")
    
    # Tạo mục tiêu từ conversation (có thể cải thiện sau)
    lines.append("- **Mục tiêu:** Học các mẫu câu trong bài học")
    lines.append("")
    
    # Hội thoại mẫu
    lines.append("## Hội thoại mẫu")
    lines.append("")
    lines.append("| #   | Nhân vật | Tiếng Trung    | Audio                                                      | Pinyin                 | Nghĩa                    |")
    lines.append("| --- | -------- | -------------- | ---------------------------------------------------------- | ---------------------- | ------------------------ |")
    
    conversation = data.get("conversation", [])
    for entry in conversation:
        line_id = entry.get("id")
        speaker = entry.get("speaker", "")
        text_cn = entry.get("text_cn", "")
        text_pinyin = entry.get("text_pinyin", "")
        text_en = entry.get("text_en", "")
        
        # Tạo đường dẫn audio: dùng category và code từ JSON
        # /audio/{category}/{code}/line-*.mp3
        audio_path = f"/audio/{category}/{code}/line-{int(line_id):02}.mp3"
        
        lines.append(
            f"| {line_id}   | {speaker}        | {text_cn}         | "
            f"<AudioPlayButton src=\"{audio_path}\" /> | {text_pinyin}                | {text_en}                   |"
        )
    
    lines.append("")
    
    # Ghi chú sử dụng (có thể để trống hoặc tự động tạo từ conversation)
    lines.append("## Ghi chú sử dụng")
    lines.append("")
    lines.append("_Các ghi chú về cách sử dụng các mẫu câu trong bài học._")
    lines.append("")
    
    # Chiết tự & ghi nhớ
    lines.append("## Chiết tự & ghi nhớ")
    lines.append("")
    
    analysis = data.get("analysis", [])
    chunk_index = 0
    for analysis_item in analysis:
        chunk_cn = analysis_item.get("chunk_cn", "")
        chunk_pinyin = analysis_item.get("chunk_pinyin", "")
        chunk_meaning = analysis_item.get("chunk_meaning", "")
        
        # Tạo đường dẫn audio cho chunk (riêng cho bài học này)
        chunk_index += 1
        chunk_audio_path = f"/audio/{category}/{code}/chunk-{chunk_index:02}.mp3"
        
        # Section header với AudioPlayButton
        lines.append(f"### {chunk_cn} — {chunk_pinyin} <AudioPlayButton src=\"{chunk_audio_path}\" />")
        lines.append("")
        lines.append(f"> {chunk_meaning}")
        lines.append("")
        
        # Characters
        characters = analysis_item.get("characters", [])
        for char_data in characters:
            char = char_data.get("char", "")
            pinyin = char_data.get("pinyin", "")
            meaning = char_data.get("meaning", "")
            mnemonic = char_data.get("mnemonic", "")
            components = char_data.get("components", [])
            
            # Tạo đường dẫn audio cho character (dùng chung cho TẤT CẢ bài học)
            # Audio được lưu trong thư mục chung: /audio/characters/ (không phân level)
            char_code = ord(char)
            char_audio_path = f"/audio/characters/char-{char_code:04X}.mp3"
            
            # Character line với ClickableCharacter và AudioPlayButton
            lines.append(
                f"- <ClickableCharacter char=\"{char}\">{char}</ClickableCharacter> ({pinyin}) – {meaning}. "
                f"<AudioPlayButton src=\"{char_audio_path}\" />"
            )
            
            # Components
            if components:
                lines.append("  - Thành phần:")
                for comp in components:
                    lines.append(format_component(comp))
            
            # Mnemonic sau components
            if mnemonic:
                lines.append(f"  - Mnemonic: {mnemonic}")
            
            lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append("✅ **Gợi ý luyện tập:** Thực hành hội thoại theo cặp, thay tên và cảm xúc khác nhau. "
                 "Ghi âm lại, so sánh với bản chuẩn để điều chỉnh phát âm.")
    
    # Ghi file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ Đã tạo file markdown: {output_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate markdown file from lesson JSON."
    )
    parser.add_argument(
        "json_file",
        type=Path,
        help="Path to lesson JSON file (e.g., lessons/hsk/hsk1/lesson1.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output markdown file path (default: auto-generate from JSON path)",
    )
    args = parser.parse_args(argv)
    
    if not args.json_file.exists():
        parser.error(f"JSON file not found: {args.json_file}")
    
    # Tự động tạo output path nếu không có: dùng category và code từ JSON
    if args.output is None:
        # Đọc JSON để lấy category và code
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        category = data.get("category", "")
        code = data.get("code", "")
        
        if not category or not code:
            parser.error("JSON file must contain 'category' and 'code' fields")
        
        # docs/{category}/{code}.md
        args.output = Path("docs") / category / f"{code}.md"
    
    generate_markdown(args.json_file, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

