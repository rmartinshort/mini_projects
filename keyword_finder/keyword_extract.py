from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from scipy.spatial import distance

from nltk.corpus import stopwords
eng_stopwords = stopwords.words('english')

class KeyWordFinder(object):

	"""

	Example usage 
	model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

	pp = Preprocessor(ngram_range=(1,3))
	vv = Vectorizer(model)
	kf = KeyWordFinder(preprocessor=pp,vectorizer=vv)

	kws = kf.find_within_sentence(text,sentence_breakdown=True,augment_candidates=False,topk=12)
	kws = kf.find(text,sentence_breakdown=False,augment_candidates=False,topk=10)
	"""
    
    def __init__(self,vectorizer,preprocessor):
        
        self.vectorizer = vectorizer
        self.preprocessor = preprocessor
    
    def find_within_sentence(self,text,sentence_breakdown=True,augment_candidates=False,topk=5):
        
        sentence_dict = self.preprocessor.process_text(text,sentence_breakdown=sentence_breakdown,augment_candidates=augment_candidates)
                
        output_sentence_dict = sentence_dict.copy()
        
        for s_id in sentence_dict:
            sentence = sentence_dict[s_id]["original_sentence"]
            kw_candidates = sentence_dict[s_id]["kws"]
            sentence_len = sentence_dict[s_id]["len"]
                    
            # Matrix of encoded text (one row)
            encoded_text = self.vectorizer.vectorize(sentence).reshape(1,-1)
            # Matrix of encoded ngrams (one row per ngram)
            encoded_ngrams = self.vectorizer.vectorize(kw_candidates)
        
            c_dists = distance.cdist(encoded_text,encoded_ngrams,metric="cosine").reshape(-1)
        
            key_words = [(kw_candidates[i],c_dists[i]) for i in np.argsort(c_dists)]
            if sentence_breakdown:
                output_sentence_dict[s_id]["kws"] = key_words[:sentence_len//max(self.preprocessor.ngram_range)]
            else:
                output_sentence_dict[s_id]["kws"] = key_words[:topk]
        
        return sentence_dict
    
    def find(self,text,sentence_breakdown=True,augment_candidates=False,topk=5):
        
        sentence_dict = self.find_within_sentence(text,sentence_breakdown=sentence_breakdown,augment_candidates=augment_candidates,topk=topk)
        
        kws = []
        for s in sentence_dict:
            kws += [k[0] for k in sentence_dict[s]["kws"]]
        
        return list(set(kws))
    
class Vectorizer(object):
    
    def __init__(self,model):
        
        if isinstance(model,str):
            self.vectorizer = SentenceTransformer(model_name)
        else:
            self.vectorizer = model
    
    def vectorize(self,list_of_texts):
        
        return self.vectorizer.encode(list_of_texts,convert_to_tensor=False)
    
class Preprocessor(object):
    
    def __init__(self,ngram_range=(1,3),remove_stop=True,remove_punc=True,language="english"):
        
        self.language = language
        self.remove_punctuation = remove_punc
        self.remove_stop = remove_stop
        self.ngram_range = ngram_range
        self.stopwords_set = set(stopwords.words(language))
        
    def process_text(self,text,augment_candidates=False,sentence_breakdown=True):
        
        if not sentence_breakdown:
            sentences = [text]
        else: 
            sentences = sent_tokenize(text,language=self.language)
            
        all_sents = {}
        for i, sent in enumerate(sentences):
            processed_sent, candidate_keywords = self._process_text_sentence(sent,augment_candidates=augment_candidates)
            all_sents[i] = { \
                            "original_sentence":sent,
                            "processed_sentence":processed_sent,
                            "len":len(processed_sent.split()),
                            "kws":candidate_keywords
                           }
        return all_sents
        
    def _process_text_sentence(self,sent,augment_candidates=True):
        
        if self.remove_punctuation:
            text = self._remove_puncs(sent)
        
        if self.remove_stop:
            text = self._remove_stops(text)
            
        candidate_keywords = self._ngrams_split(text)
        
        if augment_candidates:
            candidate_keywords = self._find_additional_candidates(text,candidiate_keywords)
            
        return text, candidate_keywords
    
    def _find_additional_candidates(self,processed_text,original_candidates):
        
        processed_text_words = processed_text.split()
        lp = len(processed_text_words)
        p1 = " ".join([processed_text_words[i] for i in range(0,lp,2)])
        p2 = " ".join([processed_text_words[j] for j in range(1,lp,2)])
        
        candidate_kw_1 = self._ngrams_split(p1)
        candidate_kw_2 = self._ngrams_split(p2)
        
        return list(set(original_candidates + candidate_kw_1 + candidate_kw_2))
    
    def _remove_puncs(self,text):
        
        return text.translate(str.maketrans("","",string.punctuation))
    
    def _remove_stops(self,text):
        
        toks = word_tokenize(text.lower(),language=self.language)
        return " ".join(t for t in toks if t not in self.stopwords_set)
    
    def _ngrams_split(self,text):
        
        vectorizer = CountVectorizer(ngram_range=self.ngram_range)
        _ = vectorizer.fit_transform([text])
        
        return list(vectorizer.get_feature_names_out())