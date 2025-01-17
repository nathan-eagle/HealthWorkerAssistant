from real_time_guidance.guidance_engine import GuidanceEngine
from pathlib import Path
import json
import re

def extract_json_from_text(text: str) -> dict:
    """Extract JSON object from text that might contain other content."""
    # Find anything that looks like a JSON object
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    return {}

def test_maternal_analysis():
    # Initialize the guidance engine in testing mode
    engine = GuidanceEngine(mode='testing')
    
    # Read the test transcript
    transcript_path = Path('data/synthetic/text/prenatal_exam.txt')
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    print("Running end-to-end maternal health analysis...")
    print("-" * 50)
    
    # Extract clinical information using Claude
    print("\nExtracting clinical information...")
    try:
        response = engine.claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"""Analyze this prenatal care conversation and extract:
1. Measurements taken or mentioned
2. Symptoms reported
3. Risk factors identified
4. Health education topics covered
5. Trimester of pregnancy
6. Any danger signs

Format the response as JSON with these keys:
measurements, symptoms, risk_factors, covered_topics, trimester, danger_signs

Conversation:
{transcript}"""
            }]
        )
        
        # Extract content from Claude's response
        extracted_info = extract_json_from_text(response.content[0].text)
        if not extracted_info:
            print("\nFailed to parse JSON from response:")
            print(response.content[0].text)
            return
            
        print("\nExtracted Information:")
        print(json.dumps(extracted_info, indent=2))
        
        # Update engine context with extracted information
        engine.current_context.update(extracted_info)
        
        # Generate guidance based on maternal protocol
        guidance = engine.generate_guidance(transcript)
        
        print("\nProtocol-based Guidance:")
        print("-" * 30)
        
        print("\nSymptom-specific Guidance:")
        if guidance.get('symptom_guidance'):
            for recommendation in guidance['symptom_guidance']:
                print(f"- {recommendation}")
        else:
            print("No symptom-specific guidance generated")
        
        print("\nMissing Information:")
        for item in guidance['missing_information']:
            print(f"- {item}")
            
        print("\nDanger Signs:")
        for sign in guidance['danger_signs']:
            print(f"- {sign}")
            
        print("\nEducation Topics:")
        for topic in guidance['education_topics']:
            print(f"- {topic}")
            
        print("\nProtocol Suggestions:")
        for suggestion in guidance['protocol_suggestions']:
            print(f"- {suggestion}")
            
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        if hasattr(response, 'content'):
            print("\nRaw response content:")
            print(response.content)

if __name__ == "__main__":
    test_maternal_analysis() 