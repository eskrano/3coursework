from tkinter import *
import sqlite3

"CORE"

db = sqlite3.connect(":memory:")
cur = db.cursor()
cur.executescript("""

		create table result (
			id INTEGER PRIMARY KEY,
			one
			);


	""")
db.commit()

"FUNCTIONS"


"SAVE FUNCTION"

def Save(event):
	first_value = var.get()

	cur.execute("INSERT INTO result (one) VALUES (?)",(first_value,))

def Stats(event):
	statwindow = Tk()
	statwindow.title(u'Stats')
	statwindow.geometry('500x400+200+100')

	cur.execute("SELECT * FROM result")

	for row in cur:
		Label(statwindow, text = "Answer №" ).grid(row = row[0], column = 1)
		Label(statwindow, text = row[0]).grid(row = row[0],column = 2)
		Label(statwindow, text = "Result: ").grid(row = row[0], column = 3)
		Label(statwindow, text =row[1] ).grid(row = row[0], column = 4)

	statwindow.mainloop()

root = Tk()



"SET WINDOW PARAMS"

root.title(u'QUESTION app')
root.geometry('500x400+300+200') # ширина=500, высота=400, x=300, y=200
root.resizable(True, False) # размер окна может быть изменен только по горизонтали

"FIRST QUESTION"
Label(root,text = "Are you human?").grid(row = 1, column = 1)
var=StringVar()
var.set('I do not know')
rbutton1=Radiobutton(root,text='Yes',variable=var,value="Yes")
rbutton2=Radiobutton(root,text='No',variable=var,value="No")
rbutton3=Radiobutton(root,text='I do not know',variable=var,value="I do not know")
rbutton1.grid(row  = 2,column = 1)
rbutton2.grid(row  = 2,column = 2)
rbutton3.grid(row  = 2,column = 3)


SaveButton = Button(root,text = 'Save')
SaveButton.bind("<Button-1>",Save)
SaveButton.grid(row = 5, column =2)


StatWindowOpen =  Button(root,text = 'Stats')
StatWindowOpen.bind("<Button-1>",Stats)
StatWindowOpen.grid(row = 5, column =4)





root.mainloop()