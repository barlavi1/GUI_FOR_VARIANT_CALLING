
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:18:01 2022

@author: BarL
"""
import tkinter as tk
from tkinter import ttk
from tkinter import Tk , Button
#import tkinter.messagebox as box
#from tkinter import *
import tkinter.messagebox
from tkinter import filedialog as fd
#from tkinter import ttk
import os, sys
import tkinter.font as font
import subprocess
from tkinter import messagebox
  


msg_txt = "Press Submit to Start Analysis"
msg_txt_init = "Press Submit to Start Analysis"

def browse_bam():
    if "ctrFile" in FilesDict:
        FilesDict.pop("ctrFile")
    ctrFile = browseFile()
    FilesDict['ctrFile'] = ctrFile  
    CtrBam_btn['text'] = ctrFile
    
def browse_trt():
    if "trtFile" in FilesDict:
        FilesDict.pop("trtFile")
    trtFile = browseFile()
    FilesDict['trtFile'] = trtFile  
    #trtBam_btn['text'] = trtFile
    trtBam_btn['text'] = trtFile

def browse_folder():
    folderpath = fd.askdirectory()
    return folderpath


def browse_refGenome():
    filename = browseFile()
    refGenomeFile['text'] = filename
    FilesDict['REF_GENOME'] = filename 
    
    
def browseFile():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filetypes = (
        ('All Files', '*.*'),
    )
    filepath = fd.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes)
    return filepath

    
root = Tk()
root.title("Statistical Analysis")
root.geometry("800x600")
root.resizable(False,False)
root.configure(bg='white')
root.tk.call('tk', 'scaling', 1.0)
myFont = font.Font(family='Arial')    
global FilesDict
FilesDict = {}
Strand_var = tk.StringVar()
ExpType_var = tk.StringVar()
Allele_var = tk.StringVar()
gstart_text = tk.StringVar()
gend_text = tk.StringVar()
scaffold_text = tk.StringVar()

#current_dir = os.path.dirname(os.path.dirname(sys.argv[0]))
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
def define_treatment(event):
    if ExpType_var.get() == "OT":
        CtrBam_btn["state"] = "disable"
        FilesDict['bamFile'] = False
        CtrBam_btn['text'] = "---"

    else:
        CtrBam_btn["state"] = "active"
        if 'bamFile' in FilesDict:
            del FilesDict['bamFile']
        
def get_warnings_msg(par):

    return f"No {par} was chosen/inserted. Please insert/choose a valid {par} are re-press submit\n"

def validate():
    warnings_msg_type = "missing data"
    if ExpType_var.get()== 'Pick an option':
        msg_label['text'] = msg_txt_init
        messagebox.showwarning(warnings_msg_type,get_warnings_msg("experiment type"))
        #messagebox.showwarning("missing data", "No Experiment Type was submitted. Insert Experiment Type and re-press submit\n")
    elif ExpType_var.get() == "Control and Treatment":
        if 'ctrFile' not in FilesDict:
            msg_label['text'] = msg_txt_init
            #messagebox.showwarning("missing data",  "No Control File. Please insert a Control file and re-press Submit\n")
            messagebox.showwarning(warnings_msg_type,get_warnings_msg("control bam file"))
        if 'trtFile' not in FilesDict:
            msg_label['text'] = msg_txt_init
            #messagebox.showwarning("missing data", "No Treatment File. Please insert a Control file and re-press Submit\n")
            messagebox.showwarning(warnings_msg_type,get_warnings_msg("treatment bam file"))
    elif "trtFile" not in FilesDict:
        msg_label['text'] = msg_txt_init
        #messagebox.showwarning("missing data", "No Treatment File. Please insert a Treatment file and re-press Submit\n")
        messagebox.showwarning(warnings_msg_type,get_warnings_msg("treatment bam file"))
    elif "REF_GENOME" not in FilesDict:
        msg_label['text'] = msg_txt_init
        #messagebox.showwarning("missing data", "No ref genome was inserted. Please insert a valid ref genome file and re-press Submit\n")
        messagebox.showwarning(warnings_msg_type,get_warnings_msg("reference genome file"))
    elif len(gstart_text.get()) == 0:
        msg_label['text'] = msg_txt_init
        #messagebox.showwarning("missing data", "No gene start was inserted. please insert a valid start position")
        messagebox.showwarning(warnings_msg_type,get_warnings_msg("gene start position"))
    elif len(gend_text.get()) == 0:
        msg_label['text'] = msg_txt_init
        #messagebox.showwarning("missing data","No gene end was inserted. please insert a valid end position")
        messagebox.showwarning(warnings_msg_type,get_warnings_msg("gene end position"))
    #elif len(gend_text.get()) == 0:
        #msg_label['text'] = msg_txt_init
        #messagebox.showwarning("missing data","No gene end was inserted. please insert a valid end position")
        #messagebox.showwarning(warnings_msg_type,get_warnings_msg("Experiment type"))
    elif len(gname_text.get()) == 0:
        msg_label['text'] = msg_txt_init
        #messagebox.showwarning("missing data", "No gene name was inserted. please insert a valid gene name")
        messagebox.showwarning(warnings_msg_type,get_warnings_msg("gene name"))

    else:
        msg_txt ="starting analysis"
        msg_label['text'] = msg_txt
        root.update()
        ctrFile = False if'ctrFile' not in FilesDict else FilesDict['ctrFile']
        trtFile = FilesDict['trtFile']
        REF_GENOME = FilesDict['REF_GENOME']
        Strand = Strand_var.get()
        ExpType = ExpType_var.get()
        Rscript = current_dir+"/crispRVariants_banana_v3.3_BAR.R"

        cmd =   f"Rscript {Rscript} {ExpType} {trtFile} {ctrFile} {REF_GENOME} {Allele_var.get()} {gstart_text.get()} {gend_text.get()} {Strand} {gname_text.get()}  {scaffold_text.get()}  "

        try:
            subprocess.check_output(cmd, shell = True, stderr=subprocess.STDOUT)
        except:
            msg_txt ="couldn't finish analysis"
            msg_label['text'] = msg_txt
        else:
            msg_txt ="analysis finished\npress submit to start another analysis"
            msg_label['text'] = msg_txt
            ExpType_btn.set("Pick an option")
            Strand_btn.set("+")
            Strand_var.set("+")
            
            MultiAllele_btn.set("True")
            Allele_var.set('')
            gstart_text.set('')
            gend_text.set('')
            scaffold_text.set('')
            gname_text.set('')
            CtrBam_btn['text'] = "---"
            trtBam_btn['text'] = "---"
            refGenomeFile['text'] = "---"
            
            #root.destroy()
            FilesDict.pop("trtFile")
            #FilesDict['trtFile'] = ""
            #FilesDict['REF_GENOME'] = ""
            FilesDict.pop("REF_GENOME")
            root.update()
            if 'ctrFile' in FilesDict: 
                FilesDict.pop("ctrFile")
            

        

list1 = ["TC", "OT"]
 

ExpType_lbl = tk.Label(text="Choose experiment type" ,width=30,  
                       borderwidth=2,relief="raised",
                       anchor = "w", background = "white")
ExpType_lbl.place(x=10,y=10)
ExpType_lbl['font'] = myFont


ExpType_btn = ttk.Combobox(root, values = list1, width=45 ,textvariable=ExpType_var, background = "white")
ExpType_btn.set("Pick an option")
ExpType_btn['font'] = myFont
ExpType_btn.place(x=325,y=10)
ExpType_btn.bind('<<ComboboxSelected>>', define_treatment)

defultText = ""


FilesDict['ExpType'] = ExpType_var.get()

CtrBam_lbl = tk.Label(text="Upload control bam" ,
                      borderwidth=2,relief="raised",
                      width=30, height = 1, anchor = "w", background = "white")
CtrBam_lbl['font'] = myFont
CtrBam_lbl.place(x=10,y=50)

CtrBam_btn  = Button(root ,width=45, text="---" , anchor = "e", command=browse_bam, background = "white")#.place(x=10,y=10)
CtrBam_btn['font'] = myFont
CtrBam_btn.place(x=325,y=50)


trtBam_lbl = tk.Label(text="Upload treatment bam" ,
                      borderwidth=2,relief="raised",
                      width=30, anchor = "w", background = "white")
trtBam_lbl['font'] = myFont
trtBam_lbl.place(x=10,y=90)

trtBam_btn  = Button(root ,width=45, text="---" , anchor="e", command=browse_trt, background = "white")#.place(x=10,y=10)
trtBam_btn['font'] = myFont
trtBam_btn.place(x=325,y=90)


refGenomeFile = Button(root, text="---",width=45, anchor="e" , command=browse_refGenome, background = "white")
refGenomeFile['font'] = myFont
refGenomeFile.place(x=325,y=130)
label3 = tk.Label(text="Upload ref genome file", width=30,  
                  borderwidth=2,relief="raised",
                  anchor = "w", background = "white")
label3['font'] = myFont
label3.place(x=10,y=130)


StrandList = ["+", "-"]
 

Strand_lbl = tk.Label(text="strand" , anchor = "w",
                      borderwidth=2,relief="raised",
                      width=30,  background = "white")
Strand_lbl['font'] = myFont
Strand_lbl.place(x=10,y=170)


Strand_btn = ttk.Combobox(root, values = StrandList, 
                          width=45,textvariable=Strand_var)
Strand_btn.set("+")
Strand_btn['font'] = myFont
Strand_btn.place(x=325,y=170)

Strand_value = Strand_var.get()
FilesDict['Strand_value'] = ExpType_var.get()


MultiAllele_lbl = tk.Label(text="Multi allele" ,
                           borderwidth=2,relief="raised",
                           width=30,  anchor = "w", background = "white")
MultiAllele_lbl['font'] = myFont
MultiAllele_lbl.place(x=10,y=210)

AlleleList = ["True","False"]
MultiAllele_btn = ttk.Combobox(root, values = AlleleList, width=45,textvariable=Allele_var,background = "white")
MultiAllele_btn.set("True")
MultiAllele_btn['font'] = myFont
MultiAllele_btn.place(x=325,y=210)



gstart_btn = tk.Label(root, text="Insert gstart position",
                      borderwidth=2,relief="raised",
                      width=30, anchor="w",background = "white")
gstart_btn['font'] = myFont
gstart_btn.place(x=10,y=250)
gstart_entry = tk.Entry(root, textvar=gstart_text, width=47,background = "white")
gstart_entry['font'] = myFont

gstart_entry.place(x=325,y=250)




gend_btn = tk.Label(root, text="Insert gend position",
                    borderwidth=2,relief="raised",
                    width=30, anchor="w",background = "white")
gend_btn['font'] = myFont
gend_btn.place(x=10,y=290)
gend_entry = tk.Entry(root, textvar=gend_text, width=47,background = "white")
gend_entry['font'] = myFont

gend_entry.place(x=325,y=290)

gname_text = tk.StringVar()
gnamed_btn = tk.Label(root, text="Insert gname",
                      borderwidth=2,relief="raised",
                      width=30, anchor="w",background = "white")
gnamed_btn['font'] = myFont
gnamed_btn.place(x=10,y=330)
gnamed_entry = tk.Entry(root, textvar=gname_text, width=47,background = "white")
gnamed_entry['font'] = myFont

gnamed_entry.place(x=325,y=330)


scaffold_btn = tk.Label(root, text="Insert allele/chr/scaffold name",
                        borderwidth=2,relief="raised",
                        width=30, anchor="w",
                        background = "white")
scaffold_btn['font'] = myFont
scaffold_btn.place(x=10,y=370)
scaffold_entry = tk.Entry(root, textvar=scaffold_text, width=47,background = "white")
scaffold_entry['font'] = myFont

scaffold_entry.place(x=325,y=370)

#myFont = font.Font(family='Arial')  
msg_label = tk.Label(root, text=msg_txt,background = "white")
msg_label['font'] = font.Font(family='Arial',size = 12,weight = "bold") 
msg_label.place(x = 500, y = 440)


Submit_Button = Button(root, text='SUBMIT',width=20,height = 2, command=validate, fg='white', bg='blue')
Submit_Button['font'] = font.Font(family='Arial',size = 13,weight = "bold", ) 
Submit_Button.place(x=500,y=480)


from PIL import ImageTk, Image
Logo = current_dir+"/RAHAN_LOGO.png"
img=Image.open(Logo)
img=img.resize((int(img.size[0]/2), int(img.size[1]/2)))
#img.save("ArtWrk.ppm", "ppm")

image=ImageTk.PhotoImage(img)

label = tk.Label(root, image = image)
label.place(x = 10, y = 450)

root.mainloop()

#log_fh.close()

