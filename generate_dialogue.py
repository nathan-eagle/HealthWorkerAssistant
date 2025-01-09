import os
from openai import OpenAI
from datetime import datetime

class DialogueGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.condition_types = [
            "prenatal",
            "communicable_disease",
            "non_communicable_disease"
        ]

    def create_dialogue_prompt(self, condition_type):
        """Create a prompt for generating a Tagalog dialogue."""
        return f"""Generate a realistic 15-minute dialogue between a Barangay Health Worker (BHW) and a patient in Quezon Province, Philippines. The dialogue should be in Tagalog (Tayabas dialect).

Context:
- The patient has a {condition_type.replace('_', ' ')} condition
- The conversation takes place during a home visit
- Include typical symptoms, concerns, and cultural context relevant to Quezon Province
- Each timestamp MUST show natural time progression (no sudden jumps)
- The conversation MUST continue with substance until [14:55] or later
- Use natural Tagalog (Tayabas dialect) as spoken in Quezon Province, including common local expressions and medical terms as understood by locals

Required conversation structure (MUST follow these time allocations):
1. [00:00-02:00] Initial greetings and rapport building
2. [02:00-06:00] Comprehensive symptom assessment and detailed medical history
3. [06:00-09:00] Thorough discussion of lifestyle factors and family background
4. [09:00-12:00] Detailed health education and advice specific to the condition
5. [12:00-15:00] Clear follow-up plans, recommendations, and proper closing

Format each line as:
[MM:SS] Speaker: Dialogue text"""

    def get_next_sequence_number(self, condition_type):
        """Get the next sequence number for a given condition type."""
        output_dir = "Synthetic_Interactions/text"
        if not os.path.exists(output_dir):
            return 1
            
        existing_files = [f for f in os.listdir(output_dir) 
                         if f.startswith(condition_type) and f.endswith('.txt')]
        if not existing_files:
            return 1
            
        import re
        numbers = [int(re.search(r'_(\d+)\.txt$', f).group(1)) 
                  for f in existing_files if re.search(r'_(\d+)\.txt$', f)]
        return max(numbers) + 1 if numbers else 1

    def generate_dialogue(self, condition_type):
        """Generate a single Tagalog dialogue for the given condition type."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in Philippine healthcare, particularly familiar with BHW protocols and healthcare in Quezon Province. You are fluent in Tagalog (Tayabas dialect)."
                },
                {
                    "role": "user",
                    "content": self.create_dialogue_prompt(condition_type)
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        dialogue_content = response.choices[0].message.content
        
        # Get next sequence number
        seq_num = self.get_next_sequence_number(condition_type)
        
        # Save the dialogue to a file and return the filename
        output_dir = "Synthetic_Interactions/text"
        os.makedirs(output_dir, exist_ok=True)
        
        # Simplify condition type for filename
        simple_condition = condition_type.replace("_disease", "")
        filename = os.path.join(output_dir, f"{simple_condition}_{seq_num}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Condition Type: {condition_type.replace('_', ' ')}\n")
            f.write(f"Language: Tagalog\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + dialogue_content)
        
        return filename

    def generate_all_dialogues(self):
        """Generate one dialogue for each condition type."""
        generated_files = []
        for condition_type in self.condition_types:
            print(f"\nGenerating dialogue for {condition_type}...")
            filename = self.generate_dialogue(condition_type)
            generated_files.append(filename)
            print(f"Generated: {filename}")
        return generated_files 