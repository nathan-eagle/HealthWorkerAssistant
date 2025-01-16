# BHW Copilot 🏥

An AI-powered platform to enhance Barangay Health Worker decision-making and patient care.

## Overview

BHW Copilot is a comprehensive support system that assists Barangay Health Workers in providing healthcare services to their communities. The system uses advanced AI to process health interactions in both English and Filipino, providing real-time guidance based on Department of Health (DOH) protocols.

## Protocol Implementation

The system implements DOH protocols through a structured, codified approach:

### Basic Assessment Protocol (`basic-assessment.json`)
- Initial vital signs and measurements required for all patient interactions
- Standard health assessment questions and observations
- Early warning signs that require immediate attention
- Guidance for determining the appropriate care pathway

### Maternal Health Protocol (`maternal-health.json`)
- Trimester-specific assessments and measurements
- Required prenatal check-up components
- Nutrition and lifestyle guidance
- Danger signs requiring immediate medical attention
- Educational topics for each stage of pregnancy
- Risk factor monitoring and management

### Communicable Disease Protocol (`communicable-disease.json`)
- Symptom assessment and documentation
- Contact tracing requirements
- Isolation and quarantine guidelines
- Disease-specific warning signs
- Community health protection measures
- Patient education and prevention strategies

### Non-Communicable Disease Protocol (`noncommunicable-disease.json`)
- Chronic condition assessment guidelines
- Required regular measurements (BP, blood sugar, etc.)
- Lifestyle modification recommendations
- Medication adherence monitoring
- Complication warning signs
- Long-term management strategies

## Key Features

### Bilingual Support
- Real-time processing of conversations in both Filipino and English
- Context-aware translation of medical terminology
- Culturally appropriate health guidance
- Code-switching support for natural communication

### Protocol-Based Guidance
- Real-time analysis of patient interactions
- Automatic protocol selection based on condition type
- Structured guidance generation:
  - Symptom-specific recommendations
  - Required measurements and assessments
  - Educational topics to cover
  - Risk factor monitoring
  - Danger sign alerts

### LLM-Enhanced Analysis
- Semantic understanding of health conversations
- Context-aware symptom analysis
- Natural language processing for Filipino medical terms
- Intelligent protocol matching and validation

### Voice Processing
- Real-time audio transcription
- Speaker diarization for conversation tracking
- Support for both Filipino and English speech
- Background noise handling for field conditions

## Usage

### Testing Mode
```bash
# Test with a specific transcript
python src/main.py --transcript path/to/transcript.txt

# Run with synthetic test data
python src/main.py --mode synthetic

# Test with real recordings
python src/main.py --mode testing
```

### Production Mode
```bash
# Run in production mode with live audio
python src/main.py --mode production
```

## Output Format

The system provides guidance in both Filipino and English, structured as follows:

### Tagalog Section
- Gabay para sa mga Sintomas (Symptom-specific guidance)
- Kulang na Impormasyon (Missing information)
- Mga Palatandaan ng Panganib (Danger signs)
- Mga Paksang Pang-edukasyon (Education topics)
- Mga Mungkahi ayon sa Protokol (Protocol suggestions)

### English Section
- Symptom-specific Guidance
- Missing Information
- Danger Signs
- Education Topics
- Protocol Suggestions

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
   ```
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```
4. Create necessary directories: `python src/main.py`

## Contributing

We welcome contributions to enhance the protocol implementations, improve language processing, or add new features. Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

