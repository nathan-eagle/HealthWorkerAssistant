# BHW Copilot 🏥

An AI-powered platform providing real-time protocol support for over 200,000 Barangay Health Workers (BHWs) serving as frontline healthcare providers across rural Philippines.

## The Challenge

The Philippines faces a critical healthcare crisis with just 1 doctor per 25,280 people. As a result, 200,000 Barangay Health Workers - 90% of whom are women - must deliver essential primary care despite receiving only 5 days of formal training. These dedicated frontline workers serve 70% of Filipinos living in rural and underserved communities.[^1]

## Our Solution

BHW Copilot processes health worker-patient conversations in real-time, comparing them against [Department of Health (DOH) protocols](tree/main/docs) to provide relevant guidance while respecting BHW expertise. By combining generative AI with offline-capable speech recognition, it delivers context-specific support in both Tagalog and English, even in areas with limited connectivity.

Studies show this type of AI guidance can:
- Improve protocol adherence by 67%[^2]
- Enhance diagnostic accuracy by 70%[^2] 
- Increase BHW confidence by 75%[^3]
- Reduce preventable complications through earlier detection and referral[^3]

[^1]: Department of Health Philippines. (2023). Ratio of active barangay health workers to population in the Philippines in 2023, by region. Statista. https://www.statista.com/statistics/1370633/philippines-number-of-health-workers-by-region
[^2]: Babel et al. (2021). Artificial Intelligence Solutions to Increase Medication Adherence in Patients With Non-communicable Diseases. Frontiers in Digital Health, 3, 669869. https://pmc.ncbi.nlm.nih.gov/articles/PMC8521858
[^3]: Kearns et al. (2024). Bridging the Skills Gap: Evaluating an AI-Assisted Provider Platform to Support Care Providers with Empathetic Delivery of Protocolized Therapy. arXiv:2401.03631. https://arxiv.org/abs/2401.03631


### Focus Areas
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
