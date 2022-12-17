from tkinter import *
# Self written datastructures
from DataStructures import *
from main import *
# For time
import datetime
from datetime import date

# Window setup
window = Tk()
window.geometry("255x450")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Creating all frames
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
frame_defaultQ = Frame(window)

# Global lists/variables data storage
localUser = User([],None,None,None,None)
allDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
listOfQ = ["Spiser du morgenmad?", "Børste du tænder?"]
listofEventTitles = ["Morgenmad","Børst tænder"]
# (Title :: str, DoingEvent :: Bool, Minutes :: Int, Weekdays :: [Int])  -- Weekdays has 1 or 0 for happening/not happening
qAnswers = [() for i in listOfQ]
# (Title :: str, Minutes :: Int, Weekdays :: [Int], Repeat :: Bool, RepeatNr :: Int)
listOfAddEvents = []
commuteList = [""] * 4
doneQuestionnaire = False

# Init frames
for frame in (frame_menu, frame_settings, frame_addevent, frame_questionnaire, frame_questionnaire_done,
                frame_weeks, frame_days, frame_tasks, frame_home, frame_defaultQ):
    frame.grid(row=1,column=0,sticky="nsew")
frame_top.grid(row=0,column=0,sticky='n')
frame_bottom.grid(row=100,column=0,sticky='s')

# Raise function for correct display of frames
def show_frame(frame):
    frame.tkraise()

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
        command=lambda:open_weeks(date.today().isocalendar().week)
        ).grid(row='100',column='1')
# Add Event button
Button(frame_bottom, text="+",height=3, width=9,
        command=lambda:open_addevent()
        ).grid(row='100',column='2', sticky='e')

################################################################################
############################## FRAME: HOME #####################################
################################################################################
def open_home():
    show_frame(frame_home)
    open_topframe("Home")
    open_tasks(date.today().isocalendar().week, date.today().isocalendar().weekday - 1, True)

################################################################################
############################## FRAME: WEEKS ####################################
################################################################################
def open_weeks(week):
    show_frame(frame_weeks)
    label_top = Label(frame_weeks, text="Week overview").grid(row=0,column=1)

    # Week wraparound handler
    weekList = [week, week+1, week+2, week+3, week+4]
    weekList = [week if week <= 52 else week - 52 for week in weekList]

    # Buttons:
    btn1 = Button(frame_weeks, text="Week: " + str(weekList[0]) + " (current week)",height=3, width=30, command=lambda:open_days(weekList[0])).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_weeks, text="Week: " + str(weekList[1]),height=3, width=30, command=lambda:open_days(weekList[1])).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_weeks, text="Week: " + str(weekList[2]),height=3, width=30, command=lambda:open_days(weekList[2])).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_weeks, text="Week: " + str(weekList[3]),height=3, width=30, command=lambda:open_days(weekList[3])).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_weeks, text="Week: " + str(weekList[4]),height=3, width=30, command=lambda:open_days(weekList[4])).grid(row='5',column='1', pady=8, padx=20)

################################################################################
############################### FRAME: DAYS ####################################
################################################################################
def open_days(week):
    show_frame(frame_days)
    label_top = Label(frame_days, text="Week: " + str(week)).grid(row='0',column='1')

    # Buttons:
    btn1 = Button(frame_days, text=allDays[0], height=3, width=30,
                    command=lambda:open_tasks(week, 0)).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_days, text=allDays[1], height=3, width=30,
                    command=lambda:open_tasks(week, 1)).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_days, text=allDays[2], height=3, width=30,
                    command=lambda:open_tasks(week, 2)).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_days, text=allDays[3], height=3, width=30,
                    command=lambda:open_tasks(week, 3)).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_days, text=allDays[4], height=3, width=30,
                    command=lambda:open_tasks(week, 4)).grid(row='5',column='1', pady=8, padx=20)

