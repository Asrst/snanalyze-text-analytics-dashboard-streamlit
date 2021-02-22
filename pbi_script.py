import os, re
import pandas as pd
import numpy as np
from expertai.nlapi.cloud.client import ExpertAiClient
import preprocessor as p
p.set_options(p.OPT.URL,p.OPT.HASHTAG, p.OPT.RESERVED)
import emoji
language= 'en'

os.environ["EAI_USERNAME"] = ""
os.environ["EAI_PASSWORD"] = ""

# intialize expert.ai
client = ExpertAiClient()

def preprocess_text(t):
    t = p.clean(t)
    t = emoji.demojize(t, delimiters=("", " "))
    return t

def analyze_doc(txt):

    doc = client.full_analysis(
        body={"document": {"text": preprocess_text(txt)}}, 
        params={'language': language})

    doc_topics = [(t.label, t.score) for t in doc.topics if t.winner]                
    doc_ents = [(et.lemma, et.type_) for et in doc.entities]
    doc_syncons = [(mc.lemma, mc.score) for mc in doc.main_syncons]
    doc_sent_score = doc.sentiment.overall

    if doc_sent_score > 1:
        sent_type = 'positive'
    elif doc_sent_score < -1:
        sent_type = 'negative'
    else:
        sent_type = 'neutral'
    return doc_sent_score, sent_type, doc_topics, doc_ents, doc_syncons


def analyze_text_df(df):
    sent_scores = []
    topics = []
    syncons = []
    entities = []
    sent_types = []
    
    for txt in df['text'].tolist():
        try:
            dscore, dtype, dtopics, dents, dsyncons = analyze_doc(txt)
        except Exception as e:
            print(e)
            dscore = 0
            dtype = 'neutral'
            dtopics = []
            dents = []
            dsyncons = []
                
        sent_scores.append(dscore)
        sent_types.append(dtype)
        topics.append(dtopics)
        entities.append(dents)
        syncons.append(dsyncons)
        
    df['sentiment_score'] = sent_scores
    df['sentiment'] = sent_types
    df['topics'] = topics
    df['syncons'] = syncons
    df['entities'] = entities
    return df
    

dataset = dataset.drop_duplicates(subset=['text']).reset_index(drop=True)
rdf = analyze_text_df(dataset)
rdf