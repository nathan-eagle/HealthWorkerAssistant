import os
from generate_dialogue import DialogueGenerator
from translate_dialogue import DialogueTranslator
from generate_audio import AudioGenerator
from transcribe_analyze import AudioAnalyzer
import traceback

def main():
    try:
        # Create necessary directories
        os.makedirs("input_transcripts/tagalog", exist_ok=True)
        os.makedirs("input_transcripts/english", exist_ok=True)
        os.makedirs("interview_recordings/tagalog", exist_ok=True)
        os.makedirs("interview_recordings/english", exist_ok=True)
        os.makedirs("audio_transcription", exist_ok=True)
        os.makedirs("copilot_output", exist_ok=True)

        # Check if we already have audio files
        audio_files = [f for f in os.listdir("interview_recordings/tagalog") 
                      if f.endswith('.mp3') and not f.startswith('.')]

        if not audio_files:
            # Initialize generators
            dialogue_gen = DialogueGenerator()
            translator = DialogueTranslator()
            audio_gen = AudioGenerator()

            # Configuration
            num_condition_examples = 1
            condition_types = [
                "prenatal",
                "communicable_disease",
                "non_communicable_disease"
            ]

            for condition_type in condition_types:
                try:
                    for example_num in range(num_condition_examples):
                        print(f"\n1. Generating Tagalog dialogue for {condition_type} condition (Example {example_num + 1}/{num_condition_examples})...")
                        tagalog_file = dialogue_gen.generate_dialogue(condition_type, "tagalog")
                        
                        print("\n2. Translating to English...")
                        english_file = translator.translate_file(tagalog_file)
                        
                        print("\n3. Generating Tagalog audio file...")
                        tagalog_audio = audio_gen.create_conversation_audio(tagalog_file)

                        print("\n4. Generating English audio file...")
                        english_audio = audio_gen.create_conversation_audio(english_file)

                        print("\nProcess completed!")
                        print(f"\nGenerated files:")
                        print(f"Tagalog Transcript: {tagalog_file}")
                        print(f"Tagalog Audio: {tagalog_audio}")
                        print(f"English Transcript: {english_file}")
                        print(f"English Audio: {english_audio}")

                except Exception as e:
                    print(f"\nError processing {condition_type}: {str(e)}")
                    print(traceback.format_exc())
                    continue

        # Initialize audio analyzer
        analyzer = AudioAnalyzer()
        
        # Process existing audio files
        print("\nAnalyzing audio recordings...")
        analysis_results = analyzer.process_all_recordings()
        
        print("\nAnalysis complete! Results have been saved to:")
        print("- Transcriptions: audio_transcription/")
        print("- Analysis: copilot_output/")

    except Exception as e:
        print(f"\nError in main process: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 