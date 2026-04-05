"""
Optional CV Review and Refinement Module
Allows interactive review and ATS optimization of generated CVs
"""

import json
from langchain_ollama import OllamaLLM


def check_ats_compatibility(cv_text, jd_json):
    """
    Calculate ATS compatibility score based on keyword matching.
    
    Args:
        cv_text (str): Generated CV text
        jd_json (dict): Job description JSON with keywords and skills
    
    Returns:
        dict: Score and missing keywords
    """
    # Extract keywords from JD
    jd_keywords = []
    if 'keywords' in jd_json:
        jd_keywords.extend(jd_json['keywords'])
    if 'required_skills' in jd_json:
        jd_keywords.extend(jd_json['required_skills'])
    
    # Flatten and clean keywords (handle both strings and nested structures)
    cleaned_keywords = []
    for k in jd_keywords:
        if isinstance(k, str):
            cleaned_keywords.append(k.lower().strip())
        elif isinstance(k, dict):
            # If it's a dict, extract string values
            for v in k.values():
                if isinstance(v, str):
                    cleaned_keywords.append(v.lower().strip())
        elif isinstance(k, list):
            # If it's a list, flatten it
            for item in k:
                if isinstance(item, str):
                    cleaned_keywords.append(item.lower().strip())
    
    # Remove duplicates
    jd_keywords = list(set(cleaned_keywords))
    
    # Check which keywords are present in CV
    matched_keywords = []
    missing_keywords = []
    
    cv_lower = cv_text.lower()
    for keyword in jd_keywords:
        if keyword in cv_lower:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    
    # Calculate score
    total_keywords = len(jd_keywords)
    score = int((len(matched_keywords) / total_keywords) * 100) if total_keywords > 0 else 100
    
    return {
        'score': score,
        'matched': matched_keywords,
        'missing': missing_keywords,
        'total': total_keywords
    }


def add_keywords_to_cv(cv_text, keywords, jd_json, model_name):
    """
    Use LLM to naturally integrate missing keywords into CV.
    
    Args:
        cv_text (str): Current CV text
        keywords (str or list): Keywords to add
        jd_json (dict): Job description JSON
        model_name (str): LLM model name
    
    Returns:
        str: Updated CV with keywords integrated
    """
    if isinstance(keywords, list):
        keywords = ", ".join(keywords)
    
    prompt = f"""You are an expert ATS resume optimizer. Your task is to naturally integrate these missing keywords into the existing CV: {keywords}

CRITICAL RULES:
1. DO NOT create a separate "Keywords" section at the end
2. DO NOT list keywords as a comma-separated list anywhere
3. INTEGRATE keywords naturally into existing sections:
   - Add technical keywords to the SKILLS section (merge with existing skills)
   - Add tool/technology names to WORK EXPERIENCE bullet points where relevant
   - Add methodology keywords to PROJECT descriptions where they fit
4. ONLY add keywords where they make logical sense based on the candidate's background
5. Keep the EXACT same format and structure as the input CV
6. Return the COMPLETE CV with keywords woven into appropriate sections

Example of GOOD integration:
- If keyword is "Docker": Add to Skills section like "Docker, Kubernetes, CI/CD"
- If keyword is "Agile": Add to experience like "Collaborated in Agile/Scrum environment"
- If keyword is "TensorFlow": Add to project like "Built ML models using TensorFlow and PyTorch"

Example of BAD integration (DO NOT DO THIS):
- Creating a section: "Keywords: Docker, Agile, TensorFlow, ..."

Current CV:
{cv_text}

Return ONLY the updated CV text .
"""
    
    llm = OllamaLLM(model=model_name, base_url="http://localhost:11434")
    return llm.invoke(prompt)


def enhance_section(cv_text, section, jd_json, model_name):
    """
    Enhance a specific section of the CV using LLM.
    
    Args:
        cv_text (str): Current CV text
        section (str): Section to enhance (summary, skills, experience, projects)
        jd_json (dict): Job description JSON
        model_name (str): LLM model name
    
    Returns:
        str: Updated CV with enhanced section
    """
    prompt = f"""
    You are an expert resume writer. Enhance the {section.upper()} section of this CV to better match the job requirements.
    
    Job Requirements:
    {json.dumps(jd_json, indent=2)}
    
    Rules:
    - Keep the existing format and structure
    - Make the {section} section more impactful and relevant
    - Use keywords from job requirements naturally
    - Maintain professional tone
    - Return the complete updated CV
    
    Current CV:
    {cv_text}
    
    Return ONLY the updated CV text.
    """
    
    llm = OllamaLLM(model=model_name, base_url="http://localhost:11434")
    return llm.invoke(prompt)


