import numpy as np
from PIL import Image as PilImage
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

def clear_folder(folder):
    for f in os.listdir(folder): 
        if f.endswith('.jpg'):
            os.remove(folder+'/'+f)

            
def pdf_to_text(pdf_file):
    pdf_in=PdfFileReader(open(pdf_file, "rb"))
    npage = pdf_in.getNumPages(); print(npage)
    pdf_out = PdfFileWriter()
    for pg_num in range(npage):
        pdf_out.addPage(pdf_in.getPage(pg_num))
    out_stream = open('adhoc/pdfout.txt','wb')
    pdf_out.write(out_stream)
    out_stream.close()
    
#------------------creating images------------------------------------------------#

def pdf_to_jpg(pdf_stream, pgNo, img_path):
    page0 = pdf_stream.getPage(pgNo)
    dpi=(300,300)
    xObject = page0['/Resources']['/XObject'].getObject()
    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj].getData()
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            if xObject[obj]['/Filter'] == '/FlateDecode':
                img_path=img_path+".png"
                img = PilImage.frombytes(mode, size, data)
                img.save(img_path, dpi=dpi)
            #elif xObject[obj]['/Filter'] in ['/DCTDecode', '/JPXDecode', '/CCTTFaxDecode']:
            else:
                img_path=img_path+".jpg"
                img = open(img_path,"wb")
                img.write(data)
                img.close()
                im = PilImage.open(img_path)
                im.save(img_path, dpi=dpi)
    
    
def create_images(directory,filename):
    prefix = filename[:-4]
    if not os.path.exists(directory+"/temp"):
        os.makedirs(directory+"/temp")
    org_path=directory+'/'+filename
    
    if filename.lower()[-4:] in ['.jpg','.png']:
        im = PilImage.open(org_path); #print(im.info)
        im.save(directory+"/temp/"+prefix+".jpg")
    
    if filename.lower().endswith(".pdf"):
        pdf_stream = PdfFileReader(open(org_path, "rb"))
        npage = pdf_stream.getNumPages(); print(npage)
        for pgNo in range(npage):
            print('pdf->jpg converting pg '+str(pgNo))
            f=prefix+'_'+str(pgNo)
            img_path=directory+"/temp/"+f;print(img_path)
            pdf_to_jpg(pdf_stream, pgNo, img_path)
        
    if filename.lower().endswith(".tif"):
        im = PilImage.open(org_path)
        pgcount=im.n_frames
        for pgNo in range(pgcount):
            print('tif->jpg converting pg '+str(pgNo))
            img_path = directory+"/temp/"+prefix+"_"+str(pgNo)+".jpg"
            if pgcount>1:
                img=im.seek(pgNo)
            else:
                img=im
            img.save(img_path)
    
#create_images('input','chk.pdf')          

#------------------image pre processing - Noise------------------------------------------------#
            
def bg_stats(data):    
    cdict={}; s=data.shape; outdict={'bg':[],'txt':[]}
    if len(s)==2: 
        total=s[0]*s[1]
        for row in data:
            for val in row:
                if val not in cdict:
                    cdict[val]=0
                cdict[val]=cdict[val]+1
    else: 
        total=s[0]
        for val in data:
            if val not in cdict:
                cdict[val]=0
            cdict[val]=cdict[val]+1
    
    bmax=max(cdict,key=cdict.get)
    outdict['bg']=[bmax,round(cdict[bmax]/total,2)]
    tmax=bmax; i=0; ilen=len(cdict)
    for i in range(ilen):
        cdict[tmax]=0;
        tmax=max(cdict,key=cdict.get)
        if bmax-tmax>=5: break
    outdict['txt']=[tmax,round(cdict[tmax]/total,2)]
    return outdict
    
    
from collections import Counter  
def remove_noise(data):
    n=data.shape[0]; depth=10; th=130; tc=int(th/2); catch=0
    for s in range(n):
        e=s+depth; 
        if e>n:e=s+(n-s)
        row=data[s:e]; #print(s,e)
        bg_dict=bg_stats(row); #print(bg_dict)
        bg_val=bg_dict['bg'][0]
        if bg_val<th:
          row[row<th]=tc; #print(bg_dict)
          catch=s+depth
    if catch!=0:
        for s in range(catch):
            row=data[s]
            bg_dict=bg_stats(row); 
            bg_val=bg_dict['bg'][0];
            if bg_val==tc:
                rowx=row.tolist()
                temp_row=[]; lenx=len(rowx)
                for c in range(lenx):
                    col=rowx[c]; ce=c+5
                    if col>=th: 
                        if ce<lenx and len(Counter(rowx[c:ce]))>1:col=0
                    else: col=255
                    temp_row.append(col)
                data[s]=np.array(temp_row)         
    data[data>th]=255
    data[data<th-10]=0            
    return data
    
#------------------image pre processing - lines------------------------------------------------#            
    
def remove_hlines(img):
    #img=img.convert('L')
    data = np.array(img)
    row_count=data.shape[0]
    col_count=data.shape[1]
    limit=5
    for row in range(row_count):
        if row>2:
            cur_row=data[row]
            black_len=len(cur_row[cur_row<20])
            black_line=black_len/col_count
            if black_line>0.3:
                for i in range(-limit,limit):
                    data[row+i]=np.repeat([255],col_count)
    rimg = PilImage.fromarray(data)
    return rimg
    
    
