#!/usr/bin/env python3
"""
Script tổng hợp để tạo cả markdown và audio cho bài học từ JSON.

Usage:
    python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json
    python scripts/generate_lesson.py lessons/hsk/hsk1/lesson1.json --rate=-20% --force
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate both markdown and audio files from lesson JSON."
    )
    parser.add_argument(
        "json_file",
        type=Path,
        help="Path to lesson JSON file (e.g., lessons/hsk/hsk1/lesson1.json)",
    )
    parser.add_argument(
        "--rate",
        type=str,
        default="-20%",
        help="Speech rate adjustment for conversation audio (default: -20%%)",
    )
    parser.add_argument(
        "--char-rate",
        type=str,
        default="-40%",
        help="Speech rate adjustment for character audio (default: -40%%)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate files even if they already exist.",
    )
    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Skip audio generation, only generate markdown.",
    )
    parser.add_argument(
        "--skip-md",
        action="store_true",
        help="Skip markdown generation, only generate audio.",
    )
    parser.add_argument(
        "--skip-characters",
        action="store_true",
        help="Skip character audio generation, only generate conversation audio.",
    )
    args = parser.parse_args(argv)
    
    if not args.json_file.exists():
        parser.error(f"JSON file not found: {args.json_file}")
    
    scripts_dir = Path(__file__).parent
    
    # Generate markdown
    if not args.skip_md:
        print("📝 Generating markdown...")
        md_script = scripts_dir / "generate_lesson_md.py"
        md_args = [str(args.json_file)]
        # Note: generate_lesson_md.py doesn't support --force, it always overwrites
        result = subprocess.run(
            [sys.executable, str(md_script)] + md_args,
            check=False,
        )
        if result.returncode != 0:
            print("⚠️  Markdown generation failed!")
            return result.returncode
        print()
    
    # Generate audio
    if not args.skip_audio:
        print("🎵 Generating audio...")
        audio_script = scripts_dir / "generate_lesson_audio.py"
        audio_args = [str(args.json_file), f"--rate={args.rate}", f"--char-rate={args.char_rate}"]
        if args.force:
            audio_args.append("--force")
        if args.skip_characters:
            audio_args.append("--skip-characters")
        result = subprocess.run(
            [sys.executable, str(audio_script)] + audio_args,
            check=False,
        )
        if result.returncode != 0:
            print("⚠️  Audio generation failed!")
            return result.returncode
        print()
    
    print("✅ Hoàn thành! Đã tạo markdown và audio cho bài học.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

