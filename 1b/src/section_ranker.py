from sentence_transformers import SentenceTransformer, util

_MODEL = None

def load_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL

def rank_sections(sections, persona, job):
    """
    Rank sections by semantic similarity to persona+job description.

    sections: list of (text, title, page_num, doc_name)
    Returns: list of (score, docname, section_title, page_num, text)
    """
    model = load_model()
    if len(sections) == 0:
        return []
    combined_texts = [f"{title}: {text}" if title else text for text, title, _, _ in sections]
    embeddings = model.encode(combined_texts, convert_to_tensor=True, show_progress_bar=False)
    query_emb = model.encode(persona + " " + job, convert_to_tensor=True, show_progress_bar=False)
    cosine_scores = util.cos_sim(query_emb, embeddings)[0]

    scored_sections = []
    for i, score in enumerate(cosine_scores):
        text, title, page_num, docname = sections[i]
        scored_sections.append((score.item(), docname, title, page_num, text))

    ranked = sorted(scored_sections, key=lambda x: x[0], reverse=True)
    return ranked
