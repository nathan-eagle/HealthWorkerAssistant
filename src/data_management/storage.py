import os
import json
import datetime
from pathlib import Path

class DataStorage:
    def __init__(self):
        self.base_dir = Path("data")
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        
        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def store_interaction(self, audio_data, transcript, guidance):
        """Store a complete interaction including audio, transcript, and guidance."""
        # Generate timestamp for unique identification
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Store audio data
        audio_path = self.raw_dir / "audio" / f"interaction_{timestamp}.wav"
        self._save_audio(audio_data, audio_path)
        
        # Store transcript and guidance
        metadata = {
            "timestamp": timestamp,
            "audio_file": str(audio_path),
            "transcript": transcript,
            "guidance": guidance
        }
        
        metadata_path = self.processed_dir / "analysis" / f"interaction_{timestamp}.json"
        self._save_metadata(metadata, metadata_path)

    def _save_audio(self, audio_data, path):
        """Save audio data to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(audio_data)

    def _save_metadata(self, metadata, path):
        """Save metadata to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def get_interaction(self, timestamp):
        """Retrieve a stored interaction by timestamp."""
        audio_path = self.raw_dir / "audio" / f"interaction_{timestamp}.wav"
        metadata_path = self.processed_dir / "analysis" / f"interaction_{timestamp}.json"
        
        if not audio_path.exists() or not metadata_path.exists():
            return None
            
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            
        return metadata 