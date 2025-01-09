import os
import re
from openai import OpenAI
from datetime import datetime
from pathlib import Path

class DialogueExpander:
    def __init__(self, api_key=None):
        """Initialize the DialogueExpander with OpenAI API key."""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.text_folder = "Synthetic_Interactions/text"
        
    def get_original_files(self):
        """Get a list of all dialogue files that haven't been expanded yet."""
        if not os.path.exists(self.text_folder):
            raise FileNotFoundError(f"Directory {self.text_folder} does not exist")
            
        all_files = [f for f in os.listdir(self.text_folder) if f.endswith('.txt')]
        original_files = []
        
        for file in all_files:
            if not file.endswith('_o1.txt'):
                filepath = os.path.join(self.text_folder, file)
                original_files.append(filepath)
                
        return original_files
        
    def read_script(self, filepath):
        """Read and return the contents of a script file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
            
    def build_expansion_prompt(self, original_script):
        """Create a prompt for expanding the dialogue."""
        # Extract metadata from header
        header_lines = original_script.split('\n\n')[0].split('\n')
        condition_type = header_lines[0].split(': ')[1] if len(header_lines) > 0 else "Unknown"
        
        # Remove timestamps using regex
        dialogue_text = re.sub(r'\[\d{2}:\d{2}\] ', '', original_script)
        
        # Remove header lines
        dialogue_text = '\n\n'.join(original_script.split('\n\n')[1:])
        
        prompt = f"""You are an official Barangay Health Worker (BHW) in Quezon Province. 
This is an existing healthcare dialogue for a {condition_type} condition.

Your task is to expand this dialogue while:
1. Making it 2-3 times longer
2. Keeping it natural and conversational
3. Incorporating appropriate small talk
4. Including occasional, subtle BHW mistakes if deemed realistic
5. Removing timestamps
6. Maintaining a cohesive conversation flow
7. Preserving the speaker labels (BHW/Patient/Pasiente)
8. Using natural Tagalog (Tayabas dialect) as spoken in Quezon Province

Original dialogue to expand:
{dialogue_text}"""

        return prompt
        
    def expand_with_o1(self, prompt_message):
        """Expand the dialogue using OpenAI's o1 model."""
        try:
            response = self.client.chat.completions.create(
                model="o1", #only works with an OpenAI Tier 5 account as of 01/09/2025. 
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in Philippine healthcare, particularly familiar with BHW protocols and healthcare in Quezon Province. You are fluent in Tagalog (Tayabas dialect)."
                    },
                    {
                        "role": "user",
                        "content": prompt_message
                    }
                ],
                temperature=0.7,
                max_tokens=20000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in API call: {str(e)}")
            return None
            
    def post_process_expanded(self, original_script, expanded_script):
        """Clean and validate the expanded dialogue."""
        # Get original header
        original_header = original_script.split('\n\n')[0]
        
        # Count original dialogue lines
        original_lines = len(re.findall(r'(?:BHW|Patient|Pasiente):', original_script))
        expanded_lines = len(re.findall(r'(?:BHW|Patient|Pasiente):', expanded_script))
        
        # Verify expansion ratio
        if expanded_lines < original_lines * 1.5:
            print("Warning: Expansion ratio is lower than expected")
            return None
            
        # Ensure proper speaker labels
        expanded_script = re.sub(r'(?:Doctor|Nurse|Health Worker):', 'BHW:', expanded_script)
        expanded_script = re.sub(r'(?:Client|Pasyente):', 'Patient:', expanded_script)
        
        # Combine header with expanded content
        final_script = f"{original_header}\n\n{expanded_script}"
        
        return final_script
        
    def save_expanded_script(self, original_filepath, expanded_script):
        """Save the expanded script with _o1.txt suffix."""
        original_path = Path(original_filepath)
        new_filename = original_path.stem + "_o1.txt"
        output_path = original_path.parent / new_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(expanded_script)
            
        return output_path
        
    def process_all_files(self):
        """Process all original dialogue files and expand them."""
        results = {
            'success': [],
            'failed': []
        }
        
        try:
            original_files = self.get_original_files()
            print(f"\nFound {len(original_files)} files to process")
            
            for filepath in original_files:
                try:
                    print(f"\nProcessing: {os.path.basename(filepath)}")
                    
                    # Read original script
                    original_script = self.read_script(filepath)
                    
                    # Build and execute expansion
                    prompt = self.build_expansion_prompt(original_script)
                    expanded_script = self.expand_with_o1(prompt)
                    
                    if expanded_script:
                        # Clean and validate
                        final_script = self.post_process_expanded(original_script, expanded_script)
                        
                        if final_script:
                            # Save expanded version
                            output_path = self.save_expanded_script(filepath, final_script)
                            results['success'].append(output_path)
                            print(f"Successfully expanded: {output_path}")
                        else:
                            results['failed'].append(filepath)
                            print(f"Failed to validate expansion for: {filepath}")
                    else:
                        results['failed'].append(filepath)
                        print(f"Failed to expand: {filepath}")
                        
                except Exception as e:
                    results['failed'].append(filepath)
                    print(f"Error processing {filepath}: {str(e)}")
                    
            # Print summary
            print("\nExpansion Summary:")
            print(f"Successfully processed: {len(results['success'])} files")
            print(f"Failed to process: {len(results['failed'])} files")
            
            if results['success']:
                print("\nExpanded files:")
                for path in results['success']:
                    print(f"- {path}")
                    
            if results['failed']:
                print("\nFailed files:")
                for path in results['failed']:
                    print(f"- {path}")
                    
        except Exception as e:
            print(f"Error in main process: {str(e)}")
            
        return results

def main():
    """Main entry point for dialogue expansion."""
    expander = DialogueExpander()
    results = expander.process_all_files()
    return results

if __name__ == "__main__":
    main() 