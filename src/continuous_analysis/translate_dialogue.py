import os
from openai import OpenAI
from datetime import datetime
import re

class DialogueTranslator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def extract_dialogue_content(self, filepath):
        """Extract the dialogue content and metadata from a file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split header and dialogue
        parts = content.split('\n\n', 1)
        header = parts[0]
        dialogue = parts[1] if len(parts) > 1 else ""
        
        return header, dialogue

    def translate_dialogue(self, dialogue_text, source_lang="tagalog", target_lang="english"):
        """Translate the dialogue while preserving timestamps and speaker labels."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert translator specializing in medical terminology and healthcare dialogues between {source_lang} and {target_lang}. Maintain the exact same format, including timestamps and speaker labels."
                },
                {
                    "role": "user",
                    "content": f"Translate this healthcare dialogue from {source_lang} to {target_lang}. Preserve all timestamps and speaker labels exactly as they appear:\n\n{dialogue_text}"
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent translations
            max_tokens=2000
        )
        return response.choices[0].message.content

    def translate_file(self, input_filepath):
        """Translate a dialogue file and save it."""
        # Extract content
        header, dialogue = self.extract_dialogue_content(input_filepath)
        
        # Determine source and target languages
        source_lang = "tagalog" if "tagalog" in input_filepath.lower() else "english"
        target_lang = "english" if source_lang == "tagalog" else "tagalog"
        
        # Translate the dialogue
        translated_dialogue = self.translate_dialogue(dialogue, source_lang, target_lang)
        
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(input_filepath)
        condition_type = re.search(r'dialogue_(.+?)_(?:tagalog|english)', base_name).group(1)
        
        output_filepath = f"transcripts/dialogue_{condition_type}_{target_lang}_{timestamp}.txt"
        
        # Save translated file
        with open(output_filepath, 'w', encoding='utf-8') as f:
            # Update language in header
            header = re.sub(r'Language: \w+', f'Language: {target_lang}', header)
            f.write(header + "\n\n" + translated_dialogue)
        
        return output_filepath

    def translate_all_files(self, source_lang="tagalog"):
        """Translate all dialogue files from source language to target language."""
        source_dir = f"transcripts/{source_lang.lower()}"
        translated_files = []
        
        for filename in os.listdir(source_dir):
            if filename.startswith('dialogue_') and filename.endswith('.txt'):
                input_filepath = os.path.join(source_dir, filename)
                print(f"Translating {filename}...")
                translated_file = self.translate_file(input_filepath)
                translated_files.append(translated_file)
        
        return translated_files 