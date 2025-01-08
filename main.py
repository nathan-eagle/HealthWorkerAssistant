import os
from generate_dialogue import DialogueGenerator
from translate_dialogue import DialogueTranslator
from generate_audio import AudioGenerator
import traceback

def main():
    try:
        # Create necessary directories
        os.makedirs("transcripts", exist_ok=True)
        os.makedirs("audio_output", exist_ok=True)

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
                    
                    # Rename the Tagalog file to include language suffix
                    new_tagalog_file = tagalog_file.replace(".txt", "_tagalog.txt")
                    os.rename(tagalog_file, new_tagalog_file)

                    print("\n2. Translating to English...")
                    english_file = translator.translate_file(new_tagalog_file)
                    
                    # Rename the English file to include language suffix
                    new_english_file = english_file.replace(".txt", "_english.txt")
                    os.rename(english_file, new_english_file)

                    print("\n3. Generating Tagalog audio file...")
                    tagalog_audio = audio_gen.create_conversation_audio(new_tagalog_file)

                    print("\n4. Generating English audio file...")
                    english_audio = audio_gen.create_conversation_audio(new_english_file)

                    print("\nProcess completed!")
                    print(f"\nGenerated files:")
                    print(f"Tagalog Transcript: {new_tagalog_file}")
                    print(f"Tagalog Audio: {tagalog_audio}")
                    print(f"English Transcript: {new_english_file}")
                    print(f"English Audio: {english_audio}")

            except Exception as e:
                print(f"\nError processing {condition_type}: {str(e)}")
                print(traceback.format_exc())
                continue

    except Exception as e:
        print(f"\nError in main process: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 