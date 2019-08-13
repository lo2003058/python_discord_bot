from tkinter import *
from time import sleep
import pyautogui

win = Tk()
win.title('Get x,y')
# size
win.geometry('200x30')
# resize false
win.resizable(False, False)
# icon
win.iconbitmap('img/lm.ico')
# always top
win.attributes('-topmost', 1)

lb = Label(text=pyautogui.position())
lb.pack()



win.mainloop()
