from datetime import datetime as dt
from .ai_textclass import split_alpha_numeric, split_spl_chr

unitlist=[
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
        "hundred", "thousand", "million", "billion", "trillion",
        'first', 'second', 'third', 'fifth', 'eighth', 'ninth', 'twelfth',
        'ieth', "and"
        ]

def text2int(textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units): numwords[word] = (1, idx)
        for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    for word in textnum.split():
        if word in ordinal_words: 
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replace in ordinal_endings:
                if word.endswith(ending): word = word.replace(word[:-len(ending)], replace)

        if word not in numwords: return 'non'
        scale, increment = numwords[word]

        current = current * scale + increment
        if scale > 100: result += current; current = 0

    return result + current
    

def text2num(query):
    query=str(query)+" ."; qlist=query.split(); 
    numval=""; txtval=""; qlen=len(qlist); q=0; #print(qlen)
    #incase number with space
    for u in unitlist: query=query.replace(u,u+" ")
        
    while q<qlen:
        if qlist[q] in unitlist:
            for i in range(q, qlen):
                if qlist[i] not in unitlist: break
                numval=str(numval)+" "+str(qlist[i])
            if numval.strip()!='and': numval=text2int(numval.strip())
            txtval=txtval+" "+str(numval); numval=""; q=i
        else:
            txtval=txtval+" "+qlist[q]; q=q+1
    txtval=txtval[:-1].strip()
    return txtval
    
    
def get_num_seq(query):
    numdict={'eight': 8, 'four': 4, 'six': 6, 'three': 3, 'five': 5, 'one': 1, 'two': 2, 'zero': 0, 'seven': 7, 'nine': 9}
    alphalist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    numlist=[0,1,2,3,4,5,6,7,8,9]
    newquery=""; query=query.lower()
    for q in query.split():
        if q in alphalist or q in numdict or q in numlist:
            if q in numdict: q=numdict[q]
            newquery=newquery+str(q)
    return newquery

