


import operator
def sort_by_value(dictx):
    dicty=sorted(dictx.items(),key=operator.itemgetter(1),reverse=True)
    dictz={}
    for k,v in dicty: dictz[k]=v
    return dictz

def sort_by_value_data_extra(dictx):
    dicty=sorted(dictx.items(),key=operator.itemgetter(1),reverse=True)
    return dicty

from .ai_nlp import remove_stopwords
def fd(list_content):
    word_corpus = [w.lower() for s in list_content for w in split_spl_chr(s).split()]
    list_corpus = [split_spl_chr(s).lower().split() for s in list_content]
    tfdict={}
    for word in set(word_corpus):
        tfdict[word]=0
        for sentlist in list_corpus:
            sentlist=remove_stopwords(sentlist)
            if word in sentlist: tfdict[word]=tfdict[word]+1
    for tf in tfdict: tfdict[tf]=tfdict[tf]/len(list_content)
    return tfdict

import os
def extract_path(fpath):
    path = ""; file=""
    if os.path.isdir(fpath): return fpath, file
    if '/' in fpath: split_chr='/'
    elif '\\' in fpath: split_chr='\\'
    npath = fpath.split(split_chr);  # print(npath)
    dir = npath[:-1]
    for p in dir: path = path + p + '/'
    path=path.strip('/')
    file = npath[-1]
    return path, file


def manage_spl_chr(text_seq):
    new_seq=""
    text_list=text_seq.split()
    for word in text_list:
        if '@' in word and '.' in word: continue
        for p in [0, -1]:
            if word[p].isdigit()==False and word[p].isalpha()==False: 
                word=word.replace(word[p], ' '+word[p]+' '); #print(word)
        new_seq=new_seq+word+" "
    return new_seq


def exit_condition(inputlist,y,exitlist):
    e=0; #print(ocrlist[y])
    for x in exitlist:
        xlen=len(x.split())
        k=""
        for i in range(xlen):
            k=k+inputlist[y+i]+ " "
        k=k.strip()
        xsim=sim(x.lower(), k.lower())
        if ':' in k.lower(): xsim=xsim+0.05
        if xsim>=0.9: 
            #print(x)
            e=1
            break
    return e


def isnumericorfloat(txt):
    for s in range(len(txt)):
        val = 'n'
        for n in range(10):
            if txt[s] in ['/','.']:val = 'y'
            if txt[s] == str(n):val = 'y'
        if val == 'n':break
    return val

def isnum(word):
    num=['0','1','2','3','4','5','6','7','8','9']
    for w in str(word):
        if w not in num: return False
    return True


def split_alpha_numeric(query):
    queryx = ""; qlen=len(query.strip())
    for x in range(qlen):
        chr1 = query[x]
        if chr1 == " ":
            queryx = queryx + chr1
            continue
        
        if x<qlen-1:
            chr2=query[x+1]
            if chr1.isdigit() and chr2 == ".":
                queryx = queryx+chr1
            elif chr1 == "." and chr2.isdigit():
                queryx = queryx+chr1
            elif chr1.isalpha() and chr2.isdigit():
                queryx = queryx+chr1+" "
            elif chr1.isdigit() and chr2.isalpha():
                queryx = queryx+chr1+" "
            elif not chr1.isalpha() and not chr1.isdigit():
                queryx = queryx+chr1
            else:
                queryx=queryx+chr1
        else:
            queryx = queryx + chr1
    return queryx.strip()


def split_spl_chr(q,split_digit=False):
    num=['0','1','2','3','4','5','6','7','8','9']
    exp=[' ',"'"]
    temp=""; qlen=len(q.strip())
    for p in range(qlen):
        if q[p].isdigit() or q[p].isalpha() or q[p] in num or q[p] in exp:
            temp=temp+q[p]
        else:
            temp=temp+" "+q[p]+" "
    queryx=temp.strip()
    return queryx


def defined_split(query,chrlist):
    rquery=""
    for q in query.split():
        for c in chrlist:
            q=q.strip(c)
        rquery=rquery+q+" "
    return rquery

#Exact word form - order and length
def word_form(txt):
    converted_txt=""
    txt=txt.lower()
    for d in txt:
        myval=''
        if d.isalpha(): myval="a"
        elif d.isdigit():myval="n"
        else: myval=d
        converted_txt=converted_txt+myval
    return converted_txt

#Unique word form - order only , no length
def word_pattern(txt):
    converted_txt=""; lastval=''
    txt=txt.lower()
    for d in txt:
        myval=''
        if d.isalpha(): myval="a"
        elif d.isdigit():myval="n"
        else: myval=d
        if myval!=lastval:
            converted_txt=converted_txt+myval
        lastval=myval
    return converted_txt
    
    