def review_and_refine_cv(cv_text, jd_json, model_name):
    """
    Interactive CV review and refinement interface.
    
    Args:
        cv_text (str): Generated CV text
        jd_json (dict): Job description JSON
        model_name (str): LLM model name
    
    Returns:
        str: Refined CV text
    """
    print("\n" + "="*70)
    print("CV REVIEW & REFINEMENT MODE")
    print("="*70)
    
    # Initial ATS check
    ats_result = check_ats_compatibility(cv_text, jd_json)
    print(f"\n Initial ATS Compatibility Score: {ats_result['score']}/100")
    print(f"   Matched Keywords: {len(ats_result['matched'])}/{ats_result['total']}")
    
    if ats_result['missing']:
        print(f"\n Missing Keywords: {', '.join(ats_result['missing'][:10])}")
        if len(ats_result['missing']) > 10:
            print(f"   ... and {len(ats_result['missing']) - 10} more")
    
    while True:
        print("\n" + "-"*70)
        print("Options:")
        print("  1. View current CV preview")
        print("  2. Add missing keywords automatically")
        print("  3. Add custom keywords")
        print("  4. Enhance specific section (summary/skills/experience/projects)")
        print("  5. Re-check ATS compatibility")
        print("  6. Finalize and save")
        print("  0. Exit without saving changes")
        print("-"*70)
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "1":
            print("\n" + "="*70)
            print("CV PREVIEW (First 800 characters)")
            print("="*70)
            print(cv_text[:800])
            if len(cv_text) > 800:
                print(f"\n... ({len(cv_text) - 800} more characters)")
            
        elif choice == "2":
            if ats_result['missing']:
                print(f"\n Adding {len(ats_result['missing'])} missing keywords...")
                cv_text = add_keywords_to_cv(cv_text, ats_result['missing'], jd_json, model_name)
                ats_result = check_ats_compatibility(cv_text, jd_json)
                print(f" Keywords added! New ATS Score: {ats_result['score']}/100")
            else:
                print(" No missing keywords to add!")
            
        elif choice == "3":
            keywords = input("Enter keywords to add (comma-separated): ").strip()
            if keywords:
                print(f"\n Adding custom keywords...")
                cv_text = add_keywords_to_cv(cv_text, keywords, jd_json, model_name)
                print(" Custom keywords added!")
            
        elif choice == "4":
            section = input("Which section to enhance? (summary/skills/experience/projects): ").strip().lower()
            if section in ['summary', 'skills', 'experience', 'projects']:
                print(f"\n Enhancing {section} section...")
                cv_text = enhance_section(cv_text, section, jd_json, model_name)
                print(f" {section.title()} section enhanced!")
            else:
                print(" Invalid section. Choose: summary, skills, experience, or projects")
            
        elif choice == "5":
            ats_result = check_ats_compatibility(cv_text, jd_json)
            print(f"\n ATS Compatibility Score: {ats_result['score']}/100")
            print(f"   Matched Keywords: {len(ats_result['matched'])}/{ats_result['total']}")
            if ats_result['missing']:
                print(f"   Missing Keywords: {', '.join(ats_result['missing'][:10])}")
                if len(ats_result['missing']) > 10:
                    print(f"   ... and {len(ats_result['missing']) - 10} more")
            else:
                print("  All keywords matched!")
            
        elif choice == "6":
            print("\n CV finalized!")
            return cv_text
            
        elif choice == "0":
            print("\n  Exiting without saving changes...")
            return None
            
        else:
            print(" Invalid choice. Please enter 0-6.")


