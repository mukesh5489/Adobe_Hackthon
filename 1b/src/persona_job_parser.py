import json

def load_persona_job(input_json_path):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    persona_data = data.get('persona', {})
    if isinstance(persona_data, dict):
        role = persona_data.get('role', '')
    else:
        role = str(persona_data)
    job_data = data.get('job_to_be_done', {})
    job_task = job_data.get('task', '') if isinstance(job_data, dict) else str(job_data)
    return role, job_task

def load_documents_info(input_json_path):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('documents', [])
