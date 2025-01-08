import os
from anthropic import Anthropic
from pathlib import Path
import json

class AudioAnalyzer:
    def __init__(self, api_key=None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        
    def transcribe_audio(self, audio_file_path):
        """Transcribe Tagalog audio file using Claude."""
        with open(audio_file_path, 'rb') as audio:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please transcribe this Tagalog audio file of a conversation between a Barangay Health Worker and a patient. Maintain all speaker labels and include timestamps."
                        },
                        {
                            "type": "audio",
                            "audio": audio
                        }
                    ]
                }]
            )
        return response.content

    def translate_transcription(self, tagalog_text):
        """Translate Tagalog transcription to English using Claude."""
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"Please translate this Tagalog medical conversation to English, maintaining all speaker labels and timestamps:\n\n{tagalog_text}"
            }]
        )
        return response.content

    def analyze_interaction(self, english_transcription):
        """Analyze the interaction and provide medical insights."""
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Please analyze this medical conversation and provide:
1. A thorough diagnosis of the simulated patient
2. Additional questions that should have been asked
3. Recommendations for improving the interaction
4. Any red flags or concerns that should be addressed
5. Cultural competency observations

Conversation transcript:
{english_transcription}"""
            }]
        )
        return response.content

    def process_audio_file(self, audio_file_path):
        """Process a single audio file through the entire pipeline."""
        print(f"\nProcessing: {audio_file_path}")
        
        # Create output paths
        base_name = Path(audio_file_path).stem
        tagalog_trans_path = f"audio_transcription/{base_name}_tagalog.txt"
        english_trans_path = f"audio_transcription/{base_name}_english.txt"
        analysis_path = f"copilot_output/{base_name}_analysis.json"
        
        # Ensure directories exist
        os.makedirs("audio_transcription", exist_ok=True)
        os.makedirs("copilot_output", exist_ok=True)
        
        # 1. Transcribe audio
        print("Transcribing audio...")
        tagalog_transcription = self.transcribe_audio(audio_file_path)
        with open(tagalog_trans_path, 'w', encoding='utf-8') as f:
            f.write(tagalog_transcription)
        
        # 2. Translate to English
        print("Translating to English...")
        english_transcription = self.translate_transcription(tagalog_transcription)
        with open(english_trans_path, 'w', encoding='utf-8') as f:
            f.write(english_transcription)
        
        # 3. Analyze interaction
        print("Analyzing interaction...")
        analysis = self.analyze_interaction(english_transcription)
        
        # Save analysis as JSON
        analysis_data = {
            "audio_file": audio_file_path,
            "tagalog_transcription": tagalog_trans_path,
            "english_transcription": english_trans_path,
            "analysis": analysis
        }
        
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        return analysis_data

    def process_all_recordings(self):
        """Process all audio files in the interview_recordings directory."""
        recordings_dir = "interview_recordings"
        results = []
        
        for filename in os.listdir(recordings_dir):
            if filename.endswith(".mp3") and not filename.startswith("."):
                audio_path = os.path.join(recordings_dir, filename)
                result = self.process_audio_file(audio_path)
                results.append(result)
        
        return results 