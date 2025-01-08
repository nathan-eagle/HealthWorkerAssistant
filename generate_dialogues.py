import os
from openai import OpenAI
from datetime import datetime
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define condition types
CONDITION_TYPES = [
    "prenatal",
    "communicable_disease",
    "non_communicable_disease"
]

def create_conversation_prompt(condition_type):
    return f"""Generate a realistic 15-minute dialogue between a Barangay Health Worker (BHW) and a patient in Quezon Province, Philippines. The dialogue is conducted in Tayabas dialect of Tagalog. It MUST be a FULL 15-minute conversation with continuous dialogue and proper time progression throughout.

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

Additional requirements:
- EVERY minute must have at least one exchange
- Include natural pauses and detailed responses
- Show timestamps progressing naturally (e.g., [01:23], [01:45], [02:10], etc.)
- The final exchange MUST occur between [14:45] and [15:00]
- NO sudden time jumps (maximum 30-second gaps between exchanges)
- Include detailed explanations and follow-ups
- Cover multiple aspects of the patient's condition and concerns
- Include cultural elements specific to Quezon Province

Format each line as:
[MM:SS] Speaker: Dialogue text

The conversation MUST maintain a natural flow with consistent time progression until the 15-minute mark."""

def generate_dialogue(condition_type):
    response = client.chat.completions.create(
        model="gpt-4",  # Fixed model name
        messages=[
            {
                "role": "system", 
                "content": """You are an expert in Philippine healthcare, particularly familiar with Barangay Health Worker protocols and the healthcare landscape in Quezon Province. 
Your task is to generate COMPLETE 15-minute dialogues that demonstrate comprehensive healthcare interactions.
You MUST maintain proper time progression throughout the entire 15 minutes, with no sudden jumps or gaps.
Every minute must contain at least one exchange, and the conversation must continue meaningfully until the end."""
            },
            {"role": "user", "content": create_conversation_prompt(condition_type)}
        ],
        temperature=0.7,
        max_tokens=15000
    )
    return response.choices[0].message.content

def save_dialogue(dialogue, condition_type, index):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transcripts/dialogue_{condition_type}_{index+1}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Condition Type: {condition_type.replace('_', ' ')}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n" + dialogue)

def main():
    # Create transcripts directory if it doesn't exist
    os.makedirs("transcripts", exist_ok=True)
    
    # Generate dialogues for each condition type
    for condition_type in CONDITION_TYPES:
        for i in range(3):  # Generate 3-4 dialogues per condition type
            print(f"Generating dialogue {i+1} for {condition_type}...")
            dialogue = generate_dialogue(condition_type)
            save_dialogue(dialogue, condition_type, i)
            print(f"Saved dialogue {i+1} for {condition_type}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        exit(1)
    main() 