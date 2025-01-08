# HealthWorker Copilot

A tool for generating realistic healthcare dialogues between Barangay Health Workers (BHWs) and patients in Quezon Province, Philippines. The tool generates dialogues in both Tagalog (Tayabas dialect) and English, complete with audio recordings.

## Features

- Generates realistic 15-minute healthcare dialogues for three conditions:
  - Prenatal care
  - Communicable diseases
  - Non-communicable diseases
- Supports both Tagalog (Tayabas dialect) and English
- Generates high-quality audio with different voices for BHW and patients
- Maintains natural conversation flow with appropriate timing

## Example Outputs

The repository includes example outputs in both Tagalog and English:
- `transcripts/tagalog/` - Example Tagalog dialogue transcripts
- `transcripts/english/` - Example English translations
- `audio_output/tagalog/` - Example Tagalog audio recordings
- `audio_output/english/` - Example English audio recordings

These examples demonstrate the format, quality, and style of the generated content.

## Requirements

- Python 3.11 or higher
- OpenAI API key
- FFmpeg (for audio processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nathan-eagle/HealthWorkerCopilot.git
cd HealthWorkerCopilot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run the main script to generate dialogues and audio:
```bash
python main.py
```

This will:
1. Generate Tagalog dialogues for all conditions
2. Translate them to English
3. Generate audio files for Tagalog dialogues
4. Generate audio files for English dialogues

Output files will be organized in:
- `transcripts/tagalog/` - Tagalog dialogue transcripts
- `transcripts/english/` - English dialogue transcripts
- `audio_output/tagalog/` - Tagalog audio files
- `audio_output/english/` - English audio files

## Project Structure

- `main.py` - Main script orchestrating the entire process
- `generate_dialogue.py` - Handles dialogue generation
- `translate_dialogue.py` - Handles translation between languages
- `generate_audio.py` - Handles audio generation
- `requirements.txt` - Python package dependencies

## License

MIT License 