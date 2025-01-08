import os
from generate_dialogue import DialogueGenerator
from translate_dialogue import DialogueTranslator
from generate_audio import AudioGenerator
from transcribe_analyze import AudioAnalyzer
import traceback

def main():
    try:
        # Create necessary directories
        os.makedirs("Synthetic_Interactions/audio", exist_ok=True)
        os.makedirs("Synthetic_Interactions/text/tagalog", exist_ok=True)
        os.makedirs("Synthetic_Interactions/text/english", exist_ok=True)
        os.makedirs("Interaction_Analysis/transcriptions", exist_ok=True)
        os.makedirs("Interaction_Analysis/analysis", exist_ok=True)

        # Check if we already have audio files
        audio_files = []
        for filename in os.listdir("Synthetic_Interactions/audio"):
            if filename.endswith(".mp3") and not filename.startswith(".") and "tagalog" in filename.lower():
                audio_files.append(filename)

        if not audio_files:
            print("No existing audio files found. Generating new dialogues...")
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
        else:
            print(f"\nFound {len(audio_files)} Tagalog audio files. Proceeding with analysis...")
            # Initialize audio analyzer
            analyzer = AudioAnalyzer()
            
            # Process existing audio files
            print("\nAnalyzing audio recordings...")
            analysis_results = analyzer.process_all_recordings()
            
            print("\nAnalysis complete! Results have been saved to:")
            print("- Transcriptions (Tagalog & English): Interaction_Analysis/transcriptions/")
            print("- Analysis: Interaction_Analysis/analysis/")

    except Exception as e:
        print(f"\nError in main process: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 