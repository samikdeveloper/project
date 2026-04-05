import json
from langchain_ollama import OllamaLLM

def generate_ats_cv(resume_json, jd_json, model_name):
  """
    Generates a polished, ATS-friendly CV text using Gemma3 via Ollama.

    Args:
        resume_json (dict): JSON output from resume extraction.
        jd_json (dict): JSON output from job description extraction.
        model_name (str): Gemma model name.

    Returns:
        str: Polished CV text.
    """
  prompt = f"""
    You are an expert resume writer.

    Create an ATS-friendly, polished CV text based on the following JSON inputs.
    Incorporate relevant skills and experiences from the resume and match them with
    requirements and responsibilities from the job description.

    Rules:
    - **Format the entire CV using GitHub Flavored Markdown (GFM) syntax.**
    - **Start with the name of candidate as a large heading using '# Name'** (single # for the name only).
    - Follow the name with contact information on the next line (email | phone | location).
    - Use '##' for all section titles (e.g., '## SUMMARY', '## WORK EXPERIENCE', '## SKILLS', '## EDUCATION', '## PROJECTS','## CERTIFICATIONS').
    - Use bullet points ('* ') for all lists (skills, responsibilities, projects).
    - **Ensure the output starts immediately with the formatted content.**
    - Include the following sections, and *only* these sections: Name (as # heading), Contact Info, Summary, Skills, Education, Work Experience, Projects,Certifications.
    - **DO NOT include a separate "Keywords" section.** Instead, naturally integrate relevant keywords from the job description into the Skills, Summary, and Work Experience sections. Check the start date and end date of a job carefully. Mention the quantifiable achievements if any.
    - **ONLY include actual work experience, education, projects, and skills from the Resume JSON.** DO NOT add placeholder text, template instructions, or example entries like "[Previous Company - If Applicable]" or "[Briefly describe...]".
    - **DO NOT add any content that is not explicitly present in the Resume JSON.**
    - If a section has no data in the Resume JSON, either omit that section or leave it minimal.
    - Make the content concise, professional, and optimized for ATS scanning by prioritizing keywords.
    - Do not include any introductory or concluding remarks, explanations, or notes; only return the formatted CV text.

    Resume JSON:
    {json.dumps(resume_json, indent=2)}

    Job Description JSON:
    {json.dumps(jd_json, indent=2)}
    """
  llm = OllamaLLM(model=model_name,base_url="http://localhost:11434")
  llm_output=llm.invoke(prompt)
 
 # Post-processing: Remove Keywords section and ensure proper formatting
  llm_output = remove_keywords_section(llm_output)
  llm_output = fix_name_header(llm_output, resume_json)
  llm_output = ensure_education_header(llm_output)
 
  return llm_output


def remove_keywords_section(cv_text):
    """
    Removes the Keywords section from the CV text if present.
    
    Args:
        cv_text (str): The CV text in Markdown format.
    
    Returns:
        str: CV text with Keywords section removed.
    """
    import re
    
    # Pattern to match ## Keywords section and its content until the next ## section or end
    # This handles both "## Keywords" and "##Keywords" variations
    pattern = r'##\s*Keywords\s*\n.*?(?=\n##|\Z)'
    
    # Remove the Keywords section
    cleaned_text = re.sub(pattern, '', cv_text, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up any excessive blank lines (more than 2 consecutive newlines)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text.strip()


def fix_name_header(cv_text, resume_json):
    """
    Ensures the candidate's actual name appears in the H1 header.
    Replaces generic "# Name" with actual name from resume JSON.
    
    Args:
        cv_text (str): The CV text in Markdown format.
        resume_json (dict): Resume JSON containing the candidate name.
    
    Returns:
        str: CV text with proper name header.
    """
    import re
    
    # Extract candidate name from JSON
    candidate_name = resume_json.get('name', 'Candidate Name')
    
    # Check if the first line is "# Name" (case-insensitive)
    lines = cv_text.split('\n')
    if len(lines) > 0:
        first_line = lines[0].strip()
        # If first line is exactly "# Name" or "# name", replace it
        if re.match(r'^#\s*Name\s*$', first_line, re.IGNORECASE):
            lines[0] = f'# {candidate_name}'
            cv_text = '\n'.join(lines)
    
    return cv_text


def ensure_education_header(cv_text):
    """
    Ensures the EDUCATION section has a proper ## EDUCATION header.
    Detects education content and adds header if missing.
    
    Args:
        cv_text (str): The CV text in Markdown format.
    
    Returns:
        str: CV text with proper education header.
    """
    import re
    
    lines = cv_text.split('\n')
    result_lines = []
    i = 0
    
    # Check if ## EDUCATION header already exists
    if any('## EDUCATION' in line.upper() for line in lines):
        return cv_text  # Already has proper header
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect education content patterns (typically after work experience)
        # Look for university names or degree titles that appear without a ## header
        is_university_line = any(keyword in line.lower() for keyword in [
            'university', 'college', 'institute', 'school of'
        ])
        
        is_degree_line = any(keyword in line for keyword in [
            'Bachelor', 'Master', 'PhD', 'Ph.D', 'Doctorate', 'B.S.', 'M.S.', 'B.A.', 'M.A.'
        ])
        
        # Check if we're past WORK EXPERIENCE section
        recent_text = '\n'.join(result_lines[-10:]).upper()
        past_work_experience = '## WORK EXPERIENCE' in recent_text
        
        # If we find education content without a header, add the header
        if past_work_experience and (is_university_line or is_degree_line):
            # Check if previous few lines don't have an ## header
            prev_lines = result_lines[-3:] if len(result_lines) >= 3 else result_lines
            has_recent_header = any(l.strip().startswith('##') for l in prev_lines)
            
            if not has_recent_header:
                # Add education header before this content
                result_lines.append('')
                result_lines.append('## EDUCATION')
                result_lines.append('')
        
        result_lines.append(lines[i])
        i += 1
    
    # Clean up excessive blank lines
    final_text = '\n'.join(result_lines)
    final_text = re.sub(r'\n{3,}', '\n\n', final_text)
    
    return final_text.strip()

