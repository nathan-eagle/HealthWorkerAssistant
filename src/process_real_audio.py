import os
from pathlib import Path
from anthropic import Anthropic
from openai import OpenAI
import json

def extract_claude_content(response):
    """Extract clean text content from Claude's response."""
    content = response.content
    if isinstance(content, list):
        content = content[0].text
    return content.strip()

def transcribe_audio_with_speaker_segmentation(audio_file_path):
    """Transcribe audio file with speaker segmentation using Whisper and Claude."""
    print(f"\nProcessing audio file: {audio_file_path}")
    
    # Initialize clients
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # 1. Transcribe using OpenAI's Whisper
    print("Transcribing audio...")
    with open(audio_file_path, 'rb') as audio:
        response = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            language="tl",  # ISO code for Tagalog
            response_format="text",
            prompt="This is a conversation between a Barangay Health Worker and a patient in Tagalog (Tayabas dialect)."
        )
    
    raw_transcription = str(response)
    
    # 2. Use Claude to structure the transcription with speaker labels
    print("Adding speaker segmentation...")
    response = claude_client.messages.create(
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
    
    structured_transcription = extract_claude_content(response)
    print("Structuring complete.")
    
    # 3. Translate to English
    print("Translating to English...")
    response = claude_client.messages.create(
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
    
    english_translation = extract_claude_content(response)
    print("Translation complete.")
    
    # 4. Analyze the interaction
    print("Analyzing interaction...")
    response = claude_client.messages.create(
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
    
    analysis = extract_claude_content(response)
    print("Analysis complete.")
    
    # 5. Perform enhanced analysis with original Tagalog transcript
    print("Performing enhanced analysis with Claude 3.7 Sonnet...")
    response = claude_client.messages.create(
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
    
    enhanced_analysis = extract_claude_content(response)
    print("Enhanced analysis complete.")
    
    return {
        "tagalog_structured": structured_transcription,
        "english_translation": english_translation,
        "analysis": analysis,
        "enhanced_analysis": enhanced_analysis
    }

def main():
    # Setup directories
    for directory in ["data/processed/raw/transcriptions", "data/processed/raw/analysis"]:
        os.makedirs(directory, exist_ok=True)
    
    # Process the first audio file
    audio_dir = Path("data/raw/audio")
    audio_files = sorted(list(audio_dir.glob("*.mp3")))
    
    if not audio_files:
        print("No audio files found in data/raw/audio/")
        return
    
    first_audio = audio_files[0]
    print(f"Processing file: {first_audio}")
    
    # Process the audio
    result = transcribe_audio_with_speaker_segmentation(first_audio)
    
    # Save results
    base_name = first_audio.stem
    
    # Save Tagalog transcription
    with open(f"data/processed/raw/transcriptions/{base_name}_tagalog.txt", "w", encoding="utf-8") as f:
        f.write(result["tagalog_structured"])
    
    # Save English translation
    with open(f"data/processed/raw/transcriptions/{base_name}_english.txt", "w", encoding="utf-8") as f:
        f.write(result["english_translation"])
    
    # Save analysis
    with open(f"data/processed/raw/analysis/{base_name}_analysis.txt", "w", encoding="utf-8") as f:
        f.write(result["analysis"])
    
    # Save enhanced analysis
    with open(f"data/processed/raw/analysis/{base_name}_analysis2.txt", "w", encoding="utf-8") as f:
        f.write(result["enhanced_analysis"])
    
    print(f"\nProcessing complete!")
    print(f"Tagalog transcription saved to: data/processed/raw/transcriptions/{base_name}_tagalog.txt")
    print(f"English translation saved to: data/processed/raw/transcriptions/{base_name}_english.txt")
    print(f"Analysis saved to: data/processed/raw/analysis/{base_name}_analysis.txt")
    print(f"Enhanced analysis saved to: data/processed/raw/analysis/{base_name}_analysis2.txt")

if __name__ == "__main__":
    main() 