################################################################################
############################### FRAME: TASKS ####################################
################################################################################
def open_tasks(week, day, isToday = False):
    # Kill previous frames
    for widgets in frame_tasks.winfo_children():
        widgets.destroy()

    show_frame(frame_tasks)
    label_top = Label(frame_tasks, text="Week: " + str(week) + ", " + str(day)).grid(row='0',column='1')
    
    # Debugging:
    # print("At open_tasks: " + "week: " + str(week) + " day: " + str(day) + " " + str(doneQuestionnaire))

    if doneQuestionnaire:
        eventText = []
        eventTime = [] 
        eventTimeStrings = []
        timeIndex = 0

        # Calculate travel time to work/school (only if the date is today), and add as event
        if isToday:
            apiInfo = apiRequests(localUser)
            todayTime = calculateWind(apiInfo[0],apiInfo[1],apiInfo[2],apiInfo[3],apiInfo[4],apiInfo[5],apiInfo[6])
            localUser.getCalendar()[week-1].getDays()[day].insertEvent(0,Event("go to work/school",todayTime))

        # Add alarm
        localUser.getCalendar()[week-1].getDays()[day].getEvents().append(Event("Alarm/get up",5))

        # Add events
        for event in localUser.getCalendar()[week-1].getDays()[day].getEvents():
            # Debugging: 
            # print("Found an event")
            eventText.append(event.getTitle())
            if timeIndex == 0:
                eventTime.append(event.getTime())
            else:
                eventTime.append(event.getTime() + eventTime[timeIndex-1])
            timeIndex = timeIndex + 1
        
        # Create time Strings
        offsetIndex = -1
        for event in localUser.getCalendar()[week-1].getDays()[day].getEvents():
            if offsetIndex == -1:
                eventTimeStrings.append(formatTime(event.getTime(),0,localUser))
            else:
                eventTimeStrings.append(formatTime(event.getTime(),eventTime[offsetIndex],localUser))
            offsetIndex = offsetIndex + 1

        # Delete work event, for repeated calls
        if isToday:
            del localUser.getCalendar()[week-1].getDays()[day].getEvents()[0]

        # Delete alarm, for repeated calls
        eventListLength = len(localUser.getCalendar()[week-1].getDays()[day].getEvents())
        del localUser.getCalendar()[week-1].getDays()[day].getEvents()[eventListLength-1]

        eventText.reverse()
        eventTimeStrings.reverse()

        # Debugging:
        # print("EventText:")
        # print(eventText)
        # print("EventTime:")
        # print(eventTime)
        # print("EventTimeStrings:")
        # print(eventTimeStrings)

        # List all the tasks in the frame (display at max 7 tasks)
        for taskNr in range(min(7, len(eventTimeStrings))):
            if (taskNr % 2) == 0:
                Label(frame_tasks, text=eventTimeStrings[taskNr] + "     " + eventText[taskNr],height=2, width=30,anchor='w',relief=GROOVE).grid(row=taskNr + 1,column=1, pady=8, padx=20)
            else:
                Label(frame_tasks, text=eventTimeStrings[taskNr] + "     " + eventText[taskNr],height=2, width=30,anchor='w',relief=GROOVE).grid(row=taskNr + 1,column=1, padx=20)

################################################################################
########################### FRAME: SETTINGS ####################################
################################################################################
def open_settings():
    show_frame(frame_settings)
    label_top = Label(frame_settings, text="Settings").grid(row='0',column='1')

    # Buttons:
    btn1 = Button(frame_settings, text="Take questionnaire",height=3, width=30,
                    command=lambda:open_defaultQ()).grid(row='1',column='1', pady=8, padx=20)
    btn2 = Button(frame_settings, text="Language",height=3, width=30).grid(row='2',column='1', padx=20)
    btn3 = Button(frame_settings, text="Ring Tone",height=3, width=30).grid(row='3',column='1', pady=8, padx=20)
    btn4 = Button(frame_settings, text="Terms of service",height=3, width=30).grid(row='4',column='1', padx=20)
    btn5 = Button(frame_settings, text="Delete everything",height=3, width=30).grid(row='5',column='1', pady=8, padx=20)

