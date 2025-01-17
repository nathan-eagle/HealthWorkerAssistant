import json
import os
import re
from typing import Dict, Any, List, Tuple

from protocols.protocol_manager import ProtocolManager
from anthropic import Anthropic

def extract_json_from_text(text: str) -> dict:
    """Extract JSON object from text that might contain other content."""
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    return {}

class GuidanceEngine:
    """
    GuidanceEngine uses the BHW manual (via ProtocolManager) to analyze health conversations 
    and generate context-aware recommendations—including filtered danger signs and missing 
    measurements. The ProtocolManager encapsulates the logic for referencing official guidelines.
    """

    def __init__(self, mode='production'):
        self.protocol_manager = ProtocolManager()
        self.mode = mode
        # Used to track the relevant context from the latest transcript
        self.current_context = {
            'condition_type': None,
            'measurements': [],
            'symptoms': [],
            'covered_topics': [],
            'risk_factors': [],
            'trimester': None,
            'danger_signs': []
        }
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))  # LLM instance
        self.confidence_threshold = 0.8 if mode == 'production' else 0.6

    def generate_guidance(self, transcript: str, transcript_filename: str = "") -> Dict[str, Any]:
        """
        Main entry to produce symptom guidance, protocol suggestions, missing info,
        danger signs, and education topics for the user interface.
        If condition_type is not yet set, we try to infer it from the filename start:
         - 'prenatal_' for prenatal
         - 'non-communicable_' for NCD
         - 'communicable_' for communicable diseases
        """
        
        # 1. Infer condition_type from the start of the filename
        if not self.current_context['condition_type'] and transcript_filename:
            base_name = os.path.basename(transcript_filename).lower()
            if base_name.startswith("prenatal"):
                self.current_context['condition_type'] = "prenatal"
            elif base_name.startswith("non-communicable"):
                self.current_context['condition_type'] = "non-communicable"
            elif base_name.startswith("communicable"):
                self.current_context['condition_type'] = "communicable"

        # 2. Fall back to classification if needed
        if not self.current_context['condition_type']:
            condition_type, confidence = self._classify_condition_type(transcript)
            if confidence >= self.confidence_threshold:
                self.current_context['condition_type'] = condition_type

        # 2. Extract medical info if not already done
        if not any([
            self.current_context['measurements'], 
            self.current_context['symptoms'],
            self.current_context['covered_topics']
        ]):
            extracted_info = self._extract_information(transcript)
            self._update_context(extracted_info)

        # 3. Generate protocol-based guidance
        guidance = self._generate_protocol_guidance()

        # 4. Attempt translation if desired
        try:
            response = self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                system="You are a medical translation system...",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Translate these medical recommendations to Tagalog...
Symptom Guidance:
{json.dumps(guidance['symptom_guidance'], indent=2)}

Protocol Suggestions:
{json.dumps(guidance['protocol_suggestions'], indent=2)}"""
                    }
                ]
            )
            translations = extract_json_from_text(response.content[0].text)
            if not translations:
                translations = {
                    "tagalog": {
                        "symptoms": guidance['symptom_guidance'],
                        "protocols": guidance['protocol_suggestions']
                    },
                    "english": {
                        "symptoms": guidance['symptom_guidance'],
                        "protocols": guidance['protocol_suggestions']
                    }
                }
        except Exception as e:
            print(f"Error calling translation API: {str(e)}")
            translations = {
                "tagalog": {
                    "symptoms": guidance['symptom_guidance'],
                    "protocols": guidance['protocol_suggestions']
                },
                "english": {
                    "symptoms": guidance['symptom_guidance'],
                    "protocols": guidance['protocol_suggestions']
                }
            }

        # 5. Build final return structure
        return {
            'symptom_guidance': translations['tagalog']['symptoms'],
            'protocol_suggestions': translations['tagalog']['protocols'],
            'missing_information': guidance['missing_information'],
            'danger_signs': guidance['danger_signs'],
            'education_topics': guidance['education_topics']
        }

    def _classify_condition_type(self, transcript: str) -> Tuple[str, float]:
        """Uses LLM to classify condition (prenatal, communicable, or noncommunicable)."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": f"""Analyze this medical conversation and determine if it is:
- prenatal
- communicable
- non-communicable

Respond ONLY with the condition type and confidence score (0.0-1.0) separated by a pipe character.
Example: prenatal|0.95

Conversation:
{transcript}"""
            }]
        )

        try:
            condition_type, confidence = response.content[0].text.strip().split('|')
            return condition_type.strip(), float(confidence)
        except (ValueError, AttributeError, IndexError):
            return 'unknown', 0.0

    def _extract_information(self, transcript: str) -> Dict[str, Any]:
        """
        Extract key medical information from the transcript via LLM JSON format.
        Only add a 'danger_sign' if the user actually reports it, not merely
        when the BHW lists possible signs.
        """
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Analyze this medical conversation:
1. Identify the measurements the mother already has.
2. Gather any actual symptoms the mother says she is experiencing.
3. Gather any relevant risk factors and topics covered.
4. Determine the pregnancy trimester if possible.
5. ONLY include a danger sign (in "danger_signs") if the mother actually reports it, not just if the BHW mentions it as a possibility.

