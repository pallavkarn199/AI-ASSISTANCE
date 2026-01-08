# AI-ASSISTANCE

A simple voice assistant built with Python, using speech recognition and text-to-speech APIs for smooth processing.

## Features

- Speech recognition using Google's API
- Text-to-speech using pyttsx3
- Basic command processing (time, date, hello)
- AI-powered responses for unknown commands using Google's Gemini API
- Graphical User Interface (GUI) with Tkinter

## Requirements

- Python 3.x
- Microphone for input
- Speakers for output

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set your Google API key (optional, for AI responses):
   ```
   export GOOGLE_API_KEY='AIzaSyCZBvwdUovVL-qzROtg4obe3UGD_mJeLjw'
   ```

## Usage

Activate the virtual environment:
```
source .venv/bin/activate
```

Run the voice assistant:
```
python voice_assistant.py
```

The GUI will open with:
- A text area showing the conversation
- "Listen" button to start voice recognition
- Quick buttons for Time, Date, and Exit

Speak commands like:
- "What is the time?"
- "What is the date?"
- "Hello"
- "Exit" to quit

For other queries, it will use AI to generate responses if API key is set.

## APIs Used

- Google Speech Recognition API for converting speech to text
- Google Gemini API for processing unknown commands (optional)
- pyttsx3 for text-to-speech (offline)