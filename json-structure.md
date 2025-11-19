# JSON Structure Specification

## 1. Root Object

The output is a single JSON object representing a complete Lesson. It contains metadata about the lesson, the conversation flow, and the detailed lexical analysis.

### Root Fields:

- `id`: (String/Number) Unique identifier for the lesson (e.g., "lesson_001").
- `title`: (String) The name of the lesson (e.g., "Greetings & Introduction").
- `category`: (String) The topic/category (e.g., "Communication", "Travel").
- `level`: (String) Difficulty level (e.g., "HSK 1", "Beginner").
- `description`: (String) Short summary of learning objectives.
- `audio_url`: (String/Null) URL to the full audio recording of the conversation.
- `conversation`: (Array) The sequential dialogue lines.
- `analysis`: (Array) Detailed "Chiết tự" analysis of vocabulary.

---

## 2. Nested Field Definitions

### Key: `conversation` (Array)

Represents the dialogue flow.

- `id`: (Number) Sequence order.
- `speaker`: (String) The character speaking.
- `text_cn`: (String) Original Chinese text.
- `text_pinyin`: (String) Pinyin transcription.
- `text_en`: (String) English translation.

### Key: `analysis` (Array)

Represents the deep breakdown of vocabulary (Chunks -> Characters -> Components).

- `chunk_cn`: (String) The phrase/word in Chinese.
- `chunk_pinyin`: (String) Pinyin of the phrase.
- `chunk_meaning`: (String) Meaning in Vietnamese.
- `characters`: (Array) List of characters in the chunk.
  - `char`: (String) Single character.
  - `pinyin`: (String) Pinyin.
  - `meaning`: (String) Sino-Vietnamese/Basic meaning.
  - `mnemonic`: (String) Story to remember the character.
  - `components`: (Array) Radicals/parts.
    - `part`: (String) Radical character.
    - `name`: (String) Sino-Vietnamese name.
    - `pinyin`: (String) Pinyin.
    - `meaning`: (String) Meaning.

---

## 3. Example JSON

```json
{
  "id": "lesson_001",
  "title": "Bài 1: Chào hỏi và Làm quen",
  "category": "Giao tiếp xã giao",
  "level": "HSK 1",
  "description": "Học các mẫu câu chào hỏi cơ bản, cách hỏi tên và giới thiệu bản thân.",
  "audio_url": "[https://api.example.com/audio/lesson_001.mp3](https://api.example.com/audio/lesson_001.mp3)",
  "conversation": [
    {
      "id": 1,
      "speaker": "A",
      "text_cn": "你好！",
      "text_pinyin": "Nǐ hǎo!",
      "text_en": "Hello!"
    },
    {
      "id": 2,
      "speaker": "A",
      "text_cn": "你叫什么名字？",
      "text_pinyin": "Nǐ jiào shénme míngzi?",
      "text_en": "What is your name?"
    }
  ],
  "analysis": [
    {
      "chunk_cn": "你好",
      "chunk_pinyin": "Nǐ hǎo",
      "chunk_meaning": "Xin chào. Dùng để chào hỏi xã giao thông thường.",
      "characters": [
        {
          "char": "你",
          "pinyin": "Nǐ",
          "meaning": "Bạn (Nhân)",
          "mnemonic": "Người (亻) đứng đó chính là bạn (Nhĩ).",
          "components": [
            {
              "part": "亻",
              "name": "Nhân đứng",
              "pinyin": "rén",
              "meaning": "Người"
            },
            {
              "part": "尔",
              "name": "Nhĩ",
              "pinyin": "ěr",
              "meaning": "Bạn/Anh"
            }
          ]
        },
        {
          "char": "好",
          "pinyin": "Hǎo",
          "meaning": "Tốt, đẹp",
          "mnemonic": "Mẹ (Nữ) có con (Tử) là điều tốt đẹp nhất.",
          "components": [
            {
              "part": "女",
              "name": "Nữ",
              "pinyin": "nǚ",
              "meaning": "Phụ nữ/Mẹ"
            },
            { "part": "子", "name": "Tử", "pinyin": "zǐ", "meaning": "Con" }
          ]
        }
      ]
    }
  ]
}
```
