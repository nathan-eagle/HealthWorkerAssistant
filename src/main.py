import os
import argparse
from dotenv import load_dotenv
from synthetic.generate_dialogue import DialogueGenerator
from synthetic.generate_audio import AudioGenerator
from continuous_analysis.transcribe_analyze import AudioAnalyzer
from voice_processing.voice_input import VoiceInputProcessor
from data_management.storage import DataStorage
from real_time_guidance.guidance_engine import GuidanceEngine
import json
from pathlib import Path
from anthropic import Anthropic
from openai import OpenAI

class BHWAssistant:
    def __init__(self, mode='synthetic'):
        self.mode = mode
        self.data_storage = DataStorage()
        self.analyzer = AudioAnalyzer()
        self.guidance_engine = GuidanceEngine()
        
        # Initialize OpenAI and Claude clients
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        if mode == 'production':
            self.voice_processor = VoiceInputProcessor()
        
    def setup_directories(self):
        """Create necessary data directories."""
        dirs = [
            "data/synthetic/text",
            "data/synthetic/audio",
            "data/raw/audio",
            "data/processed/synthetic/transcriptions",
            "data/processed/synthetic/analysis",
            "data/processed/raw/transcriptions",
            "data/processed/raw/analysis"
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)

    def synthetic_testing_mode(self):
        """Run the system using synthetic data for testing."""
        print("\n=== Running in Synthetic Testing Mode ===")
        
        # Check for existing synthetic dialogues
        text_files = [f for f in os.listdir("data/synthetic/text") if f.endswith('.txt')]
        print(f"\nFound {len(text_files)} synthetic dialogues")
        
        if len(text_files) < 3:  # Generate if we need more test data
            print("\n=== Generating Synthetic Dialogues ===")
            dialogue_generator = DialogueGenerator()
            dialogue_files = dialogue_generator.generate_all_dialogues()
            
            print("\n=== Generating Audio Files ===")
            audio_generator = AudioGenerator()
            audio_files = audio_generator.generate_all_audio()
        
        # Process all synthetic data
        print("\n=== Analyzing Synthetic Interactions ===")
        results = self.analyzer.process_all_recordings(
            audio_dir="data/synthetic/audio",
            output_dir="data/processed/synthetic"
        )
        self._print_results(results)

    def testing_mode(self):
        """Run the system using real but pre-recorded interactions."""
        print("\n=== Running in Testing Mode with Real Recordings ===")
        
        # Process all recordings in the raw audio directory
        results = self.analyzer.process_all_recordings(
            audio_dir="data/raw/audio",
            output_dir="data/processed"
        )
        self._print_results(results)
        
    def real_audio_mode(self, process_all=False):
        """Process real audio files with speaker segmentation."""
        print("\n=== Running in Real Audio Mode with Speaker Segmentation ===")
        
        # Ensure directories exist
        for directory in ["data/processed/raw/transcriptions", "data/processed/raw/analysis"]:
            os.makedirs(directory, exist_ok=True)
        
        # Get audio files
        audio_dir = Path("data/raw/audio")
        audio_files = sorted(list(audio_dir.glob("*.mp3")))
        
        if not audio_files:
            print("No audio files found in data/raw/audio/")
            return
            
        if process_all:
            # Process all audio files
            print(f"Processing all {len(audio_files)} audio files...")
            for audio_file in audio_files:
                self._process_real_audio_file(audio_file)
        else:
            # Process only the first audio file
            first_audio = audio_files[0]
            print(f"Processing file: {first_audio}")
            self._process_real_audio_file(first_audio)
            
        print("\nProcessing of real audio files complete!")
    
    def _extract_claude_content(self, response):
        """Extract clean text content from Claude's response."""
        content = response.content
        if isinstance(content, list):
            content = content[0].text
        return content.strip()
    
    def _process_real_audio_file(self, audio_file_path):
        """Process a single real audio file with speaker segmentation."""
        print(f"\nProcessing audio file: {audio_file_path}")
        
        # Create output paths
        base_name = audio_file_path.stem
        tagalog_path = Path(f"data/processed/raw/transcriptions/{base_name}_tagalog.txt")
        english_path = Path(f"data/processed/raw/transcriptions/{base_name}_english.txt")
        analysis_path = Path(f"data/processed/raw/analysis/{base_name}_analysis.txt")
        enhanced_analysis_path = Path(f"data/processed/raw/analysis/{base_name}_analysis2.txt")
        
        # Check if files already exist
        if tagalog_path.exists() and english_path.exists() and analysis_path.exists() and enhanced_analysis_path.exists():
            print(f"Files for {base_name} already exist, skipping...")
            return
        
        # 1. Transcribe using OpenAI's Whisper
        print("Transcribing audio...")
        with open(audio_file_path, 'rb') as audio:
            response = self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                language="tl",  # ISO code for Tagalog
                response_format="text",
                prompt="This is a conversation between a Barangay Health Worker and a patient in Tagalog (Tayabas dialect)."
            )
        
        raw_transcription = str(response)
        
        # 2. Use Claude to structure the transcription with speaker labels
        print("Adding speaker segmentation...")
        response = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",  # Updated to Claude 3.7 Sonnet
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Please analyze this medical conversation between a Barangay Health Worker (BHW) and a patient.
Structure it with speaker labels (BHW or Pasiente) based on the context of each statement.
If there are multiple participants, differentiate them by their roles.
Make sure to preserve ALL the original Tagalog text exactly as it appears.
Use this exact format for each line, with no introduction or other text:

