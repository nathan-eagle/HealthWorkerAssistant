# BHW Copilot

An AI-powered platform designed to augment Barangay Health Worker (BHW) decision-making and patient care, built on official Department of Health (DOH) protocols and guidelines.

## Project Structure

```
├── src/
│   ├── voice_processing/      # Real-time audio capture and processing
│   ├── continuous_analysis/   # Transcription, translation, and analysis
│   ├── real_time_guidance/    # Protocol-based BHW prompts
│   ├── post_interaction/      # Quality assessment and feedback
│   ├── data_management/       # Storage and synchronization
│   ├── protocols/            # Clinical protocol definitions
│   ├── synthetic/            # Test data generation
│   └── frontend/             # Web interface components
├── tests/                    # Test suites
├── data/
│   ├── synthetic/           # Generated test data
│   │   ├── text/           # Generated dialogues
│   │   └── audio/          # Synthesized speech
│   ├── raw/                # Real BHW recordings
│   │   └── audio/          # Actual patient interactions
│   ├── processed/          # Analysis outputs
│   │   ├── transcriptions/ # Transcripts and translations
│   │   └── analysis/       # Interaction assessments
│   └── protocols/          # Protocol JSON definitions
└── docs/                    # Documentation
```

## Operation Modes

### 1. Synthetic Testing Mode
For initial development and testing using AI-generated conversations:
```bash
python src/main.py --mode=synthetic
```
- Generates realistic BHW-patient dialogues in Tagalog with code-switching
- Creates multi-voice audio using OpenAI TTS
- Tests full analysis pipeline with synthetic data
- Useful for protocol validation and system testing

### 2. Testing Mode with Real Recordings
For testing with actual BHW-patient interactions (pre-recorded):
```bash
python src/main.py --mode=testing
```
- Processes real audio recordings from past interactions
- Performs full transcription and analysis
- Validates protocol compliance
- Helps refine the guidance engine with real data

### 3. Production Mode
For live deployment with real-time BHW interactions:
```bash
python src/main.py --mode=production
```
- Captures live audio from BHW's phone
- Provides real-time transcription and guidance
- Monitors protocol adherence
- Stores interactions for later analysis

## Key Features

1. **Voice Processing**
   - Real-time speech recognition (Whisper)
   - Multilingual support with code-switching (Tagalog/English)
   - Voice activity detection
   - Multiple speaker identification

2. **Continuous Analysis**
   - Real-time transcription
   - Code-switching translation
   - Protocol compliance checking
   - Risk assessment

3. **Real-Time Guidance**
   - Context-aware prompts
   - Protocol-based suggestions
   - Danger sign alerts
   - Bilingual guidance

4. **Post-Interaction Analysis**
   - Visit quality assessment
   - Learning recommendations
   - Follow-up planning
   - Cultural competency evaluation

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Required environment variables:
```
OPENAI_API_KEY=your_openai_key    # For GPT-4, Whisper, and TTS
ANTHROPIC_API_KEY=your_claude_key # For analysis and translation
```

## Development Workflow

1. **Initial Testing with Synthetic Data**
```bash
# Generate test data
python src/main.py --mode=synthetic

# Check generated files in:
data/synthetic/text/     # Generated dialogues
data/synthetic/audio/    # Synthesized conversations
data/processed/         # Analysis results
```

2. **Testing with Real Recordings**
```bash
# Place audio files in:
data/raw/audio/

# Process recordings
python src/main.py --mode=testing
```

3. **Production Deployment**
```bash
# Start the live system
python src/main.py --mode=production
```

## Data Flow

1. **Audio Capture**
   - Real-time recording (production mode)
   - Pre-recorded files (testing mode)
   - Synthetic generation (synthetic mode)

2. **Processing Pipeline**
   - Speech recognition (Whisper)
   - Speaker identification
   - Code-switching translation (Claude)
   - Protocol compliance checking
   - Real-time guidance generation

3. **Storage and Analysis**
   - Secure audio storage
   - Structured transcripts
   - Analysis reports
   - Follow-up recommendations

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for details.

