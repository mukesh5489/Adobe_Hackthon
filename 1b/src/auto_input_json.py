import os
import json
import pdfplumber

def guess_title(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            lines = (first_page.extract_text() or '').split('\n')
            for line in lines:
                if len(line.strip()) > 5:
                    return line.strip()
    except Exception:
        pass
    # Fallback: filename without extension
    return os.path.splitext(os.path.basename(pdf_path))[0]

def create_input_json(collection_dir, persona=None, job_to_be_done=None, input_name='collection1_input.json'):
    pdf_files = [f for f in os.listdir(collection_dir) if f.lower().endswith('.pdf')]
    documents = [{"filename": fn, "title": guess_title(os.path.join(collection_dir, fn))} for fn in pdf_files]

    if persona is None:
        persona = {
            "role": "Default Role",
            "expertise": "General expertise",
            "focus_areas": ["General"]
        }
    if job_to_be_done is None:
        job_to_be_done = {
            "task": "Default job to be done"
        }

    input_data = {
        "documents": documents,
        "persona": persona,
        "job_to_be_done": job_to_be_done
    }

    input_path = os.path.join(collection_dir, input_name)
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(input_data, f, indent=2)
    print(f"[INFO] Auto-created input JSON at: {input_path}")
    return input_path