################################################################################
######################### FRAMES: QUESTIONNAIRES ###############################
################################################################################
def questionnaire(qList, currentQ):
    # Debugging:
    # print(commuteList)

    # Kill widgets needed!
    for widgets in frame_questionnaire.winfo_children():
        widgets.destroy()

    show_frame(frame_questionnaire)
    label_top = Label(frame_questionnaire, text="Questionnaire").grid(row=0,column=0, columnspan=10)

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
        
        # Checkboxes for days (and titles)
        label_days = Label(frame_questionnaire, text="Which days do you do it?").grid(row=7,column=0, columnspan=10)
        d1 = IntVar()
        d2 = IntVar()
        d3 = IntVar()
        d4 = IntVar()
        d5 = IntVar()
        d6 = IntVar()
        d7 = IntVar()
        Label(frame_questionnaire, text="Mo").grid(row=8,column=0)
        Label(frame_questionnaire, text="Tu").grid(row=8,column=1)
        Label(frame_questionnaire, text="We").grid(row=8,column=2)
        Label(frame_questionnaire, text="Th").grid(row=8,column=3)
        Label(frame_questionnaire, text="Fr").grid(row=8,column=4)
        Label(frame_questionnaire, text="Sa").grid(row=8,column=5)
        Label(frame_questionnaire, text="Su").grid(row=8,column=6)
        Checkbutton(frame_questionnaire, variable=d1).grid(row=9,column=0)
        Checkbutton(frame_questionnaire, variable=d2).grid(row=9,column=1)
        Checkbutton(frame_questionnaire, variable=d3).grid(row=9,column=2)
        Checkbutton(frame_questionnaire, variable=d4).grid(row=9,column=3)
        Checkbutton(frame_questionnaire, variable=d5).grid(row=9,column=4)
        Checkbutton(frame_questionnaire, variable=d6).grid(row=9,column=5)
        Checkbutton(frame_questionnaire, variable=d7).grid(row=9,column=6)
        
        nextOrDone_button = Button(frame_questionnaire, text="Next / Done", 
                                    command=lambda:getVariables()
                                    ).grid(row=10,column=0,sticky='e',columnspan=10)
    
    # Inner function to grab all the entered data, before next question is shown.
    def getVariables():
        qAnswers[currentQ] = (listofEventTitles[currentQ], doingEvent.get(), int(getMinutes.get(
                                )), [d1.get(),d2.get(),d3.get(),d4.get(),d5.get(),d6.get(),d7.get()])
        questionnaire(qList,currentQ+1)

################################################################################
########################### FRAME: QUESTIONNAIRE DONE ##########################
################################################################################
def questionnaireDone():
    global doneQuestionnaire
    doneQuestionnaire = True

    # Debugging:
    # print(str(doneQuestionnaire))

    # Enter user information
    localUser.setHomeAddress(commuteList[0])
    localUser.setWorkAddress(commuteList[1])
    localUser.setTransportType(commuteList[2])
    localUser.setTime(datetime.time.fromisoformat(commuteList[3]))

    # Make an empty calendar
    for weeks in range(52):
        localUser.getCalendar().append(Week("Week " + str(weeks+1),[]))
        # Create every day
        for day in range(len(allDays)):
            localUser.getCalendar()[weeks].getDays().append(Day(allDays[day],[]))

    # Add events
    counter = 0
    for answer in qAnswers:
        # If they are doing the event
        if answer[1]:
            for weeks in range(52):
                currentWeekDay = 0
                for weekDay in answer[3]:
                    # If they do it on the weekday
                    if weekDay == 1:
                        # Debugging:
                        #print("adding event "+str(currentWeekDay))
                        #print(answer[0] + answer[2])
                        localUser.getCalendar()[weeks].getDays()[currentWeekDay].getEvents(
                            ).append(Event(listofEventTitles[counter],answer[2]))
                    currentWeekDay = currentWeekDay + 1
        counter = counter + 1
    
    # Frame display
    show_frame(frame_questionnaire_done)
    label_top = Label(frame_questionnaire_done, text="Questionnaire").grid(row=0,column=0, columnspan=10)
    Label(frame_questionnaire_done).grid(row=1,column=0)
    l_completed1 = Label(frame_questionnaire_done, width=35, text="You succesfully completed"
                        ).grid(row=2,column=0, columnspan=10)
    l_completed2 = Label(frame_questionnaire_done, width=35, text="the questionnaire!"
                        ).grid(row=3,column=0, columnspan=10)
    Label(frame_questionnaire_done).grid(row=4,column=1)

    # Debugging:    
    # Button(frame_questionnaire_done, text="print values",command=lambda:printstuff()).grid(row=4)

