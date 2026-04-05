================================================================================
                    CV CREATION USING LLMs PIPELINE
================================================================================

OVERVIEW
--------
This project automatically generates ATS-optimized CVs by analyzing input 
resumes and job descriptions using LLMs. It extracts structured data, tailors 
content to match job requirements, and produces professionally formatted PDFs.


PREREQUISITES
-------------
1. Python 3.8 or higher
2. Ollama installed and running locally (http://localhost:11434)
3. Required LLM models downloaded:
   - llama3.2:3b (for resume and JD extraction)
   - gemma3:1b (for CV generation)

To download respective models:
   ollama pull llama3.2:3b
   ollama pull gemma3:1b


INSTALLATION
------------
1. Navigate to the project directory:
   cd Capstone_Project-HPPCS[01]/Codebase

2. Install required Python packages:
   pip install -r requirements.txt


PROJECT STRUCTURE
-----------------
Codebase/
├── main.py                    # Main pipeline script
├── pdf_utilities.py           # PDF extraction and creation utilities
├── resume_extractor.py        # Resume data extraction using LLM
├── jd_extractor.py           # Job description extraction using LLM
├── cv_creator.py             # CV generation and optimization using LLM
├── cv_reviewer.py            # Optional CV review and refinement
├── requirements.txt          # Python dependencies
├── README.txt               # This file
│
├── Input Files:
│   ├── 10 Resume PDFs:
│   │   ├── SarahChen_InputResume.pdf
│   │   ├── PriyaSharma_InputResume.pdf
│   │   ├── OmarHassan_InputResume.pdf
│   │   ├── AlexRodriguez_InputResume.pdf
│   │   ├── EmilyWong_InputResume.pdf
│   │   ├── LisaGrant_InputResume.pdf
│   │   ├── JessicaKim_InputResume.pdf
│   │   ├── MikeJohnson_InputResume.pdf
│   │   ├── DavidLee_InputResume.pdf
│   │   └── BenCarter_InputResume.pdf
│   │
│   └── 3 Job Descriptions:
│       ├── JD-01 Senior Data Scientist.txt
│       ├── JD-02 Senior Data Engineer.txt
│       └── JD-03 Full-Stack Developer.txt
│
└── Output Files:
    └── [CandidateName]_[JD-Title]_OutputCV.pdf


HOW TO RUN
----------

BASIC USAGE :
------------------------------------------
Run the pipeline with default settings (no user interaction required):

   python main.py

This will:
- Extract text from the specified input resume PDF
- Parse resume data using LLM
- Extract job requirements from the specified job description using LLM
- Generate ATS-optimized CV tailored to the job using LLM
- Create professionally formatted output CV PDF
- Display ATS compatibility score


ADVANCED USAGE:
---------------

1. AUTO-OPTIMIZE MODE (Automatic keyword optimization):
   
   python main.py --auto-optimize
   
   OR
   
   python main.py -a
   
   This automatically adds missing keywords to reach 80% ATS score.


2. INTERACTIVE REVIEW MODE (Manual refinement):
   
   python main.py --interactive
   
   OR
   
   python main.py -i
   
   This enables an interactive menu where user can:
   - View CV preview
   - Add missing keywords automatically
   - Add custom keywords
   - Enhance specific sections (summary, skills, experience, projects)
   - Re-check ATS compatibility
   - Finalize and save


3. SHOW HELP:
   
   python main.py --help
   
   OR
   
   python main.py -h


CUSTOMIZATION
-------------
To process different resumes or job descriptions, edit main.py:

Line 31:  candidate_name = "[CandidateName]"       # Change candidate name
Line 33:  jd_file = "JD-0X [Job Title].txt"       # Change job description

Example configurations:
- For Sarah Chen applying to ML role:
  candidate_name = "SarahChen"
  resume_file = "SarahChen_InputResume.pdf"
  jd_file = "JD-01 Senior Data Scientist.txt"
  cv_output_file = "SarahChen_JD-01 Senior Data Scientist_OutputCV.pdf"

To modify LLM models:
Line 38:  resume_model_name = "llama3.2:3b"   # Resume extraction model
Line 39:  jd_model_name = "llama3.2:3b"       # JD extraction model
Line 40:  cv_model_name = "gemma3:1b"         # CV content generation model


INPUT FILE FORMATS
------------------

RESUME (PDF):
- Standard resume format with sections like:
  - Contact Information
  - Professional Summary
  - Education
  - Certifications
  - Work Experience
  - Technical Skills
  - Projects

JOB DESCRIPTION (TXT):
- Plain text file containing:
  - Position title and location
  - About the role
  - Key responsibilities
  - Required skills & qualifications
  - Nice to have skills
  - Example tech stack


OUTPUT
------
The pipeline generates:

1. Console Output:
   - Extracted resume data (JSON format)
   - Extracted JD data (JSON format)
   - Generated CV text (Markdown format)
   - ATS compatibility score

2. PDF File:
   - Professionally formatted CV (SarahChen_JD-01 Senior Data Scientist_OutputCV.pdf)
   - ATS-friendly layout with:
     * Centered name and contact info
     * Blue section headers with underlines
     * Proper bullet points
     * Optimized for keyword matching


ATS COMPATIBILITY SCORE
------------------------
The pipeline calculates an ATS score based on keyword matching:
- 80-100%: Excellent match
- 60-79%:  Good match
- 40-59%:  Fair match
- Below 40%: Needs improvement

TROUBLESHOOTING
---------------

1. "ModuleNotFoundError":
   Solution: Install missing packages using pip install -r requirements.txt

2. "Connection refused" or Ollama errors:
   Solution: Ensure Ollama is running (ollama serve)
   
3. "Model not found":
   Solution: Download required models using ollama pull <model-name>

4. PDF extraction issues:
   Solution: Ensure input PDF is text-based (not scanned image)

5. Low ATS score:
   Solution: Use --auto-optimize or --interactive mode to improve


AVAILABLE CANDIDATES AND JOB DESCRIPTIONS
------------------------------------------
The project includes 10 candidate resumes and 3 job descriptions.

RECOMMENDED CANDIDATE-JOB MAPPINGS:

1. JD-01: Senior Data Scientist (Machine Learning & AI)
   Recommended Candidates:
   - Sarah Chen (SarahChen_InputResume.pdf)
   - Priya Sharma (PriyaSharma_InputResume.pdf)
   - Omar Hassan (OmarHassan_InputResume.pdf)
   
   Skills Match: Python, TensorFlow, PyTorch, ML, Statistical Analysis,
                 Recommendation Systems, A/B Testing, MLOps

2. JD-02: Senior Data Engineer
   Recommended Candidates:
   - Alex Rodriguez (AlexRodriguez_InputResume.pdf)
   - Emily Wong (EmilyWong_InputResume.pdf)
   - Lisa Grant (LisaGrant_InputResume.pdf)
   - Jessica Kim (JessicaKim_InputResume.pdf)
   
   Skills Match: SQL, Spark, Airflow, ETL, Data Pipelines, Cloud Platforms,
                 Big Data Technologies, Data Warehousing

3. JD-03: Full-Stack Developer
   Recommended Candidates:
   - Mike Johnson (MikeJohnson_InputResume.pdf)
   - David Lee (DavidLee_InputResume.pdf)
   - Ben Carter (BenCarter_InputResume.pdf)
   
   Skills Match: JavaScript, React, Node.js, REST APIs, Databases,
                 Frontend/Backend Development, Microservices



PERFORMANCE
-----------
Typical processing time:
- Resume extraction: 30-60 seconds
- JD extraction: 30-60 seconds
- CV generation: 60-90 seconds
- Total: 180-210 seconds per resume

Time varies based on:
- LLM model size
- Hardware specifications
- Resume complexity


FEATURES
--------
✓ Automatic resume parsing using LLM
✓ Job description analysis
✓ ATS-optimized CV generation
✓ Keyword matching and optimization
✓ Professional PDF formatting
✓ Interactive review mode (optional)
✓ Auto-optimization mode (optional)
✓ Real-time ATS scoring
✓ Markdown-based CV formatting
✓ Custom CSS styling for PDFs


================================================================================
                              END OF README
================================================================================
