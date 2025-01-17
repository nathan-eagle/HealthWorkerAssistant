# HealthWorkerCopilot 🏥

An AI-powered platform for augmenting Barangay Health Worker (BHW) interactions in the Philippines, built on official Department of Health (DOH) protocols and guidelines.

## Overview

HealthWorkerCopilot helps BHWs deliver better community healthcare by:
1. Providing protocol-based decision support
2. Capturing and validating vital signs
3. Identifying cases needing referral
4. Supporting health education efforts
5. Operating offline-first for reliability

### Core Features

#### 1. Protocol-Based Support
- Built on DOH BHW Reference Manual
- Clear scope of practice guidelines
- Standardized vital sign collection
- Evidence-based referral criteria
- Health education support

#### 2. Offline-First Design
- Local SQLite database
- Queued sync operations
- Voice recording storage
- Protocol validation offline
- Sync when connection available

#### 3. Voice Interface
- Record patient interactions
- Capture vital signs verbally
- Natural conversation flow
- Local audio storage
- Quality checks built-in

### Technical Architecture

- **Core Protocol Engine**
  - DOH-based clinical protocols
  - Vital sign validation
  - Referral guidelines
  - Health education topics

- **Data Management**
  - SQLite local storage
  - Async sync operations
  - Conflict resolution
  - Audit logging

- **Voice Processing**
  - Local recording
  - Quality checks
  - Storage management
  - Upload queuing

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

3. Set up environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Project Structure

```
HealthWorkerCopilot/
├── bhw/                    # Core BHW support
│   ├── protocols/          # Clinical protocols
│   │   ├── maternal.py    # Maternal health
│   │   ├── child.py       # Child health
│   │   └── emergency.py   # Emergency care
│   ├── voice/             # Voice interface
│   │   ├── recorder.py    # Recording
│   │   └── quality.py     # Quality checks
│   └── sync/              # Offline sync
│       └── database.py    # Local storage
├── training/              # Training tools
│   └── dialogue_gen/     # Synthetic dialogues
└── tests/                # Test suite
```

## Usage

### Start BHW Assistant
```bash
python -m bhw.main
```
Launches the main BHW support interface:
- Protocol-based guidance
- Vital sign collection
- Voice recording
- Offline sync

### Training Mode
```bash
python -m training.main
```
Generates synthetic training data:
- Dialogue generation
- Audio synthesis
- Protocol testing

## Key Features

### Protocol Support
- Maternal health
- Child health
- Emergency care
- Health education
- Referral guidelines

### Offline Capabilities
- Local protocol validation
- Voice recording storage
- Queued sync operations
- Conflict resolution

### Voice Interface
- Natural interaction
- Vital sign capture
- Quality checks
- Local storage

## Contributing

Priority areas:
1. Protocol implementations
2. Offline sync improvements
3. Voice interface enhancement
4. Test coverage
5. Documentation

See CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE

## Acknowledgments

Built with guidance from:
- DOH BHW Reference Manual
- TESDA Training Regulations
- BHW Benefits and Incentives Act