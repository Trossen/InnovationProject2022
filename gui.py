from tkinter import *

def show_frame(frame):
    frame.tkraise()

window = Tk()
window.geometry("255x450")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

frame_menu = Frame(window)
frame_settings = Frame(window)
frame_addevent = Frame(window)
frame_questionnaire = Frame(window)
frame_questionnaire_done = Frame(window)
frame_home = Frame(window)
frame_weeks = Frame(window)
frame_days = Frame(window)
frame_tasks = Frame(window)
frame_bottom = Frame(window)
frame_top = Frame(window)

allDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
listOfQ = ["Spiser du morgenmad?", "Børste du tænder?"]
# (Title :: str, DoingEvent :: Bool, Minutes :: Int, Weekdays :: [Int])  -- Weekdays has 1 or 0 for happening/not happening
qAnswers = [() for i in listOfQ]
# (Title :: str, Minutes :: Int, Weekdays :: [Int], Repeat :: Bool, RepeatNr :: Int)
listOfAddEvents = []

for frame in (frame_menu, frame_settings, frame_addevent, frame_questionnaire, frame_questionnaire_done,
                frame_weeks, frame_days, frame_tasks, frame_home):
    frame.grid(row=1,column=0,sticky="nsew")

frame_top.grid(row=0,column=0,sticky='n')
frame_bottom.grid(row=100,column=0,sticky='s')

def printAddEvent():
    for i in listOfAddEvents:
        print(i)

############################## TOP FRAME #######################################
def open_topframe(title):
    show_frame(frame_top)
    label1 = Label(frame_top, text=title, width=30, anchor='e').grid(row=0,column=0,padx=20)
    Button(frame_top, text="Today", height=1, width=10,
            command=lambda:open_home()
            ).grid(row=0,column=0, sticky='w', padx=20)

############################# BOTTOM FRAME #####################################
# Settings button
Button(frame_bottom, text="Settings",height=3, width=9,
        command=lambda:open_settings()
        ).grid(row='100',column='0', sticky='w')
# Menu button
Button(frame_bottom, text="Weekview",height=3, width=9,
        command=lambda:open_weeks(50)
        ).grid(row='100',column='1')
# Add Event button
Button(frame_bottom, text="+",height=3, width=9,
        command=lambda:open_addevent()
        ).grid(row='100',column='2', sticky='e')

########################### BOTTOM BUTTONS #####################################
# def bottom_buttons(curFrame):
#     # Today button
#     Button(curFrame, text="Today", height=1, width=5,
#             command=lambda:open_home()
#             ).grid(row=0,column=1, sticky='w', padx=20)

#     # Settings button
#     btn5 = Button(curFrame, text="Settings",height=3, width=9,
#                     command=lambda:open_settings()
#                     ).grid(row='100',column='1', sticky='w', padx=20)
#     # Menu button
#     btn5 = Button(curFrame, text="Weekview",height=3, width=9,
#                     command=lambda:open_weeks(50)
#                     ).grid(row='100',column='1')
#     # Add Event button
#     btn5 = Button(curFrame, text="+",height=3, width=9,
#                     command=lambda:open_addevent()
#                     ).grid(row='100',column='1', sticky='e', padx=20)

################################################################################
############################## FRAME: HOME #####################################
################################################################################
def open_home():
    show_frame(frame_home)
    open_topframe("Home")
    
    # Frame Title:
    label1 = Label(frame_home, text="Dato, Week, Tidspunkt").grid(row='0',column='1')

    # Buttons:
    # Kan laves som loop for ukendt antal, ellers bare stik to hardcode, måske med 7?
    btn1 = Label(frame_home, text="Dø",height=2, width=30,relief=GROOVE).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Label(frame_home, text="genopstå",height=2, width=30,relief=GROOVE).grid(row='2',column='1', padx=20)
    btn3 = Label(frame_home, text="dø version 2",height=2, width=30,relief=GROOVE).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Label(frame_home, text="Børst tænder",height=2, width=30,relief=GROOVE).grid(row='4',column='1', padx=20)
    btn5 = Label(frame_home, text="Rid på job",height=2, width=30,relief=GROOVE).grid(row='5',column='1', pady=8, padx=20)
    # btn5 = Label(frame_home, text="Rid på job",height=2, width=30,relief=GROOVE).grid(row='6',column='1', pady=8, padx=20)
    # btn5 = Label(frame_home, text="Rid på job",height=2, width=30,relief=GROOVE).grid(row='7',column='1', pady=8, padx=20)
    # btn5 = Label(frame_home, text="Rid på job",height=2, width=30,relief=GROOVE).grid(row='8',column='1', pady=8, padx=20)
    # btn5 = Label(frame_home, text="Rid på job",height=2, width=30,relief=GROOVE).grid(row='9',column='1', pady=8, padx=20)
    # btn5 = Label(frame_home, text="Rid på job",height=2, width=30,relief=GROOVE).grid(row='10',column='1', pady=8, padx=20)


    # Bottom buttons:
    # bottom_buttons(frame_home)

