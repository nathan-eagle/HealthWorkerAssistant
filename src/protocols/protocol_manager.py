import json
from pathlib import Path
from typing import Dict, Any, Optional

class ProtocolManager:
    """Manages loading and accessing BHW protocol definitions."""
    
    def __init__(self):
        self.protocols_dir = Path(__file__).parent / "definitions"
        self.protocols: Dict[str, Any] = {}
        self._load_all_protocols()
    
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
        return protocol.get('education_topics', []) if protocol else []
    
    def validate_interaction(self, condition_type: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an interaction against the relevant protocol."""
        protocol = self.get_protocol(f"{condition_type}-disease" if condition_type != 'prenatal' else 'maternal-health')
        if not protocol:
            return {"valid": False, "errors": ["Unknown condition type"]}
            
        validation = {
            "valid": True,
            "missing_measurements": [],
            "missing_topics": [],
            "detected_danger_signs": [],
            "recommendations": []
        }
        
        # Check required measurements
        required_measurements = protocol.get('required_measurements', [])
        for measurement in required_measurements:
            if measurement not in interaction_data.get('measurements', []):
                validation['missing_measurements'].append(measurement)
        
        # Check education topics
        required_topics = protocol.get('education_topics', [])
        for topic in required_topics:
            if topic not in interaction_data.get('covered_topics', []):
                validation['missing_topics'].append(topic)
        
        # Check for danger signs
        danger_signs = protocol.get('danger_signs', [])
        for sign in danger_signs:
            if sign in interaction_data.get('symptoms', []):
                validation['detected_danger_signs'].append(sign)
        
        # Update validity
        validation['valid'] = not (validation['missing_measurements'] or 
                                 validation['missing_topics'] or 
                                 validation['detected_danger_signs'])
        
        return validation 