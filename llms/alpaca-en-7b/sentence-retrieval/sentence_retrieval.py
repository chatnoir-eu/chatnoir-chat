from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd
import ir_datasets
from flask import Flask, request, jsonify

import pyterrier as pt
if not pt.started():
  pt.init()

from chatnoir_pyterrier import ChatNoirRetrieve
from chatnoir_pyterrier.feature import Feature
from chatnoir_api import Index

app = Flask(__name__)

def to_sentences(docs):
    ret = []
    i = 0
    for doc in docs:
      for paragraph in doc['default_text'].split('\n\n'):
        for s in sent_tokenize(paragraph):
          s = {'docno': str(i), 'docno': str(i), 'body': s, 'metadata': {}}
          if 'doc_id' in doc:
            s['metadata']['doc_id'] = doc['doc_id']
          if 'url' in doc:
            s['metadata']['url'] = doc['url']
          ret += [s]
          i += 1
    return ret

def normalize_query(query):
    #inspired by https://github.com/terrier-org/pyterrier/blob/master/pyterrier/io.py#L339
    #tokeniser = autoclass("org.terrier.indexing.tokenisation.Tokeniser").getTokeniser()
    #from jnius import autoclass
    replacement_terms = {'born': ['birth', 'data']}
    ret = []
    
    for i in word_tokenize(query):
        if len(i) < 2:
            continue
        for t in replacement_terms.get(i.lower(), [i.lower()]):
         
            ret += [t.replace("'", "").replace('?', '').replace('.', '').replace('!', '')]

    return ' '.join(ret)

@app.route('/retrieve-top-sentences-cw22', methods=['GET'])
def retrieve_top_sentences():
    query = request.args.get('query')
    normalized_query = normalize_query(query)
    ret = retrieve_top_sentence_against_chatnoir(normalized_query)
    offset = 3
    sources = [i['source'] for i in ret[:offset]]
    ret = ' '.join([i['body'] for i in ret[:offset]]).replace('\\s', ' ').replace('\n', ' ')
    
    return jsonify({'query': query, 'normalized_query': normalized_query, 'response': ret, 'sources': sources})


@app.route('/add-references', methods=['GET'])
def add_references():
    answer = request.args.get('answer')
    answer_sentences = sent_tokenize(answer)
    chatnoir = ChatNoirRetrieve("JHNjvkvzzb4cjbAhehlQCVTp4XqxMFL0", features=[Feature.TREC_ID, Feature.TARGET_URI, Feature.TITLE, Feature.SNIPPET_TEXT], staging=True)
    chatnoir.index = Index.ClueWeb22
    
    ret = ''
    ret_sources = []
    for i in range(len(answer_sentences)):
        s = answer_sentences[i][:-1]
        try:
            if len(ret_sources) < 6:
                curr_index = len(ret_sources) +1
            
                for _, r in chatnoir.search(answer_sentences[i][:-1]).head(2).iterrows():
                    ret_sources += [{'headline': '[' + str(len(ret_sources) +1) + '] ' + r['target_uri'], 'link': r['target_uri'], 'description': r['snippet_text']}]
            
                s += ' [' + str(curr_index) + ']'
        except Exception as e:
            pass
        
        s += answer_sentences[i][-1]
        ret += ' ' + s
    
    return jsonify({'answer': ret, 'sources': ret_sources})
        
    

def retrieve_top_sentence_against_chatnoir(query):
    chatnoir = ChatNoirRetrieve("JHNjvkvzzb4cjbAhehlQCVTp4XqxMFL0", features=[Feature.TREC_ID], staging=True)
    chatnoir.index = Index.ClueWeb22
    docs = [i.trec_id for _, i in chatnoir.search(query).iterrows()]
    
    return retrieve_against_irds(docs, irds_id='clueweb22/b', query=query)
    

def retrieve_against_irds(doc_ids, irds_id, query):
  ds = ir_datasets.load(irds_id).docs_store()
  docs = []
  for doc in [ds.get(i) for i in doc_ids]:
      s = {'default_text': doc.default_text()}  
      for k in ['doc_id', 'url']:
        try:
          s[k] = getattr(doc, k)
        except:
          continue
        
      docs += [s]

  return retrieve_against_full_text_docs(docs, query)


def retrieve_against_full_text_docs(docs, query):
    sentences = to_sentences(docs)
    sentence_to_metadata = {i['docno']: i for i in sentences}
    df = pd.DataFrame([{'qid': '1', 'docno': i['docno'], 'body': i['body'], 'query': query} for i in sentences])

    ret = pt.text.scorer(wmodel="BM25")(df)
    ret = ret.sort_values('rank').head(5)
    ret_list = []
    for _, i in ret.iterrows():
        i = i.to_dict()
        i['source'] = sentence_to_metadata[i['docno']]
        
        ret_list += [i]

    return ret_list

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

