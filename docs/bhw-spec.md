# BHW Copilot Specification

## Platform Overview

The Barangay Health Worker (BHW) Copilot is an AI-powered platform designed to augment BHW decision-making and patient care, while respecting their central role in community healthcare. It is built on official Department of Health (DOH) protocols and guidelines.

Primary goals of the platform include:
1. Enhancing patient interactions through real-time, context-aware support
2. Ensuring adherence to clinical protocols while respecting BHW judgment
3. Supporting continuous learning and skill development
4. Enabling better tracking and follow-up of community health outcomes

## 1. Real-Time Interaction Support

### 1.1 Voice Input Processing
The system begins recording when the BHW starts their interaction with a patient. The voice interface should:
- Use voice activity detection to infer speaker changes
- Support both Tagalog and English, including code-switching
- Handle ambient noise typical in home visit settings
- Work offline with local processing when needed

### 1.2 Continuous Analysis Pipeline
As the conversation progresses, the system should:
- Transcribe speech in near real-time using Whisper
- Extract key clinical information:
  * Mentioned symptoms
  * Vital signs as they're measured
  * Risk factors
  * Current medications
  * Recent health history
- Compare extracted information against relevant protocols
- Identify gaps in information gathering
- Monitor for danger signs or red flags
- Track which health education topics have been covered

### 1.3 Real-Time Guidance
The system should provide unobtrusive guidance to the BHW through:
- A smartphone screen displaying key information, suggestions, and alerts (no audio interruptions)

Guidance should include:
1. Missing Information Prompts
   - "Ask about family history of diabetes"
   - "Need to check blood pressure"
   - "Verify last menstrual period date"

2. Protocol-Based Suggestions
   - Required measurements for this visit type
   - Expected health education topics
   - Risk assessment questions

3. Danger Sign Alerts
   - Immediate notification when risk factors identified
   - Clear escalation protocols
   - Emergency contact information

4. Cultural Considerations
   - Local health beliefs to address
   - Family involvement suggestions
   - Community resource recommendations

### 1.4 Interaction Support Features
The system should help BHWs:
1. Follow Clinical Protocols
   - Basic vital signs collection
   - Trimester-specific maternal care guidelines
   - Disease-specific management protocols and surveillance

2. Provide Health Education
   - Access explanatory materials
   - Follow structured education protocols
   - Document topics covered

3. Make Referral Decisions
   - Clear criteria for different care levels

4. Handle Emergency Situations
   - Step-by-step emergency protocols
   - Quick access to emergency contacts
   - Offline emergency reference materials

## 2. Post-Interaction Analysis and Support

### 2.1 Comprehensive Visit Analysis
After each interaction, the system performs detailed analysis:

1. Clinical Assessment
   - Completeness of examination
   - Appropriateness of recommendations
   - Adherence to protocols
   - Quality of documentation

2. Communication Analysis
   - Effectiveness of health education
   - Cultural competency
   - Patient engagement
   - Use of appropriate language level

3. Decision Making Review
   - Appropriateness of referral decisions
   - Recognition of danger signs
   - Follow-up planning
   - Resource utilization

### 2.2 Learning and Development
The system should support BHW skill development through:

1. Personalized Feedback
   - Specific improvement areas
   - Recognition of good practices
   - Suggested learning resources
   - Practice scenarios

2. Knowledge Building
   - Updates on health protocols
   - New medical information
   - Local health trends
   - Community resources

3. Skill Enhancement
   - Communication techniques
   - Clinical assessment skills
   - Emergency response
   - Health education methods

### 2.3 Patient Follow-up Support
The system should help manage ongoing patient care:

1. Follow-up Planning
   - Automated scheduling suggestions
   - Risk-based prioritization
   - Visit preparation prompts

2. Patient Tracking
   - Health status monitoring
   - Appointment adherence
   - Treatment compliance
   - Outcome tracking

3. Care Coordination
   - Referral tracking
   - Communication with other providers
   - Resource coordination
   - Family engagement

### 2.4 Community Health Management
Support for broader community health activities:

1. Health Trend Analysis
   - Disease patterns
   - Risk factor prevalence
   - Intervention effectiveness
   - Resource utilization

2. Resource Planning
   - Supply needs prediction
   - Workload distribution
   - Training requirements
   - Emergency preparedness

## 3. System Integration Features

### 3.1 Data Management
Robust data handling capabilities:

1. Secure Storage
   - Encryption
   - Audit trails

2. Offline Operation
   - Local protocol storage
   - Queued sync operations
   - Conflict resolution
   - Emergency access

3. Integration
   - BHW protocols and training materials
   - Health facility systems
   - Emergency services

### 3.2 Privacy and Security
Comprehensive privacy protection:

1. Patient Privacy
   - Data encryption
   - Access controls
   - Consent management
   - Information sharing protocols

2. System Security
   - Authentication
   - Authorization
   - Audit logging


### 3.3 Quality Assurance
Continuous quality improvement:

1. Performance Monitoring
   - Protocol adherence
   - Outcome tracking
   - Error detection
   - Efficiency metrics

2. System Improvement
   - User feedback
   - Error analysis
   - Protocol updates
   - Feature enhancement

## 4. Implementation Considerations

### 4.1 Technology/Smartphone Requirements
- Cellular connectivity + web browser
- Reliable capture of up to 1 hour of audio

### 4.2 Training Requirements
- Initial system training
- Ongoing support
- Protocol updates
- Emergency procedures
- Troubleshooting
- Best practices

### 4.3 Support Infrastructure
- Technical support
- Clinical supervision
- Protocol updates

