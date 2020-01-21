import tkinter
from tkinter.constants import *

filename = 'a.sac'

def save(event):
    global text
    cont = text.get("1.0", END)
    with open(filename, 'w') as fl:
        fl.write(cont)

commands = ["mov", "halt", "prob", "load", "eql", "go", "goio", "gono", "add", "dec", "div", "mul", "show", "rand"]

def synt_col(event):
    global text
    cont = text.get("1.0", END)
    lines = cont.split('\n')
    lnum = 1
    for line  in lines:
        text.tag_remove(str(lnum) + ".0", str(lnum) + ".100")
        ls = line.split()
        if len(ls) == 0:
            continue
        if len(ls) > 0 and ls[0][0] == '~':
            text.tag_add("segment-point", str(lnum) + ".0",str(lnum) + ".1")
            text.tag_add("segment", str(lnum) + ".1",str(lnum) + "." + str(len(ls[0])))
        elif len(ls) > 0 and ls[0][0] == ']':
            text.tag_add("variable-point", str(lnum) + ".0",str(lnum) + ".1")
            text.tag_add("variable", str(lnum) + ".1",str(lnum) + "." + str(len(ls[0])))
        elif len(ls) > 0 and ls[0][0] == ':':
            text.tag_add("pointer-point", str(lnum) + ".0",str(lnum) + ".1")
            text.tag_add("pointer", str(lnum) + ".1",str(lnum) + "." + str(len(ls[0])))
        elif len(ls) > 0 and ls[0][0] == '#':
            text.tag_add("info-point", str(lnum) + ".0",str(lnum) + ".1")
            text.tag_add("info", str(lnum) + ".1",str(lnum) + "." + str(len(ls[0])))
        elif len(ls) > 0 and ls[0] in commands:
            text.tag_add("command", str(lnum) + ".0",str(lnum) + "." + str(len(ls[0])))
        sml = len(ls[0]) + 1
        for i in range(1, len(ls)):
            if ls[i][0] == '@':
                text.tag_add("variable-point", str(lnum) + "." + str(sml),str(lnum) + "." + str(sml + 1))
                text.tag_add("variable", str(lnum) + "." + str(sml + 1),str(lnum) + "." + str(sml + len(ls[i])))
            elif ls[i][0] == '%':
                text.tag_add("constant-point", str(lnum) + "." + str(sml),str(lnum) + "." + str(sml + 1))
                text.tag_add("constant", str(lnum) + "." + str(sml + 1),str(lnum) + "." + str(sml + len(ls[i])))
            elif ls[i][0] == '*':
                text.tag_add("pointer-point", str(lnum) + "." + str(sml),str(lnum) + "." + str(sml + 1))
                text.tag_add("pointer", str(lnum) + "." + str(sml + 1),str(lnum) + "." + str(sml + len(ls[i])))
            else:
                text.tag_add("number", str(lnum) + "." + str(sml), str(lnum) + "." + str(sml + len(ls[i])))
            sml += len(ls[i]) + 1
        lnum += 1

root = tkinter.Tk()
frame = tkinter.Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
label = tkinter.Label(frame, text='SAC IDE')
label.pack(fill=X)

text = tkinter.Text(frame)
text.pack(fill=BOTH, expand=1)

text.tag_config("segment-point", background="black", foreground="white")
text.tag_config("segment", background="black", foreground="yellow")
text.tag_config("variable-point", background="blue", foreground="white")
text.tag_config("variable", background="green", foreground="white")
text.tag_config("constant-point", background="lime", foreground="white")
text.tag_config("constant", background="brown", foreground="white")
text.tag_config("pointer-point", background="white", foreground="orange")
text.tag_config("pointer", background="white", foreground="red")
text.tag_config("info-point", background="red", foreground="white")
text.tag_config("info", background="red", foreground="white")
text.tag_config("command", background="orange", foreground="blue")
text.tag_config("number", background="white", foreground="darkblue")
with open(filename, 'r') as fl:
    text.insert(END, ''.join(fl.readlines()))
synt_col(1)

text.bind('<Control-Key-s>', save)
text.bind('<KeyRelease>', synt_col)

text.focus()

root.mainloop()
