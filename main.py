#Made by Christopher Hatton (558)

# -*-coding: utf-8-*-

from tkinter import *            #for Tk window
import tkinter as tk             #to make Frame
from tkinter import filedialog   #to open and choose documents
from sys import platform         #to make sure that the os is win32
import ctypes                    #to make sure that the screen size is large enough
import time                      #to make better timings
import os                        #to allow help button open help web page
import subprocess                #to run .bat files


name = "Christopher's Text Editor"

def f_main():

    #START:
    root = tk.Tk()
                                                                           
    root.state('zoomed')                                                                                  #Sets default state to zoomed
    root.bind('<F11>', lambda event: root.attributes('-fullscreen',not root.attributes('-fullscreen')))   #Binds F11 to fullscreen
    root.bind('<Escape>', lambda event: root.attributes('-fullscreen', False))                            #Binds Escape to leave fullscreen
    root.bind('<F10>', lambda event: root.state('zoomed'))                                                #Binds F10 to zoomed    
    root.title(name)                                                                                      #Sets the title of the window

    #Make global variables:
    file_location_save = ['']
    file_open = [False] 
    file_open_name = ['']
    file_types_name = 'Text files'
    file_types = 'txt'


    #Textbox class:
    class TextLineNumbers(tk.Canvas):
        def __init__(self, *args, **kwargs):
            tk.Canvas.__init__(self, *args, **kwargs)
            self.textwidget = None

        def attach(self, text_widget):
            self.textwidget = text_widget
            
        def redraw(self, *args):
            '''redraw line numbers'''
            self.delete("all")

            i = self.textwidget.index("@0,0")
            while True :
                dline= self.textwidget.dlineinfo(i)
                if dline is None: break
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.create_text(2,y,anchor="nw", text=linenum)
                i = self.textwidget.index("%s+1line" % i)

    class CustomText(tk.Text):
        def __init__(self, *args, **kwargs):
            tk.Text.__init__(self, *args, **kwargs)

            # create a proxy for the underlying widget
            self._orig = self._w + "_orig"
            self.tk.call("rename", self._w, self._orig)
            self.tk.createcommand(self._w, self._proxy)

        def _proxy(self, *args):
            # let the actual widget perform the requested action
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)

            # generate an event if something was added or deleted,
            # or the cursor position changed
            if (args[0] in ("insert", "replace", "delete") or 
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
            ):
                self.event_generate("<<Change>>", when="tail")

            # return what the actual widget returned
            return result        

    class all_together(tk.Frame):
        def __init__(self, *args, **kwargs):
            tk.Frame.__init__(self, *args, **kwargs)
            self.text = CustomText(self)
            self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
            self.text.configure(yscrollcommand=self.vsb.set)
            self.text.configure(font=('Times 20'))
            self.linenumbers = TextLineNumbers(self, width=30)
            self.linenumbers.attach(self.text)

            self.vsb.pack(side="right", fill="y")
            self.linenumbers.pack(side="left", fill="y")
            self.text.pack(side="right", fill="both", expand=True)

            self.text.bind("<<Change>>", self._on_change)
            self.text.bind("<Configure>", self._on_change)

        def _on_change(self, event):
            self.linenumbers.redraw()

    def f_open_file(): #Open files:
        file_location = ''
        file_location = filedialog.askopenfilename() #Gets the file location (local variable)
        file_location_save[0] = file_location #Puts the file location in it's global variable
        while True:
            try:
                f = open(file_location,'r') #Opens the file
            except FileNotFoundError:
                break
            else:
                contents = f.read() #Reads the file
                f.close() #Closes the file
                textbox.text.delete("1.0","end")
                textbox.text.insert("end-1c",contents) #Puts the contents of the file in the textbox
                x = []
                x = file_location.split('/') #Gets the name of the file(local variable)
                file_open_name[0] = x[-1] #Puts the file name in it's global variable
                file_open[0] = 'True' #File has been opened (useful)
                root.title(file_open_name[0]+' - ' + name) #Puts the name of the file in the window's title
                break

    def f_open_file_key(event): #Open files:
        file_location = ''
        file_location = filedialog.askopenfilename(filetypes=((file_types_name,file_types),)) #Gets the file location (local variable)
        file_location_save[0] = file_location #Puts the file location in it's global variable
        while True:
            try:
                f = open(file_location,'r') #Opens the file
            except FileNotFoundError:
                break
            else:
                contents = f.read() #Reads the file
                f.close() #Closes the file
                textbox.text.delete("1.0","end")
                textbox.text.insert("end-1c",contents) #Puts the contents of the file in the textbox
                x = []
                x = file_location.split('/') #Gets the name of the file(local variable)
                file_open_name[0] = x[-1] #Puts the file name in it's global variable
                file_open[0] = 'True' #File has been opened (useful)
                root.title(file_open_name[0]+' - ' + name) #Puts the name of the file in the window's title
                break

    def f_save_file(): #Save files:
        if file_open[0] == 'True':
            #If one or more file has beened opened:
            x = file_location_save[0]
            f = open(x,'w')
            f.write(textbox.text.get("1.0",'end-1c')) #Saves file to the opened file
            f.close()
        else:
            #If no files been opened:
            file_location = ''
            file_location = filedialog.askopenfilename(filetypes=((file_types_name,file_types),)) #Gets the file to save to (local variable)
            file_location_save[0] = file_location  #Puts the file location in it's global variable
            while True:
                try:
                    f = open(file_location,'w') 
                except FileNotFoundError:
                    break
                else:
                    f.write(textbox.text.get("1.0",'end-1c')) #Saves the file
                    f.close()
                    file_open[0] = True #File has been opened
                    x = []
                    x = file_location.split('/') #Gets the name of the file(local variable)
                    file_open_name[0] = x[-1] #Puts it in a global variable
                    root.title(file_open_name[0]+' - ' + name) #Puts the name of the file in the window's title
                    break

    def f_save_file_key(event): #Save files:
            if file_open[0] == 'True':
                #If one or more file has beened opened:
                x = file_location_save[0]
                f = open(x,'w')
                f.write(textbox.text.get("1.0",'end-1c')) #Saves file to the opened file
                f.close()
            else:
                #If no files been opened:
                file_location = ''
                file_location = filedialog.askopenfilename(filetypes=((file_types_name,file_types),)) #Gets the file to save to (local variable)
                file_location_save[0] = file_location  #Puts the file location in it's global variable
                while True:
                    try:
                        f = open(file_location,'w') 
                    except FileNotFoundError:
                        break
                    else:
                        f.write(textbox.text.get("1.0",'end-1c')) #Saves the file
                        f.close()
                        file_open[0] = True #File has been opened
                        x = []
                        x = file_location.split('/') #Gets the name of the file(local variable)
                        file_open_name[0] = x[-1] #Puts it in a global variable
                        root.title(file_open_name[0]+' - ' + name) #Puts the name of the file in the window's title
                        break

    def f_save_as(): #Save file as:
        file_location = ''
        file_location = filedialog.askopenfilename(filetypes=((file_types_name,file_types),)) #Gets the file to save to (local variable)
        file_location_save[0] = file_location  #Puts the file location in it's gloval variable
        while True:
            try:
                f = open(file_location,'w') 
            except FileNotFoundError:
                break
            else:
                f.write(textbox.text.get("1.0",'end-1c')) #Saves the file
                f.close()
                file_open[0] = True #File has been opened
                x = []
                x = file_location.split('/') #Gets the name of the file(local variable)
                file_open_name[0] = x[-1] #Puts it in a global variable
                root.title(file_open_name[0]+' - ' + name) #Puts the name of the file in the window's title
                break

    def f_save_as_key(event): #Save file as:
        file_location = ''
        file_location = filedialog.askopenfilename(filetypes=((file_types_name,file_types),)) #Gets the file to save to (local variable)
        file_location_save[0] = file_location  #Puts the file location in it's gloval variable
        while True:
            try:
                f = open(file_location,'w') 
            except FileNotFoundError:
                break
            else:
                f.write(textbox.text.get("1.0",'end-1c')) #Saves the file
                f.close()
                file_open[0] = True #File has been opened
                x = []
                x = file_location.split('/') #Gets the name of the file(local variable)
                file_open_name[0] = x[-1] #Puts it in a global variable
                root.title(file_open_name[0]+' - ' + name) #Puts the name of the file in the window's title
                break
    
    def f_replace_text(original_text,replace_text): #Replaces text

        x = textbox.text.get("1.0",'end-1c')
        y = x.replace(original_text, replace_text)
        textbox.text.delete("1.0","end")
        textbox.text.insert("end-1c",y) #Puts the contents of the file in the textbox

    def f_replace(): #Replace text

        def f_submit():
            original_text = original.get() #Gets inputs
            replace_text = replace.get()
            f_replace_text(original_text,replace_text)
            popup.destroy()

        def f_submit_key(event):
            original_text = original.get() #Gets inputs
            replace_text = replace.get()
            f_replace_text(original_text,replace_text)
            popup.destroy()

        popup = Toplevel(root) #Creates a popup
        popup.title('Replace Text - ' + name)
        original_label = Label(popup, text = 'What do you want to replace?')
        replace_label = Label(popup,text = 'What do you want to replace it with?')
        original = Entry(popup)
        replace = Entry(popup)
        submit = Button(popup,text = 'Submit',command = f_submit,bg = 'gray',fg = 'white')
        original_label.grid(row = 0,column = 0)
        replace_label.grid(row = 0,column = 2)
        original.grid(row = 1,column = 0)
        replace.grid(row = 1,column = 2)
        submit.grid(row = 2,column = 1,pady = 3)
        popup.bind('<Return>',f_submit_key)

    def f_replace_key(event): #Replace text

        def f_submit():
            original_text = original.get() #Gets inputs
            replace_text = replace.get()
            f_replace_text(original_text,replace_text)
            time.sleep(0.5)
            popup.destroy()

        def f_submit_key(event):
            original_text = original.get() #Gets inputs
            replace_text = replace.get()
            f_replace_text(original_text,replace_text)
            popup.destroy()

        popup = Toplevel(root) #Creates a popup
        popup.title('Replace Text - ' + name)
        original_label = Label(popup, text = 'What do you want to replace?')
        replace_label = Label(popup,text = 'What do you want to replace it with?')
        original = Entry(popup)
        replace = Entry(popup)
        submit = Button(popup,text = 'Submit',command = f_submit,bg = 'gray',fg = 'white')
        original_label.grid(row = 0,column = 0)
        replace_label.grid(row = 0,column = 2)
        original.grid(row = 1,column = 0)
        replace.grid(row = 1,column = 2)
        submit.grid(row = 2,column = 1,pady = 3)
        popup.bind('<Return>',f_submit_key)

    def f_change_text_style(): #Changes font style of textbox

        def f_submit():
            text_style = text_style_entry.get()     
            textbox.text.configure(font=text_style)
            time.sleep(0.5)
            popup.destroy()

        def f_submit_key(event):
            text_style = text_style_entry.get()     
            textbox.text.configure(font=text_style)
            time.sleep(0.5)
            popup.destroy()

        popup = Toplevel(root) #Creates a popup
        popup.title('Change Text Style - ' + name)
        text_style_label = Label(popup, text = 'Enter text style here:')
        text_style_entry = Entry(popup)
        submit = Button(popup,text = 'Submit',command = f_submit,bg = 'gray',fg = 'white')
        text_style_label.grid(row = 0,column = 0)
        text_style_entry.grid(row = 1,column = 0,padx = 5)
        submit.grid(row = 2,column = 0,pady = 3)
        popup.bind('<Return>',f_submit_key)

    def f_change_text_style_key(event): #Changes font style of textbox

        def f_submit():
            text_style = text_style_entry.get()     
            textbox.text.configure(font=text_style)
            time.sleep(0.5)
            popup.destroy()

        def f_submit_key(event):
            text_style = text_style_entry.get()     
            textbox.text.configure(font=text_style)
            time.sleep(0.5)
            popup.destroy()

        popup = Toplevel(root) #Creates a popup
        popup.title('Change Text Style - ' + name)
        text_style_label = Label(popup, text = 'Enter text style here:')
        text_style_entry = Entry(popup)
        submit = Button(popup,text = 'Submit',command = f_submit,bg = 'gray',fg = 'white')
        text_style_label.grid(row = 0,column = 0)
        text_style_entry.grid(row = 1,column = 0,padx = 5)
        submit.grid(row = 2,column = 0,pady = 3)
        popup.bind('<Return>',f_submit_key)

    def f_run():
        code = textbox.text.get("1.0",'end-1c')
        os.rename('run.py','run.txt')
        f = open('run.txt','w')
        f.write(code)
        f.close()
        os.rename('run.txt','run.py')
        subprocess.call("[F:\Code\Python\Christopher's Python IDE\run.bat")

    #Configure grid:
    Grid.rowconfigure(root,index = 2,weight = 4)
    Grid.columnconfigure(root,index = 0,weight = 1)

    #Make Tk:
    heading = Label(root,text = name,font = 'Helvetica 30 bold')
    textbox = all_together(root)
    frame_buttons = tk.Frame(root)
    open_file = Button(frame_buttons,text = 'Open',command = f_open_file,bg = 'gray',fg = 'white')
    open_file.pack(side=tk.LEFT,padx=(3),pady=(3))
    save_file = Button(frame_buttons,text = 'Save',command=lambda : f_save_file(),bg = 'gray',fg = 'white')
    save_file.pack(side=tk.LEFT,padx=(3),pady=(3))
    save_as = Button(frame_buttons,text = 'Save As',command=lambda : f_save_as(),bg = 'gray',fg = 'white')
    save_as.pack(side=tk.LEFT,padx=(3),pady=(3))
    replace_button = Button(frame_buttons,text = 'Replace Text',command=lambda : f_replace(),bg = 'gray',fg = 'white')
    replace_button.pack(side=tk.LEFT,padx=(3),pady=(3))
    change_text_style = Button(frame_buttons,text = 'Change Text Style',command=lambda : f_change_text_style(),bg = 'gray',fg = 'white')
    change_text_style.pack(side=tk.LEFT,padx=(3),pady=(3))
    run_button = Button(frame_buttons,text = 'Run',command=lambda : f_run(),bg = 'gray',fg = 'white')
    run_button .pack(side=tk.LEFT,padx=(3),pady=(3))
    help_button = Button(frame_buttons,text = 'Help',command=lambda : os.system('start \"\" https://github.com/C-Hatton/Python-IDE'),bg = 'gray',fg = 'white')
    help_button.pack(side=tk.LEFT,padx=(3),pady=(3))
    copyright = Label(root,text = '© 2021 - Christopher Hatton (558) - Christopher@Christopher-Hatton.co.uk')

    #Arrange Tk:
    heading.grid(row = 0,column = 0,sticky = 'nsew')
    frame_buttons.grid(row = 1,column = 0)
    textbox.grid(row = 2,column = 0,sticky = 'nsew')
    copyright.grid(row = 3,column = 0,sticky = 'nsew')

    #Keybinds:
    root.bind('<Control-s>', f_save_file_key)
    root.bind('<Control-o>', f_open_file_key)
    root.bind('<F12>', f_save_as_key)
    root.bind('<Control-h>', f_replace_key)
    root.bind('<Control-f>', f_change_text_style_key)

    root.mainloop()
     
