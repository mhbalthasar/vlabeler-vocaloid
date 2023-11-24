#!/bin/env python3

import os
import sys
import wave
import traceback


CHN_STA=["a","o","7","aI","ei","@`","AU","@U","a_n","@_n","AN","@N","i\\","i`","i","ia","iE_r","iAU","i@U","iE_n","i_n","iAN","iN","iUN","u","ua","uo","uaI","uei","ua_n","u@_n","uAN","UN","u@N","y","yE_r","y{_n","y_n"]
JPN_STA=["a","i","M","e","o"]
ENG_STA=["I","e","{","Q","V","U","@","i:","u:","O:","@r","eI","aI","OI","@U","aU","I@","e@","U@","O@","Q@","@l","e@0"]
EXT_STA=[]

PIN_LENGTH=-1

DefObj=[100,200,300,400,500]  #default Value define in labeler.json, sign the data is None

def isDefaultObj(obj):
    if len(obj)!=5:
        return False
    if (float(obj[0])==float(DefObj[0]) and 
        float(obj[1])==float(DefObj[1]) and 
        float(obj[2])==float(DefObj[2]) and 
        float(obj[3])==float(DefObj[3]) and 
        float(obj[4])==float(DefObj[4])) :
        return True
    return False

def read_file(file_path):
    ret=[]
    with open(file_path,"rt") as f:
        for l in f.readlines():
            while(l.endswith("\n") or l.endswith("\r")):
                l=l[:-1]
            l=l.strip()
            if(len(l)>0):
                ret.append(l)
    return ret

def get_trans(wav_dir):
    ret = []
    for f in os.listdir(wav_dir):
        if f.endswith(".trans"):
            ret.append(f)
    return ret

def compare_array(ar1,ar2):
    c1=" ".join(ar1)
    c2=" ".join(ar2)
    return c1==c2

def check_is_zero(arr):
    for i in arr:
        if(i!=0):
            return False
    return True


def pinVLabel(sgo,obj):
    if sgo==None:
        return obj
    lastED=float(sgo["ed"])
    if lastED<=0:
        return obj
    ph1=float(obj["ph1"])
    if ph1-lastED<=PIN_LENGTH:
        obj["ph1"]=sgo["ed"]
    return obj

def readVLabel(sgi,trans_file,is_innerFunc=False):
    sFile,_=os.path.splitext(trans_file)
    rFile="{}.vlab{}".format(sFile,sgi)
    vData=[]
    if(not os.path.exists(rFile)):
        return None
    with open(rFile,"rt") as f:
        vData=f.readline().split('|')
    if len(vData)<6:
        return None
    if isDefaultObj(vData[1:]) : return None
    obj={
        "wav_file":vData[0],
        "cutBegin":vData[1],
        "ph1":vData[2],
        "ph2":vData[3],
        "ed":vData[4],
        "cutEnd":vData[5]
    }
    if PIN_LENGTH>=0 and sgi>0 and not is_innerFunc:
        sgo=readVLabel(sgi-1,trans_file,is_innerFunc=True)
        obj=pinVLabel(sgo,obj)
    return obj
        
def get_wav_len(wav_file):
    wave_file = wave.open(wav_file,'rb')
    wav_len = float(wave_file.getnframes()) / float(wave_file.getframerate())
    wave_file.close()
    return wav_len * 1000 # to ms

def trans_to_seg_sta(trans_file,wav_dir):
    tf=read_file(trans_file)
    base_file,_=os.path.splitext(trans_file)
    wav_file=base_file+".wav"
    seg_file=base_file+".seg"
    retD=tf[0].split(" ")
    retT=[]
    for k in retD:
        retT.append(0)
    vLab=readVLabel(0,trans_file)
    if(vLab==None):return None

    cId=0
    if retD[0]=="Sil":
        retT[cId]=0
        cId=cId+1
    retT[cId]=float(vLab["ph1"])
    cId=cId+1
    if(len(retT)==3):
        retT[cId]=float(vLab["ed"])

    try:
        retT.append(get_wav_len(wav_file))
        build_seg(retD,retT,seg_file,True)
    except:
        traceback.print_exc()
    