def chr_type(chrx):
    if chrx.isalpha()==True:
        return 'a'
    elif chrx.isdigit()==True:
        return 'n'
    else:
        return 's'
        
#Unique mix of the word - no order & no lenght
def word_mix(txt):
    txt=txt.lower().strip()
    if len(txt)==1:
        return chr_type(txt)
    elif len(txt)>1:
        wm=[]
        wmix=""
        for t in txt:
            wm.append(chr_type(t))
        wm=sorted(set(wm))
        for w in wm:
            wmix=wmix+w
        return wmix


def sim(a,b):
    from difflib import SequenceMatcher
    sim_score = SequenceMatcher(None,a,b).ratio()
    return sim_score


#applies only equal length strings
def lsim(a,b):
    if type(a)==str: a=a.split()
    if type(b)==str: b=b.split()
    lenb=len(b); lena=len(a); lenavg=(lena+lenb)/2; match=0
    for i in a:
        for j in b:
            if sim(i, j)>=0.8:
                match=match+1
    return match/lenavg


def word2list_sim(word, wlist):
    pos = -1
    for w in wlist:
        pos = pos + len(w)
        if sim(word.lower(), w.lower()) > 0.85: return [1, pos]
    return [0, pos]


def list2list_sim(alist,blist):
    t=max(len(alist),len(blist)); n=0
    if t==0: return 0
    for b in blist:
        b=b.lower()
        for a in alist:
            a=a.lower()
            if a[:2]==b[:2] and a[-2:]==b[-2:]:
                n=n+1; break
    return n/t


def ngram_compile(text_seq,n):
    txt_list=text_seq.split()
    ngram_list=[]; temp_list=[]
    txt_len=len(txt_list)
    for x in range(txt_len):
        for m in range(n+1):
            if m<=0: continue
            ngram=""
            for y in range(m):
                if x+y >= txt_len: break
                ngram=ngram+" "+txt_list[x+y]
            temp_list.append(ngram.strip())
    for w in temp_list: 
        if w not in ngram_list:
            ngram_list.append(w)
    return ngram_list



def ngram_map(txt_list,token_position,token_direction,token_size,break_list):
    #No case change
    ngram_list=[]; ngram=""
    if token_direction==1: s=0; e=token_size; 
    else: s=-token_size; e=0; 
    
    bsts=0; val=0; txtlen=len(txt_list)
    for c in range(s,e):
        if val>=txtlen: break
        for t in range(token_size-1,token_size+2):
            if val>=txtlen: break
            ngram=""
            for n in range(t):
                val=token_position+c+n
                if val>=txtlen: break
                ngram=ngram+" "+txt_list[val]
            ngram=ngram.strip()
            if ngram.lower() in break_list:
                bsts=1
                break
            if ngram not in ngram_list:
                ngram_list.append(ngram)
        if bsts==1: break
    return ngram_list   
    
#returns mix of ngram
def ngram_check(ngram):
    cdict={'a':0, 'n':0, 's':0}
    for n in ngram.split():
        if word_mix(n)=='a':cdict['a']=cdict['a']+1
        if word_mix(n)=='n':cdict['n']=cdict['n']+1
        if word_mix(n)=='s':cdict['s']=cdict['s']+1
    return cdict
    
    
def count_spl_chr(ngram):
    conj_b=['/','-','.',',']; spl=[]
    for i in ngram:
        if i in conj_b and i not in spl: spl.append(i)
    return len(spl)
    
    
def alpha_condition(ngram,excep_list):
    for word in ngram.split():
        if word.isalpha() and word.lower() not in excep_list:
            if len(word)<3 or len(word)>9: return 0
    return 1
    

#replace text
def rep_txt(txt,starttxt,endtxt,reptxt):
    startpos=0
    while startpos>=0:
        startpos=txt.find(starttxt)
        endpos=txt.find(endtxt)
        substr=txt[startpos:endpos+len(endtxt)]
        txt=txt.replace(substr,reptxt)
    return txt


def remove_accents(input_str):
    import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('ascii')  


def list2text(input_list,addchr):
    temp_text=""
    for word in input_list:
        temp_text=temp_text+word+addchr
    return temp_text.strip()
                
    
def trim_list(source,target):
    for s in source:
        if s.lower() in target:
            source.remove(s)
    return source
   
#keep only alpha
def alpha_list(source):
    for s in source:
        if not s.isalpha():
            source.remove(s)
    return source

    
def manage_space(txt):
    txt=txt.replace(" ","<->")
    txt_list=txt.split("<->")
    temp_list=[]
    for word in txt_list:
        if word !='':
            temp_list.append(word)
    newtxt=list2text(temp_list," ")
    return newtxt
    
    
