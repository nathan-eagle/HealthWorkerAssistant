# HealthWorkerCopilot 🏥

An advanced AI-powered platform for generating, analyzing, and understanding healthcare worker interactions in multilingual contexts, with a specific focus on Tagalog-English healthcare conversations.

## Overview

HealthWorkerCopilot leverages state-of-the-art language models and speech synthesis to create, analyze, and understand healthcare worker interactions. It employs a sophisticated multi-stage pipeline that generates realistic healthcare dialogues, converts them to natural speech, and provides deep analytical insights.

### Key Features

- **Multi-LLM Architecture**
  - Uses GPT-4 for generating nuanced, contextually-appropriate healthcare dialogues
  - Employs Claude Opus for deep semantic analysis of interactions
  - Combines multiple AI models for enhanced accuracy and insight

- **Multilingual Capabilities**
  - Generates authentic Tagalog-English code-switched conversations
  - Provides accurate translations and transcriptions
  - Maintains cultural and linguistic authenticity

- **Advanced Audio Synthesis**
  - Utilizes OpenAI's latest TTS models for natural-sounding speech
  - Supports multiple voice profiles for different speakers
  - Automatically handles gender-appropriate voice selection
  - Implements intelligent pause timing for natural conversation flow

- **Comprehensive Analysis Pipeline**
  - Transcribes audio back to text with high accuracy
  - Provides detailed interaction analysis
  - Identifies key healthcare communication patterns
  - Assesses cultural and linguistic competency

## System Requirements

- Python 3.11+
- OpenAI API key (for GPT-4 and TTS)
- Anthropic API key (for Claude Opus)

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

Run the main script to generate and analyze interactions:
```bash
python main.py
```

The system will:
1. Generate synthetic healthcare dialogues if needed
2. Create audio recordings with natural speech
3. Transcribe and analyze the interactions
4. Provide detailed analysis and insights

## Project Structure

- `Synthetic_Interactions/`
  - `text/` - Generated dialogue transcripts
  - `audio/` - Synthesized conversation audio files
- `Interaction_Analysis/`
  - `transcriptions/` - Audio transcription results
  - `analysis/` - Detailed interaction analysis

## Technical Details

### Dialogue Generation
- Utilizes GPT-4 for creating realistic healthcare scenarios
- Implements sophisticated prompting for authentic code-switching
- Maintains medical accuracy and cultural sensitivity

### Audio Synthesis
- Uses OpenAI's TTS API with multiple voice profiles
- Implements intelligent speaker detection
- Handles natural conversation timing and pauses

### Analysis Pipeline
- Employs Claude Opus for deep semantic analysis
- Provides insights into:
  - Communication effectiveness
  - Cultural competency
  - Medical accuracy
  - Language use patterns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Special thanks to:
- OpenAI for GPT-4 and TTS capabilities
- Anthropic for Claude Opus
- The healthcare workers who inspire this work 