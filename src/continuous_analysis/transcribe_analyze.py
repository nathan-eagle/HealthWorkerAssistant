import os
from anthropic import Anthropic
from openai import OpenAI
from pathlib import Path

class AudioAnalyzer:
    def __init__(self, anthropic_api_key=None, openai_api_key=None):
        self.claude = Anthropic(api_key=anthropic_api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.openai = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))
        
        # Set up paths
        self.data_dir = Path("data")
        self.synthetic_dir = self.data_dir / "synthetic"
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"

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

    def process_audio_stream(self, audio_data):
        """Process a stream of audio data in real-time."""
        # TODO: Implement real-time audio processing
        # This will be used in production mode
        pass

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

    def process_audio_file(self, audio_file_path, output_dir=None):
        """Process a single audio file through the entire pipeline."""
        print(f"\nProcessing: {audio_file_path}")
        
        # Create simplified base name
        audio_filename = Path(audio_file_path).stem
        
        # Use provided output directory or default to processed
        output_dir = Path(output_dir) if output_dir else self.processed_dir
        
        # Create output paths
        transcriptions_dir = output_dir / "transcriptions"
        analysis_dir = output_dir / "analysis"
        
        tagalog_trans_path = transcriptions_dir / f"{audio_filename}_tagalog.txt"
        english_trans_path = transcriptions_dir / f"{audio_filename}_english.txt"
        analysis_path = analysis_dir / f"{audio_filename}_analysis.txt"
        
        # Ensure directories exist
        transcriptions_dir.mkdir(parents=True, exist_ok=True)
        analysis_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Check if all files exist
            if (tagalog_trans_path.exists() and 
                english_trans_path.exists() and 
                analysis_path.exists()):
                print(f"All files already exist for {audio_filename}, skipping processing")
                return {
                    "audio_file": str(audio_file_path),
                    "tagalog_transcription": str(tagalog_trans_path),
                    "english_transcription": str(english_trans_path),
                    "analysis": str(analysis_path)
                }

            # 1. Transcribe and structure audio if Tagalog transcription doesn't exist
            if not tagalog_trans_path.exists():
                print("Transcribing audio...")
                raw_transcription = self.transcribe_audio(audio_file_path)
                print("Structuring transcription with speaker labels...")
                tagalog_transcription = self.structure_transcription(raw_transcription)
                tagalog_trans_path.write_text(tagalog_transcription, encoding='utf-8')
            else:
                print(f"Tagalog transcription exists, loading from {tagalog_trans_path}")
                tagalog_transcription = tagalog_trans_path.read_text(encoding='utf-8')
            
            # 2. Translate to English if English transcription doesn't exist
            if not english_trans_path.exists():
                print("Translating to English...")
                english_transcription = self.translate_transcription(tagalog_transcription)
                english_trans_path.write_text(english_transcription, encoding='utf-8')
            else:
                print(f"English transcription exists, loading from {english_trans_path}")
                english_transcription = english_trans_path.read_text(encoding='utf-8')
            
            # 3. Analyze interaction if analysis doesn't exist
            if not analysis_path.exists():
                print("Analyzing interaction...")
                analysis = self.analyze_interaction(english_transcription)
                analysis_path.write_text(analysis, encoding='utf-8')
            else:
                print(f"Analysis exists, loading from {analysis_path}")
            
            return {
                "audio_file": str(audio_file_path),
                "tagalog_transcription": str(tagalog_trans_path),
                "english_transcription": str(english_trans_path),
                "analysis": str(analysis_path)
            }
            
        except Exception as e:
            print(f"Error processing {audio_file_path}: {str(e)}")
            return None

    def process_all_recordings(self, audio_dir=None, output_dir=None):
        """Process all audio files in the specified directory."""
        # Use provided paths or defaults
        audio_dir = Path(audio_dir) if audio_dir else self.synthetic_dir / "audio"
        output_dir = Path(output_dir) if output_dir else self.processed_dir
        
        results = []
        
        # Process only .mp3 files that are not hidden files
        for audio_path in sorted(audio_dir.glob("*.mp3")):
            if audio_path.name.startswith('.'):
                continue
                
            # Check if analysis already exists
            base_name = self.get_simplified_name(audio_path)
            analysis_path = output_dir / "analysis" / f"{base_name}_analysis.txt"
            
            if analysis_path.exists():
                print(f"\nSkipping {audio_path.name} - analysis already exists")
                results.append({
                    "audio_file": str(audio_path),
                    "tagalog_transcription": str(output_dir / "transcriptions" / f"{base_name}_tagalog.txt"),
                    "english_transcription": str(output_dir / "transcriptions" / f"{base_name}_english.txt"),
                    "analysis": str(analysis_path)
                })
                continue
            
            print(f"\nProcessing audio file: {audio_path.name}")
            result = self.process_audio_file(audio_path, output_dir)
            if result:
                results.append(result)
        
        return results 