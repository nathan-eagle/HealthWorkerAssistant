# BHW Copilot 🏥

An AI-powered platform that enhances Barangay Health Worker interactions by providing minimally intrusive, protocol-based guidance.

## Overview

BHW Copilot processes health worker-patient conversations in real-time, comparing them against Department of Health (DOH) protocols to provide relevant guidance while respecting BHW expertise. The system focuses on three key areas:
- Prenatal care
- Communicable diseases
- Non-communicable diseases

## Key Features

### Minimally Intrusive Design
- Simple audio recording interface
- Alerts only for critical danger signs
- Post-interaction guidance review
- Manual verification and editing of captured data

### Protocol-Based Analysis
- Real-time processing of health conversations
- Automatic extraction of:
  * Symptoms and complaints
  * Vital signs and measurements
  * Risk factors
  * Current medications
  * Recent health history
- Comparison against DOH protocols
- Generation of:
  * Missing information checklist
  * Symptom-specific guidance
  * Education topic suggestions
  * Protocol recommendations

### Multilingual Support
- Handles Tagalog, English, and code-switching
- Context-aware medical terminology processing
- Culturally appropriate health guidance
- Natural language understanding for Filipino medical terms

### Offline Capabilities
- Local audio processing
- Offline transcription
- Local protocol storage and matching
- Secure data handling

## System Requirements

### Hardware
- Android/iOS smartphone with:
  * Adequate microphone
  * Sufficient storage for offline models
  * Full-day battery life

### Software Dependencies
- Python 3.11+
- OpenAI API key (for GPT-4 and Whisper)
- Anthropic API key (for Claude)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/bhw-copilot.git
cd bhw-copilot
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

### Testing Mode
```bash
# Test with sample transcripts
python src/main.py --mode test

# Generate and test with synthetic data
python src/main.py --mode synthetic
```

### Production Mode
```bash
# Run with real-time audio processing
python src/main.py --mode production
```

## Output Format

The system provides analysis output containing:
```
Extracted Information:
- Condition type
- Measurements
- Symptoms
- Covered topics
- Risk factors
- Trimester (if applicable)
- Danger signs

Realtime Alerts:
- Critical danger signs requiring immediate attention

Missing Information:
- Required measurements not yet taken
- Protocol-required questions not yet asked

Symptom-specific Guidance:
- Recommendations based on reported symptoms

Education Topics:
- Suggested health education topics to cover

Protocol Suggestions:
- Next steps based on DOH protocols
```

## Contributing

We welcome contributions! Key areas include:
- Protocol implementation improvements
- Language processing enhancements
- UI/UX refinements
- Documentation updates

## License

This project is licensed under the MIT License - see the LICENSE file for details.
