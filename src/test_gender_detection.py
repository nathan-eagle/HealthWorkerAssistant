from synthetic.generate_audio import AudioGenerator
from pathlib import Path

def test_gender_detection():
    # Initialize the audio generator
    generator = AudioGenerator()
    
    # Test file path
    transcript_path = Path('data/synthetic/text/prenatal_1_o1_sonnet.txt')
    
    print(f"\nTesting gender detection with: {transcript_path}")
    print("-" * 50)
    
    # Extract dialogues
    dialogues, _ = generator.extract_dialogues(transcript_path)
    
    # Test without condition type
    print("\nTesting without condition type:")
    gender = generator.determine_patient_gender(dialogues)
    print(f"Detected gender (no condition): {gender}")
    
    # Test with condition type
    print("\nTesting with condition type 'prenatal':")
    gender = generator.determine_patient_gender(dialogues, condition_type='prenatal')
    print(f"Detected gender (prenatal): {gender}")
    
    # Print some dialogue context
    print("\nDialogue context sample:")
    for i, d in enumerate(dialogues[:5]):  # First 5 exchanges
        print(f"{d['speaker']}: {d['text'][:100]}...")  # First 100 chars of each line

if __name__ == "__main__":
    test_gender_detection() 