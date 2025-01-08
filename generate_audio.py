import os
from openai import OpenAI
from pathlib import Path
import re
import json
from datetime import datetime
from pydub import AudioSegment
import tempfile

class AudioGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.voices = {
            "BHW": "nova",  # Female voice for BHW
            "Patient_F": "alloy",  # Female voice for female patients
            "Patient_M": "echo"  # Male voice for male patients
        }

    def extract_dialogues(self, transcript_path):
        """Extract timestamped dialogues from transcript file."""
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip header lines and get to dialogue
        dialogue_text = content.split('\n\n', 2)[-1]
        
        # Extract all dialogue lines with timestamps
        pattern = r'\[(\d{2}:\d{2})\] (BHW|Patient): (.+)'
        matches = re.finditer(pattern, dialogue_text)
        
        dialogues = []
        for match in matches:
            timestamp, speaker, text = match.groups()
            minutes, seconds = map(int, timestamp.split(':'))
            total_milliseconds = (minutes * 60 + seconds) * 1000
            
            dialogues.append({
                'timestamp': timestamp,
                'timestamp_ms': total_milliseconds,
                'speaker': speaker,
                'text': text.strip()
            })
        
        return dialogues

    def determine_patient_gender(self, dialogues):
        """Determine patient gender based on context clues in the dialogue."""
        text = ' '.join(d['text'].lower() for d in dialogues[:10])
        male_indicators = ['kuya', 'sir', 'tatay', 'tito', 'manong']
        female_indicators = ['ate', 'maam', 'nanay', 'tita', 'manang', 'aling']
        
        male_count = sum(1 for ind in male_indicators if ind in text)
        female_count = sum(1 for ind in female_indicators if ind in text)
        
        return "Patient_M" if male_count > female_count else "Patient_F"

    def generate_audio_segment(self, text, voice):
        """Generate audio for a single dialogue line."""
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=1.0
        )
        return response.content

    def create_conversation_audio(self, transcript_path, language="tagalog"):
        """Create a single audio file from a transcript with different voices for speakers."""
        # Create output directory
        output_dir = f"audio_output/{language.lower()}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract dialogues from transcript
        dialogues = self.extract_dialogues(transcript_path)
        
        # Determine patient gender
        patient_voice_key = self.determine_patient_gender(dialogues)
        
        print(f"Processing {Path(transcript_path).name}...")
        
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate all audio segments
            segments = []
            for i, dialogue in enumerate(dialogues):
                print(f"Generating audio for line {i+1}/{len(dialogues)}...")
                
                # Generate audio for this line
                voice = self.voices["BHW"] if dialogue['speaker'] == "BHW" else self.voices[patient_voice_key]
                audio_data = self.generate_audio_segment(dialogue['text'], voice)
                
                # Save temporary audio file
                temp_path = Path(temp_dir) / f"temp_{i}.mp3"
                with open(temp_path, 'wb') as f:
                    f.write(audio_data)
                
                # Load and normalize the audio segment
                segment = AudioSegment.from_mp3(temp_path)
                normalized_segment = segment.normalize()
                
                # Calculate natural pause based on timestamp difference
                if i > 0:
                    time_diff = dialogue['timestamp_ms'] - dialogues[i-1]['timestamp_ms']
                    pause_duration = min(time_diff, 1500)  # Max 1.5 second pause
                    pause_duration = max(pause_duration, 300)  # Min 0.3 second pause
                else:
                    pause_duration = 500  # Initial pause
                
                segments.append({
                    'audio': normalized_segment,
                    'timestamp_ms': dialogue['timestamp_ms'],
                    'pause_before': pause_duration,
                    'duration': len(normalized_segment)
                })
            
            # Calculate total duration needed
            max_time = max(s['timestamp_ms'] + s['duration'] for s in segments)
            
            # Create the final audio
            final_audio = AudioSegment.silent(duration=max_time)
            
            # Add segments with appropriate spacing
            current_position = 0
            for segment_data in segments:
                current_position += segment_data['pause_before']
                audio = segment_data['audio'].fade_in(20).fade_out(20)
                final_audio = final_audio.overlay(audio, position=current_position)
                current_position += len(audio)
            
            # Normalize final audio
            final_audio = final_audio.normalize()
            
            # Save the final audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = Path(transcript_path).stem
            output_path = Path(output_dir) / f"{base_filename}_{timestamp}.mp3"
            
            # Export with high quality
            final_audio.export(
                output_path,
                format="mp3",
                bitrate="192k",
                parameters=["-ac", "2"]  # Force stereo output
            )
            
            print(f"Generated conversation audio: {output_path}")
            return output_path

    def generate_all_audio(self, language="tagalog"):
        """Generate audio for all dialogue files in the specified language."""
        transcript_dir = f"transcripts/{language.lower()}"
        generated_files = []
        
        for filename in os.listdir(transcript_dir):
            if filename.startswith('dialogue_') and filename.endswith('.txt'):
                transcript_path = os.path.join(transcript_dir, filename)
                audio_file = self.create_conversation_audio(transcript_path, language)
                generated_files.append(audio_file)
        
        return generated_files 