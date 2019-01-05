from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
import os
import re

root = Tk()
root.geometry('2000x1000+0+0')
root.title("Text Editor")

def saveAs(evt):
	global text  
	t = typing.get("1.0", "end-1c")
	savelocation=filedialog.asksaveasfilename()
	file1=open(savelocation, "w+")
	file1.write(t)
	file1.close()

def openDialog():
	global text
	global location
	location = filedialog.askdirectory()
	files = []
	for file in os.listdir(location):
		files.append(file)
	for i in range(len(files)):
		openFiles.insert(END, files[i])

def openFile(evt):
	global location
	global text

	w = evt.widget
	index = int(w.curselection()[0])
	val = w.get(index)
	path = location + '/' + val
	with open(path, "r") as data:
		readData = data.read()
		typing.delete("1.0", END)
		typing.insert(END, readData)
	colorize(evt)

typing = Text(root, width=170, height=50, borderwidth=2, relief=GROOVE)
typing.place(x=190, y=50)

def colorize(evt):
	global typing
	typing.tag_config("RED", foreground="red")
	typing.tag_config("BLUE", foreground="blue")
	typing.tag_config("YELLOW", foreground="yellow")
	typing.tag_config("GREEN", foreground="green")

	stringPattern = '[A-Za-z0-9-]+'

	strings1 = re.findall('"' +stringPattern + '"', typing.get("1.0", "end-1c"))
	strings2 = re.findall( "'" + stringPattern + "'", typing.get("1.0", "end-1c"))
	print(strings1, strings2)

	for i in range(len(strings1)):
		strings1_pos_start = typing.search(strings1[i], "1.0", END)
		strings1Offset = '+%dc' % len(strings1[i])

		while strings1_pos_start:
			strings1_pos_end = strings1_pos_start + strings1Offset
			typing.tag_add('GREEN', strings1_pos_start, strings1_pos_end)
			strings1_pos_start = typing.search(strings1[i], strings1_pos_end, END)

	for i in range(len(strings2)):
		strings2_pos_start = typing.search(strings2[i], "1.0", END)
		strings2Offset = '+%dc' % len(strings2[i])
		while strings2_pos_start:
			strings2_pos_end = strings2_pos_start + strings2Offset
			typing.tag_add('GREEN', strings2_pos_start, strings2_pos_end)
			strings2_pos_start = typing.search(strings2[i], strings2_pos_end, END)

	this = 'this'
	thisOffset = '+%dc' % len(this)
	function = 'function'
	functionOffset = '+%dc' % len(function)
	new = 'new'
	newOffset = '+%dc' % len(new)
	this_pos_start = typing.search(this, '1.0', END)
	function_pos_start = typing.search(function, '1.0', END)
	new_pos_start = typing.search(new, '1.0', END)
	while this_pos_start:
		this_pos_end = this_pos_start + thisOffset
		typing.tag_add('RED', this_pos_start, this_pos_end)
		this_pos_start = typing.search(this, this_pos_end, END)
	while function_pos_start:
		function_pos_end = function_pos_start + functionOffset
		typing.tag_add('BLUE', function_pos_start, function_pos_end)
		function_pos_start = typing.search(function, function_pos_end, END)
	while new_pos_start:
		new_pos_end = new_pos_start + newOffset
		typing.tag_add('YELLOW', new_pos_start, new_pos_end)
		new_pos_start = typing.search(new, new_pos_end, END)

openFiles = Listbox(root, width=20, height=30)
openFiles.place(x=0, y=50)

openFiles.bind('<Double-Button-1>', openFile)

menuBar = Menu(root)

filemenu = Menu(menuBar, tearoff=0)
filemenu.add_command(label="Open", command=openDialog)
filemenu.add_command(label="Save")
filemenu.add_command(label="Save As", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menuBar.add_cascade(label="File", menu=filemenu)

root.bind('<Command-s>', saveAs)
root.bind('<Key>', colorize)
root.config(menu=menuBar)
root.mainloop()