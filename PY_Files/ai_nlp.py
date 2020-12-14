import nltk

from .stopwords import stopwords
def remove_stopwords(input_list):
    use_list=[]
    for y in input_list:
        if y.lower() not in stopwords:
            use_list.append(y)
    return use_list

    
from nltk.tag.perceptron import PerceptronTagger
def postag(txt):
    precptag = PerceptronTagger()
    input_list=txt.split()
    try:
        tagged=nltk.tag._pos_tag(tokens=input_list, tagset=None, tagger=precptag, lang='eng')
    except:
        tagged=nltk.tag._pos_tag(tokens=input_list, tagset=None, tagger=precptag)
    return tagged


def postag_pattern(txt):
    words = nltk.word_tokenize(txt)
    tagged = nltk.pos_tag(words)
    pattern=""
    for tag in tagged:
        pattern=pattern+" "+tag[1]
    pattern=pattern.strip()
    return pattern

    
def filter_input(txt):
    precptag = PerceptronTagger()
    input_list=txt.lower().split()
    temp_list=nltk.tag._pos_tag(input_list, None, tagger=precptag); return_list=[]
    for temp in temp_list:
        if temp[1] not in ['CC','WDT','WP','WRB']: 
            return_list.append(temp[0])
    #return_list=remove_stopwords(return_list)
    return return_list
    

# from PyDictionary import PyDictionary
# dictionary=PyDictionary()

def meaning(txt):
    return dictionary.meaning(txt)
        
def synonym(txt):
    return dictionary.synonym(txt)
    
def antonym(txt):
    return dictionary.antonym(txt)


from nltk.corpus import wordnet
def get_syn(w):
    syns = wordnet.synsets(w); synw=[]
    if len(syns)>0:
        if len(syns[0].lemmas())>0:
            for i in syns[0].lemmas():
                if i.name()!=w:
                    synw.append(i.name())  
    return synw
    
    
from nltk.tokenize import word_tokenize, sent_tokenize
def word_tokenizer(txt):
    w=word_tokenize(txt)
    return w

def sent_tokenizer(txt):
    s=sent_tokenize(txt)
    return s
    
    
from nltk.corpus import words    
def unwords(text):
    reftxt=words.words()
    txt=[]    
    txt = text.strip( ).split(' ')
    #return txt
    text_vocab = set(w.lower() for w in txt if w.isalpha())
    english_vocab = set(w.lower() for w in reftxt)
    unusual = text_vocab.difference(english_vocab)
    return sorted(unusual)
    
    
def plural(word):
    #this is wrong indian will be indien
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'	

        
from nltk.stem import PorterStemmer
def stemming(w):
    #txt = "it is very important to be pythonly while pythoning with python. All pythoners have pythoned good."
    ps = PorterStemmer()
    p = ps.stem(w)
    return str(p)


from nltk.stem import WordNetLemmatizer
def lemmatizing(txt):
    #print(wnl.lemmatize("cacti"))
    #print(wnl.lemmatize("better")) 
    wnl = WordNetLemmatizer()
    w = wnl.lemmatize(txt)
    print(w)
    return w
    
        
def named_entity(txt):
    tagged=postag(txt)
    namedEnt = nltk.ne_chunk(tagged,binary=True)
    return namedEnt
    
    
def namext(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(namext(child))
    return entity_names
    

def chunking(txt):
    tagged=postag(txt)
    chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP><NN>}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged)
    #print(chunked)
    #chunked.draw()
    return chunked
    
    
def syns(word):
    from nltk.corpus import wordnet
    syns=wordnet.synsets(word)
    #print(syns)
    #print(syns[0].name())
    #print(syns[0].lemmas()[0].name())
    #print(syns[0].definition())
    #print(syns[0].examples())
    alts=[]
    synms=[]
    antms=[]
    for syn in syns:
        for l in syn.lemmas():
            if l.name() not in synms:
                synms.append(l.name())
            if l.antonyms():
                antms.append(l.antonyms()[0].name())
    #print(synms)
    #print(antms)
    #alts.append(synms)
    #alts.append(antms)
    #return alts
    return synms
    
    
def contextsim(w1,w2):
    from nltk.corpus import wordnet
    # synsets & synset are different outputs
    w1 = wordnet.synset(w1)
    w2 = wordnet.synset(w2)
    s = w1.wup_similarity(w2)
    return s

    
def lexdiv(text):
    return len(text)/len(set(text))

    
def cfraction(text):
    from nltk.corpus import stopwords
    stopwords =stopwords.words('english')
    txt=[]    
    txt = text.strip( ).split(' ')
    content = [w for w in txt if w.lower() not in stopwords]
    return len(content) / len(text)
    return content

    
def fdl(text):
    #return list of keys
    import nltk
    d=nltk.FreqDist(text)
    dlist = [pair[0] for pair in sorted(d.items(), key=lambda item: item[1],reverse=True)]    
    return dlist

    
def fdd(text):
    #return dictionary of keys and values
    import nltk
    d=nltk.FreqDist(text)
    ddict = sorted(d.items(), key=lambda item: item[1],reverse=True)
    return ddict

    
def fd2(text):
    #return list of key and values seperately
    import nltk
    d=nltk.FreqDist(text)
    dlist = [pair[0] for pair in sorted(d.items(), key=lambda item: item[1],reverse=True)]    
    dfreq = [pair[1] for pair in sorted(d.items(), key=lambda item: item[1],reverse=True)]    
    dlf2=[]
    dlf2.append(dlist)
    dlf2.append(dfreq)    
    return dlf2

    
def fd(text):
    fdist=nltk.FreqDist(text)
    long_words=[w.lower() for w in text if len(w) > 10 and w.isalpha and fdist[w]>1]
    long_words=set(long_words)
    return long_words
    
    
def cfd(text, tgt_list):
    from nltk.corpus import inaugural
    cfd = nltk.ConditionalFreqDist( (target, fileid[:4]) for fileid in inaugural.fileids() for w in inaugural.words(fileid) for target in tgt_list if w.lower().startswith(target))
    #cfd.plot()
    return cfd

    