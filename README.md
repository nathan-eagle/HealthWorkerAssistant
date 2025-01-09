# HealthWorkerCopilot 🏥

A tool for generating, analyzing, and augmenting healthcare worker interactions in Tagalog and English, focused on common medical conditions in the Quezon province of the Philippines.

## Overview

HealthWorkerCopilot uses language models and speech synthesis to create and analyze simulated community health worker interactions. It processes dialogues through multiple stages: generation, speech synthesis, and analysis.

### AI Models Used

- **Dialogue Generation**
  - GPT-4o and o1 for initial dialogue creation
  - Claude Opus for dialogue expansion and enhancement
  - Focus on maintaining medical accuracy and cultural context

- **Audio Processing**
  - OpenAI TTS for natural speech synthesis
  - Whisper for accurate Tagalog transcription
  - Support for multiple voice profiles and natural conversation flow

- **Analysis Pipeline**
  - Claude Opus for translation and in-depth interaction analysis

### Current Features

- **Dialogue Generation**
  - Generates healthcare dialogues in Tagalog with English code-switching
  - Focuses on common conditions: prenatal care, communicable diseases, and non-communicable diseases
  - Includes cultural context specific to Quezon Province

- **Audio Processing**
  - Converts text dialogues to speech using text-to-speech models
  - Supports different voices for health workers and patients
  - Includes natural pauses and conversation flow

- **Basic Analysis**
  - Transcribes audio back to text
  - Translates between Tagalog and English
  - Provides initial interaction analysis

### Upcoming Features

#### AI-Powered Symptom Checking
- Identify potential red flags in patient symptoms
- Suggest possible diagnoses based on symptoms and medical history
- Recommend appropriate treatments or referrals
- Integration with local healthcare resource information

#### AI-Powered Patient Education
- Provide condition-specific information in Tagalog
- Offer health promotion and disease prevention advice
- Generate answers to common patient questions
- Create culturally appropriate educational materials

#### AI-Enabled Decision Support
- Step-by-step guidance on treatment protocols
- Assistance with referral decisions
- Information on available local healthcare resources
- Support for medication management and safety checks

## System Requirements

- Python 3.11+
- OpenAI API key (for GPT-4 and TTS)
- Anthropic API key (for Claude)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nathan-eagle/HealthWorkerCopilot.git
cd HealthWorkerCopilot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## Usage

Run the main script:
```bash
python main.py
```

The system will:
1. Generate dialogue transcripts if needed
2. Create audio recordings
3. Transcribe and analyze the interactions

## Project Structure

- `Synthetic_Interactions/`
  - `text/` - Dialogue transcripts
  - `audio/` - Conversation audio files
- `Interaction_Analysis/`
  - `transcriptions/` - Audio transcriptions
  - `analysis/` - Interaction analysis

## Contributing

Contributions are welcome. Please submit a Pull Request with your proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

