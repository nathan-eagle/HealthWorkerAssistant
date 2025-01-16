import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from src.protocols.protocol_manager import ProtocolManager
from anthropic import Anthropic
import os

class GuidanceEngine:
    def __init__(self, mode='production'):
        self.protocol_manager = ProtocolManager()
        self.mode = mode
        self.current_context = {
            'condition_type': None,
            'measurements': [],
            'symptoms': [],
            'covered_topics': [],
            'risk_factors': [],
            'trimester': None,
            'danger_signs': []
        }
        # Initialize Claude for both modes, but with different confidence thresholds
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # Higher threshold for real-time to avoid premature switching
        self.confidence_threshold = 0.8 if mode == 'production' else 0.6

    def generate_guidance(self, transcript: str) -> Dict[str, Any]:
        """Generate real-time guidance based on the current transcript."""
        # Try to classify condition type if not set
        if not self.current_context['condition_type']:
            condition_type, confidence = self._classify_condition_type(transcript)
            if confidence >= self.confidence_threshold:
                self.current_context['condition_type'] = condition_type
        
        # Extract key information from transcript if not already done
        if not any([self.current_context['measurements'], 
                   self.current_context['symptoms'],
                   self.current_context['covered_topics']]):
            extracted_info = self._extract_information(transcript)
            self._update_context(extracted_info)
        
        # Generate guidance based on protocols and context
        guidance = self._generate_protocol_guidance()
        
        return guidance

    def _classify_condition_type(self, transcript: str) -> Tuple[str, float]:
        """Use LLM to classify the conversation into a condition type with confidence."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": f"""Analyze this medical conversation and:
1. Classify it into ONE of these categories:
   - prenatal (for maternal/pregnancy care)
   - communicable (for infectious diseases)
   - noncommunicable (for chronic conditions)
2. Provide your confidence level (0.0 to 1.0)

Respond in this format exactly:
CATEGORY|CONFIDENCE

Example:
prenatal|0.95

Conversation:
{transcript}"""
            }]
        )
        
        result = response.content[0].text.strip()
        category, confidence = result.split('|')
        return category.strip(), float(confidence)

    def _extract_information(self, transcript: str) -> Dict[str, Any]:
        """Extract key clinical information from the transcript using Claude."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"""Analyze this medical conversation and extract:
1. Measurements taken or mentioned (e.g. BP, weight, hemoglobin)
2. Symptoms reported by the patient
3. Risk factors identified
4. Health education topics covered
5. Trimester (if prenatal)
6. Any danger signs or concerning symptoms

Format the response as JSON with these keys:
measurements, symptoms, risk_factors, covered_topics, trimester, danger_signs

Conversation:
{transcript}"""
            }]
        )
        
        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                'measurements': [],
                'symptoms': [],
                'risk_factors': [],
                'covered_topics': [],
                'trimester': None,
                'danger_signs': []
            }

    def _update_context(self, new_info: Dict[str, Any]):
        """Update the conversation context with new information."""
        for key, value in new_info.items():
            if key in self.current_context:
                if isinstance(value, list):
                    self.current_context[key].extend(value)
                else:
                    self.current_context[key] = value

    def _generate_protocol_guidance(self) -> Dict[str, Any]:
        """Generate guidance based on current context and protocols."""
        condition_type = self.current_context.get('condition_type')
        if not condition_type:
            return self._generate_initial_guidance()
            
        # Get the appropriate protocol
        if condition_type == 'prenatal':
            protocol = self.protocol_manager.get_maternal_protocol()
        elif condition_type == 'communicable':
            protocol = self.protocol_manager.get_communicable_protocol()
        else:
            protocol = self.protocol_manager.get_noncommunicable_protocol()
            
        # Validate current interaction against protocol
        validation = self.protocol_manager.validate_interaction(
            condition_type,
            self.current_context
        )
        
        guidance = {
            "missing_information": [],
            "protocol_suggestions": [],
            "danger_signs": [],
            "education_topics": [],
            "symptom_guidance": []
        }
        
        # Add missing measurements to guidance
        if validation['missing_measurements']:
            guidance['missing_information'].extend([
                f"Need to check {measurement}"
                for measurement in validation['missing_measurements']
            ])
        
        # Add uncovered education topics
        if validation['missing_topics']:
            guidance['education_topics'].extend([
                f"Discuss {topic}"
                for topic in validation['missing_topics']
            ])
        
        # Add danger sign alerts
        if validation['detected_danger_signs']:
            guidance['danger_signs'].extend([
                f"ALERT: {sign} detected - requires immediate attention"
                for sign in validation['detected_danger_signs']
            ])
        
        # Add trimester-specific guidance for prenatal care
        if condition_type == 'prenatal' and self.current_context.get('trimester'):
            trimester = self.current_context['trimester']
            guidance['protocol_suggestions'].extend([
                f"Follow {trimester} trimester checklist",
                "Schedule next prenatal visit",
                "Review pregnancy warning signs"
            ])
            
            # Use LLM to analyze symptoms and generate guidance
            if self.current_context.get('symptoms'):
                response = self.claude.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=500,
                    messages=[{
                        "role": "user",
                        "content": f"""Analyze these pregnancy-related symptoms and provide guidance:

Symptoms reported:
{json.dumps(self.current_context['symptoms'], indent=2)}

Additional context:
- Trimester: {self.current_context['trimester']}
- Risk factors: {json.dumps(self.current_context['risk_factors'], indent=2)}
- Measurements: {json.dumps(self.current_context['measurements'], indent=2)}

For each symptom, provide specific, actionable guidance that a Barangay Health Worker can give to the patient.
Start each symptom's section with the symptom name followed by a period.
Write each piece of advice for that symptom on a new line.
Focus only on symptom-specific guidance.
Do not add any general advice or closing remarks at the end."""
                    }]
                )
                
                # Clean up the guidance text and preserve symptom grouping
                guidance_text = response.content[0].text.strip()
                guidance['symptom_guidance'] = [
                    line.strip().lstrip('- •*').strip() 
                    for line in guidance_text.split('\n') 
                    if line.strip() and not any(x in line.lower() for x in [
                        'here', 'for each', 'additional', 'remember', 'monitor', 'discuss', 'continue', 'let me know'
                    ])
                ]
            
            # Add risk-factor specific guidance
            for risk in self.current_context.get('risk_factors', []):
                guidance['protocol_suggestions'].append(
                    f"Monitor closely due to risk factor: {risk}"
                )
        
        return guidance

    def _generate_initial_guidance(self) -> Dict[str, Any]:
        """Generate initial guidance when condition type is unknown."""
        # Get basic assessment protocol
        basic_protocol = self.protocol_manager.get_vital_signs_protocol()
        
        return {
            "missing_information": [
                f"Check {measurement}"
                for measurement in basic_protocol.get('required_measurements', [])
            ],
            "protocol_suggestions": [
                "Determine primary reason for visit",
                "Assess for any immediate concerns"
            ],
            "danger_signs": [],
            "education_topics": []
        }

    def reset_context(self):
        """Reset the conversation context for a new interaction."""
        self.current_context = {
            'condition_type': None,
            'measurements': [],
            'symptoms': [],
            'covered_topics': [],
            'risk_factors': [],
            'trimester': None,
            'danger_signs': []
        } 