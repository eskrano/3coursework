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

admin_password = 123456

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
	
	if (admin_root_password_entry.get() == admin_password):

		Label(root,text = 'Пароль введен верно!').grid(row =  20, column =1 )

		statwindow = Tk()
		statwindow.title(u'Статистика')
		statwindow.geometry('500x400+200+100')


		#first question ansvers counter
		cur.execute("SELECT `id` FROM result WHERE one = ?",('Мужской',))
		f1_q_f_a = len(cur.fetchall())
		cur.execute("SELECT `id` FROM result WHERE one = ?",('Женский',))
		f1_q_s_a = len(cur.fetchall())
		cur.execute("SELECT `id` FROM result WHERE one = ?",('Не знаю',))
		f1_q_t_a = len(cur.fetchall())

		#second question ansvers counter

		cur.execute("SELECT `id` FROM result WHERE second = ?",('1945',))
		s_q_f_a = len(cur.fetchall())
		cur.execute("SELECT `id` FROM result WHERE second = ?",('1991',))
		s_q_s_a = len(cur.fetchall())
		cur.execute("SELECT `id` FROM result WHERE second = ?",('988',))
		s_q_t_a = len(cur.fetchall())

		#third
		cur.execute("SELECT `id` FROM `result` WHERE `third` = ?",('Очень плохо',))
		t_q_f_a = len(cur.fetchall());
		cur.execute("SELECT `id` FROM `result` WHERE `third` = ?",('Хорошо',))
		t_q_s_a = len(cur.fetchall())


		#four

		cur.execute("SELECT `id` FROM `result` WHERE `four` = ?",('Хорошо',))
		f_q_f_a = len(cur.fetchall())

		cur.execute("SELECT `id` FROM `result` WHERE `four` = ?",('Плохо',))
		f_q_s_a = len(cur.fetchall())

		#five

		cur.execute("SELECT `id` FROM `result` WHERE `five` = ? ",('Хорошо',))
		five_f_a = len(cur.fetchall())
		cur.execute("SELECT `id` FROM `result` WHERE `five` = ? ",('Плохо',))
		five_s_a = len(cur.fetchall())


		##labels

		Label(statwindow,text = "1й вопрос").grid(row = 1, column = 1)

		#result_1
		Label(statwindow,text = "Мужской: ").grid(row = 2, column = 1)
		Label(statwindow,text = f1_q_f_a).grid(row = 2,column = 2)

		Label(statwindow,text = "Женский: ").grid(row = 3, column = 1)
		Label(statwindow,text = f1_q_s_a).grid(row = 3,column = 2)

		Label(statwindow,text = "Не знаю: ").grid(row = 4, column = 1)
		Label(statwindow,text = f1_q_t_a).grid(row = 4,column = 2)

		#result_2

		Label(statwindow,text = "2й вопрос").grid(row = 5,column = 1)

		Label(statwindow,text = "1945: ").grid(row = 6, column = 1)
		Label(statwindow,text = s_q_f_a).grid(row = 6,column = 2)

		Label(statwindow,text = "1991: ").grid(row = 7, column = 1)
		Label(statwindow,text = s_q_s_a).grid(row = 7,column = 2)

		Label(statwindow,text = "988: ").grid(row =8, column = 1)
		Label(statwindow,text = s_q_t_a).grid(row = 8,column = 2)

		#result_3
		
		Label(statwindow,text = '3й вопрос').grid(row = 9, column = 1)

		Label(statwindow, text = 'Очень плохо').grid(row = 10, column = 1)
		Label(statwindow, text = t_q_f_a).grid(row = 10 , column = 2)

		Label(statwindow, text = 'Хорошо').grid(row = 11, column = 1)
		Label(statwindow, text = t_q_s_a).grid(row = 11, column = 2)

		#result 4
		

		Label(statwindow,text = '4й вопрос').grid(row = 12, column = 1)
		
		Label(statwindow, text = 'Хорошо').grid(row = 13, column =  1)
		Label(statwindow, text = f_q_f_a).grid(row = 13 , column = 2)

		Label(statwindow, text = 'Плохо').grid(row = 14 , column =1)
		Label(statwindow, text = f_q_s_a).grid( row = 14 , column = 2)

		#result 5 
		
		Label(statwindow,text = '5й вопрос').grid(row = 15, column = 1)

		Label(statwindow, text = 'Хорошо').grid(row = 16 , column = 1)
		Label(statwindow, text = five_f_a).grid(row = 16, column = 2)

		Label(statwindow, text = 'Плохо').grid(row = 17, column = 1)
		Label(statwindow, text = five_s_a).grid(row = 17, column = 2 )


		statwindow.mainloop()

	else:
		Label(root,text = 'Не верный пароль').grid(row =  20, column =1 )

root = Tk()



"SET WINDOW PARAMS"

root.title(u'QUESTION app')
root.geometry('500x400+300+200') # ширина=500, высота=400, x=300, y=200
root.resizable(False, False) #denny size change
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
rbutton9=Radiobutton(root,text='Хорошо',variable=var_fourth,value="Хорошо")
rbutton10=Radiobutton(root,text='Плохо',variable=var_fourth,value="Плохо")
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
SaveButton.grid(row = 11, column =1)



admin_root_password_entry = IntVar()
Label(root,text = 'Введите пароль для входа в админ меню').grid(row = 17, column = 1)
Entry(root,textvariable = admin_root_password_entry).grid(row = 18, column  = 1)
SaveButton = Button(root,text = 'Войти')
SaveButton.bind("<Button-1>",Stats)
SaveButton.grid(row = 19, column =1)
root.mainloop()
