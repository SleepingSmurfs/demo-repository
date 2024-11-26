import spacy

nlp = spacy.load("env_core_web_sm")


def process_query(query):
    doc = nlp(query)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities