import os
from generate_dialogue import DialogueGenerator
from translate_dialogue import DialogueTranslator
from generate_audio import AudioGenerator

def main():
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        return
    
    # Create necessary directories
    for lang in ['tagalog', 'english']:
        os.makedirs(f"transcripts/{lang}", exist_ok=True)
        os.makedirs(f"audio_output/{lang}", exist_ok=True)
    
    # Initialize components
    generator = DialogueGenerator()
    translator = DialogueTranslator()
    audio_gen = AudioGenerator()
    
    print("\n1. Generating Tagalog dialogues...")
    tagalog_files = generator.generate_all_dialogues()
    
    print("\n2. Translating to English...")
    english_files = translator.translate_all_files(source_lang="tagalog")
    
    print("\n3. Generating Tagalog audio files...")
    tagalog_audio = audio_gen.generate_all_audio(language="tagalog")
    
    print("\n4. Generating English audio files...")
    english_audio = audio_gen.generate_all_audio(language="english")
    
    print("\nProcess completed!")
    print("\nGenerated files:")
    print("\nTagalog Transcripts:")
    for f in tagalog_files:
        print(f"- {f}")
    
    print("\nEnglish Transcripts:")
    for f in english_files:
        print(f"- {f}")
    
    print("\nTagalog Audio Files:")
    for f in tagalog_audio:
        print(f"- {f}")
    
    print("\nEnglish Audio Files:")
    for f in english_audio:
        print(f"- {f}")

if __name__ == "__main__":
    main() 