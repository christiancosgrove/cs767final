import numpy as np
import pandas as pd
import string
import argparse
from typing import Dict, List, NamedTuple
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from collections import Counter, defaultdict, namedtuple
from rank_bm25 import BM25Okapi

# import torch
# from sentence_transformers import SentenceTransformer



stemmer = SnowballStemmer('english')

class Document(NamedTuple):
    doc_id: int
    last_updated: str
    topic: str
    claim: List[str]

    def sections(self):
        return [self.claim]

    def __repr__(self):
        return (f"doc_id: {self.doc_id}\n" +
            f"  last_updated: {self.last_updated}\n" +
            f"  topic: {self.topic}\n" +
            f"  claim: {self.claim}\n")


def read_stopwords(file):
    with open(file) as f:
        return set([x.strip() for x in f.readlines()])


def read_data(file):
    '''
    Reads the corpus into a list of Documents
    '''
    docs = []
    with open(file) as f:
        lines = f.readlines()[1:]
    for i, line in enumerate(lines, start=1):
        line = line.strip().split('\t')
        # topic = [word.lower() for word in word_tokenize(line[1])]
        claim = [word.lower() for word in word_tokenize(line[2])]
        claim = [word for word in claim if not all(w in string.punctuation for w in word)]
        claim = [word for word in claim if word != '–'] # for some reason this is not being treated as punctuation
        docs.append((i, line[0].lower(), line[1].lower(), claim))

    return [Document(d[0], d[1], d[2], d[3]) for d in docs]


def stem_doc(doc: Document):
    return Document(doc.doc_id, doc.last_updated, doc.topic, *[[stemmer.stem(word) for word in sec]
        for sec in doc.sections()])

def stem_docs(docs: List[Document]):
    return [stem_doc(doc) for doc in docs]

def remove_stopwords_doc(doc: Document):
    stopwords = read_stopwords('common_words')
    return Document(doc.doc_id, doc.last_updated, doc.topic, *[[word for word in sec if word not in stopwords]
        for sec in doc.sections()])

def remove_stopwords(docs: List[Document]):
    return [remove_stopwords_doc(doc) for doc in docs]


def process_docs(docs, stem=True, removestop=True):
    processed_docs = docs
    if removestop:
        processed_docs = remove_stopwords(processed_docs)
    if stem:
        processed_docs = stem_docs(processed_docs)
    return processed_docs


def process_query(raw_query):
    if raw_query != '':
        query = [word.lower() for word in word_tokenize(raw_query)]
    return [Document(None, None, None, query)]

def retrieve_document(docs, score):
    # print('score: {}'.format(max(score)))
    return ' '.join(docs[np.argmax(score)].claim)


def get_args():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument('--mode', help='Mode to run program in', type=str,
        choices=['interactive', 'from-file', 'bert'], default='interactive')
    args = parser.parse_args()
    return args

def search(bm25, docs, raw_query):
    query = process_query(raw_query)
    processed_query = process_docs(query)[0]
    score = bm25.get_scores(processed_query.claim)
    return retrieve_document(docs, score)

def get_score(bm25, raw_query):
    query = process_query(raw_query)
    processed_query = process_docs(query)[0]
    return max(bm25.get_scores(processed_query.claim))


def match():
    docs = read_data('latest_ideas_misinformation.csv')
    processed_docs = process_docs(docs)
    bm25 = BM25Okapi([doc.claim for doc in processed_docs])

    with open('quorona.txt', 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    df = pd.DataFrame({'sentence': lines})
    df['match'] = df.apply(lambda x: search(bm25, docs, x.sentence), axis=1)
    df['score'] = df.apply(lambda x: get_score(bm25, x.sentence), axis=1)
    df = df.sort_values(by=['score'], ascending=False)
    df.to_csv('quorona_matched_misinformation.csv', index=False)
    # import pdb; pdb.set_trace()


def interactive():
    docs = read_data('latest_ideas_misinformation.csv')
    processed_docs = process_docs(docs)
    bm25 = BM25Okapi([doc.claim for doc in processed_docs])

    while True:
        raw_query = input('Please write query.\n')
        print(search(bm25, docs, raw_query), '\n')

def bert_semantic_search():
    docs = read_data('latest_ideas_misinformation.csv')
    processed_docs = process_docs(docs)
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    with open('quorona.txt', 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    df = pd.DataFrame({'sentence': lines})
    import pdb; pdb.set_trace()

        
def main():
    args = get_args()
    if args.mode == 'interactive':
        interactive()
    elif args.mode == 'from-file':
        match()
    elif args.mode == 'bert':
        bert_semantic_search()

if __name__ == '__main__':
    main()