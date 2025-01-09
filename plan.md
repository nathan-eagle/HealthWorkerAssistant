# Plan for Expanding Dialogues with o1

## Overview
We will read all original dialogue files from the "Synthetic_Interactions/text" directory, expand their content using OpenAI’s o1 model, replace timestamps with a cohesive conversation flow, and write the updated, realistic dialogues back to the same directory with the "_o1.txt" suffix.

Below is the high-level pseudocode to guide implementation.

---

## Steps & Pseudocode

1. SETUP & ENVIRONMENT  
   ```
   PSEUDOCODE:
     - confirm that "Synthetic_Interactions/text" directory exists and contains .txt files
   ```

2. GET A LIST OF **ALL** DIALOGUE FILES  
   ```
   PSEUDOCODE:
     text_folder = "Synthetic_Interactions/text"
     all_files = list all .txt files in text_folder
     for each file in all_files:
       if filename does not already have "_o1.txt":
         store it in a list original_files
   ```

3. DEFINE A FUNCTION TO READ AND PARSE THE ORIGINAL SCRIPT  
   ```
   PSEUDOCODE:
     function read_script(filepath):
       - Open the file in read mode
       - Read contents into a variable (script_content)
       - Return script_content
   ```

4. DEFINE A FUNCTION TO CREATE AN EXPANDED DIALOGUE PROMPT  
   ```
   PSEUDOCODE:
     function build_expansion_prompt(original_script):
       - We do not need to keep timestamps - remove them from text if present
         => use regex to remove patterns like [HH:MM or [MM:SS
       - Read the script line by line, ignoring lines with "Condition Type:" and such if not needed
       - Construct a message to pass to o1:
         => Instruct the model:
            "You are an official BHW in Quezon Province. This is an existing script. 
             Expand it to 2-3 times its length, 
             keep it natural, incorporate small talk, 
             avoid or subtly include BHW mistakes as appropriate,
             remove timestamps, 
             keep the conversation cohesive."
       - Return the final prompt_message
   ```

5. DEFINE A FUNCTION TO CALL OPENAI’s o1 MODEL  
   ```
   PSEUDOCODE:
     function expand_with_o1(prompt_message):
        - Make the API call to openai with the specified model=“o1”
        - Provide system/user instructions as needed
        - capture the response -> expanded_script
        - return expanded_script
   ```

6. CLEAN & VALIDATE THE RESULT  
   ```
   PSEUDOCODE:
     function post_process_expanded(expanded_script):
       - remove any leftover formatting that includes timestamps or extraneous text
       - ensure conversation is purely text with speaker labels (BHW or Patient)
       - verify length is roughly 2-3 times original
       - check for unnatural jargon or overly technical references
       - return cleaned_text
       - The key is to keep the conversation natural and cohesive, while adding more content. An actual BHW should not be able to tell the difference between the transcript of a real interaction and this new expanded one.
   ```

7. WRITE RESULTS TO A NEW FILE WITH “_o1.txt” SUFFIX  
   ```
   PSEUDOCODE:
     function save_expanded_script(original_filename, expanded_script):
       - new_filename = replace ".txt" with "_o1.txt"
       - file_path = text_folder + "/" + new_filename
       - open the file in write mode
       - write expanded_script to the file
       - close file
   ```

8. MAIN WORKFLOW  
   ```
   PSEUDOCODE:
     for each file in original_files:
       original_script = read_script(file)
       prompt_message = build_expansion_prompt(original_script)
       expanded_script = expand_with_o1(prompt_message)
       final_script = post_process_expanded(expanded_script)
       save_expanded_script(file, final_script)
   ```

9. OPTIONAL: LOGGING & ERROR HANDLING  
   ```
   PSEUDOCODE:
     - if any step fails, log the error and skip or retry
     - keep track of success/failure for each file
   ```

10. WRAP-UP  
   ```
   PSEUDOCODE:
     - print a summary of the files processed and their new output paths
     - End
   ```

---

## Implementation Notes
- Adjust the number of tokens or temperature in the OpenAI call to achieve a balance of creativity and realism.  
- If the expansions are too short or too long, prompt tuning in “build_expansion_prompt” might be needed.  
- For subtle mistakes, ensure the prompt conveys that they should be infrequent and easily self-corrected if it makes sense.  

--- 