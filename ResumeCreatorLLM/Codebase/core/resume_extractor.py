"""
Resume Data Extraction Module

Uses Llama3.2 via Ollama to parse unstructured resume text into structured JSON format.
Extracts: name, contact, education, certifications, work experience, skills, projects.
"""

import json
from langchain_ollama import OllamaLLM

def extract_resume_data_with_ollama(resume_text,resume_model_name):
    """Extracts structured data from resume text using Ollama LLM.

    Args:
        resume_text (str): Raw text extracted from resume PDF
        resume_model_name (str): Name of Ollama model to use (e.g., 'llama3.2')

    Returns:
        dict: Structured resume data in JSON format, or None if extraction fails
    """
    # Build prompt with resume text and JSON schema
    prompt = build_prompt(resume_text)

    # Call Ollama LLM with JSON output format
    llm = OllamaLLM(model=resume_model_name,base_url="http://localhost:11434",format="json")
    llm_output=llm.invoke(prompt)
    
    # Parse LLM output as JSON
    try:
        structured_data = json.loads(llm_output)
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON from model. Raw output:\n", llm_output)
        return None
    
    # Validate required fields to prevent hallucination
    required_fields = ["name", "contact", "education", "work_experience", "skills", "projects", "certifications"]
    for field in required_fields:
        if field not in structured_data:
            print(f"[WARNING] Missing required field: {field}. Adding empty value.")
            if field in ["education", "work_experience", "skills", "projects", "certifications"]:
                structured_data[field] = []
            elif field == "contact":
                structured_data[field] = {"phone": "", "email": "", "location": ""}
            else:
                structured_data[field] = ""
    
    # Validate contact structure
    if isinstance(structured_data.get("contact"), dict):
        contact_fields = ["phone", "email", "location"]
        for cf in contact_fields:
            if cf not in structured_data["contact"]:
                structured_data["contact"][cf] = ""
        
    return structured_data


def build_prompt(resume_text):
    """Constructs the prompt for LLM to extract resume data.

    Args:
        resume_text (str): Raw resume text

    Returns:
        str: Formatted prompt with JSON schema and instructions
    """
    return f"""
    You are an intelligent assistant for resume data extraction.
    
    CRITICAL INSTRUCTIONS:
    1. Extract ONLY information that is explicitly present in the resume text below
    2. DO NOT make up, infer, or hallucinate any information
    3. If a field is not present in the resume, use empty string "" or empty array []
    4. Return a single, valid JSON object ONLY
    5. DO NOT include any text, explanations, or markdown fences (```json) around the JSON object
    6. DO NOT add placeholder text or example data

    The required JSON structure is:
    {{
      "name": "Full Name",
      "contact": {{
        "phone": "Phone number",
        "email": "Email address",
        "location": "City, State"
      }},
      "education": [
        {{
          "degree": "Degree and Major",
          "university": "University Name",
          "year": "Graduation Year"
        }}
      ],
      "certifications": [
        "Certification 1", "Certification 2", "Certification 3"
      ],
      "work_experience": [
        {{
          "company": "Company Name",
          "role": "Job Title",
          "start_date": "Start Date",
          "end_date": "End Date",
          "responsibilities": ["List of responsibilities as a bulleted list"],
          "tech_stack": ["List of technologies"]
        }}
      ],
      "skills": [
        "Skill 1", "Skill 2", "Skill 3"
      ],
      "projects": [
        {{
          "title": "Project Title",
          "description": "Project Description",
          "tech_stack": ["List of technologies"]
        }}
      ]
    }}

    ### RESUME TEXT START ###
    {resume_text}
    ### RESUME TEXT END ###

    Return ONLY the valid JSON object that strictly adheres to the structure above.
    """