BHW: [text spoken by health worker]
Pasiente: [text spoken by patient]

Here's the conversation:
{raw_transcription}"""
            }]
        )
        
        structured_transcription = self._extract_claude_content(response)
        
        # 3. Translate to English
        print("Translating to English...")
        response = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",  # Updated to Claude 3.7 Sonnet
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Translate this Tagalog medical conversation to English.
Maintain the exact same speaker labels format (BHW: and Pasiente:), with no introduction or other text.
Make sure to preserve ALL medical terminology accurately.

{structured_transcription}"""
            }]
        )
        
        english_translation = self._extract_claude_content(response)
        
        # 4. Analyze the interaction
        print("Analyzing interaction...")
        response = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",  # Updated to Claude 3.7 Sonnet
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
{english_translation}"""
            }]
        )
        
        analysis = self._extract_claude_content(response)
        
        # 5. Perform enhanced analysis with original Tagalog transcript
        print("Performing enhanced analysis with Claude 3.7 Sonnet...")
        response = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""I have a Tagalog medical conversation between a Barangay Health Worker (BHW) and a patient, and an initial analysis of this conversation. 

Please review both the original Tagalog transcript and the initial analysis, then enhance the analysis with any additional insights or issues that may have been missed or overlooked in the initial analysis.

Make sure to maintain exactly the same structure and section headings as the original analysis document:

1. Patient Diagnosis
2. Additional Questions
3. Recommendations
4. Red Flags and Concerns
5. Cultural Competency Observations

Original Tagalog conversation:
{structured_transcription}

Initial analysis:
{analysis}"""
            }]
        )
        
        enhanced_analysis = self._extract_claude_content(response)
        
        # 6. Save results
        with open(tagalog_path, "w", encoding="utf-8") as f:
            f.write(structured_transcription)
        
        with open(english_path, "w", encoding="utf-8") as f:
            f.write(english_translation)
        
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write(analysis)
        
        with open(enhanced_analysis_path, "w", encoding="utf-8") as f:
            f.write(enhanced_analysis)
        
        print(f"Processing complete for {base_name}!")
        print(f"Files saved to:")
        print(f"- {tagalog_path}")
        print(f"- {english_path}")
        print(f"- {analysis_path}")
        print(f"- {enhanced_analysis_path}")

    def production_mode(self):
        """Run the system in production mode with live audio input."""
        print("\n=== Running in Production Mode ===")
        print("Starting voice input processor...")
        
        try:
            while True:
                # Start listening for voice input
                audio_data = self.voice_processor.listen()
                
                if audio_data:
                    # Process the audio in real-time
                    transcript = self.analyzer.process_audio_stream(audio_data)
                    
                    # Generate real-time guidance
                    guidance = self.guidance_engine.generate_guidance(transcript)
                    
                    # Store the interaction
                    self.data_storage.store_interaction(audio_data, transcript, guidance)
                    
        except KeyboardInterrupt:
            print("\nStopping voice input processor...")
            self.voice_processor.stop()

    def _print_results(self, results):
        """Helper to print analysis results."""
        print("\n=== Processing Results ===")
        for result in results:
            if result:
                print(f"\nAudio: {result['audio_file']}")
                print(f"Tagalog Transcription: {result['tagalog_transcription']}")
                print(f"English Translation: {result['english_transcription']}")
                print(f"Analysis: {result['analysis']}")

    def test_transcript(self, transcript_path):
        """Test the guidance engine with a specific transcript."""
        print(f"\n=== Testing with transcript: {transcript_path} ===")
        
        # Read the transcript
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
        
        # Pass both transcript and filename to guidance engine
        guidance = self.guidance_engine.generate_guidance(
            transcript,
            transcript_filename=os.path.basename(transcript_path)
        )
        
        # Get translations using Claude
        response = self.guidance_engine.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": f"""Translate all sections of the medical guidance into both Tagalog and English.

Original guidance:
Symptom Guidance:
{json.dumps(guidance['symptom_guidance'], indent=2)}

Protocol Suggestions:
{json.dumps(guidance['protocol_suggestions'], indent=2)}

Respond with ONLY a JSON object in this exact format:
{{
    "tagalog": {{
        "symptoms": [
            "Symptom in Tagalog.",
            "Advice point 1 in Tagalog",
            "Advice point 2 in Tagalog"
        ],
        "protocols": [
            "Protocol suggestion 1 in Tagalog",
            "Protocol suggestion 2 in Tagalog"
        ]
    }},
    "english": {{
        "symptoms": [
            "Symptom in English.",
            "Advice point 1 in English",
            "Advice point 2 in English"
        ],
        "protocols": [
            "Protocol suggestion 1 in English",
            "Protocol suggestion 2 in English"
        ]
    }}
}}

