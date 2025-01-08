import os
from openai import OpenAI
from datetime import datetime
import json

class DialogueGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.condition_types = [
            "prenatal",
            "communicable_disease",
            "non_communicable_disease"
        ]

    def create_dialogue_prompt(self, condition_type, language="tagalog"):
        base_prompt = f"""Generate a realistic 15-minute dialogue between a Barangay Health Worker (BHW) and a patient in Quezon Province, Philippines. The dialogue should be in {language}.

Context:
- The patient has a {condition_type.replace('_', ' ')} condition
- The conversation takes place during a home visit
- Include typical symptoms, concerns, and cultural context relevant to Quezon Province
- Each timestamp MUST show natural time progression (no sudden jumps)
- The conversation MUST continue with substance until [14:55] or later

Required conversation structure (MUST follow these time allocations):
1. [00:00-02:00] Initial greetings and rapport building
2. [02:00-06:00] Comprehensive symptom assessment and detailed medical history
3. [06:00-09:00] Thorough discussion of lifestyle factors and family background
4. [09:00-12:00] Detailed health education and advice specific to the condition
5. [12:00-15:00] Clear follow-up plans, recommendations, and proper closing

Format each line as:
[MM:SS] Speaker: Dialogue text"""

        if language.lower() == "tagalog":
            base_prompt += "\n\nNote: Use natural Tagalog (Tayabas dialect) as spoken in Quezon Province, including common local expressions and medical terms as understood by locals."
        
        return base_prompt

    def generate_dialogue(self, condition_type, language="tagalog"):
        """Generate a single dialogue for the given condition type."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert in Philippine healthcare, particularly familiar with BHW protocols and healthcare in Quezon Province. You are fluent in both English and Tagalog (Tayabas dialect)."
                },
                {
                    "role": "user",
                    "content": self.create_dialogue_prompt(condition_type, language)
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        dialogue_content = response.choices[0].message.content
        
        # Save the dialogue to a file and return the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"Synthetic_Interactions/text/{language.lower()}"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"dialogue_{condition_type}_{language}_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Condition Type: {condition_type.replace('_', ' ')}\n")
            f.write(f"Language: {language}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + dialogue_content)
        
        return filename

    def generate_all_dialogues(self):
        """Generate dialogues for all condition types in Tagalog."""
        generated_files = []
        for condition_type in self.condition_types:
            print(f"Generating {condition_type} dialogue in Tagalog...")
            dialogue = self.generate_dialogue(condition_type, "tagalog")
            generated_files.append(dialogue)
        return generated_files 