def small_monitor(): #displays error message for small screen
    root = Tk()
    warning_label = Label(text = 'Your screen is too small')
    warning_label.grid(row = 0,column = 0)
    root.mainloop()

def f_linux(): #displays error message for wrong os
    root = Tk()
    warning_label = Label(text = 'Email Christopher@Christopher-Hatton.co.uk for the Linux version')
    warning_label.grid(row = 0,column = 0)
    root.mainloop()  

def f_mac(): #displays error message for wrong os
    root = Tk()
    warning_label = Label(text = 'Email Christopher@Christopher-Hatton.co.uk for the Mac version')
    warning_label.grid(row = 0,column = 0)
    root.mainloop()  

def f_unknown_os(): #displays error message for wrong os
    root = Tk()
    warning_label = Label(text = name + ' is not available for your operating system.')
    warning_label.grid(row = 0,column = 0)
    root.mainloop()      

def run(): #if screen size big enough, run
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)

    if width >= 1280 and height >= 720:
        f_main()
    else:
        small_monitor()

if platform == 'win32': #if os = win32, run
    run()
elif platform == 'linux' or platform == 'linux32':
    f_linux() #if os = linux, asks the user to get the linux version
elif platform == 'darwin':
    f_mac() #if os = osx, asks the user to get the osx version
else:
    f_unknown_os() #for unknown os