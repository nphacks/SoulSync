from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util

def extract_topics(text): 
    kw_model = KeyBERT()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Extract 10 candidates first
    candidates = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', top_n=10)
    unique_topics = []

    for phrase, _ in candidates:
        if all(util.cos_sim(model.encode(phrase), model.encode(prev))[0][0] < 0.7 for prev in unique_topics):
            unique_topics.append(phrase)
        if len(unique_topics) == 5:
            break
    return unique_topics