def manage_sequence(txt, target_list):
    txt_list=txt.split()
    for w in range(len(txt_list)):
        if w==0:continue
        if w==len(txt_list)-1:break
        word=txt_list[w]; pre_word=txt_list[w-1]; nxt_word=txt_list[w+1]
        if word.lower() in target_list:
            if pre_word.isdigit() and nxt_word.isdigit():repstr=" "+word+" "
            if pre_word.isdigit() and not nxt_word.isdigit():repstr=" "+word
            if not pre_word.isdigit() and nxt_word.isdigit():repstr=word+" "
            if not pre_word.isdigit() and not nxt_word.isdigit():repstr=word
            txt=txt.replace(repstr,word.lower())
    txt_list=txt.split()
    for w in range(len(txt_list)):
        if w==len(txt_list)-1:break
        word=txt_list[w]
        for target in target_list:
            if target in word.lower():
                txt=txt.replace(word,word.lower())
    return txt
    

# npos aligned with ngram_map logic - every 3 positions are created from same x postion
def get_match_pos(curpos, ngramlist, tgt):
    lastsim=0; rpos=-1; npos=0; tpos=-1; tgt=tgt.lower(); match=""
    
    tgtlen=len(tgt.split())
    if tgtlen<2: tgtsim=0.8
    if tgtlen<4: tgtsim=0.85
    if tgtlen<6: tgtsim=0.9
    if tgtlen>=6: tgtsim=0.95
    
    for ntxt in ngramlist:
        if npos==3:
            npos=0
        if npos==0:
            tpos=tpos+1
        npos=npos+1
        #print(npos, tpos)
        
        #if abs(len(ntxt.split())-len(tgt.split()))>1:continue
        ntxt=ntxt.lower()
        if ntxt==tgt:
            rpos=curpos+tpos
            match=ntxt
            break
        cursim=sim(ntxt,tgt)
        if cursim>=tgtsim and cursim>lastsim:
            lastsim=cursim
            rpos=curpos+tpos
            match=ntxt
            if cursim==1:break
            if ntxt.split()[0]==tgt.split()[0]: break
    return rpos, match


def filter_options(optdict, ocrlist):
    #print(len(optdict))
    newdict={}
    for opt in optdict:
        print(opt)
        optlen=len(opt.split())
        sts=0
        for x in range(len(ocrlist)):
            nlist=ngram_map(ocrlist, x, 1, optlen+1, [])
            if nlist!=[]:
                for ntxt in nlist:
                    if abs(len(ntxt.split())-optlen)>1: continue
                    if lsim(ntxt.lower(), opt.lower())>0.5:
                        newdict[opt]=optdict[opt]
                        sts=1
                        x=x+optlen
                        break
            if sts==1: break
    optdict=newdict
    #print(len(optdict))
    return optdict


def split_spl_chr_dot(query, numerics):
    num=['0','1','2','3','4','5','6','7','8','9','.']
    querylist=[]    
    querylist=query.strip( ).split(' '); #print(querylist)
    tempquery=""
    for q in querylist:
        temp=""; qlen=len(q)
        for p in range(qlen):
            if q[p].isdigit() or q[p].isalpha() or q[p] in num:
                temp=temp+q[p];
            else:
                if q[p-1] in num and numerics==1:
                    temp=temp+q[p]
                else:
                    if p-1<0: continue
                    if p+1>= qlen: break
                    if q[p-1]==" " and q[p+1]!=" ":                        
                        temp=temp+q[p]+" "
                    if q[p-1]!=" " and q[p+1]==" ":
                        temp=temp+" "+q[p]
                    if q[p-1]==" " and q[p+1]==" ":
                        temp=temp+q[p]
                    if q[p-1]!=" " and q[p+1]!=" ":
                        temp=temp+" "+q[p]+" "
        tempquery=tempquery+" "+temp
    queryx=tempquery
    return queryx


def split_spl_chr_quto(query, numerics):
    num=['0','1','2','3','4','5','6','7','8','9',':','.','/','-','+']
    querylist=[]    
    querylist=query.strip( ).split(' '); #print(querylist)
    tempquery=""
    for q in querylist:
        temp=""; qlen=len(q)
        for p in range(qlen):
            if q[p].isdigit() or q[p].isalpha() or q[p] in num:
                temp=temp+q[p];
            else:
                if q[p-1] in num and numerics==1:
                    temp=temp+q[p]
                else:
                    if p-1<0: continue
                    if p+1>= qlen: break
                    if q[p-1]==" " and q[p+1]!=" ":                        
                        temp=temp+q[p]+" "
                    if q[p-1]!=" " and q[p+1]==" ":
                        temp=temp+" "+q[p]
                    if q[p-1]==" " and q[p+1]==" ":
                        temp=temp+q[p]
                    if q[p-1]!=" " and q[p+1]!=" ":
                        temp=temp+" "+q[p]+" "
        tempquery=tempquery+" "+temp
    queryx=tempquery
    return queryx