################################################################################
############################## FRAME: WEEKS ####################################
################################################################################
def open_weeks(week):
    show_frame(frame_weeks)

    def weekNr(i):
        if i > 52:
            return str(i - 52)
        else:
            return str(i)

    # Frame Title:
    label1 = Label(frame_weeks, text="Week overview").grid(row='0',column='1')

    # Buttons:
    # Kan laves som loop for ukendt antal, ellers bare stik to hardcode, måske med 7?
    btn1 = Button(frame_weeks, text="Week: " + weekNr(week) + " (current week)",height=3, width=30, command=lambda:open_days(week)).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_weeks, text="Week: " + weekNr(week+1),height=3, width=30, command=lambda:open_days(week+1)).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_weeks, text="Week: " + weekNr(week+2),height=3, width=30, command=lambda:open_days(week+2)).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_weeks, text="Week: " + weekNr(week+3),height=3, width=30, command=lambda:open_days(week+3)).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_weeks, text="Week: " + weekNr(week+4),height=3, width=30, command=lambda:open_days(week+4)).grid(row='5',column='1', pady=8, padx=20)

    # Bottom buttons:
    # bottom_buttons(frame_weeks)

################################################################################
############################### FRAME: DAYS ####################################
################################################################################
def open_days(week):
    show_frame(frame_days)

    # Frame Title:
    label1 = Label(frame_days, text="Week: " + str(week)).grid(row='0',column='1')

    # Buttons:
    # Kan laves som loop for ukendt antal, ellers bare stik to hardcode, måske med 7?
    btn1 = Button(frame_days, text=allDays[0],height=3, width=30).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_days, text=allDays[1],height=3, width=30).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_days, text=allDays[2],height=3, width=30).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_days, text=allDays[3],height=3, width=30).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_days, text=allDays[4],height=3, width=30).grid(row='5',column='1', pady=8, padx=20)

    # Bottom buttons:
    # bottom_buttons(frame_days)

################################################################################
############################### FRAME: TASKS ####################################
################################################################################
def open_tasks():
    show_frame(frame_tasks)

    # Frame Title:
    label1 = Label(frame_tasks, text="de").grid(row='0',column='1')

    # Buttons:
    # Kan laves som loop for ukendt antal, ellers bare stik to hardcode, måske med 7?
    btn1 = Button(frame_tasks, text=allDays[0],height=3, width=30).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_tasks, text=allDays[1],height=3, width=30).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_tasks, text=allDays[2],height=3, width=30).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_tasks, text=allDays[3],height=3, width=30).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_tasks, text=allDays[4],height=3, width=30).grid(row='5',column='1', pady=8, padx=20)

    # Bottom buttons:
    # bottom_buttons(frame_tasks)

##### ???????????????????????????????? Skal laves om til tasks overview
def open_frame(curFrame, frameTitle, listOfStr):
    show_frame(curFrame)
    # Frame Title:
    label1 = Label(curFrame, text=frameTitle).grid(row='0',column='1')

    # Buttons:
    # Kan laves som loop for ukendt antal, ellers bare stik to hardcode, måske med 7?
    btn1 = Button(curFrame, text=listOfStr[0],height=3, width=30, command=lambda:open_weeks(50)).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(curFrame, text=listOfStr[1],height=3, width=30).grid(row='2',column='1', padx=20)
    btn3 = Button(curFrame, text=listOfStr[2],height=3, width=30).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(curFrame, text=listOfStr[3],height=3, width=30).grid(row='4',column='1', padx=20)
    btn5 = Button(curFrame, text=listOfStr[4],height=3, width=30).grid(row='5',column='1', pady=8, padx=20)

    # Bottom buttons:
    # bottom_buttons(curFrame)

