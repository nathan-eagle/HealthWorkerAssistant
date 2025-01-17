import os
from openai import OpenAI
from pathlib import Path
import re
import json
from datetime import datetime
from pydub import AudioSegment
import tempfile
from anthropic import Anthropic

class AudioGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.voices = {
            "BHW": "nova",  # Female voice for BHW
            "Patient_F": "alloy",  # Female voice for female patients
            "Patient_M": "echo"  # Male voice for male patients
        }
        self.text_dir = Path("data/synthetic/text")
        self.audio_dir = Path("data/synthetic/audio")

    def determine_patient_gender(self, dialogues, condition_type=None):
        """Determine patient gender based on context clues in the dialogue."""
        # Force female for prenatal conditions
        if condition_type and "prenatal" in condition_type.lower():
            print("Prenatal condition detected - setting patient gender to Female")
            return "Patient_F"

        # Join dialogue text for analysis
        dialogue_text = '\n'.join(f"{d.get('speaker', 'Unknown')}: {d.get('text', '')}" for d in dialogues)
        
        # Use Claude to analyze the dialogue
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": f"""Analyze this medical conversation between a BHW and patient. Determine the patient's gender based on context clues, pronouns, terms of address, and cultural indicators.

Consider:
1. Filipino terms of address (e.g., ate, kuya)
2. Pronouns used
3. Context of the conversation
4. Cultural indicators

Respond with EXACTLY one word: "male" or "female"

Conversation:
{dialogue_text}"""
            }]
        )
        
        gender = response.content[0].text.strip().lower()
        print(f"Gender detection - LLM determined patient is: {gender}")
        
        return "Patient_F" if gender == "female" else "Patient_M"

    def extract_dialogues(self, transcript_path):
        """Extract dialogues from transcript file, with or without timestamps."""
        with open(transcript_path, 'r', encoding='utf-8') as f:
            dialogue_text = f.read()
        
        dialogues = []
        
        # Try parsing with timestamps first
        timestamp_pattern = r'\[(\d{2}:\d{2})\] ([^:]+): (.+)'
        matches = re.finditer(timestamp_pattern, dialogue_text)
        
        # If we find timestamped lines, use those
        has_timestamped_lines = False
        for match in matches:
            has_timestamped_lines = True
            _, speaker, text = match.groups()
            
            # Clean up any extra whitespace and quotes
            text = text.strip().strip('"\'')
            
            # Simplify speaker detection - if it's not BHW, it's Patient
            speaker = "BHW" if "BHW" in speaker else "Patient"
            
            dialogues.append({
                'speaker': speaker,
                'text': text
            })
        
        # If no timestamped lines found, try parsing without timestamps
        if not has_timestamped_lines:
            # Split by newlines and process each non-empty line
            for line in dialogue_text.split('\n'):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                # Try to split on colon for speaker and text
                parts = line.split(':', 1)
                if len(parts) == 2:
                    speaker, text = parts
                    
                    # Clean up speaker and text
                    speaker = speaker.strip()
                    text = text.strip().strip('"\'')
                    
                    # Simplify speaker detection - if it's not BHW, it's Patient
                    speaker = "BHW" if "BHW" in speaker else "Patient"
                    
                    dialogues.append({
                        'speaker': speaker,
                        'text': text
                    })
        
        return dialogues, None

    def generate_audio_segment(self, text, voice):
        """Generate audio for a single dialogue line."""
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=1.0
        )
        return response.content

    def create_conversation_audio(self, transcript_path):
        """Create a single audio file from a transcript with different voices for speakers."""
        # Create output directory
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract dialogues from transcript
        dialogues, _ = self.extract_dialogues(transcript_path)
        if not dialogues:
            print("No dialogues found in transcript")
            return None
        
        # Determine patient gender based on the dialogue content
        patient_voice_key = self.determine_patient_gender(dialogues)
        print(f"\nDetected patient gender: {'Male' if patient_voice_key == 'Patient_M' else 'Female'}")
        
        print(f"\nProcessing {Path(transcript_path).name}...")
        
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate all audio segments
            segments = []
            for i, dialogue in enumerate(dialogues):
                print(f"Generating audio for line {i+1}/{len(dialogues)}: {dialogue['speaker']} - {dialogue['text'][:50]}...")
                
                # Generate audio for this line
                voice = self.voices["BHW"] if dialogue['speaker'] == "BHW" else self.voices[patient_voice_key]
                try:
                    audio_data = self.generate_audio_segment(dialogue['text'], voice)
                    
                    # Save temporary audio file
                    temp_path = Path(temp_dir) / f"temp_{i}.mp3"
                    with open(temp_path, 'wb') as f:
                        f.write(audio_data)
                    
                    # Load the audio segment
                    segment = AudioSegment.from_mp3(temp_path)
                    
                    segments.append({
                        'audio': segment,
                        'duration': len(segment),
                        'speaker': dialogue['speaker']
                    })
                    
                except Exception as e:
                    print(f"Error generating audio for line {i+1}: {str(e)}")
                    continue
            
            if not segments:
                print("No audio segments were generated successfully.")
                return None
            
            # Create the final audio
            final_audio = AudioSegment.empty()
            
            # Add segments with natural spacing
            for i, segment_data in enumerate(segments):
                # Add a pause between segments
                if i > 0:
                    pause_duration = 750 if segments[i-1]['speaker'] != segment_data['speaker'] else 500
                    final_audio += AudioSegment.silent(duration=pause_duration)
                
                # Add the segment with fades
                audio = segment_data['audio'].fade_in(100).fade_out(100)
                final_audio += audio
                
                print(f"Added {segment_data['speaker']} segment (duration: {segment_data['duration']}ms)")
            
            # Add a short silence at the end
            final_audio += AudioSegment.silent(duration=500)
            
            # Use the same base name as the text file
            base_name = Path(transcript_path).stem
            output_path = self.audio_dir / f"{base_name}.mp3"
            
            # Export with high quality
            final_audio.export(
                output_path,
                format="mp3",
                bitrate="192k",
                parameters=["-ac", "2"]  # Force stereo output
            )
            
            print(f"\nGenerated conversation audio: {output_path}")
            return output_path

    def generate_all_audio(self):
        """Generate audio for all dialogue files, skipping those that already have audio."""
        generated_files = []
        
        # Get list of existing audio files
        existing_audio = {f.stem for f in self.audio_dir.glob("*.mp3")}
        
        for transcript_path in self.text_dir.glob("*.txt"):
            # Use the same base name as the text file
            base_name = transcript_path.stem
            expected_audio_path = self.audio_dir / f"{base_name}.mp3"
            
            # Check if audio already exists
            if base_name in existing_audio:
                print(f"\nSkipping {transcript_path.name} - audio already exists")
                generated_files.append(expected_audio_path)
                continue
            
            # Generate audio if it doesn't exist
            audio_file = self.create_conversation_audio(transcript_path)
            if audio_file:
                generated_files.append(audio_file)
        
        return generated_files 