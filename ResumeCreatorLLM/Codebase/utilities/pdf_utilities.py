import pdfplumber
from markdown_pdf import MarkdownPdf, Section

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def create_pdf_from_text(cv_text, output_path):
    """
    Converts plain text cv into a polished PDF with bold headers and bullets.

    Args:
        cv_text (str): CV text content in Markdown format.
        output_path (str): Output PDF file path.
    """
    
    # 1. Define custom CSS for a professional, ATS-friendly CV style
    custom_css = """
    body {
        font-family: Arial, sans-serif;
        font-size: 10.5pt;
        line-height: 1.5;
        padding: 0.5in 0.75in;
        color: #1a1a1a;
    }
    
    /* Name heading (h1) */
    h1 {
        font-size: 24pt;
        font-weight: bold;
        color: #1a1a1a;
        text-align: center;
        margin-top: 0;
        margin-bottom: 8px;
        border-bottom: none;
    }
    
    /* Section headers (h2) */
    h2 {
        font-size: 13pt;
        font-weight: bold;
        color: #2c5282;
        border-bottom: 2px solid #2c5282;
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    /* Bold text styling */
    strong {
        font-weight: bold;
        color: #1a1a1a;
    }

    /* Bullet points */
    ul {
        list-style-type: disc;
        padding-left: 22px;
        margin-top: 8px;
        margin-bottom: 10px;
    }
    
    li {
        margin-bottom: 5px;
        line-height: 1.6;
    }
    
    /* Paragraphs */
    p {
        margin-top: 6px;
        margin-bottom: 6px;
        line-height: 1.5;
    }
    """
    
    # 2. Initialize the PDF generator
    pdf = MarkdownPdf(toc_level=0)
    
    # 3. Add the content section with custom CSS
    pdf.add_section(Section(cv_text), user_css=custom_css)

    # 4. Save the file
    try:
        pdf.save(output_path)
        print(f"✅ Success! The CV has been generated as a styled PDF: {output_path}")
    except Exception as e:
        print(f"❌ An error occurred while saving the PDF: {e}")
 

