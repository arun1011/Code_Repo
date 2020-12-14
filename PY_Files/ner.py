import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk import pos_tag
ner = en_core_web_sm.load()

from bs4 import BeautifulSoup
import requests
import re

#from ai_nlp import pos 
data = ['European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
,"I was working in nigh shift. But not getting allowance. help me"]

def get_ent_list(txt):
    doc = ner(txt)
    ent_data = doc.ents
    ent_list = [(X.text, X.label_) for X in ent_data]
    return ent_list
    
def get_all_tags(txt):
    doc = ner(txt)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

#get_all_tags(data[0])

def get_ent_dict(data):
    ent_dict={}
    for txt in data:
        ent_list=get_ent_list(txt)
        pos_list = pos_tag(txt.split())
        print("Sentence:"); print(txt); print("NLTK POS:"); print(pos_list); print("Spacy NER:"); print(ent_list); print("")
        ent_dict[txt]=ent_list
    return ent_dict

#get_ent_dict(data)   

def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))

def analyze_article():
    ny_bb = url_to_string('https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
    article = ner(ny_bb)
    len(article.ents)
    labels = [x.label_ for x in article.ents]
    cl=Counter(labels); print(cl)
    
    items = [x.text for x in article.ents]
    ci=Counter(items).most_common(3); print(ci)
    
    #random sentence- check
    sentences = [x for x in article.sents]
    print(sentences[10])
#    displacy.render(ner(str(sentences[20])), jupyter=True, style='ent')
#    displacy.render(ner(str(sentences[20])), style='dep', jupyter = True, options = {'distance': 120})

#analyze_article()