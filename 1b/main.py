import os
import sys
import datetime
import json

from src.auto_input_json import create_input_json
from src.persona_job_parser import load_persona_job, load_documents_info
from src.extract_text import extract_pdf_sections
from src.section_ranker import rank_sections
from src.utils import split_sections

def process_collection(collection_dir, input_json_name='collection1_input.json', output_json_name='collection1_output.json'):
    print("=== Persona-Driven Document Intelligence ===\n")

    print("Enter Persona Role (e.g., Investment Analyst, PhD Researcher):")
    persona_role = input("> ").strip()
    print("Enter Persona Expertise (e.g., Computational Biology, Finance):")
    persona_expertise = input("> ").strip()
    print("Enter Persona Focus Areas (comma separated):")
    persona_focus = [x.strip() for x in input("> ").split(",") if x.strip()]
    print("Enter Job-To-Be-Done (one sentence):")
    job_task = input("> ").strip()

    persona = {
        "role": persona_role if persona_role else "Default Role",
        "expertise": persona_expertise if persona_expertise else "General",
        "focus_areas": persona_focus if persona_focus else ["General"]
    }
    job_to_be_done = {
        "task": job_task if job_task else "Default task"
    }

    # Auto create input JSON
    input_json_path = create_input_json(
        collection_dir=collection_dir,
        persona=persona,
        job_to_be_done=job_to_be_done,
        input_name=input_json_name
    )

    # Load persona, job, and docs
    persona_str, job_str = load_persona_job(input_json_path)
    doc_infos = load_documents_info(input_json_path)
    input_documents = [d['filename'] for d in doc_infos]

    all_sections = []

    # Extract text and split into sections for each document
    for doc in doc_infos:
        filename = doc['filename']
        filepath = os.path.join(collection_dir, filename)
        page_map = extract_pdf_sections(filepath)
        for pg, page_text in page_map.items():
            sections = split_sections(page_text)
            for sec_text, sec_title in sections:
                if len(sec_text.strip()) < 50:
                    continue
                all_sections.append((sec_text, sec_title, pg, filename))

    # Rank sections
    ranked_sections = rank_sections(all_sections, persona_str, job_str)
    top_sections = ranked_sections[:8]

    output = {
        "metadata": {
            "input_documents": input_documents,
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for importance_rank, (score, docname, title, page_num, body) in enumerate(top_sections, 1):
        output["extracted_sections"].append({
            "document": docname,
            "section_title": title,
            "importance_rank": importance_rank,
            "page_number": page_num
        })
        output["subsection_analysis"].append({
            "document": docname,
            "refined_text": body[:1300],
            "page_number": page_num
        })

    output_path = os.path.join(collection_dir, output_json_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"[INFO] Output JSON written to {output_path}")
    print("\n=== Processing Complete ===")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/main.py data/<collection_dir>/")
        sys.exit(1)
    collection_dir = sys.argv[1]
    process_collection(collection_dir)
