# Co-Speech Gesture Analysis with Gemini API 

This project analyzes co-speech gestures in videos using the Google Gemini API and generates formatted Word documents with the analysis.

**Created by:** Kate Carter for the Distributed Little Red Hen Lab  
**Last Updated:** November 2024 (please note this project is not updated regularly, so to use it you may have to update some packages based on the version of python you're using)

## Requirements

- **Python:** 3.10.9 (Anaconda recommended)
- **System Tools:** FFmpeg with ffprobe (for video duration extraction)
- **Python Packages:** See `requirements.txt`

## Setup Instructions

### 1. Install Python Environment

This project uses **Anaconda Python 3.10.9**. If you don't have it:
```bash
# Download Anaconda from https://www.anaconda.com/download
# Or verify your current Python version:
python --version
```

### 2. Install Required Packages

Install all dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install google-generativeai==0.8.5 python-docx==1.2.0 ffmpeg-python==0.2.0
```

### 3. Install FFmpeg (if not already installed)

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### 4. Set Up Gemini API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey), then:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Important:** Add this to your shell profile (~/.bashrc, ~/.zshrc, etc.) to make it persistent:
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 5. Configure Script Paths

Open the script you want to use and update these paths:
- `OUTPUT_DIR`: Where to save the Word document results
- `CONTEXT_PDF`: Path to context PDF (if using context versions)
- `videos_to_analyze`: List of video file paths to process

## Available Scripts

### Main Analysis Scripts

1. **`gemini2.0_context.py`** - Gemini 2.0 Flash with PDF context
   - Uses McNeill's gesture classification PDF as context
   - Best for categorized gesture analysis
   
2. **`gemini2.0_nocontext.py`** - Gemini 2.0 Flash without context
   - Direct video analysis without reference material
   
3. **`gemini2.5_context.py`** - Gemini 2.5 Flash with PDF context
   - Newer model with context
   
4. **`gemini2.5_nocontext.py`** - Gemini 2.5 Flash without context
   - Newer model, no context

### Utility Scripts

- **`list_models.py`** - Lists available Gemini models
- **`APIScript.py`** - Basic API testing script

## Usage

1. Make sure your API key is set:
```bash
echo $GEMINI_API_KEY  # Should display your API key
```

2. Run the desired script:
```bash
python gemini2.0_context.py
```

3. When prompted:
   - Choose whether you want timestamped logs in terminal (yes/no)
   - Wait for analysis to complete
   - Choose whether to save the document (yes/no)

## Input Format

- **Video Format:** .mp4 files
- **Video Content:** One actor performing 1-2 gestures (with one main/target gesture)
- **Context PDF:** (Optional) Reference material for gesture classification

## Output Format

The generated Word document includes:

- **Title and Timestamp** - Document metadata
- **Processing Times Summary** - Table of processing times per video
- **For Each Video:**
  - Video filename and duration
  - Action performed (visual description)
  - Co-speech gesture category (with context from PDF if applicable)
  - Processing time
- **Request Count** - Total API calls made
- **Total Processing Time** - Cumulative time for all videos

## Configuration Options

Edit these variables at the top of each script:

```python
MODEL_NAME = "gemini-2.0-flash-001"  # Model to use
OUTPUT_DIR = "/path/to/output"       # Where to save documents
CONTEXT_PDF = "/path/to/context.pdf" # Optional context PDF
MAX_REQUESTS = 175                   # API request limit per run

# Generation config
generation_config = {
    "temperature": 0.4,              # Lower = more focused
    "top_p": 0.95,                   # Higher = more reliable
    "top_k": 32,
    "max_output_tokens": 1024,
}
```

## Features

- **Formatted Output:** Bold and italic text formatting in Word documents
- **Error Handling:** Comprehensive error logging with tracebacks
- **Request Limiting:** Built-in API request counter to prevent overuse
- **Flexible Logging:** Choose between timestamped or simple console logs
- **Video Duration:** Automatic extraction using ffprobe
- **Context Awareness:** Upload reference PDFs for better analysis
- **Safe Exit:** Prompts to save document even on interruption

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'docx'"**
```bash
pip install python-docx
```

**"GEMINI_API_KEY environment variable not set"**
```bash
export GEMINI_API_KEY="your-key"
```

**"python: can't open file"**
- Check filename (note: `gemini2.0_context.py` has underscore between 0 and context)
- Verify you're in the correct directory

**"[Errno 30] Read-only file system"**
- Check that OUTPUT_DIR exists and is writable
- Verify video files exist at specified paths

### Checking Installation

Verify all imports work:
```bash
python -c "import google.generativeai; from docx import Document; import subprocess; print('All imports successful!')"
```

## Notes

- The script handles multiple response formats (numbered lists, labeled sections)
- Text surrounded by **asterisks** will be formatted as bold in Word
- Text surrounded by *single asterisks* will be formatted as italic
- Video files must be accessible at the paths specified
- The context PDF (if used) is uploaded once and reused for all videos
- Progress and errors are logged to both console and `gemini_analysis.log`

## API Rate Limits

Be aware of Google's API rate limits:
- Default script limit: 175 requests per run
- Adjust `MAX_REQUESTS` variable as needed
- Monitor your usage at [Google AI Studio](https://aistudio.google.com/)

## Project Structure

```
Gemini_API_Co-Speech-1121/
├── gemini2.0_context.py       # Main script (Gemini 2.0 + context)
├── gemini2.0_nocontext.py     # Gemini 2.0 without context
├── gemini2.5_context.py       # Gemini 2.5 + context
├── gemini2.5_nocontext.py     # Gemini 2.5 without context
├── list_models.py             # List available models
├── APIScript.py               # Basic API test
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── gemini_analysis.log        # Log file (generated on run)
```

## Support

For issues or questions about this project, contact Kate Carter (kxc750@case.edu) or refer to the [Google Gemini API Documentation](https://ai.google.dev/docs).

