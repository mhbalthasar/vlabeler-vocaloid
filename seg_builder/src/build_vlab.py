#!/bin/env python3

import os
import sys
import wave

CHN_STA=["a","o","7","aI","ei","@`","AU","@U","a_n","@_n","AN","@N","i\\","i`","i","ia","iE_r","iAU","i@U","iE_n","i_n","iAN","iN","iUN","u","ua","uo","uaI","uei","ua_n","u@_n","uAN","UN","u@N","y","yE_r","y{_n","y_n"]
JPN_STA=["a","i","M","e","o"]
ENG_STA=["I","e","{","Q","V","U","@","i:","u:","O:","@r","eI","aI","OI","@U","aU","I@","e@","U@","O@","Q@","@l","e@0"]
EXT_STA=[]

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

def wav_cutdown(wav_file,downf):
    wave_file = wave.open(wav_file,'rb')
    wav_channel=wave_file.getnchannels()
    wav_samplewith=wave_file.getsampwidth()
    wav_framerate=wave_file.getframerate()
    wav_framecount=wave_file.getnframes()
    wav_len = float(wave_file.getnframes()) / float(wave_file.getframerate())
    wave_file.close()    
    return float(downf) / float(wave_file.getframerate())

def readAS(sgi,trans_file):
    sFile,_=os.path.splitext(trans_file)
    rFile="{}.as{}".format(sFile,sgi)
    wavFile="{}.wav".format(sFile)
    _,wavName=os.path.split(wavFile)
    if(not os.path.exists(rFile)):
        return None
    if(not os.path.exists(wavFile)):
        return None
    vLines=[]
    with open(rFile,"rt") as f:
        for l in f.readlines():
            vLines.append(l[:-1].strip())
    if(vLines[1]!="{"):return None
    cdown=[-1,-1]
    vbound=[]
    for i in range(1,len(vLines)):
        cl = vLines[i].split(":")
        if(len(cl)!=2):continue
        chead=cl[0].strip()
        cvalue=cl[1].strip()
        if cvalue.endswith("\n"):cvalue=cvalue[:-1]
        if cvalue.endswith(";"):cvalue=cvalue[:-1]
        if(chead=="cut offset"):
            cdown[0]=wav_cutdown(wavFile,int(cvalue))
        elif (chead=="cut length"):
            cdown[1]=wav_cutdown(wavFile,int(cvalue))
        elif (chead=="boundaries"):
            if cvalue.startswith("["): cvalue=cvalue[1:]
            if cvalue.endswith("]"): cvalue=cvalue[:-1]
            for vb in cvalue.split(','):
                vbound.append(float(vb.strip()))
    vData=[]
    try:
        if(len(vbound)==2):
            vbound.insert(1,(vbound[0]+vbound[1])/2)
        cdown[1]=(cdown[1]+cdown[0])*1000.0
        vbound[0]=(vbound[0]+cdown[0])*1000.0
        vbound[1]=(vbound[1]+cdown[0])*1000.0
        vbound[2]=(vbound[2]+cdown[0])*1000.0
        cdown[0]=cdown[0]*1000.0
        vData=[wavName]+[cdown[0]]+vbound[0:3]+[cdown[1]]
    except:
        return None
    if(len(vData)<6):return None
    obj={
        "wav_file":vData[0],
        "cutBegin":vData[1],
        "ph1":vData[2],
        "ph2":vData[3],
        "ed":vData[4],
        "cutEnd":vData[5]
    }
    return obj

        
def trans_to_vlab(trans_file,wav_dir):
    tf=read_file(trans_file)[1:]
    base_file,_=os.path.splitext(trans_file)
    wav_file=base_file+".wav"
    for vindex in range(0,len(tf)):
        vlab=readAS(vindex,trans_file)
        if(vlab==None):continue
        vlab_file="{}.vlab{}".format(base_file,vindex)
        content="{}|{:.6f}|{:.6f}|{:.6f}|{:.6f}|{:.6f}".format(
            vlab["wav_file"],vlab["cutBegin"],
            vlab["ph1"],vlab["ph2"],vlab["ed"],
            vlab["cutEnd"]
        )
        with open(vlab_file,"wt") as f:
            print("building vlab file:",vlab_file)
            f.write(content)


def read_and_build_vlab(wav_dir):
    trans_files=get_trans(wav_dir)
    for tr in trans_files:
        trans_to_vlab(os.path.join(wav_dir,tr),wav_dir)    

def main(args):
    if len(args)==0:
        print("This tool is use for transfrom .as* back to vlab* for edit the labels in vlabeler")
        print("build_vlab.py [wav_folder]")
        
        return
    read_and_build_vlab(os.path.abspath(args[0]))

if __name__=="__main__":
    main(sys.argv[1:])