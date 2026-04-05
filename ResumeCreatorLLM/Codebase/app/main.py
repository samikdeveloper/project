"""
Main Pipeline for ATS-Friendly CV Generation

This file orchestrates the entire CV generation process:
1. Extracts text from input resume PDF
2. Parses resume and job description using LLMs
3. Generates tailored CV matching job requirements
4. Optionally optimizes CV for ATS compatibility
5. Creates final PDF output
"""

from pdf_utilities import extract_text_from_pdf
from pdf_utilities import create_pdf_from_text
from resume_extractor import extract_resume_data_with_ollama
from jd_extractor import extract_jd_with_ollama
from cv_creator import generate_ats_cv
from cv_reviewer import review_and_refine_cv, auto_optimize_cv, check_ats_compatibility
import json
import time
import sys

def main(interactive_review=False, auto_optimize=False):
    """Main pipeline function that processes resume and generates tailored CV.

    Args:
        interactive_review (bool): Enable interactive CV review mode
        auto_optimize (bool): Enable automatic ATS optimization
    """
    
    # Configuration: Set input/output file names and LLM models
    candidate_name="BenCarter"
    resume_file = f"{candidate_name}_InputResume.pdf"
    jd="JD-03 Full-Stack Developer"
    jd_file=f"{jd}.txt"
    cv_output_file= f"{candidate_name}_{jd}_OutputCV.pdf"
    
    # LLM models: llama3.2 for extraction, gemma3 for generation
    resume_model_name="llama3.2:3b"
    jd_model_name="llama3.2:3b"
    cv_model_name="gemma3:1b"
    
    # Step 1: Extract text from PDF resume
    resume_text = extract_text_from_pdf(resume_file)
    print("[INFO] Extracted resume text successfully.")
    
    # Step 2: Parse resume into structured JSON using LLM
    print("[INFO] Extracting structured data from resume using Llama...")
    resume_json_data = extract_resume_data_with_ollama(resume_text,resume_model_name)
    
    if resume_json_data:
        print("[INFO] Structured Resume Data:")
        print(json.dumps(resume_json_data, indent=2))
        
    else:
        print("[ERROR] Could not extract structured data.")


    # Step 3: Read job description from text file
    with open(jd_file, "r", encoding="utf-8") as f:
     jd_text = f.read()

    # Step 4: Parse job description into structured JSON using LLM
    print("[INFO] Extracting structured data from job description using Llama...")
    jd_json_data = extract_jd_with_ollama(jd_text,jd_model_name)


    print("INFO Structured JD Data:")
    print(json.dumps(jd_json_data, indent=2))


    # Step 5: Generate ATS-optimized CV by combining resume and JD data
    print("[INFO] Generating ATS-compliant CV using Gemma...")
    cv_data=generate_ats_cv(resume_json_data,jd_json_data,cv_model_name)   
    print("INFO Structured CV Data:")
    print(cv_data)
    
    # Step 6 (Optional): Interactive Review Mode - allows manual refinement
    if interactive_review:
        print("\n[INFO] Entering interactive review mode...")
        refined_cv = review_and_refine_cv(cv_data, jd_json_data, cv_model_name)
        if refined_cv:  # User finalized the CV
            cv_data = refined_cv
        else:  # User exited without saving
            print("[INFO] Using original CV without refinements.")
    
    # Step 6 (Optional): Auto-optimization Mode - automatically adds missing keywords
    elif auto_optimize:
        cv_data = auto_optimize_cv(cv_data, jd_json_data, cv_model_name, target_score=80)
    
    # Step 7: Calculate and display final ATS compatibility score
    ats_result = check_ats_compatibility(cv_data, jd_json_data)
    print(f"\n[INFO] Final ATS Compatibility Score: {ats_result['score']}/100")

    # Step 8: Convert markdown CV to professionally formatted PDF
    create_pdf_from_text(cv_data,cv_output_file)
    

if __name__ == "__main__":
    # Parse command-line arguments for optional features
    interactive = "--interactive" in sys.argv or "-i" in sys.argv
    auto_opt = "--auto-optimize" in sys.argv or "-a" in sys.argv
    
    # Show help if requested
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Usage: python main.py [OPTIONS]

Options:
  --interactive, -i     Enable interactive CV review and refinement
  --auto-optimize, -a   Automatically optimize CV for ATS compatibility
  --help, -h           Show this help message

Examples:
  python main.py                    # Standard pipeline (no review)
  python main.py --interactive      # With interactive review
  python main.py --auto-optimize    # With automatic optimization
        """)
        sys.exit(0)
    
    main(interactive_review=interactive, auto_optimize=auto_opt)