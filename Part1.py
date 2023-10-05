

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:18:01 2022

@author: BarL
"""
import tkinter as tk
from tkinter import Tk , Button
#import tkinter.messagebox as box
#from tkinter import *
import tkinter.messagebox
from tkinter import filedialog as fd
#from tkinter import ttk
import os,sys
import tkinter.font as font
import subprocess
from tkinter import messagebox


FilesDict={}
msg_txt = "press submit to start analysis"
msg_txt_init = "press submit to start analysis"
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))

def browse_R1():
    # Allow user to select a directory and store it in global var
    # called folder_path
    if "R1" in FilesDict:
        FilesDict.pop("R1")
    R1 = browseFile()
    r1_button['text'] = R1
    FilesDict['R1'] = R1 
    #messages_text.insert('end', "R1 name files does not match R2 name files, please insert a correct fastq folders\n")
       

def browse_refGenome():
    filename = browseFile()
    refGenomeFile['text'] = filename
    FilesDict['REF_GENOME'] = filename 
    
def browse_AlleleFile():
    filename = browseFile()
    AlleleFile['text'] = filename
    FilesDict['ALLELE_FILE'] = filename 
    
def ClearAll():
    FilesDict = {}
    AlleleFile['text'] = "---"
    refGenomeFile['text'] = "---"
    r1_button['text'] = "---"
    name_entry.set("")
    
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



def validate():
    
    msg_txt ="starting analysis"
    msg_label['text'] = msg_txt
    if len(name_entry.get().strip(" ")) < 1:
        msg_label['text'] = msg_txt_init
        messagebox.showwarning("missing data", "No run name was inserted. Please insert a valid run name and re-press Submit\n")

    elif "R1" not in FilesDict:
        msg_label['text'] = msg_txt_init
        root.update()
        messagebox.showwarning("missing data", "No R1/R2 file was inserted. Please insert a valid R1/R2 fastq file and re-press Submit\n")
    elif "REF_GENOME" not in FilesDict:
        msg_label['text'] = msg_txt_init
        root.update()
        messagebox.showwarning("missing data", "No ref genome was inserted. Please insert a valid ref genome file and re-press Submit\n")
    else:

        root.update()
        
        if "ALLELE_FILE" in FilesDict:
            ALLELE_FILE = False if len(FilesDict['ALLELE_FILE']) == 0 else FilesDict['ALLELE_FILE']
        else:
            ALLELE_FILE = False
        
        REF_GENOME = FilesDict['REF_GENOME']
        samplePath = FilesDict['R1']
        OUTPUT = name_entry.get()
        #messagebox.showinfo("continue?", "Press OK to start analysis")
        bashScript = current_dir+"/clean_n_aligned_per_allele_v2.sh"
        cmd = f"bash {bashScript} {samplePath} {REF_GENOME} {OUTPUT} {ALLELE_FILE}"

        try:
            subprocess.check_output(cmd, shell = True, stderr=subprocess.STDOUT)
        except:
            msg_txt ="couldn't finish analysis"
            msg_label['text'] = msg_txt
            #messagebox.showerror("Error", "Coudn't finish analysis")
            #print(cmd)
        else:
            #messagebox.showinfo("done", "Analysis finished")
            msg_txt ="analysis finished\npress submit to start another analysis"
            msg_label['text'] = msg_txt
            AlleleFile['text'] = "---"
            refGenomeFile['text'] = "---"
            r1_button['text'] = "---"
            name_text.set("")
            



    
root = Tk()
root.title("VARIANT ANALYSYS")
root.geometry("800x500")
root.configure(bg='white')
root.resizable(False,False)
root.tk.call('tk', 'scaling', 1.0)
myFont = font.Font(family='Arial', size = 14)    



r1_label = tk.Label(text="Upload R1 or R2 fastq file" ,
                      borderwidth=2,relief="raised",
                      width=30, height = 1, anchor = "w", background = "white")
r1_label.place(x=10,y=10)
r1_label['font'] = myFont
r1_button  = Button(root, text="---" ,width=45, anchor="e", command=browse_R1,background = "white")#.place(x=10,y=10)
r1_button['font'] = myFont
r1_button.place(x=325, y=10)


label3 = tk.Label(text="Upload ref genome file",
                      borderwidth=2,relief="raised",
                      width=30, height = 1, anchor = "w", background = "white")
label3['font'] = myFont
label3.place(x=10, y=50)
refGenomeFile = Button(root, text="---",width=45, anchor="e" , command=browse_refGenome,background = "white")
refGenomeFile['font'] = myFont
refGenomeFile.place(x=325,y=50)




name_text = tk.StringVar()
RunName = tk.Label(root, text="Insert run name",
                      borderwidth=2,relief="raised",
                      width=30, height = 1, anchor = "nw", background = "white")
RunName['font'] = myFont
RunName.place(x=10,y=90)
name_entry = tk.Entry(root, textvar=name_text,    width=47,background = "white")
name_entry['font'] = myFont

name_entry.place(x=325,y=90)



label4 = tk.Label(text="Upload allele txt file",
                      borderwidth=2,relief="raised",
                      width=30, height = 1, anchor = "w", background = "white")
label4['font'] = myFont
label4.place(x=10,y=135)


AlleleFile = Button(root, text="---",width=45, anchor="e" , command=browse_AlleleFile,background = "white")
AlleleFile['font'] = myFont
AlleleFile.place(x=325,y=130)



msg_label = tk.Label(root, text=msg_txt,background = "white", anchor = "w")
msg_label['font'] = font.Font(family='Arial',size = 12,weight = "bold") 
msg_label.place(x = 500, y = 240)
Submit_Button = Button(root, text='SUBMIT',width=20,height = 2, command=validate, fg="white", bg='blue')
Submit_Button['font'] = font.Font(family='Arial',size = 13,weight = "bold") 
Submit_Button.place(x=500,y=300)

from PIL import ImageTk, Image
Logo = current_dir+"/RAHAN_LOGO.png"
img=Image.open(Logo)
img=img.resize((int(img.size[0]/2), int(img.size[1]/2)))
#img.save("ArtWrk.ppm", "ppm")

image=ImageTk.PhotoImage(img)

label = tk.Label(root, image = image)
label.place(x = 10, y = 275)
    
root.mainloop()

#log_fh.close()