def trans_to_seg(trans_file,wav_dir):
    tf=read_file(trans_file)
    base_file,_=os.path.splitext(trans_file)
    wav_file=base_file+".wav"
    seg_file=base_file+".seg"
    retD=tf[0].split(" ")
    if len(retD)<=3:
        ccf=[]
        for i in retD:
            if i!="Sil":ccf.append(i)
        if len(ccf)==1 and sign_sta(ccf[0]):
            return trans_to_seg_sta(trans_file,wav_dir)
    retT=[]
    for k in retD:
        retT.append(0)

    for sg in range(1,len(tf)):
        sgi=sg-1
        sgl=tf[sg]
        if sgl.startswith("["):
            if sgl.endswith("]"):
                sgs=0
            else:
                sgs=int(sgl[sgl.index("]")+1:])-1
            sgc=sgl[1:sgl.index("]")].split(" ")
            fnd=-1
            for i in range(0,len(retD)):
                if compare_array(sgc,retD[i:i+len(sgc)]):
                    sgs=sgs-1
                if sgs<0:
                    fnd=i
                    break
            if(fnd>-1):
                vLab=readVLabel(sgi,trans_file)
                if vLab!=None:
                    retT[fnd+1]=float(vLab["ph2"])
                    if retT[fnd]==0:
                        retT[fnd]=float(vLab["ph1"])
                    if fnd+2<len(retT) and retT[fnd+2]==0:
                        retT[fnd+2]=float(vLab["ed"])

    if not check_is_zero(retT):
        #HAVE VALUE
        try:
            retT.append(get_wav_len(wav_file))
            build_seg(retD,retT,seg_file)
        except:
            traceback.print_exc()

def sign_sta(fh):
    if fh in CHN_STA+ENG_STA+JPN_STA:
        return True
    else:
        return False

def sortItr(phi,time):
    n=len(phi)
    for i in range(n):
        for j in range(n-i-1):
            if time[phi[j]] > time[phi[j+1]]:
                time[phi[j]],time[phi[j+1]] = time[phi[j+1]],time[phi[j]]
    return time

def build_seg(sign,time,seg_file,is_sta=False):
    #Sort Seg
    phn_index={}
    for phn in sign:
        if phn in phn_index.keys():
            continue
        ind=[]
        for i in range(0,len(sign)):
            if sign[i]==phn:
                if time[i]!=0:
                    ind.append(i)
        phn_index[phn]=ind
    for phk in phn_index.keys():
        phi=phn_index[phk]
        time=sortItr(phi,time)

    lines=[]
    lastValue=0
    for index in range(0,len(sign)):
        if index==0 and time[index]>0:
            if sign[index]=="Sil":
                time[index]=0
            else:
                lines.append("Sil\t{:.6f}\t{:.6f}\n".format(0,time[index]/1000.0))
                lastValue=time[index]
        if time[index]!=lastValue:
            time[index]=lastValue
        if time[index+1]<time[index]:
            if index+2==len(time):
                time[index]=time[index+1]
            else:
                time[index+1]=time[index]
        lastValue=time[index+1]
        lines.append("{}\t\t{:.6f}\t\t{:.6f}\n".format(sign[index],
                                                 time[index]/1000.0,
                                                 time[index+1]/1000.0
                                                 ))
    lines.insert(0,"nPhonemes {}\n".format(len(lines)))
    lines.insert(1,"articulationsAreStationaries = {}\n".format("1" if is_sta else "0"))
    lines.insert(2,"phoneme\t\tBeginTime\t\tEndTime\n")
    lines.insert(3,"===================================================\n")
    with open(seg_file,"wt") as f:
        print("building seg file:",seg_file)
        f.writelines(lines)

def read_and_build_seg(wav_dir):
    trans_files=get_trans(wav_dir)
    for tr in trans_files:
        trans_to_seg(os.path.join(wav_dir,tr),wav_dir)    

def main(args):
    global PIN_LENGTH
    if len(args)==0:
        print("build_seg.py [wav_folder]")
        print("Enhanced settings:")
        print("\tcommand:\tbuild_seg.py [wav_folder] [pin_length]")
        print("\tintroduce:\tpin_length\tdefault:",PIN_LENGTH,", pin_length is a value in milliseconds. When the distance between two rows between the previous marker's ed and the current marker's ph1 is less than this value, ph1 is adjusted to merge into one row at ed's position. Similarly, when two marker regions overlap, the same operation is done to avoid pronunciation faults. This feature is turned off if pin_length is negative.")
        return
    if(len(args)>1):
        PIN_LENGTH=int(args[1])
    print("PIN_LENGTH:",PIN_LENGTH)
    read_and_build_seg(os.path.abspath(args[0]))

if __name__=="__main__":
    main(sys.argv[1:])