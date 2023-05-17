from keybert import KeyBERT

kw_model = KeyBERT()

def getKeywords(question):
    arr = question.split(" ")
    n = int(((len(arr)) / 2) + 1)
    keywords=kw_model.extract_keywords(question, keyphrase_ngram_range=(1, n), stop_words=None)
    return keywords[0][0]

# YAKE Algorithm 
import yake 

def getKeywords2(text):
    kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, dedupFunc='seqm', windowsSize=2, top=10, features=None)
    keywords = kw_extractor.extract_keywords(text)
    return keywords[0][0]


# In[25]:


# RAKE Algorithm 

# import nltk
# nltk.download('punkt')

# from rake_nltk import Rake
# r = Rake()

# def getKeywords(text):
#     r.extract_keywords_from_text(text)
#     keywords = r.get_ranked_phrases() 
#     return keywords[0]
