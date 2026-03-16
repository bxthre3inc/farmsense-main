# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import os
import sys

try:
    import fitz  # PyMuPDF
    def extract_text(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
except ImportError:
    try:
        import PyPDF2
        def extract_text(pdf_path):
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
    except ImportError:
        print("Required PDF parsing libraries not found. Please run: pip install pymupdf")
        sys.exit(1)

pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
pdf_files.sort()

with open('hardware_specs_full.txt', 'w') as out_f:
    for pdf_file in pdf_files:
        out_f.write(f"\n==================== {pdf_file} ====================\n")
        text = extract_text(pdf_file)
        out_f.write(text)
        out_f.write("\n\n")
