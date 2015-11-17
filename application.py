# -*- coding: utf-8 -*- 
from tkinter import *
import sqlite3

"CORE"

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
cur = db.cursor()
cur.executescript("""

		create table if not exists result (
			id INTEGER PRIMARY KEY,
			question INTEGER,
			one text,
			second text,
			third text,
			four text,
			five text,
			six text,
			seven text
			);

	

	""")
db.commit()

"FUNCTIONS"


"SAVE FUNCTION"

def Save(event):
	first_value = var.get()
	second = var_second.get()
	third = var_third.get()
	four = var_fourth.get()
	five = var_five.get()

	cur.execute("INSERT INTO result (one,second,third,four,five) VALUES (?,?,?,?,?)",(first_value,second,third,four,five,))
	db.commit()
def Stats(event):
	statwindow = Tk()
	statwindow.title(u'Статистика')
	statwindow.geometry('500x400+200+100')


	#first question ansvers counter
	cur.execute("SELECT `id` FROM result WHERE one = ?",('Мужской',))
	f_q_f_a = len(cur.fetchall())
	cur.execute("SELECT `id` FROM result WHERE one = ?",('Женский',))
	f_q_s_a = len(cur.fetchall())
	cur.execute("SELECT `id` FROM result WHERE one = ?",('Не знаю',))
	f_q_t_a = len(cur.fetchall())
	print(f_q_f_a)
	#second question ansvers counter
	
	cur.execute("SELECT `id` FROM result WHERE second = ?",('1945',))
	s_q_f_a = len(cur.fetchall())
	cur.execute("SELECT `id` FROM result WHERE second = ?",('1991',))
	s_q_s_a = len(cur.fetchall())
	cur.execute("SELECT `id` FROM result WHERE second = ?",('988',))
	s_q_t_a = len(cur.fetchall())

	#third 
	


	print(f_q_f_a)
	
	statwindow.mainloop()

root = Tk()



"SET WINDOW PARAMS"

root.title(u'QUESTION app')
root.geometry('500x400+300+200') # ширина=500, высота=400, x=300, y=200
root.resizable(True, False) # размер окна может быть изменен только по горизонтали

#first question
Label(root,text = "Ваш пол").grid(row = 1, column = 1)
var=StringVar()
var.set(0)
rbutton1=Radiobutton(root,text='Мужской',variable=var,value="Мужской")
rbutton2=Radiobutton(root,text='Женский',variable=var,value="Женский")
rbutton3=Radiobutton(root,text='Не знаю',variable=var,value="Не знаю")
rbutton1.grid(row  = 2,column = 1)
rbutton2.grid(row  = 2,column = 2)
rbutton3.grid(row  = 2,column = 3)

#second question
Label(root,text = "Год объявления независимости Украины").grid(row = 3, column = 1)
var_second=IntVar()
var_second.set(0)
rbutton4=Radiobutton(root,text='1945',variable=var_second,value="1945")
rbutton5=Radiobutton(root,text='1991',variable=var_second,value="1991")
rbutton6=Radiobutton(root,text='988',variable=var_second,value="988")
rbutton4.grid(row  = 4,column = 1)
rbutton5.grid(row  = 4,column = 2)
rbutton6.grid(row  = 4,column = 3)


#third question
Label(root,text = "Хорошо ли вы относитесь к природе?").grid(row = 5, column = 1)
var_third=StringVar()
var_third.set(0)
rbutton7=Radiobutton(root,text='Очень плохо',variable=var_third,value="Очень плохо")
rbutton8=Radiobutton(root,text='Хорошо',variable=var_third,value="Хорошо")
rbutton7.grid(row  = 6,column = 1)
rbutton8.grid(row  = 6,column = 2)

#fourth question

Label(root,text = "Как вы оцениваете свои знания английского?").grid(row = 7, column = 1)
var_fourth=StringVar()
var_fourth.set(0)
rbutton9=Radiobutton(root,text='Beginner',variable=var_fourth,value="Beginner")
rbutton10=Radiobutton(root,text='Intermediatle',variable=var_fourth,value="Intermediatle")
rbutton9.grid(row  = 8,column = 1)
rbutton10.grid(row  = 8,column = 2)

#five question


Label(root,text = "Как дела?").grid(row = 9, column = 1)
var_five=StringVar()
var_five.set(0)
rbutton11=Radiobutton(root,text='Хорошо',variable=var_five,value="Хорошо")
rbutton12=Radiobutton(root,text='Плохо',variable=var_five,value="Плохо")
rbutton11.grid(row  = 10,column = 1)
rbutton12.grid(row  = 10,column = 2)



SaveButton = Button(root,text = 'Сохранить')
SaveButton.bind("<Button-1>",Save)
SaveButton.grid(row = 11, column =0)


StatWindowOpen =  Button(root,text = 'Stats')
StatWindowOpen.bind("<Button-1>",Stats)
StatWindowOpen.grid(row = 11, column =1)





root.mainloop()