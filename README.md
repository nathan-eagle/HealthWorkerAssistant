# HealthWorker Copilot

A Python application that generates realistic dialogues between Barangay Health Workers (BHWs) and patients in Quezon Province, Philippines. The dialogues are generated in Tagalog (Tayabas dialect) and translated to English, with audio generation for both languages.

## Features

- Generates realistic healthcare dialogues for three conditions:
  - Prenatal care
  - Communicable diseases
  - Non-communicable diseases
- Uses OpenAI's GPT-4 for dialogue generation
- Generates dialogues in Tagalog (Tayabas dialect)
- Translates dialogues to English
- Generates audio files for both Tagalog and English versions
- Maintains consistent speaker voices across languages

## Requirements

- Python 3.8+
- OpenAI API key
- FFmpeg (for audio processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HealthWorkerCopilot.git
cd HealthWorkerCopilot
```

2. Create a virtual environment and activate it:
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

Run the main script to generate dialogues:
```bash
python main.py
```

The script will:
1. Generate Tagalog dialogues
2. Translate them to English
3. Generate audio files for both languages
4. Save all outputs in the appropriate directories

## Output Structure

- `transcripts/`: Contains dialogue transcripts
  - `*_tagalog.txt`: Tagalog dialogue transcripts
  - `*_english.txt`: English dialogue transcripts
- `audio_output/`: Contains generated audio files
  - Audio files for both Tagalog and English versions

## License

MIT License 