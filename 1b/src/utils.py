import re

def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_sections(text):
    """
    Split text into sections based on heuristics:
    - Lines in ALL CAPS or ending with colon ':'
    - Numbered section titles like 1. or 2.1 etc.

    Returns list of (section_text, section_title).
    If no sections found, return one section with title 'Full Text'.
    """
    lines = text.split('\n')
    sections = []
    curr_title = None
    curr_section_lines = []

    for line in lines:
        trimmed = line.strip()
        if len(trimmed) == 0:
            continue
        # Detect section titles
        if (trimmed.isupper() or trimmed.endswith(':') or re.match(r'^\d+(\.\d+)*\s', trimmed)):
            if curr_title and curr_section_lines:
                sections.append((' '.join(curr_section_lines).strip(), curr_title.strip()))
                curr_section_lines = []
            curr_title = trimmed.rstrip(':')
        else:
            curr_section_lines.append(trimmed)
    # Add last section
    if curr_title and curr_section_lines:
        sections.append((' '.join(curr_section_lines).strip(), curr_title.strip()))
    # If no sections found, return whole text as one section
    if not sections and text.strip():
        sections = [(text.strip(), 'Full Text')]
    return sections
