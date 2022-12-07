from tkinter import *
from tkinter.ttk import *

# writing code needs to
# create the main window of
# the application creating
# main window object named root
root = Tk()
root.geometry("400x800")

# giving title to the main window
root.title("Morning Butler")

# Label is what output will be
# show on the window
button1 = Button(root,text='mandag').pack()
button2 = Button(root,text='tirsdag').pack()
button3 = Button(root,text='onsdag').pack()
button4 = Button(root,text='torsdag').pack()
button5 = Button(root,text='fredag').pack()


# calling mainloop method which is used
# when your application is ready to run
# and it tells the code to keep displaying
root.mainloop()