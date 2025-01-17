# BHW Copilot Specification

## Platform Overview

The Barangay Health Worker (BHW) Copilot is an AI-powered platform designed to augment BHW decision-making and patient care, while respecting their central role in community healthcare. It is built on protocols extracted from the Department of Health (DOH) BHW Reference Manual and other official guidelines.

Primary goals of the platform include:
1. Enhancing patient interactions through minimally intrusive, context-aware support
2. Ensuring adherence to clinical protocols while respecting BHW judgment
3. Supporting documentation and follow-up of community health outcomes
4. Enabling continuous improvement through analysis of interactions

## 1. Real-Time Interaction Support

### 1.1 Voice Input Processing
The system begins recording when the BHW initiates a patient interaction. The voice interface should:
- Use voice activity detection to identify speaker changes
- Support Tagalog, English, and code-switching
- Handle ambient noise typical in community settings
- Function offline with local processing when needed
- Capture clearly stated measurement results (BP, temperature, etc.)

### 1.2 Analysis Pipeline
During the conversation, the system should:
- Transcribe speech using offline-capable models
- Extract key clinical information:
  * Symptoms and complaints
  * Vital signs and measurements
  * Risk factors
  * Current medications
  * Recent health history
- Compare against relevant protocols for:
  * Prenatal care
  * Communicable diseases
  * Non-communicable diseases
- Identify gaps in information gathering
- Monitor for danger signs requiring immediate attention
- Track covered health education topics

### 1.3 Interface Design
The system should provide unobtrusive support through:
- A simple phone interface that can be positioned to capture audio
- Silent operation during normal interaction
- Visual alerts ONLY for detected danger signs
- Post-interaction review screen showing:
  * Missing information checklist
  * Symptom-specific guidance
  * Suggested education topics
  * Protocol recommendations
- Ability to review and edit extracted data before ending session

### 1.4 Protocol Implementation
The system should support BHWs across key areas:

1. Clinical Assessment
   - Vital signs collection
   - Symptom evaluation
   - Risk factor identification
   - Danger sign detection

2. Health Education
   - Topic recommendations
   - Key messages by condition
   - Documentation of topics covered

3. Referral Guidance
   - Clear criteria by condition
   - Emergency protocols
   - Facility options

## 2. Post-Interaction Analysis

### 2.1 Session Analysis
After each interaction, the system analyzes:

1. Protocol Adherence
   - Completeness of assessment
   - Appropriate measurements taken
   - Required education topics covered
   - Proper documentation

2. Clinical Decision Support
   - Appropriate referral decisions
   - Recognition of danger signs
   - Follow-up planning
   - Resource utilization

### 2.2 Data Review and Editing
The system should allow BHWs to:
- Review extracted information for accuracy
- Edit any misidentified or missing data
- Add additional context or notes
- Verify measurements and findings
- Complete any missing required fields

### 2.3 Follow-up Support
Help manage ongoing patient care through:
- Scheduling recommendations
- Risk-based prioritization
- Visit preparation guidance
- Outcome tracking

## 3. Technical Requirements

### 3.1 Core Capabilities
- Offline operation for all core functions
- Local storage of sensitive data
- Efficient audio processing
- Accurate multilingual transcription
- Protocol-based analysis
- Data review and editing interface

### 3.2 Privacy and Security
- Local processing of sensitive information
- Encrypted storage
- Minimal data transmission
- Clear consent processes
- Access controls

### 3.3 Hardware Requirements
- Standard Android/iOS smartphone
- Sufficient storage for offline models
- Adequate microphone quality
- Battery life for full day of use

### 3.4 Training Requirements
- Basic system operation
- Audio recording best practices
- Data review and editing
- Emergency protocols
- Troubleshooting guidance