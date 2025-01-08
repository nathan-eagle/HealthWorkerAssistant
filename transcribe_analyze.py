import os
from anthropic import Anthropic
from openai import OpenAI
from pathlib import Path
import json

class AudioAnalyzer:
    def __init__(self, anthropic_api_key=None, openai_api_key=None):
        self.claude = Anthropic(api_key=anthropic_api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.openai = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))
        
    def transcribe_audio(self, audio_file_path):
        """Transcribe Tagalog audio file using OpenAI's Whisper model."""
        with open(audio_file_path, 'rb') as audio:
            response = self.openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                language="tl",  # ISO code for Tagalog
                response_format="text",
                prompt="This is a conversation between a Barangay Health Worker and a patient in Tagalog (Tayabas dialect)."
            )
        return str(response)  # Ensure we return a string

    def translate_transcription(self, tagalog_text):
        """Translate Tagalog transcription to English using Claude."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"Please translate this Tagalog medical conversation to English, maintaining all speaker labels and timestamps if present:\n\n{tagalog_text}"
            }]
        )
        return str(response.content)  # Ensure we return a string

    def analyze_interaction(self, english_transcription):
        """Analyze the interaction and provide medical insights."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Please analyze this medical conversation and provide:

1. Patient Diagnosis:
[Provide a thorough diagnosis of the simulated patient]

2. Additional Questions:
[List additional questions that should have been asked]

3. Recommendations:
[Provide recommendations for improving the interaction]

4. Red Flags and Concerns:
[List any red flags or concerns that should be addressed]

5. Cultural Competency Observations:
[Provide observations about cultural competency in the interaction]

Conversation transcript:
{english_transcription}"""
            }]
        )
        return str(response.content)  # Ensure we return a string

    def process_audio_file(self, audio_file_path):
        """Process a single audio file through the entire pipeline."""
        print(f"\nProcessing: {audio_file_path}")
        
        # Create output paths
        base_name = Path(audio_file_path).stem
        tagalog_trans_path = f"Interaction_Analysis/transcriptions/{base_name}_tagalog.txt"
        english_trans_path = f"Interaction_Analysis/transcriptions/{base_name}_english.txt"
        analysis_path = f"Interaction_Analysis/analysis/{base_name}_analysis.txt"
        
        # Ensure directories exist
        os.makedirs("Interaction_Analysis/transcriptions", exist_ok=True)
        os.makedirs("Interaction_Analysis/analysis", exist_ok=True)
        
        try:
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
            
            # Save analysis as plain text
            with open(analysis_path, 'w', encoding='utf-8') as f:
                f.write(analysis)
            
            return {
                "audio_file": audio_file_path,
                "tagalog_transcription": tagalog_trans_path,
                "english_transcription": english_trans_path,
                "analysis": analysis_path
            }
            
        except Exception as e:
            print(f"Error processing {audio_file_path}: {str(e)}")
            return None

    def process_all_recordings(self):
        """Process all Tagalog audio files in the Synthetic_Interactions directory."""
        audio_dir = "Synthetic_Interactions/audio"
        results = []
        
        for filename in os.listdir(audio_dir):
            if filename.endswith(".mp3") and not filename.startswith(".") and "tagalog" in filename.lower():
                audio_path = os.path.join(audio_dir, filename)
                result = self.process_audio_file(audio_path)
                if result:
                    results.append(result)
        
        return results 