# Co-Speech Gesture Analysis with Gemini API 

This project analyzes co-speech gestures in videos using the Google Gemini API and generates a formatted Word document with the analysis.

## Setup

1. Install required packages:
```bash
pip install google-generativeai python-docx moviepy
```

2. Set up your Gemini API key:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

3. Configure the script:
   - Open `gesture_analysis_doc.py`
   - Replace `"path/to/output/directory"` with your desired output directory
   - Update the `videos_to_analyze` list with your video file paths

## Usage

Run the script:
```bash
python gesture_analysis_doc.py
```
or 
```bash
python APIScript.py
```

The script ```gesture_analysis_doc.py``` will:
1. Process each video through the Gemini API
2. Generate a Word document with:
   - Analysis of each gesture
   - Bold formatting for key terms
   - Both parsed analysis and raw response
3. Save the document in your specified output directory

The script ```APIScript.py``` will:
1. Process each video through the Gemini API
2. Populate the raw responses in terminal

## Input Format
- .mp4 video
- one actor performing 1-2 gestures (with one main or target gesture)

## Output Format

The generated Word document includes:
- Title and timestamp
- For each video:
  - Video filename
  - Action performed
  - Co-speech gesture category
  - Raw response for reference

## Notes

- The script handles both numbered list formats (1. and 2. or 1) and 2))
- Text surrounded by **asterisks** will be formatted as bold
- Make sure your videos are accessible and in a supported format
- This code was created by Kate Carter and debugged using Cursor for the Distributed Little Red Hen Lab