Maintain the same grouping and ensure all medical information is accurately translated."""
            }]
        )
        
        try:
            translations = json.loads(response.content[0].text)
        except json.JSONDecodeError:
            print("Error: Could not parse translations")
            return

        # Create analysis directory if it doesn't exist
        analysis_dir = Path("data/processed/analysis")
        analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Get base filename from transcript path
        base_name = Path(transcript_path).stem
        if base_name.endswith('_tagalog'):
            base_name = base_name[:-8]  # Remove '_tagalog' suffix
            
        # Prepare English analysis content
        english_content = f"""Extracted Information:
{json.dumps(self.guidance_engine.current_context, indent=2)}

=== ANALYSIS ===
{'-' * 30}

Realtime Alerts:
"""
        if guidance.get('realtime_alerts'):
            english_content += "\n".join(guidance['realtime_alerts']) + "\n"
        
        english_content += "\nMissing Information:\n"
        if guidance['missing_information']:
            english_content += "\n".join(guidance['missing_information']) + "\n"
        
        english_content += "\nSymptom-specific Guidance:\n"
        if translations['english']['symptoms']:
            english_content += "\n".join(translations['english']['symptoms']) + "\n"
        
        english_content += "\nEducation Topics:\n"
        if guidance['education_topics']:
            english_content += "\n".join(guidance['education_topics']) + "\n"
        
        english_content += "\nProtocol Suggestions:\n"
        if translations['english']['protocols']:
            english_content += "\n".join(translations['english']['protocols']) + "\n"

        # Prepare Tagalog analysis content
        tagalog_content = f"""Nakalap na Impormasyon:
{json.dumps(self.guidance_engine.current_context, indent=2)}

=== PAGSUSURI ===
{'-' * 30}

Gabay para sa mga Sintomas:
"""
        if translations['tagalog']['symptoms']:
            tagalog_content += "\n".join(translations['tagalog']['symptoms']) + "\n"
        
        if guidance['missing_information']:
            tagalog_content += "\nKulang na Impormasyon:\n"
            tagalog_content += "\n".join(guidance['missing_information']) + "\n"
                
        if guidance['danger_signs']:
            tagalog_content += "\nMga Palatandaan ng Panganib:\n"
            tagalog_content += "\n".join(guidance['danger_signs']) + "\n"
                
        if guidance['education_topics']:
            tagalog_content += "\nMga Paksang Pang-edukasyon:\n"
            tagalog_content += "\n".join(guidance['education_topics']) + "\n"
                
        if translations['tagalog']['protocols']:
            tagalog_content += "\nMga Mungkahi ayon sa Protokol:\n"
            tagalog_content += "\n".join(translations['tagalog']['protocols']) + "\n"

        # Save to files
        english_file = analysis_dir / f"{base_name}_analysis_english.txt"
        tagalog_file = analysis_dir / f"{base_name}_analysis_tagalog.txt"
        
        with open(english_file, 'w', encoding='utf-8') as f:
            f.write(english_content)
            
        with open(tagalog_file, 'w', encoding='utf-8') as f:
            f.write(tagalog_content)
            
        print(f"\nAnalysis files generated:")
        print(f"English: {english_file}")
        print(f"Tagalog: {tagalog_file}")

    def generate_audio_only(self, transcript_path):
        """Generate audio from a specific transcript file."""
        print(f"\n=== Generating Audio for {transcript_path} ===")
        audio_generator = AudioGenerator()
        audio_file = audio_generator.create_conversation_audio(transcript_path)
        if audio_file:
            print(f"\nSuccessfully generated audio: {audio_file}")
        else:
            print("\nFailed to generate audio")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='BHW Decision Support System')
    parser.add_argument('--mode', choices=['synthetic', 'testing', 'production', 'generate-audio', 'real_audio'],
                       default='synthetic', help='Operation mode')
    parser.add_argument('--transcript', type=str,
                       help='Path to specific transcript file for testing or audio generation')
    parser.add_argument('--all', action='store_true',
                       help='Process all audio files when using real_audio mode')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    
    # Verify API keys
    required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        return

    # Initialize and run the system
    assistant = BHWAssistant(mode=args.mode)
    assistant.setup_directories()
    
    if args.mode == 'generate-audio':
        if not args.transcript:
            print("Error: --transcript argument is required for generate-audio mode")
            return
        assistant.generate_audio_only(args.transcript)
    elif args.transcript:
        assistant.test_transcript(args.transcript)
    elif args.mode == 'synthetic':
        assistant.synthetic_testing_mode()
    elif args.mode == 'testing':
        assistant.testing_mode()
    elif args.mode == 'real_audio':
        assistant.real_audio_mode(process_all=args.all)
    else:  # production mode
        assistant.production_mode()

if __name__ == "__main__":
    main() 