################################################################################
########################### FRAME: SETTINGS ####################################
################################################################################
def open_settings():
    show_frame(frame_settings)
    # Frame Title:
    label1 = Label(frame_settings, text="Settings").grid(row='0',column='1')

    # Buttons:
    # Kan laves som loop for ukendt antal, ellers bare stik to hardcode, måske med 7?
    btn1 = Button(frame_settings, text="Repeat Questionnaire",height=3, width=30,
                    command=lambda:questionnaire(listOfQ, 0)).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_settings, text="Language",height=3, width=30).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_settings, text="Ring Tone",height=3, width=30).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_settings, text="Terms of service",height=3, width=30).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_settings, text="Delete everything",height=3, width=30).grid(row='5',column='1', pady=8, padx=20)

    # Bottom buttons:
    # bottom_buttons(frame_settings)

################################################################################
######################### FRAMES: QUESTIONNAIRES ###############################
################################################################################
def questionnaire(qList, currentQ):
    for widgets in frame_questionnaire.winfo_children():
        widgets.destroy()
    show_frame(frame_questionnaire)
    label_top_q = Label(frame_questionnaire, text="Questionnaire").grid(row=0,column=0, columnspan=10)

    if currentQ >= len(qList):
        questionnaireDone()
    else:
        label_titel = Label(frame_questionnaire, text=qList[currentQ]).grid(row=1,column=0, columnspan=10)
        doingEvent = BooleanVar()
        cYes = Radiobutton(frame_questionnaire, text="Yes", variable=doingEvent, value=True)
        cNo = Radiobutton(frame_questionnaire, text="No", variable=doingEvent, value=False)
        cYes.grid(row=2,column=0, columnspan=4)
        cNo.grid(row=2,column=3, columnspan=3)

        label_minutes = Label(frame_questionnaire, text="How long does it take in minutes?").grid(row=3,column=0, columnspan=10)
        getMinutes = Entry(frame_questionnaire, width=30)
        getMinutes.grid(row=4, column=0, columnspan=10)
        
        label_days = Label(frame_questionnaire, text="Which days do you do it?").grid(row=7,column=0, columnspan=10)
        d1 = IntVar()
        d2 = IntVar()
        d3 = IntVar()
        d4 = IntVar()
        d5 = IntVar()
        d6 = IntVar()
        d7 = IntVar()
        l1 = Label(frame_questionnaire, text="Mo").grid(row=8,column=0)
        l2 = Label(frame_questionnaire, text="Tu").grid(row=8,column=1)
        l3 = Label(frame_questionnaire, text="We").grid(row=8,column=2)
        l4 = Label(frame_questionnaire, text="Th").grid(row=8,column=3)
        l5 = Label(frame_questionnaire, text="Fr").grid(row=8,column=4)
        l6 = Label(frame_questionnaire, text="Sa").grid(row=8,column=5)
        l7 = Label(frame_questionnaire, text="Su").grid(row=8,column=6)
        c1 = Checkbutton(frame_questionnaire, variable=d1).grid(row=9,column=0)
        c2 = Checkbutton(frame_questionnaire, variable=d2).grid(row=9,column=1)
        c3 = Checkbutton(frame_questionnaire, variable=d3).grid(row=9,column=2)
        c4 = Checkbutton(frame_questionnaire, variable=d4).grid(row=9,column=3)
        c5 = Checkbutton(frame_questionnaire, variable=d5).grid(row=9,column=4)
        c6 = Checkbutton(frame_questionnaire, variable=d6).grid(row=9,column=5)
        c7 = Checkbutton(frame_questionnaire, variable=d7).grid(row=9,column=6)
        
        nextOrDone_button = Button(frame_questionnaire, text="Next / Done", 
                                    command=lambda:getVariables()
                                    ).grid(row=10,column=0,sticky='e',columnspan=10)
    
    # Inner function to grab all the entered data, before next question is shown.
    def getVariables():
        qAnswers[currentQ] = (qList[currentQ], doingEvent.get(), getMinutes.get(
                                ), [d1.get(),d2.get(),d3.get(),d4.get(),d5.get(),d6.get(),d7.get()])
        questionnaire(qList,currentQ+1)

