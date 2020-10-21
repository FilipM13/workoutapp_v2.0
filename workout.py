#imports
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
import sqlite3
import datetime as dt
import os, fnmatch

#gui_window
window = Tk()
window.title('Workout Tracker')
window.configure(bg='#BBEBF4')
window.iconbitmap('arm.ico')
window.state("zoomed")

#variables
user_dropbox_response = StringVar()
user_dropbox_response.set('chose user')
user_list = []
user_new_response = StringVar()
user_new_response.set('new user name')

exercises=[]
exercises_input_exercise = []
exercises_input_series = []
exercises_input_reps = []
exercises_input_vest = []
exercises_dropbox_response = []
exercises_list = ['pullups', 'pushups', 'leglifts', 'dips']

plot_dropbox_response = StringVar()
plot_dropbox_response.set('chose plotting option')
plot_options = ['pullups stats', 'pushups stats', 'dips stats', 'leglifts stats']

#functions
def user_update():
  user_list.clear()
  listOfFiles = os.listdir('.')
  pattern = "*.db"
  for entry in listOfFiles:
      if fnmatch.fnmatch(entry, pattern):
              user_list.append(entry)
  return None

user_update()

def user_new(drop_box, entry, user_name):
  if user_name != '':
    user_name = user_name.replace(' ', '_')

    conection = sqlite3.connect(user_name + '.db')
    cursor = conection.cursor()

    cursor.execute('''
    CREATE TABLE workouts (
      date TEXT,
      exercise TEXT,
      series INTEGER,
      reps INTEGER,
      vest INTEGER
    )
    ''')

    conection.commit()
    conection.close()

    user_update()

    entry.delete(0, 'end')

    if len(user_list) == 1:
      drop_box.destroy()
    if len(user_list) > 0:
      drop_box = OptionMenu(frame_user, user_dropbox_response, *user_list)
      drop_box.grid(row=0, column=0, padx=20, pady=10)

    messagebox.showinfo('Operation completed', 'New user added!')
    user_dropbox_response.set('chose user')
    return None
  else:
    messagebox.showerror('Wrong name.', 'Name field is empty or filled not properly.')
    return None

def exercises_next():
  exercises.append([])
  last_index = len(exercises)-1
  exercises_dropbox_response.append(StringVar())
  exercises_dropbox_response[last_index].set('chose exercise')
  exc = OptionMenu(frame_exercises, exercises_dropbox_response[last_index], *exercises_list)
  ser = Entry(frame_exercises)
  reps = Entry(frame_exercises)
  vest = Entry(frame_exercises)
  exercises_input_exercise.append(exc)
  exercises_input_exercise[last_index].grid(row=last_index+1, column=0, padx=3, pady=3)
  exercises_input_series.append(ser)
  exercises_input_series[last_index].grid(row=last_index+1, column=1, padx=3, pady=3)
  exercises_input_reps.append(reps)
  exercises_input_reps[last_index].grid(row=last_index+1, column=2, padx=3, pady=3)
  exercises_input_vest.append(vest)
  exercises_input_vest[last_index].grid(row=last_index+1, column=3, padx=3, pady=3)

def exercises_clear():
  for el in exercises_input_exercise:
    el.destroy()
  for el in exercises_input_series:
    el.destroy()
  for el in exercises_input_reps:
    el.destroy()
  for el in exercises_input_vest:
    el.destroy()
  exercises_dropbox_response.clear()
  exercises_input_exercise.clear()
  exercises_input_series.clear()
  exercises_input_reps.clear()
  exercises_input_vest.clear()
  exercises.clear()

def check_inputs():
  for el in exercises_dropbox_response:
    if el.get() == 'chose exercise':
      return False
  for el in exercises_input_series:
    if el.get().isnumeric() is False:
      return False
  for el in exercises_input_reps:
    if el.get().isnumeric() is False:
      return False
  for el in exercises_input_vest:
    if el.get().isnumeric() is False:
      return False
  return True

