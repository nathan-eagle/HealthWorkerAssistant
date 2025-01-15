import os
import argparse
from dotenv import load_dotenv
from synthetic.generate_dialogue import DialogueGenerator
from synthetic.generate_audio import AudioGenerator
from continuous_analysis.transcribe_analyze import AudioAnalyzer
from voice_processing.voice_input import VoiceInputProcessor
from data_management.storage import DataStorage
from real_time_guidance.guidance_engine import GuidanceEngine

class BHWCopilot:
    def __init__(self, mode='synthetic'):
        self.mode = mode
        self.data_storage = DataStorage()
        self.analyzer = AudioAnalyzer()
        self.guidance_engine = GuidanceEngine()
        
        if mode == 'production':
            self.voice_processor = VoiceInputProcessor()
        
    def setup_directories(self):
        """Create necessary data directories."""
        dirs = [
            "data/synthetic/text",
            "data/synthetic/audio",
            "data/raw/audio",
            "data/processed/transcriptions",
            "data/processed/analysis"
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
            output_dir="data/processed"
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

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='BHW Copilot')
    parser.add_argument('--mode', choices=['synthetic', 'testing', 'production'],
                       default='synthetic', help='Operation mode')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    
    # Verify API keys
    required_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        return

    # Initialize and run the copilot
    copilot = BHWCopilot(mode=args.mode)
    copilot.setup_directories()
    
    if args.mode == 'synthetic':
        copilot.synthetic_testing_mode()
    elif args.mode == 'testing':
        copilot.testing_mode()
    else:  # production mode
        copilot.production_mode()

if __name__ == "__main__":
    main() 