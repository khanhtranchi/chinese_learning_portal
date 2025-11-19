#!/usr/bin/env python3
"""
Script để tạo audio cho bài học từ JSON.

Usage:
    python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json
    python scripts/generate_lesson_audio.py lessons/hsk/hsk1/lesson1.json --rate=-20%
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Danh sách giọng đọc có sẵn (sẽ được gán tự động cho các nhân vật)
AVAILABLE_VOICES = [
    "zh-CN-XiaoxiaoNeural",  # Nữ, trẻ, tự nhiên
    "zh-CN-YunxiNeural",     # Nam, trẻ, tự nhiên
    "zh-CN-XiaoyiNeural",    # Nữ, trẻ, dịu dàng
    "zh-CN-YunjianNeural",   # Nam, trẻ, rõ ràng
    "zh-CN-XiaohanNeural",   # Nữ, trẻ, vui vẻ
    "zh-CN-YunxiaNeural",    # Nam, trẻ, thân thiện
]

# Giọng mặc định cho các nhân vật đã biết
KNOWN_SPEAKER_VOICES = {
    "A": "zh-CN-XiaoxiaoNeural",  # Nữ, trẻ, tự nhiên
    "B": "zh-CN-YunxiNeural",     # Nam, trẻ, tự nhiên
}


def find_edge_tts_command() -> list[str]:
    """Tìm cách gọi edge-tts: thử edge-tts, python3 -m edge_tts, hoặc python -m edge_tts."""
    print("🔍 Đang tìm edge-tts...")
    
    # Thử 1: edge-tts trực tiếp
    edge_tts_path = shutil.which("edge-tts")
    if edge_tts_path:
        print(f"  ✓ Tìm thấy: edge-tts tại {edge_tts_path}")
        return ["edge-tts"]
    else:
        print("  ✗ Không tìm thấy 'edge-tts' trong PATH")
    
    # Thử 2: sys.executable -m edge_tts (dùng cùng Python interpreter - ưu tiên nhất)
    print(f"  🔍 Thử: {sys.executable} -m edge_tts")
    try:
        # edge-tts không có --version, thử --list-voices thay thế
        result = subprocess.run(
            [sys.executable, "-m", "edge_tts", "--list-voices"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Nếu có output (dù returncode != 0 cũng OK, vì --list-voices có thể output nhiều)
        if "zh-CN" in result.stdout or result.returncode == 0:
            print(f"  ✓ Tìm thấy: {sys.executable} -m edge_tts")
            return [sys.executable, "-m", "edge_tts"]
        else:
            print(f"  ✗ Không phải edge-tts hợp lệ")
    except subprocess.TimeoutExpired:
        print("  ✗ Timeout khi kiểm tra")
    except FileNotFoundError:
        print("  ✗ Không tìm thấy Python interpreter")
    except Exception as e:
        print(f"  ✗ Lỗi: {e}")
    
    # Thử 3: python3 -m edge_tts
    python3_path = shutil.which("python3")
    if python3_path:
        print(f"  🔍 Thử: python3 -m edge_tts")
        try:
            result = subprocess.run(
                ["python3", "-m", "edge_tts", "--list-voices"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if "zh-CN" in result.stdout or result.returncode == 0:
                print(f"  ✓ Tìm thấy: python3 -m edge_tts")
                return ["python3", "-m", "edge_tts"]
            else:
                print(f"  ✗ Không phải edge-tts hợp lệ")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"  ✗ Lỗi: {e}")
    
    # Thử 4: python -m edge_tts
    python_path = shutil.which("python")
    if python_path:
        print(f"  🔍 Thử: python -m edge_tts")
        try:
            result = subprocess.run(
                ["python", "-m", "edge_tts", "--list-voices"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if "zh-CN" in result.stdout or result.returncode == 0:
                print(f"  ✓ Tìm thấy: python -m edge_tts")
                return ["python", "-m", "edge_tts"]
            else:
                print(f"  ✗ Không phải edge-tts hợp lệ")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"  ✗ Lỗi: {e}")
    
    print("  ❌ Không tìm thấy edge-tts bằng bất kỳ cách nào")
    return None


def check_edge_tts() -> list[str]:
    """Kiểm tra xem edge-tts có được cài đặt không và trả về command để gọi."""
    cmd = find_edge_tts_command()
    if cmd is None:
        print("❌ Lỗi: Không tìm thấy 'edge-tts'!")
        print("📦 Vui lòng cài đặt bằng một trong các lệnh sau:")
        print("   pip install edge-tts")
        print("   pip3 install edge-tts")
        print("   python3 -m pip install edge-tts")
        print("   python -m pip install edge-tts")
        sys.exit(1)
    return cmd


# Lưu command để dùng lại
_EDGE_TTS_CMD = None


def get_edge_tts_cmd() -> list[str]:
    """Lấy command để gọi edge-tts (cache lại để không phải tìm lại mỗi lần)."""
    global _EDGE_TTS_CMD
    if _EDGE_TTS_CMD is None:
        # check_edge_tts() sẽ exit nếu không tìm thấy, nên luôn trả về valid command
        _EDGE_TTS_CMD = check_edge_tts()
    return _EDGE_TTS_CMD


def run_edge_tts(text: str, output_path: Path, voice: str, rate: str = "-20%") -> None:
    """Invoke edge-tts CLI to synthesize text into output_path with rate control."""
    cmd = get_edge_tts_cmd() + [
        "--voice",
        voice,
        "--text",
        text,
        f"--rate={rate}",
        "--write-media",
        str(output_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi tạo audio: {e}")
        if e.stderr:
            print(f"Chi tiết lỗi: {e.stderr}")
        raise
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy 'edge-tts'!")
        print("📦 Vui lòng cài đặt bằng lệnh: pip install edge-tts")
        raise


def generate_audio(json_path: Path, output_dir: Path, rate: str = "-20%", force: bool = False) -> None:
    """Generate audio files từ JSON."""
    if force:
        print("  [Force mode: will regenerate all existing files]")
    # Đọc JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    conversation = data.get("conversation", [])
    if not conversation:
        print("⚠️  Không có conversation trong JSON!")
        return
    
    # Tạo output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Tự động phát hiện và gán giọng cho tất cả speakers
    all_speakers = set()
    for entry in conversation:
        speaker = entry.get("speaker", "").strip()
        if speaker:
            all_speakers.add(speaker)
    
    # Tạo voice mapping tự động
    voice_map = {}
    unknown_speakers = []
    for speaker in sorted(all_speakers):
        if speaker in KNOWN_SPEAKER_VOICES:
            voice_map[speaker] = KNOWN_SPEAKER_VOICES[speaker]
        else:
            unknown_speakers.append(speaker)
    
    # Gán giọng cho các speaker chưa biết theo thứ tự round-robin
    voice_index = 0
    for speaker in unknown_speakers:
        voice_map[speaker] = AVAILABLE_VOICES[voice_index % len(AVAILABLE_VOICES)]
        voice_index += 1
    
    # In ra thông tin mapping
    print("Voice mapping:")
    for speaker in sorted(voice_map.keys()):
        print(f"  {speaker} -> {voice_map[speaker]}")
    print()
    
    generated = 0
    skipped = 0
    
    for entry in conversation:
        line_id = entry.get("id")
        text = entry.get("text_cn", "").strip()
        speaker = entry.get("speaker", "").strip()
        if not line_id or not text:
            continue
        
        filename = f"line-{int(line_id):02}.mp3"
        output_path = output_dir / filename
        
        # Nếu file tồn tại và không có force, skip
        if output_path.exists() and not force:
            skipped += 1
            continue
        
        # Nếu có force và file tồn tại, sẽ tạo lại
        if output_path.exists() and force:
            print(f"  (Force: regenerating existing file)")
        
        # Chọn giọng dựa trên speaker mapping
        voice = voice_map.get(speaker, AVAILABLE_VOICES[0])
        print(f"Generating line {line_id} (Speaker: {speaker}, Voice: {voice}, Rate: {rate})...")
        
        run_edge_tts(text, output_path, voice, rate=rate)
        generated += 1
    
    print(
        f"\n✅ Audio generation completed. "
        f"{generated} file(s) generated, {skipped} skipped."
    )


def generate_character_audio(json_path: Path, rate: str = "-30%", force: bool = False) -> None:
    """Generate audio files cho từng character từ JSON với tốc độ chậm hơn.
    
    Audio được lưu vào thư mục chung: static/audio/characters/
    để có thể dùng lại cho TẤT CẢ các bài học (không phân level).
    """
    if force:
        print("  [Force mode: will regenerate all existing files]")
    # Đọc JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    analysis = data.get("analysis", [])
    if not analysis:
        print("⚠️  Không có analysis trong JSON!")
        return
    
    # Tạo output directory: static/audio/characters/ (dùng chung cho tất cả bài học)
    output_dir = Path("static") / "audio" / "characters"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Lưu character audio vào: {output_dir} (dùng chung cho tất cả bài học)")
    
    # Sử dụng giọng nữ mặc định cho characters (rõ ràng, dễ nghe)
    default_voice = "zh-CN-XiaoxiaoNeural"
    
    generated = 0
    skipped = 0
    
    # Thu thập tất cả characters
    all_characters = []
    for analysis_item in analysis:
        characters = analysis_item.get("characters", [])
        for char_data in characters:
            char = char_data.get("char", "").strip()
            if char:
                all_characters.append((char, char_data))
    
    print(f"Found {len(all_characters)} character(s) to generate audio for...")
    if force:
        print("  (Force mode: will regenerate all existing files)")
    print()
    
    for char, char_data in all_characters:
        # Tạo filename từ character (sử dụng Unicode code point để tránh vấn đề với ký tự đặc biệt)
        char_code = ord(char)
        filename = f"char-{char_code:04X}.mp3"
        output_path = output_dir / filename
        
        # Nếu file tồn tại và không có force, skip và báo
        if output_path.exists() and not force:
            print(f"⏭️  File đã tồn tại, bỏ qua: {char} ({filename})")
            skipped += 1
            continue
        
        # Nếu có force và file tồn tại, sẽ tạo lại
        if output_path.exists() and force:
            print(f"🔄 Force: tạo lại file cho {char} ({filename})")
        
        # Sử dụng chính character làm text để phát âm
        text = char
        print(f"🎵 Đang tạo audio cho: {char} (Voice: {default_voice}, Rate: {rate})...")
        
        run_edge_tts(text, output_path, default_voice, rate=rate)
        generated += 1
    
    print(
        f"\n✅ Character audio generation completed. "
        f"{generated} file(s) generated, {skipped} skipped."
    )


def generate_chunk_audio(json_path: Path, output_dir: Path, rate: str = "-30%", force: bool = False) -> None:
    """Generate audio files cho các chunk_cn từ JSON với tốc độ chậm hơn.
    
    Audio được lưu trong thư mục của bài học: static/audio/{category}/{code}/chunk-*.mp3
    KHÔNG dùng chung với các bài học khác.
    """
    if force:
        print("  [Force mode: will regenerate all existing files]")
    # Đọc JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    analysis = data.get("analysis", [])
    if not analysis:
        print("⚠️  Không có analysis trong JSON!")
        return
    
    # Tạo output directory: static/audio/{category}/{code}/ (riêng cho từng bài học)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Lưu chunk audio vào: {output_dir} (riêng cho bài học này)")
    
    # Sử dụng giọng nữ mặc định cho chunks (rõ ràng, dễ nghe)
    default_voice = "zh-CN-XiaoxiaoNeural"
    
    generated = 0
    skipped = 0
    
    # Thu thập tất cả chunks
    all_chunks = []
    chunk_index = 0
    for analysis_item in analysis:
        chunk_cn = analysis_item.get("chunk_cn", "").strip()
        if chunk_cn:
            chunk_index += 1
            all_chunks.append((chunk_cn, chunk_index))
    
    print(f"Found {len(all_chunks)} chunk(s) to generate audio for...")
    if force:
        print("  (Force mode: will regenerate all existing files)")
    print()
    
    for chunk_cn, chunk_index in all_chunks:
        # Tạo filename từ index (chunk-01.mp3, chunk-02.mp3, ...)
        filename = f"chunk-{chunk_index:02}.mp3"
        output_path = output_dir / filename
        
        # Nếu file tồn tại và không có force, skip và báo
        if output_path.exists() and not force:
            print(f"⏭️  File đã tồn tại, bỏ qua: {chunk_cn} ({filename})")
            skipped += 1
            continue
        
        # Nếu có force và file tồn tại, sẽ tạo lại
        if output_path.exists() and force:
            print(f"🔄 Force: tạo lại file cho {chunk_cn} ({filename})")
        
        # Sử dụng chunk_cn làm text để phát âm
        text = chunk_cn
        print(f"🎵 Đang tạo audio cho chunk: {chunk_cn} (Voice: {default_voice}, Rate: {rate})...")
        
        run_edge_tts(text, output_path, default_voice, rate=rate)
        generated += 1
    
    print(
        f"\n✅ Chunk audio generation completed. "
        f"{generated} file(s) generated, {skipped} skipped."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate audio files from lesson JSON."
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
        help="Output directory for audio files (default: auto-generate from JSON path)",
    )
    parser.add_argument(
        "--rate",
        type=str,
        default="-20%",
        help="Speech rate adjustment for conversation (e.g., '-20%%' for 20%% slower, default: -20%%)",
    )
    parser.add_argument(
        "--char-rate",
        type=str,
        default="-40%",
        help="Speech rate adjustment for characters (e.g., '-40%%' for 40%% slower, default: -40%%)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate audio even if the target file already exists.",
    )
    parser.add_argument(
        "--skip-characters",
        action="store_true",
        help="Skip character audio generation, only generate conversation audio.",
    )
    parser.add_argument(
        "--only-characters",
        action="store_true",
        help="Only generate character audio, skip conversation audio.",
    )
    args = parser.parse_args(argv)
    
    if not args.json_file.exists():
        parser.error(f"JSON file not found: {args.json_file}")
    
    # Debug: hiển thị trạng thái force
    if args.force:
        print(f"🔧 Force mode: ON (will regenerate all existing files)")
    else:
        print(f"🔧 Force mode: OFF (will skip existing files)")
    
    # Kiểm tra edge-tts trước khi tiếp tục và hiển thị command sẽ dùng
    edge_tts_cmd = check_edge_tts()
    print(f"🔧 Sử dụng edge-tts: {' '.join(edge_tts_cmd)}")
    
    # Đọc JSON để lấy category và code
    with open(args.json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    category = data.get("category", "")
    code = data.get("code", "")
    
    if not category or not code:
        parser.error("JSON file must contain 'category' and 'code' fields")
    
    # Tự động tạo output path cho conversation audio nếu không có
    # static/audio/{category}/{code}/
    if args.output is None:
        args.output = Path("static") / "audio" / category / code
    
    # Generate conversation audio
    if not args.only_characters:
        print("🎵 Generating conversation audio...")
        generate_audio(args.json_file, args.output, rate=args.rate, force=args.force)
        print()
    
    # Generate character audio (lưu vào thư mục chung cho tất cả bài học)
    if not args.skip_characters:
        print("🔤 Generating character audio...")
        generate_character_audio(args.json_file, rate=args.char_rate, force=args.force)
        print()
    
    # Generate chunk audio (lưu trong thư mục của bài học, không dùng chung)
    if not args.skip_characters:
        print("📝 Generating chunk audio...")
        generate_chunk_audio(args.json_file, args.output, rate=args.char_rate, force=args.force)
        print()
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