def exercises_confirm():
  if check_inputs():
    for el in exercises:
      el.clear()
      index = exercises.index(el)
      el.append(str(dt.datetime.now().strftime("%d.%m.%Y")))
      el.append(str(exercises_dropbox_response[index].get()))
      el.append(int(exercises_input_series[index].get()))
      el.append(int(exercises_input_reps[index].get()))
      el.append(int(exercises_input_vest[index].get()))
    messagebox.showinfo('Exercises confirmed.', 'Exercises saved, press Update Data Base.')
    return None
  else:
    messagebox.showerror('Input error.', 'Empty input fields detected. Fill every field.')
    return None

def info_prompt():
  messagebox.showinfo('Manual', '1.Chose user. \n2.Fill every input file. \n3.Press \'next exercise\' to add another exercise. \n4.Press \'confirm\' to save exercises. \n5.Press \'update database\' to send exercises to your data base.')
  return None

def db_update():
  if user_dropbox_response != 'chose user' and user_dropbox_response != 'no user registered':
    #adding record
    connection = sqlite3.connect(user_dropbox_response.get())
    cursor = connection.cursor()

    cursor.executemany('INSERT INTO workouts VALUES (?,?,?,?,?)', exercises)

    connection.commit()
    connection.close()
    messagebox.showinfo('DB updated', 'Update successful.')
  else:
    messagebox.showerror('Wrong user', 'Chose user from the list.')
  return None

def plot_assist(key):
  #take x and y values from db
  connection = sqlite3.connect(user_dropbox_response.get())
  cursor = connection.cursor()
  task1 = 'SELECT date FROM workouts WHERE exercise = "' + key + '"'
  task2 = 'SELECT reps FROM workouts WHERE exercise = "' + key + '"'
  task3 = 'SELECT series FROM workouts WHERE exercise = "' + key + '"'
  task4 = 'SELECT vest FROM workouts WHERE exercise = "' + key + '"'
  cursor.execute(task1)
  xvalues = cursor.fetchall()[0]
  cursor.execute(task2)
  y1values = cursor.fetchall()[0]
  cursor.execute(task3)
  y2values = cursor.fetchall()[0]
  cursor.execute(task4)
  y3values = cursor.fetchall()[0]
  connection.commit()
  connection.close()
  #create plot
  plt.title(key + ' statistics')
  plt.plot(xvalues, 
  y1values, 
  label= 'reps[n]',
  linewidth=2,
  marker='.',
  markersize=6,
  linestyle='-.'
  )
  plt.plot(xvalues, 
  y2values, 
  label= 'series[n]',
  linewidth=2,
  marker='.',
  markersize=6,
  linestyle='-.'
  )
  plt.plot(xvalues, 
  y3values, 
  label= 'vest weight[kg]',
  linewidth=2,
  marker='.',
  markersize=6,
  linestyle='-.'
  )
  plt.xlabel('date [dd.mm.yyyy]')
  plt.ylabel('values')
  plt.legend()

def plot_save_assist(key):
  plt.savefig('C:/Users/48668/Desktop/' + key + '.png', dpi=600)
  plt.clf()
  messagebox.showinfo('FYI', 'Plot saved with 600dpi on Desktop.')

def plot_save():
  if plot_dropbox_response.get() == 'pullups stats':
    plot_assist('pullups')
    plot_save_assist('pullups')
    return None
  elif plot_dropbox_response.get() == 'pushups stats':
    plot_assist('pushups')
    plot_save_assist('pushups')
    return None
  elif plot_dropbox_response.get() == 'leglifts stats':
    plot_assist('leglifts')
    plot_save_assist('leglifts')
    return None
  elif plot_dropbox_response.get() == 'dips stats':
    plot_assist('dips')
    plot_save_assist('dips')
    return None
  return None

def plot_plot():
  if plot_dropbox_response.get() == 'pullups stats':
    plot_assist('pullups')
    plt.show()
    return None
  elif plot_dropbox_response.get() == 'pushups stats':
    plot_assist('pushups')
    plt.show()
    return None
  elif plot_dropbox_response.get() == 'leglifts stats':
    plot_assist('leglifts')
    plt.show()
    return None
  elif plot_dropbox_response.get() == 'dips stats':
    plot_assist('dips')
    plt.show()
    return None
  return None

