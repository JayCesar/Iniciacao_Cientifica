from tkinter import *

my_window = Tk();
my_canvas = Canvas(my_window, width=400, height=400, background='white')
my_canvas.create_line(0,0,400,400,fill='red')
my_canvas.create_line(400,0,0,400,fill='blue')
my_canvas.create_line(200,0,200,400,fill='green')
my_canvas.create_line(0,200,400,200,fill='green')
my_canvas.grid(row=0, column=0)
my_window.mainloop()