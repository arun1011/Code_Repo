from .ai_nlp import get_syn, stemming
from .ai_textclass import split_alpha_numeric, split_spl_chr, list2text, word_mix, sim
from .ai_text2num import text2num
import re

def text_normalizer(search_query, synset, gi_tags, stopwords, voc_list):
    # preprocess
    search_query = preprocess(search_query) + " "
    
    #spell correction
    temp_query=search_query.lower()
    for w in temp_query.split():
        if len(w)<=3: continue
        if w in voc_list:
            continue
        else:
            for voc in voc_list:
                if voc[0]==w[0]:
                    wsim=sim(voc,w); #print(w,voc,wsim)
                    if wsim>0.85:
                        search_query=search_query.replace(w+" ",voc+" ")
    #print(1, search_query)
    
    # synset mapping
    search_input = ' ' + search_query.lower() + ' '
    tdict ={}
    tlist = []
    for c, lc in synset.items():
        for t in lc:
            t = t.lower()
            if ' ' + t + ' ' in search_input:
#                print(1.5,c,search_input)
                tdict[' ' + t + ' '] = ' ' + c + ' '
                tlist.append(' ' + t + ' ')
    tlist.sort(reverse=True,key=len)
    
    for x in tlist:
        if x in search_input:
            search_input = search_input.replace(x, tdict[x])
    search_input = search_input.strip()
#    print(2, search_query,synset)
    
    # stemming
    #search_input = [stemming(w) for w in set(search_input.split())]
    stem=[]
    for w in set(search_input.split()):
        if w[-3:]=="ing": w=w[:-3]
        stem.append(w)
    
    # remove stopwords and common words
    search_terms = remove_stopwords(stem, stopwords);
#    print(3, search_terms)
    
    # remove b_tags from search_terms?????????????????????????????????
    for tag, itemlist in gi_tags.items():
        if tag in ['greet', 'thank', 'intro', 'profile']:
            for item in itemlist:
                if item in search_terms: search_terms.remove(item)
#    print(4, search_terms)
                
    # keep valid terms
    search_terms = [t for t in search_terms if word_mix(t) in ['a','an','n']]
#    print(5, search_terms)
    
    # normalize by sorting
    search_terms = sorted([w.lower() for w in search_terms])
    search_norm = list2text(search_terms," ")
    search_len = len(search_terms)
#    print(6, search_terms)
    return search_query, search_terms, search_norm, search_len



def custom_changes(query):

    replace_to_empty = ['...', 'ﬁ', 'ﬂ', '\n']
    for i in replace_to_empty: query = query.replace(i, '')

    replace_to_space = [',']
    for i in replace_to_space: query = query.replace(i, ' ')

    query=" "+query+" "
    repdict={" u ":" you ", " r ":" are ", " ur ":" your "}
    # "no of":"number of",
    # 'update':'update or add', 'set up':'setup', 'mail box': 'mailbox'}
    
    for rep in repdict: query=query.replace(rep.lower(), repdict[rep].lower())
    
    return query.strip()


antonyms_list=[]
def custom_synonyms(query, bQueryLower = True):
    if bQueryLower: 
        query = query.lower()

    query = " " + query + " "
    neg=["n't","nt","n t"," not"]
    conj=["do","did","can","could"]
    negconj=[]
    for c in conj:
        for n in neg:
            negconj.append(c+n)
    #print(negconj)
    
    for line in antonyms_list:
        if line.strip()=="": continue
        keylist=line.strip().split('~')
        tgt=keylist[0]
        valist=keylist[1].split(',')
        for nc in negconj:
            for v in valist:
                #fnd=nc+" "+v
                #query = query.replace(fnd,tgt)
                fnd = re.compile(re.escape(nc + " " + v), re.IGNORECASE)
                query = fnd.sub(tgt, query)
    return query.strip()



def text_corrections(text):
    text.replace('\\n', '');
    text = text.strip(',');
    text = text.strip('"');
    text = text.strip("'")
    return text


def remove_stopwords(input_list, stopwords):
    use_list=[]
    for y in input_list:
        if y.lower() not in stopwords:
            use_list.append(y)
    return use_list


def preprocess(query, bQueryLower = True):
    query = text_corrections(query); #print('1', query)
    query = split_spl_chr(query); #print('2', query)
    query = split_alpha_numeric(query); #print('3', query)
    query = text2num(query); #print('4', query)
    query = custom_changes(query); #print('5', query)
    query = custom_synonyms(query, bQueryLower); #print('6', query)
    return query.strip()
#print(custom_preprocess("I want to access x.0 in 500mb"))


#This function will handle file open
def fileHandler(file,mode):
    tmp_file = ''
    try:
        tmp_file=open(file, mode, encoding="cp1252")
    except UnicodeEncodeError as ae:
        tmp_file=open(file, mode, encoding="iso-8859-1")
    return tmp_file

