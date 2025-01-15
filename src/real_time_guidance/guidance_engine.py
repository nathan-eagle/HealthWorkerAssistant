import json
from pathlib import Path
from typing import Dict, Any, List
from ..protocols.protocol_manager import ProtocolManager

class GuidanceEngine:
    def __init__(self):
        self.protocol_manager = ProtocolManager()
        self.current_context = {
            'condition_type': None,
            'measurements': [],
            'symptoms': [],
            'covered_topics': [],
            'risk_factors': []
        }

    def generate_guidance(self, transcript: str) -> Dict[str, Any]:
        """Generate real-time guidance based on the current transcript."""
        # Extract key information from transcript
        extracted_info = self._extract_information(transcript)
        
        # Update conversation context
        self._update_context(extracted_info)
        
        # Generate guidance based on protocols and context
        guidance = self._generate_protocol_guidance()
        
        return guidance

    def _extract_information(self, transcript: str) -> Dict[str, Any]:
        """Extract key clinical information from the transcript."""
        # TODO: Implement more sophisticated information extraction
        info = {
            'measurements': [],
            'symptoms': [],
            'covered_topics': [],
            'risk_factors': []
        }
        
        # Detect condition type if not set
        if not self.current_context['condition_type']:
            if 'pregnancy' in transcript.lower() or 'prenatal' in transcript.lower():
                info['condition_type'] = 'prenatal'
            # Add more condition type detection logic
        
        return info

    def _update_context(self, new_info: Dict[str, Any]):
        """Update the conversation context with new information."""
        for key, value in new_info.items():
            if isinstance(value, list):
                self.current_context[key].extend(value)
            else:
                self.current_context[key] = value

    def _generate_protocol_guidance(self) -> Dict[str, Any]:
        """Generate guidance based on current context and protocols."""
        condition_type = self.current_context.get('condition_type')
        if not condition_type:
            return self._generate_initial_guidance()
            
        # Validate current interaction against protocol
        validation = self.protocol_manager.validate_interaction(
            condition_type,
            self.current_context
        )
        
        guidance = {
            "missing_information": [],
            "protocol_suggestions": [],
            "danger_signs": [],
            "education_topics": []
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
            'risk_factors': []
        } 