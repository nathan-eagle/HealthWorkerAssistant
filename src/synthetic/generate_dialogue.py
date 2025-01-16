import os
from openai import OpenAI
from datetime import datetime
from pathlib import Path

class DialogueGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.condition_types = [
            "prenatal",
            "communicable_disease",
            "non_communicable_disease"
        ]
        self.output_dir = Path("data/synthetic/text")

    def create_dialogue_prompt(self, condition_type):
        """Create a prompt for generating a Tagalog dialogue."""
        
        # Define condition-specific exam components
        exam_components = {
            "prenatal": """
- Blood pressure measurement
- Weight and height
- Fundal height measurement
- Fetal heart rate check
- Checking for edema
- Abdominal examination
- Basic urinalysis results discussion""",
            
            "communicable_disease": """
- Temperature reading
- Heart rate and respiratory rate
- Lung sounds assessment
- Lymph node examination
- Throat examination (if relevant)
- Skin examination (if relevant)
- Basic neurological check""",
            
            "non_communicable_disease": """
- Blood pressure measurement
- Heart rate and rhythm check
- Lung sounds assessment
- Basic cardiovascular exam
- Weight and BMI calculation
- Blood sugar reading (if diabetic)
- Peripheral pulse check"""
        }
        
        exam_section = exam_components.get(condition_type.replace('_disease', ''), "")
        
        return f"""Generate a realistic 15-minute dialogue between a Barangay Health Worker (BHW) and a patient in Quezon Province, Philippines. The dialogue should be in Tagalog (Tayabas dialect).

Context:
- The patient has a {condition_type.replace('_', ' ')} condition
- The conversation takes place during a home visit
- Include typical symptoms, concerns, and cultural context relevant to Quezon Province
- Each timestamp MUST show natural time progression (no sudden jumps)
- The conversation MUST continue with substance until [14:55] or later
- Use natural Tagalog (Tayabas dialect) as spoken in Quezon Province, including common local expressions and medical terms as understood by locals

Physical Examination Components to Include:
{exam_components.get(condition_type.replace('_disease', ''), '')}

Required conversation structure (MUST follow these time allocations):
1. [00:00-02:00] Initial greetings and rapport building
2. [02:00-05:00] Comprehensive symptom assessment and detailed medical history
3. [05:00-08:00] Physical examination with clear verbal confirmation of measurements and findings
4. [08:00-11:00] Thorough discussion of lifestyle factors and family background
5. [11:00-13:00] Detailed health education and advice specific to the condition
6. [13:00-15:00] Clear follow-up plans, recommendations, and proper closing

Format each line as:
[MM:SS] Speaker: Dialogue text

Important Physical Exam Guidelines:
- BHW must verbally confirm all measurements and findings with the patient
- Include realistic values appropriate for the condition
- Explain each examination step to the patient
- Document patient's responses and any discomfort
- Use proper medical terminology while explaining in simple terms
- Include any relevant patient education during the examination"""

    def get_next_sequence_number(self, condition_type):
        """Get the next sequence number for a given condition type."""
        if not self.output_dir.exists():
            return 1
            
        existing_files = [f for f in self.output_dir.iterdir() 
                         if f.name.startswith(condition_type) and f.name.endswith('.txt')]
        if not existing_files:
            return 1
            
        import re
        numbers = [int(re.search(r'_(\d+)\.txt$', f.name).group(1)) 
                  for f in existing_files if re.search(r'_(\d+)\.txt$', f.name)]
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
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Simplify condition type for filename
        simple_condition = condition_type.replace("_disease", "")
        filename = self.output_dir / f"{simple_condition}_{seq_num}.txt"
        
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