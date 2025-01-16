import json
from pathlib import Path
from typing import Dict, Any, Optional
from anthropic import Anthropic
import os

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
        """Validate an interaction against the relevant protocol using LLM-based analysis."""
        protocol = self.get_protocol(f"{condition_type}-disease" if condition_type != 'prenatal' else 'maternal-health')
        if not protocol:
            return {"valid": False, "errors": ["Unknown condition type"]}

        # Prepare protocol requirements for LLM analysis
        protocol_info = {
            "required_measurements": protocol.get('required_measurements', []),
            "education_topics": protocol.get('education_topics', []),
            "danger_signs": protocol.get('danger_signs', [])
        }

        # Ask Claude to analyze the interaction against protocol requirements
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Analyze this health interaction data against the protocol requirements.
Consider Filipino terms, variations in descriptions, and semantic meaning rather than exact matches.

Protocol Requirements:
{json.dumps(protocol_info, indent=2)}

Interaction Data:
{json.dumps(interaction_data, indent=2)}

Provide analysis results in this JSON format:
{{
    "missing_measurements": [], // Required measurements not taken/mentioned
    "missing_topics": [], // Required education topics not covered
    "detected_danger_signs": [], // Identified danger signs from symptoms
    "recommendations": [] // List of guidance points based on findings
}}

For recommendations, provide clear, actionable guidance points that consider:
1. Semantic matching (e.g. "blood pressure" matches "BP", "presyon")
2. Filipino terms and code-switching
3. Implicit mentions and context
4. Cultural health practices

Each recommendation should be a clear, complete statement without any special formatting."""
            }]
        )

        try:
            validation_results = json.loads(response.content[0].text)
            validation_results["valid"] = not (
                validation_results["missing_measurements"] or 
                validation_results["missing_topics"] or 
                validation_results["detected_danger_signs"]
            )
            return validation_results
        except json.JSONDecodeError:
            return {
                "valid": False,
                "missing_measurements": [],
                "missing_topics": [],
                "detected_danger_signs": [],
                "recommendations": [],
                "errors": ["Failed to parse validation results"]
            } 