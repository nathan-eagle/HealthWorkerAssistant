import os
from dotenv import load_dotenv
from generate_dialogue import DialogueGenerator
from generate_audio import AudioGenerator
from transcribe_analyze import AudioAnalyzer

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: API keys not found. Please make sure OPENAI_API_KEY and ANTHROPIC_API_KEY are set in .env file")
        return

    # Create necessary directories
    os.makedirs("Synthetic_Interactions/text", exist_ok=True)
    os.makedirs("Synthetic_Interactions/audio", exist_ok=True)
    os.makedirs("Interaction_Analysis/transcriptions", exist_ok=True)
    os.makedirs("Interaction_Analysis/analysis", exist_ok=True)

    # Check for existing text files
    text_files = [f for f in os.listdir("Synthetic_Interactions/text") if f.endswith('.txt')]
    print(f"\nFound {len(text_files)} text files in Synthetic_Interactions/text/")
    
    if len(text_files) < 3:  # We need one for each condition type
        print("\n=== Generating Synthetic Dialogues ===")
        # Generate dialogues
        dialogue_generator = DialogueGenerator()
        dialogue_files = dialogue_generator.generate_all_dialogues()
    else:
        print("\n=== Found existing dialogue files, skipping generation ===")
        dialogue_files = [os.path.join("Synthetic_Interactions/text", f) for f in text_files]

    print("\n=== Generating Audio Files ===")
    # Generate audio files (will skip existing ones)
    audio_generator = AudioGenerator()
    audio_files = audio_generator.generate_all_audio()

    print("\n=== Analyzing Interactions ===")
    # Analyze the audio files
    analyzer = AudioAnalyzer()
    results = analyzer.process_all_recordings()
    
    print("\n=== Processing Complete ===")
    print("Generated files:")
    for result in results:
        if result:  # Only print if result is not None
            print(f"\nAudio: {result['audio_file']}")
            print(f"Tagalog Transcription: {result['tagalog_transcription']}")
            print(f"English Translation: {result['english_transcription']}")
            print(f"Analysis: {result['analysis']}")

if __name__ == "__main__":
    main() 