def remove_vlines(img):
    #img=img.convert('L')
    data = np.array(img)
    data=data.transpose()
    row_count=data.shape[0]
    col_count=data.shape[1]
    limit=10
    for row in range(row_count):
        if row>2:
            cur_row=data[row]
            black_len=len(cur_row[cur_row<20])
            black_line=black_len/col_count
            if black_line>0.3:
                for i in range(-limit,limit):
                    data[row+i]=np.repeat([255],col_count)
    data=data.transpose()
    rimg = PilImage.fromarray(data)
    return rimg
    
def remove_lines(img):
    img=remove_vlines(img)
    img=remove_hlines(img)
    return img

#------------------image pre processing - enhance------------------------------------------------#            
    
def img_resize(img, ratio):
    x,y=img.size
    w=int(x*ratio)
    h=int(y*ratio)
    img=img.resize((w,h), PilImage.ANTIALIAS)
    return img
    
    
def enhance(data):
    #data=data.transpose()
    th=20; bth=0.01; rowlen=len(data); collen=len(data[0])
    data[data<th]=0; data[data>=th]=255
    for r in range(rowlen):
        blackratio=len(data[r][data[r]<th])/len(data[r])
        if blackratio>bth:
            for c in range(collen):
                if r+2>=rowlen: break
                if c+2>=collen: break
                if data[r][c]>th:
                    iscore=0
                    for ir in range(r-1,r+2):
                        for ic in range(c-1,c+2):
                            if ir==0 and ic==0: continue
                            if data[ir,ic]<th: iscore=iscore+1
                    if iscore>4: data[r][c]=0
    #data=data.transpose()
    return data

    
def enhancer(data):
    white_range=230; threshold=0.99; r=0
    row_count=data.shape[0]; row_start=0; row_end=0; #print(row_count, row_start)
    while row_end < row_count:
        print(r); r=r+1
        region=find_blocks(data,row_end,white_range,threshold); #print(region)
        if region is None: break
        row_start=region[0]; row_end=region[1]
        buffer=int((row_end-row_start)*0.2); 
        data[row_start-buffer:row_end+buffer] = enhance(data[row_start-buffer:row_end+buffer])
    return data

    
def image_to_data(img_path):
    img = PilImage.open(img_path); img = img.convert('L')
    data = np.array(img)
    return data
    
def data_to_image(data):
    img = PilImage.fromarray(data)
    return img

def set_contrast(im):
    bval=0; lastblen=0; last_rate=1; ch_rate=1
    s=im.shape; t=s[0]*s[1]
    while True:
        if bval>220: break
        im[im<=bval]=0
        blen=0
        for row in im: blen=blen+len(row[row==0])
        if blen==0: bval=bval+10; continue
        b_rate=blen/t
        if bval>0:
            ch_rate=round((blen-lastblen)/(blen),2); #print('set_contrast-->', bval, ch_rate, blen, b_rate)
        if b_rate>0.02 and ch_rate>last_rate: 
            im[im>bval]=255; #cv2.imwrite('test/'+str(bval)+'_'+str(ch_rate)+'.jpg', im)
            break
        last_rate=ch_rate
        bval=bval+10
        lastblen=blen
    return im
    
def pre_process(img_path):
     #print(img_path)
     for i in range(1): 
        img = PilImage.open(img_path)
        img = img.convert('L')
        data = image_to_data(img_path)
        data = set_contrast(data)
        img = data_to_image(data)
        #data = enhancer(data)
#        data = remove_noise(data)
#        img = data_to_image(data)
        #img.save(img_path[:-4]+'1.jpg')
        img.save(img_path)
    

#------------------split image and creating row snippets------------------------------------------------#
            
def get_white_ratio(data,row,white_range):
    white=data[row]; white_ratio=0
    if len(white)>0:
        white_line=len(white[white>white_range])
        white_ratio=white_line/len(white); #print(white_ratio)
    return white_ratio

    
def find_blocks(data,last_row_end,white_range,threshold):
    row_count=data.shape[0]; row_start='s'; row_end='e';
    for row in range(last_row_end,row_count):
        if get_white_ratio(data,row,white_range) <= threshold : row_start=row; break
    if row_start=='s': return None
    for row in range(row_start,row_count):
        if get_white_ratio(data,row,white_range) > threshold: row_end=row; break
    if row_end=='e': row_end=row_count
    row_cordinates = [row_start, row_end]; #print(str(row_cordinates))
    return row_cordinates

    
def split_image(data,trans,white_range,threshold):
    row_count=data.shape[0]; row_start=0; row_end=0; row_array=[]
    while row_end < row_count:
        region=find_blocks(data,row_end,white_range,threshold)
        if region is None: break
        row_start=region[0]; row_end=region[1]
        buffer=int((row_end-row_start)*0.2); 
        part_row=data[row_start-buffer:row_end+buffer]        
        converted=[p for p in part_row]
        if len(converted)>0:
            converted=np.array(converted)
            if trans==1: converted=converted.transpose()
            row_array.append(converted)
    return row_array

    
def split_to_rows(inputfolder):
    i=0; sfolder=inputfolder+'/'+'snippets'
    for f in os.listdir(inputfolder+'/temp'):
        if f.lower().endswith('.jpg'):
            img_path=inputfolder+'/temp/'+f
            data=image_to_data(img_path)
            trans=0
            white_range=230
            threshold=0.99
            row_array=split_image(data,trans,white_range,threshold); #print(len(row_array)); return
            for rows in row_array:
                #if len(rows)<20 or len(rows)>60: continue
                data_to_image(rows).save(sfolder+'/'+str(i)+'.jpg')
                pre_process(sfolder+'/'+str(i)+'.jpg')
                i=i+1
                