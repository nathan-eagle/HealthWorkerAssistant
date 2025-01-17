from pathlib import Path
from typing import Optional, Dict, List, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class VisitType(str, Enum):
    """Types of BHW visits based on DOH manual"""
    ROUTINE = "routine"
    MATERNAL = "maternal"
    CHILD = "child"
    EMERGENCY = "emergency"
    HEALTH_EDUCATION = "health_education"
    FOLLOW_UP = "follow_up"

class VitalSign(BaseModel):
    """Physical measurements with validation ranges from DOH manual"""
    type: str
    value: float
    unit: str
    timestamp: datetime
    equipment_used: Optional[str]
    measurement_site: Optional[str]
    measurement_method: Optional[str]
    is_within_normal: bool
    normal_range: Dict[str, float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "blood_pressure",
                "value": 120,
                "unit": "mmHg",
                "equipment_used": "aneroid_sphygmomanometer",
                "measurement_site": "right_arm",
                "measurement_method": "auscultatory",
                "normal_range": {"min": 90, "max": 140}
            }
        }

class ClinicalFinding(BaseModel):
    """Clinical observations with references to DOH protocols"""
    type: str
    description: str
    severity: Optional[str]
    duration: Optional[str]
    requires_referral: bool
    protocol_reference: str  # Reference to specific DOH protocol
    finding_source: str  # e.g., "patient_report", "bhw_observation"

class HealthEducation(BaseModel):
    """Health education topics covered during visit"""
    topic: str
    key_messages: List[str]
    materials_provided: Optional[List[str]]
    follow_up_needed: bool
    protocol_reference: str

class Referral(BaseModel):
    """Referral details based on DOH guidelines"""
    reason: str
    urgency: str  # "immediate", "within_24_hours", "routine"
    facility_type: str  # "health_center", "hospital", etc.
    protocol_reference: str
    clinical_summary: str
    vital_signs: List[VitalSign]
    findings: List[ClinicalFinding]

class Visit(BaseModel):
    """Core model for a BHW visit"""
    id: str
    type: VisitType
    timestamp: datetime
    bhw_id: str
    patient_id: str
    location: str  # "home", "health_station", etc.
    vital_signs: List[VitalSign]
    findings: List[ClinicalFinding]
    education_provided: Optional[List[HealthEducation]]
    referral: Optional[Referral]
    next_visit_scheduled: Optional[datetime]
    
    class Config:
        arbitrary_types_allowed = True

class Protocol:
    """Base class for DOH-based clinical protocols"""
    
    def __init__(self, protocol_id: str, version: str):
        self.id = protocol_id
        self.version = version
        self.load_protocol_rules()
    
    def load_protocol_rules(self):
        """Load protocol rules from JSON files"""
        pass
    
    def validate_findings(self, findings: List[ClinicalFinding]) -> List[str]:
        """Validate findings against protocol rules"""
        pass
    
    def check_referral_needed(self, 
                            findings: List[ClinicalFinding],
                            vital_signs: List[VitalSign]) -> Optional[Referral]:
        """Check if referral is needed based on DOH guidelines"""
        pass

class OfflineSync:
    """Handles offline storage and sync of visit data"""
    
    def __init__(self, local_db_path: Path):
        self.db_path = local_db_path
        # Initialize SQLite database with proper schema
        
    async def save_visit(self, visit: Visit):
        """Save visit to local storage"""
        pass
    
    async def sync_when_online(self):
        """Sync local data when connection available"""
        pass
    
    def get_pending_syncs(self) -> List[Dict]:
        """Get list of records pending sync"""
        pass

class VoiceRecorder:
    """Handles voice recording with quality checks"""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        
    async def start_recording(self) -> Path:
        """Start recording visit"""
        pass
    
    async def stop_recording(self):
        """Stop recording and save audio file"""
        pass
    
    def check_audio_quality(self) -> Dict:
        """Check recording quality metrics"""
        pass

class BHWAssistant:
    """Main class for providing BHW decision support"""
    
    def __init__(self,
                 config: Dict,
                 protocol_path: Path,
                 offline_sync: OfflineSync):
        self.config = config
        self.protocols = self.load_protocols(protocol_path)
        self.sync = offline_sync
        
    def load_protocols(self, protocol_path: Path) -> Dict[str, Protocol]:
        """Load all protocol definitions"""
        pass
    
    async def start_visit(self, 
                         visit_type: VisitType,
                         patient_id: str,
                         location: str) -> Visit:
        """Start a new visit"""
        pass
    
    async def record_vital_sign(self,
                              visit_id: str,
                              vital_sign: VitalSign):
        """Record a vital sign measurement"""
        pass
    
    async def record_finding(self,
                           visit_id: str,
                           finding: ClinicalFinding):
        """Record a clinical finding"""
        pass
        
    def get_protocol_recommendations(self,
                                   visit: Visit) -> Dict[str, Union[str, List[str]]]:
        """Get recommendations based on protocols"""
        pass