#!/bin/env python3

import os
import sys
import wave

CHN_STA=["a","o","7","aI","ei","@`","AU","@U","a_n","@_n","AN","@N","i\\","i`","i","ia","iE_r","iAU","i@U","iE_n","i_n","iAN","iN","iUN","u","ua","uo","uaI","uei","ua_n","u@_n","uAN","UN","u@N","y","yE_r","y{_n","y_n"]
JPN_STA=["a","i","M","e","o"]
ENG_STA=["I","e","{","Q","V","U","@","i:","u:","O:","@r","eI","aI","OI","@U","aU","I@","e@","U@","O@","Q@","@l","e@0"]
EXT_STA=[]

PIN_LENGTH=20

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
            if l.endswith("\n"):
                ret.append(l[:-1])
            else:
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
    #zuan_zuan_zuan.wav|100.0|200.0|300.0|400.0|500.0
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

def trans_to_as(trans_file,wav_dir):
    tf=read_file(trans_file)[1:]
    base_file,_=os.path.splitext(trans_file)
    wav_file=base_file+".wav"
    for vindex in range(0,len(tf)):
        vlab=readVLabel(vindex,trans_file)
        if(vlab==None):continue
        sgl=tf[vindex]
        if not sgl.startswith("["):
            continue
        sgl=sgl[1:sgl.index("]")].split(" ")
        as_file=base_file+".as{}".format(vindex)
        build_as(vlab,sgl,as_file,wav_file)


def get_cutdown(vlab,wav_file):
    wave_file = wave.open(wav_file,'rb')
    wav_channel=wave_file.getnchannels()
    wav_samplewith=wave_file.getsampwidth()
    wav_framerate=wave_file.getframerate()
    wav_framecount=wave_file.getnframes()
    wav_len = float(wave_file.getnframes()) / float(wave_file.getframerate())
    wave_file.close()    
    samples1= float(vlab["cutBegin"])/1000.0  *  float(wave_file.getframerate())
    samples2 = float(vlab["cutEnd"])/1000.0  *  float(wave_file.getframerate())
    return (samples1,samples2-samples1)

def build_as_sta(vlab,phn_sign,as_file,wav_file):
    cdown=get_cutdown(vlab,wav_file)
    lines=[]
    lines.append("nphone art segmentation\n")
    lines.append("{\n")
    lines.append("\tphns: [\"{}\"];\n".format("\",\"".join(phn_sign)))
    lines.append("\tcut offset: {};\n".format(int(cdown[0])))
    lines.append("\tcut length: {};\n".format(int(cdown[1])))
    lines.append("\tboundaries: [{:.9f},{:.9f}];\n".format(
        (float(vlab["ph1"])-float(vlab["cutBegin"]))/1000.0,
        (float(vlab["ed"])-float(vlab["cutBegin"]))/1000.0
        )) #BOUND 2 to end
    lines.append("\trevised: false;\n")
    lines.append("\tvoiced: [true];\n")
    lines.append("};\n")
    with open(as_file,"wt") as f:
        print("building as file:",as_file)
        f.writelines(lines)

def build_as(vlab,phn_sign,as_file,wav_file):
    if(len(phn_sign)==1 and phn_sign[0] in CHN_STA+JPN_STA+ENG_STA):
        return build_as_sta(vlab,phn_sign,as_file,wav_file)
    cdown=get_cutdown(vlab,wav_file)
    voiced=[]
    for k in phn_sign:
        if k in ["Sil"]:
            voiced.append("false")
        else:
            voiced.append("true")
    lines=[]
    lines.append("nphone art segmentation\n")
    lines.append("{\n")
    lines.append("\tphns: [\"{}\"];\n".format("\",\"".join(phn_sign)))
    lines.append("\tcut offset: {};\n".format(int(cdown[0])))
    lines.append("\tcut length: {};\n".format(int(cdown[1])))
    lines.append("\tboundaries: [{:.9f},{:.9f},{:.9f}];\n".format(
        (float(vlab["ph1"])-float(vlab["cutBegin"]))/1000.0,
        (float(vlab["ph2"])-float(vlab["cutBegin"]))/1000.0,
        (float(vlab["ed"])-float(vlab["cutBegin"]))/1000.0
        ))
    lines.append("\trevised: false;\n")
    lines.append("\tvoiced: [{}];\n".format(",".join(voiced)))
    lines.append("};\n")
    with open(as_file,"wt") as f:
        print("building as file:",as_file)
        f.writelines(lines)

def read_and_build_as(wav_dir):
    trans_files=get_trans(wav_dir)
    for tr in trans_files:
        trans_to_as(os.path.join(wav_dir,tr),wav_dir)    

def main(args):
    global PIN_LENGTH
    if len(args)==0:
        print("build_as.py [wav_folder]")
        print("Enhanced settings:")
        print("\tcommand:\tbuild_as.py [wav_folder] [pin_length]")
        print("\tintroduce:\tpin_length\tdefault:",PIN_LENGTH,", pin_length is a value in milliseconds. When the distance between two rows between the previous marker's ed and the current marker's ph1 is less than this value, ph1 is adjusted to merge into one row at ed's position. Similarly, when two marker regions overlap, the same operation is done to avoid pronunciation faults. This feature is turned off if pin_length is negative.")
        return
    if(len(args)>1):
        PIN_LENGTH=int(args[1])
    print("PIN_LENGTH:",PIN_LENGTH)
    read_and_build_as(os.path.abspath(args[0]))

if __name__=="__main__":
    main(sys.argv[1:])