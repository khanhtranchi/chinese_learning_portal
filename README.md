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

## Lesson audio (HSK1)

The first HSK1 lesson can generate per-line audio clips via [edge-tts](https://github.com/rany2/edge-tts).

1. Install the CLI once inside WSL:

   ```bash
   python3 -m pip install --user edge-tts
   ```

2. Generate audio files (creates `static/audio/hsk1/lesson-1/line-XX.mp3` and skips existing files):

   ```bash
   python3 scripts/generate_lesson1_audio.py
   ```

3. Restart `npm start` if it was running so the dev server can serve the new static files.
