# -*- coding: utf-8 -*-

import os
from TkinterDnD2 import *
try:
    from Tkinter import *
    from ScrolledText import ScrolledText
except ImportError:
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText
import split_characters
import recognition

root = TkinterDnD.Tk()
root.withdraw()
root.title('日语手写字体识别')
root.grid_rowconfigure(1, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=300)
root.grid_columnconfigure(1, weight=1, minsize=300)

Label(root, text='将图片拖拽到本窗口:').grid(row=0, column=0, padx=10, pady=5)
Label(root, text='识别结果:').grid(row=0, column=1, padx=10, pady=5)

listbox = Listbox(root, name='dnd_demo_listbox',selectmode='extended', width=1, height=1)
listbox.grid(row=1, column=0, padx=5, pady=5, sticky='news')
text = Text(root, name='dnd_demo_text', wrap='word', undo=True, width=1, height=1)
text.grid(row=1, column=1, pady=5, sticky='news')

def  del_file(path):
      for i in os.listdir(path):
        path_file = os.path.join(path,i)
        os.remove(path_file)

def drop(event):
    if event.data:
        print('Dropped data:\n', event.data)
        #print_event_info(event)
        if event.widget == listbox:
            files = listbox.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f)
                    listbox.insert('end', f)
                    split_characters.Spliting(f)
                    result = recognition.recognize('./temp')
                    for item in result:
                        text.insert('end',item)
                    del_file('./temp/')
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        else:
            print('Error: reported event.widget not known')
    return event.data

# now make the Listbox and Text drop targets
listbox.drop_target_register(DND_FILES, DND_TEXT)

for widget in (listbox, text):
    widget.dnd_bind('<<Drop>>', drop)

buttonbox = Frame(root)
buttonbox.grid(row=2, column=0, columnspan=2, pady=5)
Button(buttonbox, text='退出', command=root.quit).pack(side=LEFT, padx=5)

listbox.drag_source_register(1, DND_TEXT, DND_FILES)

root.update_idletasks()
root.deiconify()
root.mainloop()