################################################################################
############################ FRAME: ADD EVENT ##################################
################################################################################
def open_addevent():
    show_frame(frame_addevent)
    label_top = Label(frame_addevent, text="Create new event").grid(row=0,column=0, columnspan=10)

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
    Label(frame_addevent, text="Mo").grid(row=6,column=0)
    Label(frame_addevent, text="Tu").grid(row=6,column=1)
    Label(frame_addevent, text="We").grid(row=6,column=2)
    Label(frame_addevent, text="Th").grid(row=6,column=3)
    Label(frame_addevent, text="Fr").grid(row=6,column=4)
    Label(frame_addevent, text="Sa").grid(row=6,column=5)
    Label(frame_addevent, text="Su").grid(row=6,column=6)
    Checkbutton(frame_addevent, variable=d1).grid(row=7,column=0)
    Checkbutton(frame_addevent, variable=d2).grid(row=7,column=1)
    Checkbutton(frame_addevent, variable=d3).grid(row=7,column=2)
    Checkbutton(frame_addevent, variable=d4).grid(row=7,column=3)
    Checkbutton(frame_addevent, variable=d5).grid(row=7,column=4)
    Checkbutton(frame_addevent, variable=d6).grid(row=7,column=5)
    Checkbutton(frame_addevent, variable=d7).grid(row=7,column=6)

    # Repeat even question
    label_repeat = Label(frame_addevent, text="Is this event repeating for more weeks?").grid(row=8,column=0, columnspan=10)
    repeat = BooleanVar()
    cYes = Radiobutton(frame_addevent, text="Yes", variable=repeat, value=True)
    cNo = Radiobutton(frame_addevent, text="No", variable=repeat, value=False)
    cYes.grid(row=9,column=0, columnspan=4)
    cNo.grid(row=9,column=3, columnspan=3)

    # Number of repetitions
    label_repeatNr = Label(frame_addevent, text="For how many extra weeks is it repeated?").grid(row=10,column=0, columnspan=10)
    getRepeatNr = Entry(frame_addevent, width=10)
    getRepeatNr.grid(row=11, column=0, columnspan=10)

    # Add event button
    button_add = Button(frame_addevent, text="Add event", command=lambda:getVariables()).grid(row=12, column=0, columnspan=10, sticky='e')

    def getVariables():
        listOfAddEvents.append((getTitle.get(), int(getMinutes.get()), [d1.get(),d2.get(),d3.get(),d4.get(),d5.get(),d6.get(),d7.get()],
                                    repeat.get(), int(getRepeatNr.get())))
        open_home()

################################################################################
############################ FRAME: DEAFULTQ ###################################
################################################################################
def open_defaultQ():
    show_frame(frame_defaultQ)
    label_top = Label(frame_defaultQ, text="Commute questions").grid(row=0,column=0, columnspan=10)

    # Address
    Label(frame_defaultQ, text="Please enter following addresses:").grid(row=1,column=0, columnspan=10)
    Label(frame_defaultQ, text="Eg: Exampleroad 1, 9999 Exampletown").grid(row=1,column=0, columnspan=10)
    Label(frame_defaultQ, text="Home:").grid(row=2,column=0, sticky='w')
    home = Entry(frame_defaultQ, width=30)
    home.grid(row=2,column=1, sticky='e', padx=10)
    Label(frame_defaultQ, text="Work:").grid(row=3,column=0, sticky='w')
    work = Entry(frame_defaultQ, width=30)
    work.grid(row=3,column=1, sticky='e', padx=10)

    # Transport
    Label(frame_defaultQ, text="Type of transportation?").grid(row=4,column=0, columnspan=10)
    transport = StringVar()
    Radiobutton(frame_defaultQ, text="Driving (car)", variable=transport, value="driving").grid(row=5,column=1, sticky='w', padx=20)
    Radiobutton(frame_defaultQ, text="Transit (Bus/Train)", variable=transport, value="transit").grid(row=6,column=1, sticky='w', padx=20)
    Radiobutton(frame_defaultQ, text="Walking", variable=transport, value="walking").grid(row=7,column=1, sticky='w', padx=20)
    Radiobutton(frame_defaultQ, text="Bicycling", variable=transport, value="bicycling").grid(row=8,column=1, sticky='w', padx=20)

    # Meeting time
    Label(frame_defaultQ, text="Meeting time at work/school?").grid(row=9,column=0, columnspan=10)
    Label(frame_defaultQ, text="Eg: 09:00:00").grid(row=10,column=0, columnspan=10)
    time = Entry(frame_defaultQ, width=12)
    time.grid(row=11,column=0,columnspan=4)

    Button(frame_defaultQ, text="Next / Done", command=lambda:getVariables()
            ).grid(row=12,column=0,sticky='e',columnspan=10, padx=10)

    # Method to extract entered data and call next Q
    def getVariables():
        commuteList[0] = home.get()
        commuteList[1] = work.get()
        commuteList[2] = transport.get()
        commuteList[3] = time.get()
        questionnaire(listOfQ, 0)

# First frame to be shown
open_home()

# Debugging:
# Used in questionnaireDone to print all lists of tuples
# def printstuff():
#     print("hello")
#     for x in qAnswers:
#         print(x)
# def printAddEvent():
#     for i in listOfAddEvents:
#         print(i)

window.mainloop()