# vidipt - Free AI Video Generation Platform

**Transform scripts and images into professional videos using free AI tools**

## Features

✨ **Core Capabilities**
- Convert scripts to videos with AI narration
- Support for Indian languages (Hindi, Assamese, English, Tamil, Telugu, Kannada, Malayalam)
- Northeast Indian accents
- Animation & VFX effects
- Upload images, GIFs, video clips, screenshots
- Customizable video sizes and frame rates
- Copyright-free background music
- Multi-format media support

## Tech Stack

**Backend:**
- Python 3.9+
- Flask
- FFmpeg (video processing)
- Pydub (audio manipulation)
- Pillow (image processing)

**Frontend:**
- React.js
- TypeScript
- Tailwind CSS
- Drag-and-drop file upload

**Free AI Services:**
- Google TTS (Text-to-Speech)
- Pixabay API (Copyright-free music)

## Quick Start

```bash
# Clone repository
git clone https://github.com/man2theemoboy-eng/vidipt.git
cd vidipt

# Backend setup
cd backend
pip install -r requirements.txt
python app.py

# Frontend setup (new terminal)
cd ../frontend
npm install
npm start
```

Visit `http://localhost:3000` to start creating videos!

## Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- FFmpeg installed on system

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run backend:
```bash
python app.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## Features Overview

### 🌍 Multi-Language Support
- Hindi (हिंदी)
- English
- Assamese (অসমীয়া)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)

### 🎬 Video Customization
- Resolution: 720p, 1080p, 4K, Portrait, Square
- Frame rates: 24, 30, 60 FPS
- Effects: Fade, Slide, Zoom, Typewriter, Bounce
- Background music: Yes/No

### 📁 Media Support
- Images: JPG, PNG, WebP, GIF
- Videos: MP4, AVI, MOV, MKV
- Documents: TXT, PDF

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Key Endpoints
- `POST /generate-video` - Generate new video
- `GET /job/{job_id}` - Get job status
- `GET /download/{job_id}` - Download completed video
- `POST /preview` - Preview script audio
- `GET /languages` - Get supported languages

## Troubleshooting

### FFmpeg not found
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

### Port already in use
- Backend: Change port in app.py (default 5000)
- Frontend: Set PORT environment variable

## License

MIT License - Free for personal use

## Support

For issues and feature requests, please create an issue on GitHub.

---

**Made with ❤️ for creators worldwide**
