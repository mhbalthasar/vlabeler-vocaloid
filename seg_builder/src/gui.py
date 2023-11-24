import tkinter
from tkinter import *
import tkinter.filedialog
import sys
import os
import traceback
import tkinter.messagebox as msgbox

from build_as import main as as_main
from build_seg import main as seg_main
from build_vlab import main as vlab_main

wavText=None

def event_vlab_to_as():
    val=wavText.get()
    as_main([val])
    msgbox.showinfo(title="Done",message="execute vlab to as transform done!")
    pass

def event_vlab_to_seg():
    val=wavText.get()
    seg_main([val])
    msgbox.showinfo(title="Done",message="execute vlab to seg transform done!")
    pass

def event_vlab_to_all():
    val=wavText.get()
    try:
        seg_main([val])
    except:
        traceback.print_exc()
    as_main([val])
    msgbox.showinfo(title="Done",message="execute vlab to seg/as transform done!")
    pass

def event_as_to_vlab():
    val=wavText.get()
    vlab_main([val])
    msgbox.showinfo(title="Done",message="execute as to vlab transform done!")
    pass

def event_find_folder():
    val=tkinter.filedialog.askdirectory(mustexist=True)
    ret=None
    if os.path.exists(val):
        ret=val
        wav=False
        for f in os.listdir(ret):
            if f.endswith(".trans"):
                wav=True
        if not wav:
            subF=os.path.join(ret,"wav")
            if os.path.exists(subF):
                for f in os.listdir(subF):
                    if f.endswith(".trans"):
                        ret=subF
                        break
    if not ret==None:
        wavText.set(ret)

def main():
    global wavText

    root = Tk()
    root.geometry("450x180")
    root.title("vLabeler Vocaloid Transformer")
    wavText=StringVar(root)

#----BtnGrp
    btn_grp= Frame(root)
    btn_grp.grid(row=1,column=0)

    lab1 = Label(btn_grp,text="Compile",padx=50,height=2)
    lab1.grid(row=2,column=0)
    btn1 = Button(btn_grp,text="From vLab to As",padx=50,command=event_vlab_to_as)
    btn1.grid(row=3,column=0,sticky=W+E)
    btn2 = Button(btn_grp,text="From vLab to Seg",padx=50,command=event_vlab_to_seg)
    btn2.grid(row=4,column=0,sticky=W+E)
    btn3 = Button(btn_grp,text="From vLab to As/Seg",padx=50,command=event_vlab_to_all)
    btn3.grid(row=5,column=0,sticky=W+E)

    lab2 = Label(btn_grp,text="Deompile",padx=50,height=2)
    lab2.grid(row=2,column=1)
    btn4 = Button(btn_grp,text="From As to vLab",padx=50,command=event_as_to_vlab)
    btn4.grid(row=3,column=1,sticky=W+N+S,rowspan=3)

#---CfgGrp
    f_grp = Frame(root)
    f_grp.grid(row=0,column=0)

    lab3 = Label(f_grp,text="Wav Folder:",height=2)
    lab3.grid(row=0,column=0)
    txt1 = Entry(f_grp,width=44,textvariable=wavText)
    txt1.grid(row=0,column=1,sticky=W+N+S)
    btn5 = Button(f_grp,text="  ...  ",command=event_find_folder)
    btn5.grid(row=0,column=2,sticky=W+N+S)

    root.mainloop()
    

if __name__=="__main__":
    main()