import os
from anthropic import Anthropic
from openai import OpenAI
from pathlib import Path

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
        return str(response)

    def extract_claude_content(self, response):
        """Extract clean text content from Claude's response."""
        content = response.content
        if isinstance(content, list):
            content = content[0].text
        return content.strip()

    def structure_transcription(self, raw_transcription):
        """Use Claude to structure the transcription with proper speaker labels."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Please analyze this medical conversation between a Barangay Health Worker (BHW) and a patient.
Structure it with timestamps and speaker labels (BHW or Patient) based on the context of each statement.
Use this exact format for each line, with no introduction or other text:
[MM:SS] Speaker: Text

Here's the conversation:
{raw_transcription}"""
            }]
        )
        return self.extract_claude_content(response)

    def translate_transcription(self, tagalog_text):
        """Translate Tagalog transcription to English using Claude."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Translate this Tagalog medical conversation to English.
Use the exact same format with timestamps and speaker labels, with no introduction or other text:

{tagalog_text}"""
            }]
        )
        return self.extract_claude_content(response)

    def analyze_interaction(self, english_transcription):
        """Analyze the interaction and provide medical insights."""
        response = self.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Analyze this medical conversation and provide a detailed assessment.
Use this exact format with no introduction or conclusion:

1. Patient Diagnosis
Provide a thorough diagnosis based on the symptoms and information discussed.

2. Additional Questions
List specific questions that should have been asked to gather more relevant information.

3. Recommendations
Provide concrete recommendations for improving the healthcare interaction.

4. Red Flags and Concerns
Identify any concerning aspects of the patient's condition or the interaction that need attention.

5. Cultural Competency Observations
Discuss how cultural factors were handled and could be better addressed.

Conversation transcript:
{english_transcription}"""
            }]
        )
        return self.extract_claude_content(response)

    def get_simplified_name(self, audio_file_path):
        """Extract a simplified name from the audio file path."""
        return Path(audio_file_path).stem

    def process_audio_file(self, audio_file_path):
        """Process a single audio file through the entire pipeline."""
        print(f"\nProcessing: {audio_file_path}")
        
        # Create simplified base name
        audio_filename = Path(audio_file_path).stem
        
        # Create output paths using the exact audio filename stem
        tagalog_trans_path = f"Interaction_Analysis/transcriptions/{audio_filename}_tagalog.txt"
        english_trans_path = f"Interaction_Analysis/transcriptions/{audio_filename}_english.txt"
        analysis_path = f"Interaction_Analysis/analysis/{audio_filename}_analysis.txt"
        
        # Ensure directories exist
        os.makedirs("Interaction_Analysis/transcriptions", exist_ok=True)
        os.makedirs("Interaction_Analysis/analysis", exist_ok=True)
        
        try:
            # Check if all files exist
            if (os.path.exists(tagalog_trans_path) and 
                os.path.exists(english_trans_path) and 
                os.path.exists(analysis_path)):
                print(f"All files already exist for {audio_filename}, skipping processing")
                return {
                    "audio_file": audio_file_path,
                    "tagalog_transcription": tagalog_trans_path,
                    "english_transcription": english_trans_path,
                    "analysis": analysis_path
                }

            # 1. Transcribe and structure audio if Tagalog transcription doesn't exist
            if not os.path.exists(tagalog_trans_path):
                print("Transcribing audio...")
                raw_transcription = self.transcribe_audio(audio_file_path)
                print("Structuring transcription with speaker labels...")
                tagalog_transcription = self.structure_transcription(raw_transcription)
                with open(tagalog_trans_path, 'w', encoding='utf-8') as f:
                    f.write(tagalog_transcription)
            else:
                print(f"Tagalog transcription exists, loading from {tagalog_trans_path}")
                with open(tagalog_trans_path, 'r', encoding='utf-8') as f:
                    tagalog_transcription = f.read()
            
            # 2. Translate to English if English transcription doesn't exist
            if not os.path.exists(english_trans_path):
                print("Translating to English...")
                english_transcription = self.translate_transcription(tagalog_transcription)
                with open(english_trans_path, 'w', encoding='utf-8') as f:
                    f.write(english_transcription)
            else:
                print(f"English transcription exists, loading from {english_trans_path}")
                with open(english_trans_path, 'r', encoding='utf-8') as f:
                    english_transcription = f.read()
            
            # 3. Analyze interaction if analysis doesn't exist
            if not os.path.exists(analysis_path):
                print("Analyzing interaction...")
                analysis = self.analyze_interaction(english_transcription)
                with open(analysis_path, 'w', encoding='utf-8') as f:
                    f.write(analysis)
            else:
                print(f"Analysis exists, loading from {analysis_path}")
            
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
        """Process all audio files in the Synthetic_Interactions directory."""
        audio_dir = "Synthetic_Interactions/audio"
        results = []
        
        # Process only .mp3 files that are not hidden files
        for filename in sorted(os.listdir(audio_dir)):
            if filename.endswith(".mp3") and not filename.startswith("."):
                audio_path = os.path.join(audio_dir, filename)
                
                # Check if analysis already exists
                base_name = self.get_simplified_name(audio_path)
                analysis_path = f"Interaction_Analysis/analysis/{base_name}_analysis.txt"
                
                if os.path.exists(analysis_path):
                    print(f"\nSkipping {filename} - analysis already exists")
                    results.append({
                        "audio_file": audio_path,
                        "tagalog_transcription": f"Interaction_Analysis/transcriptions/{base_name}_tagalog.txt",
                        "english_transcription": f"Interaction_Analysis/transcriptions/{base_name}_english.txt",
                        "analysis": analysis_path
                    })
                    continue
                
                print(f"\nProcessing audio file: {filename}")
                result = self.process_audio_file(audio_path)
                if result:
                    results.append(result)
        
        return results 