#gui user frame
frame_user = LabelFrame(window, bg='#06687A')
frame_user.pack(padx=100, pady=20)

if len(user_list) > 0:
  user_dropbox = OptionMenu(frame_user, user_dropbox_response, *user_list,)
  user_dropbox.grid(row=0, column=0, padx=20, pady=10)
else:
  user_dropbox = OptionMenu(frame_user, user_dropbox_response, 'no user registered')
  user_dropbox.grid(row=0, column=0, padx=20, pady=10)
user_new_input = Entry(frame_user)
user_new_input.grid(row=0, column=1, padx=20, pady=5)
user_new_btn = Button(frame_user, text='Add new user', padx=5, pady=5, command=lambda:user_new(user_dropbox, user_new_input, user_new_input.get()), bg='#012C35', fg='#BBEBF4')
user_new_btn.grid(row=0, column=2, padx=20, pady=4)

#gui exercises frame
frame_exercises = LabelFrame(window, bg='#06687A')
frame_exercises.pack(padx=100, pady=20)

exercises_label_excercises = Label(frame_exercises, text='Exercise:', padx=5, pady=10, bg='#BBEBF4')
exercises_label_excercises.grid(row=0, column=0, padx=5, pady=10)
exercises_label_series = Label(frame_exercises, text='Number of series[n]:', padx=5, pady=10, bg='#BBEBF4')
exercises_label_series.grid(row=0, column=1, padx=5, pady=10)
exercises_label_reps = Label(frame_exercises, text='Number of reps[n]:', padx=5, pady=10, bg='#BBEBF4')
exercises_label_reps.grid(row=0, column=2, padx=5, pady=10)
exercises_label_vest = Label(frame_exercises, text='Weighted vest[kg]:', padx=5, pady=10, bg='#BBEBF4')
exercises_label_vest.grid(row=0, column=3, padx=5, pady=10)

exercises_btn_cancel = Button(frame_exercises, text='Confirm', padx=5, pady=5, command=exercises_confirm, bg='#012C35', fg='#BBEBF4')
exercises_btn_cancel.grid(row=99, column=3, padx=5, pady=10)
exercises_btn_next = Button(frame_exercises, text='Next exercise', padx=5, pady=5, command=exercises_next, bg='#012C35', fg='#BBEBF4')
exercises_btn_next.grid(row=99, column=2, padx=5, pady=10)
exercises_btn_cancel = Button(frame_exercises, text='Clear', padx=5, pady=5, command=exercises_clear, bg='#012C35', fg='#BBEBF4')
exercises_btn_cancel.grid(row=99, column=1, padx=5, pady=10)

#gui footer frame
frame_footer = LabelFrame(window, bg='#06687A')
frame_footer.pack(padx=100, pady=20)

footer_info = Button(frame_footer, text='info', command=info_prompt, bg='#012C35', fg='#BBEBF4')
footer_info.grid(row=0, column=0, padx=5, pady=10)
footer_confirm = Button(frame_footer, text='Update Data Base', command=db_update, bg='#012C35', fg='#BBEBF4')
footer_confirm.grid(row=0, column=3, padx=5, pady=10)

#gui plot frame
frame_plot = LabelFrame(window, bg='#06687A')
frame_plot.pack(padx=100, pady=20)

plot_dropbox = OptionMenu(frame_plot, plot_dropbox_response, *plot_options)
plot_dropbox.grid(row=0, column=0, padx=5, pady=10)
plot_save = Button(frame_plot, text='Save HQ plot', command=plot_save, bg='#012C35', fg='#BBEBF4')
plot_save.grid(row=0, column=1, padx=5, pady=10)
plot_confirm = Button(frame_plot, text='Confirm Plot', command=plot_plot, bg='#012C35', fg='#BBEBF4')
plot_confirm.grid(row=0, column=2, padx=5, pady=10)

#gui_loop
window.mainloop()