Use a JSON format:
{{"measurements":[],"symptoms":[],"risk_factors":[],"covered_topics":[],"trimester":null,"danger_signs":[]}}

Conversation Transcript:
{transcript}"""
            }]
        )

        try:
            extracted = extract_json_from_text(response.content[0].text)
            # If the LLM returned something, we parse it. Otherwise, use safe defaults.
            if not extracted:
                extracted = {
                    'measurements': [],
                    'symptoms': [],
                    'risk_factors': [],
                    'covered_topics': [],
                    'trimester': None,
                    'danger_signs': []
                }
            return extracted
        except (json.JSONDecodeError, AttributeError, IndexError):
            return {
                'measurements': [],
                'symptoms': [],
                'risk_factors': [],
                'covered_topics': [],
                'trimester': None,
                'danger_signs': []
            }

    def _update_context(self, extracted_info: Dict[str, Any]):
        """Update the current context with new data from the transcript info."""
        self.current_context.update(extracted_info)

    def _generate_protocol_guidance(self) -> Dict[str, List[str]]:
        """
        Generate guidance based on the current context using protocols from the BHW manual.
        Returns a structured analysis with distinct sections:
        - Realtime Alerts: Critical information needed during the exam
        - Missing Information: Required measurements/tests not yet done
        - Symptom-specific Guidance: Advice based on reported symptoms
        - Education Topics: Recommended topics to cover
        - Protocol Suggestions: Follow-up actions needed
        """
        # If no condition type, return empty sets
        if not self.current_context['condition_type']:
            return {
                'realtime_alerts': [],
                'symptom_guidance': [],
                'missing_information': [],
                'education_topics': [],
                'protocol_suggestions': [],
                'danger_signs': []  # Keep this for compatibility
            }

        # Get validation results from ProtocolManager
        validation = self.protocol_manager.validate_interaction(
            self.current_context['condition_type'],
            self.current_context
        )

        # Initialize guidance structure
        guidance = {
            'realtime_alerts': [],
            'symptom_guidance': [],
            'missing_information': [],
            'education_topics': validation.get('missing_topics', []),
            'protocol_suggestions': [],
            'danger_signs': self.current_context.get('danger_signs', [])  # Keep this for compatibility
        }

        # Filter out existing measurements from the missing list
        existing_lower = [m.lower() for m in self.current_context.get('measurements', [])]
        filtered_missing = []
        for item in validation.get('missing_measurements', []):
            if item.lower() not in existing_lower:
                filtered_missing.append(item)

        guidance['missing_information'] = filtered_missing

        # Deduplicate symptom guidance
        if validation.get('recommendations'):
            guidance['symptom_guidance'] = list(set(validation.get('recommendations', [])))

        # Create protocol suggestions only for truly missing items
        guidance['protocol_suggestions'] = [
            f"Schedule follow-up to check {m}" for m in filtered_missing
        ]

        return guidance

    # If you have separate accessor methods for missing info, danger signs, etc.,
    # you can keep them or remove them if no longer needed:
    def _get_missing_information(self) -> List[str]:
        """(Optional) If you want direct list of missing measurements from the BHW manual protocols."""
        if not self.current_context['condition_type']:
            return []
        required = self.protocol_manager.get_required_measurements(self.current_context['condition_type'])
        return [m for m in required if m not in self.current_context['measurements']]

    def _get_danger_signs(self) -> List[str]:
        """(Optional) If you want default or comprehensive danger signs, but typically not used if you want only transcript ones."""
        if not self.current_context['condition_type']:
            return []
        return self.protocol_manager.get_danger_signs(self.current_context['condition_type'])

    def _get_education_topics(self) -> List[str]:
        """(Optional) If you want a direct query for education topics."""
        if not self.current_context['condition_type']:
            return []
        required = self.protocol_manager.get_education_topics(self.current_context['condition_type'])
        return [t for t in required if t not in self.current_context['covered_topics']] 