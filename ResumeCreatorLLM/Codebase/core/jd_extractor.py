"""
Job Description Extraction Module

Uses Llama3.2 via Ollama to parse job description text into structured JSON format.
Extracts: required skills, responsibilities, and important keywords.
"""

import json
from langchain_ollama import OllamaLLM


def extract_jd_with_ollama(jd_text,jd_model_name):
    """
    Extracts structured data from job description text using Ollama LLM.

    Args:
        jd_text (str): Raw job description text
        jd_model_name (str): Name of Ollama model to use (e.g., 'llama3.2')

    Returns:
        dict: Structured JD data with required_skills, responsibilities, keywords
    """
    # Build prompt with JD text
    prompt = build_prompt(jd_text)

    # Call Ollama LLM with JSON output format
    llm = OllamaLLM(model=jd_model_name,base_url="http://localhost:11434",format="json")
    llm_output=llm.invoke(prompt)
    
    # Parse LLM output as JSON
    try:
        structured_data = json.loads(llm_output)
    except json.JSONDecodeError:
        print("Invalid JSON from model. Raw output:\n", llm_output)
        return None
        
    return structured_data


def build_prompt(jd_text):
    """
    Constructs the prompt for LLM to extract job description data.

    Args:
        jd_text (str): Raw job description text

    Returns:
        str: Formatted prompt with extraction instructions
    """
    return f"""
You are an expert at analyzing job descriptions to extract key information.

Extract the following fields from the job description and return them as a single, valid JSON object ONLY:
- required_skills (list of technical and soft skills)
- responsibilities (list of key job duties)
- keywords (a list of 5-10 most important keywords from the text)

Job Description:
{jd_text}

Return ONLY the valid JSON object.
"""