################################################################################
########################### FRAME: QUESTIONNAIRE DONE ##########################
################################################################################
def questionnaireDone():
    show_frame(frame_questionnaire_done)
    label_top_q = Label(frame_questionnaire_done, text="Questionnaire").grid(row=0,column=0, columnspan=10)
    Label(frame_questionnaire_done).grid(row=1,column=0)
    l_completed = Label(frame_questionnaire_done, width=35, text="You succesfully completed"
                        ).grid(row=2,column=0, columnspan=10)
    l_completed = Label(frame_questionnaire_done, width=35, text="the questionnaire!"
                        ).grid(row=3,column=0, columnspan=10)
    Label(frame_questionnaire_done).grid(row=4,column=1)
    
    # Button(frame_questionnaire_done, text="print values",command=lambda:printstuff()).grid(row=4)
    # bottom_buttons(frame_questionnaire_done)

# Used in questionnaireDone to print all lists of tuples
def printstuff():
    print("hello")
    for x in qAnswers:
        print(x)

################################################################################
############################ FRAME: ADD EVENT ##################################
################################################################################
def open_addevent():
    show_frame(frame_addevent)
    label_top_q = Label(frame_addevent, text="Create new event").grid(row=0,column=0, columnspan=10)

    # The title
    label_title = Label(frame_addevent, text="Title of the event:").grid(row=1,column=0, columnspan=10)
    getTitle = Entry(frame_addevent, width=30)
    getTitle.grid(row=2,column=0, columnspan=10)

    # Minutes
    label_minutes = Label(frame_addevent, text="How long does it take in minutes?").grid(row=3,column=0, columnspan=10)
    getMinutes = Entry(frame_addevent, width=10)
    getMinutes.grid(row=4, column=0, columnspan=10)

    # Which weekdays
    label_days = Label(frame_addevent, text="Which days do you do it?").grid(row=5,column=0, columnspan=10)
    d1 = IntVar()
    d2 = IntVar()
    d3 = IntVar()
    d4 = IntVar()
    d5 = IntVar()
    d6 = IntVar()
    d7 = IntVar()
    l1 = Label(frame_addevent, text="Mo").grid(row=6,column=0)
    l2 = Label(frame_addevent, text="Tu").grid(row=6,column=1)
    l3 = Label(frame_addevent, text="We").grid(row=6,column=2)
    l4 = Label(frame_addevent, text="Th").grid(row=6,column=3)
    l5 = Label(frame_addevent, text="Fr").grid(row=6,column=4)
    l6 = Label(frame_addevent, text="Sa").grid(row=6,column=5)
    l7 = Label(frame_addevent, text="Su").grid(row=6,column=6)
    c1 = Checkbutton(frame_addevent, variable=d1).grid(row=7,column=0)
    c2 = Checkbutton(frame_addevent, variable=d2).grid(row=7,column=1)
    c3 = Checkbutton(frame_addevent, variable=d3).grid(row=7,column=2)
    c4 = Checkbutton(frame_addevent, variable=d4).grid(row=7,column=3)
    c5 = Checkbutton(frame_addevent, variable=d5).grid(row=7,column=4)
    c6 = Checkbutton(frame_addevent, variable=d6).grid(row=7,column=5)
    c7 = Checkbutton(frame_addevent, variable=d7).grid(row=7,column=6)

    # Repeat the events?
    label_repeat = Label(frame_addevent, text="Is this event repeating for more weeks?").grid(row=8,column=0, columnspan=10)
    repeat = BooleanVar()
    cYes = Radiobutton(frame_addevent, text="Yes", variable=repeat, value=True)
    cNo = Radiobutton(frame_addevent, text="No", variable=repeat, value=False)
    cYes.grid(row=9,column=0, columnspan=4)
    cNo.grid(row=9,column=3, columnspan=3)

    # How many repetitions?
    label_repeatNr = Label(frame_addevent, text="For how many extra weeks is it repeated?").grid(row=10,column=0, columnspan=10)
    getRepeatNr = Entry(frame_addevent, width=10)
    getRepeatNr.grid(row=11, column=0, columnspan=10)

    # Add event button
    button_add = Button(frame_addevent, text="Add event", command=lambda:getVariables()).grid(row=12, column=0, columnspan=10, sticky='e')

    def getVariables():
        listOfAddEvents.append((getTitle.get(), getMinutes.get(), [d1.get(),d2.get(),d3.get(),d4.get(),d5.get(),d6.get(),d7.get()],
                                    repeat.get(), getRepeatNr.get()))
        open_home()
    

# First frame to be shown
open_home()

window.mainloop()