def auto_optimize_cv(cv_text, jd_json, model_name, target_score=80, max_iterations=3):
    """
    Automatically optimize CV to reach target ATS score.
    Non-interactive mode for batch processing.
    
    Args:
        cv_text (str): Generated CV text
        jd_json (dict): Job description JSON
        model_name (str): LLM model name
        target_score (int): Target ATS score (default: 80)
        max_iterations (int): Maximum optimization attempts (default: 3)
    
    Returns:
        str: Optimized CV text
    """
    print(f"\n Auto-optimizing CV (Target ATS Score: {target_score}%)...")
    
    ats_result = check_ats_compatibility(cv_text, jd_json)
    initial_score = ats_result['score']
    print(f"   Initial Score: {initial_score}/100")
    print(f"   Missing Keywords: {len(ats_result['missing'])} out of {ats_result['total']}")
    
    if ats_result['score'] >= target_score:
        print(f"  Already meets target score!")
        return cv_text
    
    # Iteratively add keywords until target is reached or max iterations
    iteration = 0
    while ats_result['score'] < target_score and iteration < max_iterations and ats_result['missing']:
        iteration += 1
        print(f"\n   Iteration {iteration}: Adding top priority keywords...")
        
        # Prioritize most important missing keywords (limit to avoid overwhelming LLM)
        keywords_to_add = ats_result['missing'][:15]  # Add 15 keywords at a time
        print(f"   Keywords to integrate: {', '.join(keywords_to_add[:5])}{'...' if len(keywords_to_add) > 5 else ''}")
        
        # Add keywords with improved prompt
        updated_cv = add_keywords_to_cv(cv_text, keywords_to_add, jd_json, model_name)
        
        # Verify changes were made
        if updated_cv.strip() == cv_text.strip():
            print(f"  Warning: LLM returned unchanged CV. Trying with more explicit instructions...")
            # Try again with a simpler, more direct approach
            updated_cv = add_keywords_directly(cv_text, keywords_to_add)
        
        cv_text = updated_cv
        
        # Re-check score
        ats_result = check_ats_compatibility(cv_text, jd_json)
        improvement = ats_result['score'] - initial_score
        print(f"   Score after iteration {iteration}: {ats_result['score']}/100 (+{improvement} points)")
        
        # Break if no improvement
        if improvement == 0 and iteration > 1:
            print(f"   No improvement detected. Stopping optimization.")
            break
    
    final_score = ats_result['score']
    total_improvement = final_score - initial_score
    
    print(f"\n  Optimization complete!")
    print(f"   Final Score: {final_score}/100 (improved by {total_improvement} points)")
    print(f"   Remaining missing keywords: {len(ats_result['missing'])}")
    
    return cv_text


def add_keywords_directly(cv_text, keywords):
    """
    Fallback method: Directly add keywords to Skills section if LLM fails.
    
    Args:
        cv_text (str): Current CV text
        keywords (list): Keywords to add
    
    Returns:
        str: Updated CV with keywords added to Skills section
    """
    # Find the SKILLS section
    lines = cv_text.split('\n')
    skills_index = -1
    
    for i, line in enumerate(lines):
        if 'SKILLS' in line.upper() or 'TECHNICAL SKILLS' in line.upper():
            skills_index = i
            break
    
    if skills_index == -1:
        # No skills section found, add one before the end
        lines.insert(-5, "\n## SKILLS\n")
        lines.insert(-4, ", ".join(keywords))
    else:
        # Add keywords to existing skills section
        # Find the content lines (bullet points or comma-separated)
        next_section = len(lines)
        for i in range(skills_index + 1, len(lines)):
            if lines[i].strip().startswith('##'):
                next_section = i
                break
        
        # Get existing skills content
        skills_content = []
        for i in range(skills_index + 1, next_section):
            line = lines[i].strip()
            if line and not line.startswith('#'):
                skills_content.append(line)
        
        # Check if skills are in bullet format or comma-separated
        if any(line.startswith('•') or line.startswith('-') or line.startswith('*') for line in skills_content):
            # Bullet format - find the last bullet and append keywords there
            last_bullet_idx = -1
            for i in range(len(skills_content) - 1, -1, -1):
                if skills_content[i].startswith(('•', '-', '*')):
                    last_bullet_idx = i
                    break
            
            if last_bullet_idx >= 0:
                # Extract the text after the bullet
                bullet_text = skills_content[last_bullet_idx].lstrip('•-* ')
                # Add new keywords to this bullet
                updated_bullet = f"• {bullet_text}, {', '.join(keywords)}"
                skills_content[last_bullet_idx] = updated_bullet
        else:
            # Comma-separated format - just append keywords
            if skills_content:
                # Add to the last line
                skills_content[-1] = skills_content[-1].rstrip(', ') + ', ' + ', '.join(keywords)
            else:
                skills_content = [', '.join(keywords)]
        
        # Replace the skills section
        new_lines = lines[:skills_index + 1]
        for content in skills_content:
            new_lines.append(content)
        new_lines.append('')  # Empty line after skills
        new_lines.extend(lines[next_section:])
        
        return '\n'.join(new_lines)
    
    return '\n'.join(lines)
