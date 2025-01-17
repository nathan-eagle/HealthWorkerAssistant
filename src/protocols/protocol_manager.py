import json
from pathlib import Path
from typing import Dict, Any, Optional
from anthropic import Anthropic
import os
import re

def extract_json_from_text(text: str) -> dict:
    """Extract JSON object from text that might contain other content."""
    # Find anything that looks like a JSON object
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    return {}

class ProtocolManager:
    """Manages loading and accessing BHW protocol definitions."""
    
    def __init__(self):
        self.protocols_dir = Path(__file__).parent / "definitions"
        self.protocols: Dict[str, Any] = {}
        self._load_all_protocols()
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def _load_all_protocols(self):
        """Load all protocol JSON files from the definitions directory."""
        for protocol_file in self.protocols_dir.glob("*.json"):
            protocol_name = protocol_file.stem
            with open(protocol_file, 'r', encoding='utf-8') as f:
                self.protocols[protocol_name] = json.load(f)
    
    def get_protocol(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific protocol by name."""
        return self.protocols.get(name)
    
    def get_all_protocols(self) -> Dict[str, Any]:
        """Get all loaded protocols."""
        return self.protocols
    
    def get_vital_signs_protocol(self) -> Dict[str, Any]:
        """Get the basic assessment protocol for vital signs."""
        return self.get_protocol('basic-assessment')
    
    def get_maternal_protocol(self) -> Dict[str, Any]:
        """Get the maternal health protocol."""
        return self.get_protocol('maternal-health')
    
    def get_communicable_protocol(self) -> Dict[str, Any]:
        """Get the communicable disease protocol."""
        return self.get_protocol('communicable-disease')
    
    def get_noncommunicable_protocol(self) -> Dict[str, Any]:
        """Get the non-communicable disease protocol."""
        return self.get_protocol('noncommunicable-disease')
    
    def get_required_measurements(self, condition_type: str) -> list:
        """Get required measurements for a specific condition type."""
        if condition_type == 'prenatal':
            protocol = self.get_maternal_protocol()
            if protocol and 'trimester' in protocol:
                trimester = protocol['trimester'].lower()
                if trimester in protocol.get('trimester_specific', {}):
                    return protocol['trimester_specific'][trimester].get('required_measurements', [])
            return protocol.get('required_measurements', []) if protocol else []
        elif condition_type == 'communicable':
            protocol = self.get_communicable_protocol()
        elif condition_type == 'noncommunicable':
            protocol = self.get_noncommunicable_protocol()
        else:
            protocol = self.get_vital_signs_protocol()
            
        return protocol.get('required_measurements', []) if protocol else []
    
    def get_danger_signs(self, condition_type: str) -> list:
        """Get danger signs for a specific condition type."""
        protocol = self.get_protocol(f"{condition_type}-disease" if condition_type != 'prenatal' else 'maternal-health')
        return protocol.get('danger_signs', []) if protocol else []
    
    def get_education_topics(self, condition_type: str) -> list:
        """Get required health education topics for a condition type."""
        protocol = self.get_protocol(f"{condition_type}-disease" if condition_type != 'prenatal' else 'maternal-health')
        if protocol and condition_type == 'prenatal' and 'trimester' in protocol:
            trimester = protocol['trimester'].lower()
            if trimester in protocol.get('trimester_specific', {}):
                return protocol['trimester_specific'][trimester].get('education_topics', [])
        return protocol.get('education_topics', []) if protocol else []
    
    def validate_interaction(self, condition_type: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an interaction against the relevant protocol using LLM-based analysis."""
        protocol = self.get_protocol(f"{condition_type}-disease" if condition_type != 'prenatal' else 'maternal-health')
        if not protocol:
            return {"valid": False, "errors": ["Unknown condition type"]}

        # Get trimester-specific requirements for prenatal care
        if condition_type == 'prenatal' and 'trimester' in interaction_data:
            trimester = interaction_data['trimester'].lower()
            if 'second' in trimester.lower():
                trimester = 'second'
            elif 'third' in trimester.lower():
                trimester = 'third'
            elif 'first' in trimester.lower():
                trimester = 'first'
                
            if trimester in protocol.get('trimester_specific', {}):
                trimester_reqs = protocol['trimester_specific'][trimester]
                required_measurements = trimester_reqs.get('required_measurements', [])
                education_topics = trimester_reqs.get('education_topics', [])
            else:
                required_measurements = protocol.get('required_measurements', [])
                education_topics = protocol.get('education_topics', [])
        else:
            required_measurements = protocol.get('required_measurements', [])
            education_topics = protocol.get('education_topics', [])

        # Get symptom guidance if available
        symptom_guidance = {}
        if 'symptoms' in interaction_data and 'symptom_guidance' in protocol:
            for symptom in interaction_data['symptoms']:
                symptom_key = symptom.lower().replace(' ', '_')
                if symptom_key in protocol['symptom_guidance']:
                    symptom_guidance[symptom] = protocol['symptom_guidance'][symptom_key]

        # Ask Claude to analyze measurements and topics
        measurement_analysis = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""For each required measurement, determine if it has been taken based on the measurements list.
Consider semantic variations, Filipino terms, and different ways of expressing the same measurement.

For example:
- "Blood pressure" matches "BP", "presyon", "blood pressure reading"
- "Weight" matches "timbang", "kilos", "weight measurement"
- "Fundal height" matches "fundal measurement", "uterine height", "fundal"
- "Fetal heart rate" matches "FHR", "baby's heartbeat", "fetal heartbeat"
- "Edema check" matches "swelling check", "pamamaga", "edema assessment"
- "Urinalysis" matches "urine test", "ihi test", "protein and sugar in urine"

Required measurements:
{json.dumps(required_measurements, indent=2)}

Measurements taken:
{json.dumps(interaction_data.get('measurements', []), indent=2)}

Respond with ONLY a JSON object in this format:
{{
    "taken": [],     // List of required measurements that were taken
    "missing": []    // List of required measurements that still need to be taken
}}"""
            }]
        )

        # Ask Claude to analyze danger signs
        danger_analysis = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Analyze if any danger signs are present in the symptoms or risk factors.
Consider semantic variations and Filipino terms.

For example, these would indicate danger signs:
- "Severe headache" matches "matinding sakit ng ulo", "intense headache"
- "Vaginal bleeding" matches "pagdurugo", "spotting", "bleeding"
- "Decreased fetal movement" matches "hindi gumagalaw ang sanggol", "less baby movement"
- "High fever" matches "lagnat", "mataas na lagnat", "fever"
- "Difficulty breathing" matches "hirap huminga", "shortness of breath"

Respond with ONLY a JSON object with one key "detected_signs" containing a list of identified danger signs.

Possible danger signs:
{json.dumps(protocol.get('danger_signs', []), indent=2)}

Patient symptoms:
{json.dumps(interaction_data.get('symptoms', []), indent=2)}

Risk factors:
{json.dumps(interaction_data.get('risk_factors', []), indent=2)}"""
            }]
        )

        try:
            measurements = extract_json_from_text(measurement_analysis.content[0].text)
            danger_signs = extract_json_from_text(danger_analysis.content[0].text)
            
            # Generate recommendations based on findings
            recommendations = []
            
            # Add symptom-specific guidance
            for symptom, guidance in symptom_guidance.items():
                recommendations.extend(guidance)
            
            # Add recommendations for missing measurements
            for measurement in measurements.get('missing', []):
                recommendations.append(f"Schedule follow-up to check {measurement}")
            
            # Add recommendations for uncovered education topics
            covered = set(topic.lower() for topic in interaction_data.get('covered_topics', []))
            missing_topics = []
            for topic in education_topics:
                if not any(covered_topic in topic.lower() for covered_topic in covered):
                    missing_topics.append(topic)
                    recommendations.append(f"Discuss {topic} during next visit")
            
            return {
                "valid": not (measurements.get('missing', []) or missing_topics or danger_signs.get('detected_signs', [])),
                "missing_measurements": measurements.get('missing', []),
                "missing_topics": missing_topics,
                "detected_danger_signs": danger_signs.get('detected_signs', []),
                "recommendations": recommendations
            }
            
        except Exception as e:
            print(f"Error during validation: {str(e)}")
            return {
                "valid": False,
                "missing_measurements": [],
                "missing_topics": [],
                "detected_danger_signs": [],
                "recommendations": [],
                "errors": [f"Validation error: {str(e)}"]
            } 