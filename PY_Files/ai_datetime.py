from datetime import datetime as dt
from dateutil.parser import parse
from .ai_textclass import ngram_compile, isnum, ngram_check, word_pattern, word_mix, alpha_condition, word2list_sim, count_spl_chr, split_alpha_numeric, split_spl_chr, ngram_map

def find_date(text_seq):
    if type(text_seq) == str:
        text_seq=split_alpha_numeric(text_seq)
        text_seq=split_spl_chr(text_seq, split_digit=False)
        l=len(text_seq.strip().split())
        if l<5: nx=l
        else: nx=5 
        ngram_list=ngram_compile(text_seq,nx); #print(ngram_list)
    else:
        ngram_list=text_seq
        l=len(text_seq)
    
    #print("ngrams-->", ngram_list)
    monthx=["january","febraury","march","april","may","june","july","august","september","october","november","december"]
    monthy=[x[:3] for x in monthx]
    conj_a=['th','rd','st','nd']
    conj_b=['/','.','&','-']
    score=0; dtseq=""; last_score=0
    for ngram in ngram_list:
        #print("i==>", ngram)
        if word_mix(ngram[0])=='s':continue
        if '00' in ngram:continue
        if len(ngram.strip())==0:continue
        if len(ngram.replace(" ",""))<3:continue
        score=0; word_list=ngram.split(); l=len(word_list); pos=0;
        if alpha_condition(ngram,conj_a)==0: continue
        if count_spl_chr(ngram)>1:continue
        if ngram_check(ngram)['n']>3: continue
        mth=0; dsts=0; pre_word=''; #print("q==>",word_list)
        for word in word_list:
            #print(word_list, word, score)
            penalty=1; pos=pos+1
            if pre_word.isdigit():
                for a in conj_a:
                    if a == word[:2] and len(word)>2:
                        word=word.replace(a,'')
                        ngram=ngram.replace(a,'')
            pre_word=word
            if word.isdigit():
                score=score+0.05; penalty=0; continue
                if len(word)<=4:
                    score=score+0.1; penalty=0; continue
            else:
                if word.lower() in conj_a: 
                    score=score+0.1; penalty=0; continue
                if word.lower() in conj_b:
                    score=score+0.1; penalty=0; continue
                if word.lower() in monthx:
                    score=score+0.2; mth=mth+1; penalty=0; continue
                if word[:3].lower() in monthy:
                    score=score+0.2; mth=mth+1; penalty=0; continue
                if mth>1:
                    score=score-0.3; break
            if penalty==1 and word.isalpha(): score=score-(0.002)
            elif penalty==1: score=score-(0.001)
            
        print('>>>', score, ngram)
        if score>=0.2 and score>last_score:
            last_score=score; dtseq=ngram
    return dtseq
    

                         
def get_multiple_date(txt):
    txt=split_alpha_numeric(txt)
    txt=split_spl_chr(txt)    
    txt_list=txt.split() 
    score=0.0; match=""; l=len(txt_list); #print(txt_list); return
    for x in range(l):
        ngram_list=ngram_map(txt_list,x,1,5,[]); #print('ngram-->',ngram_list)
        #if txt_list[x]=='4': print(str(ngram_list)); return
        wgt_list=find_date(ngram_list); #print(wgt_list); #return
        if wgt_list[0]>score:
            score=wgt_list[0]; match=wgt_list[1]; #print(match, score)
    return match
    
    
def find_convert_date(txt):
    dtxt=find_date(txt); print(dtxt)
    monthx=["january","febraury","march","april","may","june","july","august","september","october","november","december"]
    monthy=[x[:3] for x in monthx]
    dtlist=dtxt.lower().split(); 
    mt=""; d=""; y=""; mtxt=""; datetxt=""
        
    for dtx in dtlist:
        if dtx.isdigit() and len(dtx)<=2: 
            d=dtx
            dtlist.remove(d)
            break
    
    for m in range(len(monthx)):
        mfound=0
        if monthx[m] in dtlist: mfound=1; dtlist.remove(monthx[m])
        elif monthy[m] in dtlist: mfound=1; dtlist.remove(monthy[m])
        if mfound==1:
            if len(str(m))==1: mt='0'+str(m+1)
            else: mt=str(m+1)
            break
        
    if mt=="":
        for m in dtlist:
            if m.isdigit() and int(m)>=1 and int(m)<=12: mt=m; break
        
    for yr in dtlist:
        if yr.isdigit() and len(yr)==4: y=yr; break
    
    if y=="" and mt!="":
        y = dt.today().year
        if "next year" in txt.lower(): y=y+1
        if "coming year" in txt.lower(): y=y+1
        if "last year" in txt.lower(): y=y-1
    
    datetxt=[mt, d, y]
    return datetxt
    
    
def check_date(txt): 
    #today=dt.today().strftime("%m/%d/%Y")
    dtval=find_convert_date(txt)
    dtval=parse(dtval); ##print(dtval)
    today=dt.today(); #print(today)
    delta=dtval-today; #print(delta.days)
    return delta.days
    

def validate_dates(plan_date, new_date):
    delta=parse(new_date)-parse(plan_date)
    return delta.days
    
    
def find_time(text_seq):
    text_seq=split_alpha_numeric(text_seq)
    text_seq=split_spl_chr(text_seq, numerics=0)
    l=len(text_seq.strip().split())
    if l<5: nx=l
    else: nx=5 
    ngram_list=ngram_compile(text_seq,nx)
    conj_a=[':',';','.']
    conj_b=['am','pm', 'noon']
    score=0; dtseq=""; last_score=0; #print(ngram_list)        
    for ngram in ngram_list:
        if 'morning' in ngram and 'am' not in ngram_list: ngram='am'
        if 'evening' in ngram and 'pm' not in ngram_list: ngram='pm'
#        if 'noon' in ngram and 'noon' not in ngram_list: ngram='noon'
        if word_pattern(ngram) not in ['nn s nn aaa','nnnn aaa','n s','nn aaaa','n aa','nn aa','n s nn','nn s nn','n s nn aa','nn s nn aa']:continue
        if len(ngram.strip())==0:continue
        score=0; word_list=ngram.split(); l=len(word_list); pos=0
        if not word_list[0].isalpha() and not word_list[0].isdigit():continue 
        if ngram_check(ngram)['n']>2: continue
        for word in word_list:
            penalty=1; pos=pos+1
            #if word.isdigit() and len(word)<=1: score=score+0.05; penalty=0; continue
            if word.isdigit() and len(word)<=2: score=score+0.05; penalty=0; continue
            if word.lower() in conj_a: score=score+0.1; penalty=0; continue
            if word.lower() in conj_b: score=score+0.2; penalty=0; continue
            if penalty==1:score=score-(0.05*pos); 
        if word_list[l-1].lower() in conj_b: score=score+0.1
        if score>=0.15 and score>last_score:
            last_score=score; dtseq=ngram
    return_list=[]; return_list.append(score); return_list.append(dtseq); return return_list
   

    