#Self written datastructures
from DataStructures import *
#For retaking the questionnaire
import os 
import sys 
import subprocess
#For time
import datetime
from datetime import date
localUser = User([],None)
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]


def formatTime(eventTime):
    printTime = (localUser.getTime().hour,localUser.getTime().minute)
    if eventTime > localUser.getTime().minute:
        printTime = (printTime[0]-1,printTime[1]-eventTime+60)
    else:
        printTime = (printTime[0],printTime[1] - eventTime)
    if printTime[1] < 10:
        return str(printTime[0]) + ":0" + str(printTime[1])
    else:
        return str(printTime[0]) + ":" + str(printTime[1])

def settings():
    userInput = 1
    while userInput > 0 and userInput < 6:
        print("This is the settings. here you can:\n")
        print(" 1 - Retake the Questionnaire\n")
        print(" 2 - Delete all events\n")
        print(" 3 - Set an alarm clock\n")
        print(" 4 - Read the Terms of Service\n")
        print(" 5 - Change language\n")
        print(" 6 - Go to main menu\n")
        userInput = int(input())
        if userInput == 1:
            userInput = input("This will wipe all events from your calendar, are you sure? y/n")
            if userInput == "y":
                subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
                sys.exit(0)
        if userInput == 2:
            for weeks in range(len(localUser.getCalendar())):
                    for day in range(len(weekdays)):
                        localUser.getCalendar()[weeks].getDays()[day].setEvents([])
            print("All events deleted successfully\n")
        if userInput == 3:
            print("Beep beep!\n")
        if userInput == 4:
            print("Made by the three musketeers, we are not responsible for any injury caused by the usage of this product\n")
        if userInput == 5:
            print("Bruh there are way too many print statements, i dont wanna support multiple languages\n")

def choosePriority(weekNum,weekDay):
    print("\nChoose when the event should happen on " + weekDay + " in week " + str(weekNum) + ":\n")
    counter = 0
    print(" " + str(counter))
    for event in localUser.getCalendar()[weekNum-1].getDays()[weekdays.index(weekDay)].getEvents():
        if event.getTitle() != "Go to work/school":
            print(" - " + event.getTitle())
            counter = counter + 1
            print(" " + str(counter))
    chosenIndex = int(input("Please enter the number where the new event should be: "))
    while chosenIndex < 0 or chosenIndex > counter:
        chosenIndex = int(input("Please choose a valid number: "))
    return chosenIndex

def addEvent():

    print("To create a new event, please answer the following questions:\n")
    newEventTitle = input("What is the title of the new event?: ")
    newEventTime = int(input("How long does the new event take?: "))
    weekNum = int(input("Which week does the event occur?: "))


    multipleWeekdays = input("Does the event occur on multiple weekdays?: y/n ")
    if multipleWeekdays == "n":
        weekDay = input("Which weekday does the event occur?: ")
    else:
        weekDays = input("Which days should the event occur on?: write a text consisting of y or n if you want to include the weekday or not eg. ynynynn: ")
    

    repeat = input("Should this event be repeated? y/n: ")

    # --- CASE NO REPEAT ---
    if repeat == "n":
        if multipleWeekdays == "n":
            localUser.getCalendar()[weekNum-1].getDays()[weekdays.index(weekDay)].insertEvent(choosePriority(weekNum,weekDay),Event(newEventTitle,newEventTime))
            print("There should now be an event in week " + str(weekNum) + " on " + weekDay +"\n")
        else:
            counter = 0
            for char in weekDays:
                if char == "y":
                    localUser.getCalendar()[weekNum-1].getDays()[counter].insertEvent(choosePriority(weekNum,weekdays[counter]),Event(newEventTitle,newEventTime))
                counter = counter + 1
            print("There should now be events in week "+str(weekNum)+"!\n")
        dummy = input(("Non repeating event(s) successfully created! Press enter to return"))
    
    # --- CASE REPEAT ---
    else:
        repeatNum = int(input("How many times should the event be repeated excluding the first one?: ")) + 1
        if multipleWeekdays == "n":
            for number in range(repeatNum):
                if weekNum + number < len(localUser.getCalendar()):
                    localUser.getCalendar()[weekNum + number - 1].getDays()[weekdays.index(weekDay)].insertEvent(choosePriority(weekNum + number,weekDay),Event(newEventTitle,newEventTime))
        else:
            for number in range(repeatNum):
                counter = 0
                if weekNum + number < len(localUser.getCalendar()):
                    for char in weekDays:
                        if char == "y":
                            localUser.getCalendar()[weekNum + number - 1].getDays()[counter].insertEvent(choosePriority(weekNum + number,weekdays[counter]),Event(newEventTitle,newEventTime))
                        counter = counter + 1
        dummy = input(("Recurring event successfully created! Press enter to return"))

def calculateTime(event):
    if not event.getTravel():
        return event.getTime()
    else:
        #--------------------------------------------------------------
        #Insert fancy math to adjust travel time according to wind here
        #--------------------------------------------------------------
        return event.getTime()

def dayCalendar(weekNum,weekDayNum):
    print("Showing routine for " + weekdays[weekDayNum-1] + " in week " + str(weekNum) + "\n")
    offset = 0
    for event in localUser.getCalendar()[weekNum-1].getDays()[weekDayNum-1].getEvents():
        offset = offset + calculateTime(event)
    for event in localUser.getCalendar()[weekNum-1].getDays()[weekDayNum-1].getEvents():
        print(formatTime(offset) + "   " + event.getTitle())
        offset = offset - calculateTime(event)
    dummy = input("\nTo go back to the menu press enter.\n")

def weekCalendar(weekNum):
    userInput = ""
    while userInput != "back":
        print("\nThis is your calendar for week " + str(weekNum+1) + "\n")
        for day in localUser.getCalendar()[weekNum].getDays():
            print(day.getName() + "\n")
        userInput = input("To see the events of a day, enter the day you would like to see, to go back to the menu enter back\n")
        for dayName in weekdays:
            if userInput == dayName:
                dayCalendar(weekNum+1,weekdays.index(dayName)+1)

def yearCalendar():
    userInput = 1
    while userInput != "back":
        print("\nThis is your week calendar\n")
        for week in localUser.getCalendar():
            print(week.getName() + "\n")
        userInput = input("To see the days of a week, enter the number of the week you would like to see, to go back to the menu enter back\n")
        if userInput.isnumeric():
            for weekNum in range(len(localUser.getCalendar())):
                if int(userInput) == weekNum + 1:
                    weekCalendar(weekNum)

def main():

    # Pull todays date
    # If raining, insert an event with get rainjacket to todays routine.
    # If dark, insert an event with get bikelights to todays routine.

    userInput = 1
    while userInput > 0 and userInput < 5:
        print("This is the main menu, you can by pressing the corresponding number:\n")
        print(" 1 - View your morning routine today\n")
        print(" 2 - View your week calendar\n")
        print(" 3 - View settings\n")
        print(" 4 - Add an event\n")
        print(" 5 - Close Morning Butler\n")
        userInput = int(input())
        if userInput == 1:
            dayCalendar(date.today().isocalendar().week,date.today().isocalendar().weekday)
        if userInput == 2:
            yearCalendar()
        if userInput == 3:
            settings()
        if userInput == 4:
            addEvent()   
    print("Goodbye!\n")

def questionnaire():
    print("\nPlease fill out the questionnaire.\n")
    brushTeeth = "y" #input("Do you brush teeth, y/n?:")
    if brushTeeth == "y":
        timeBt = 4 #int(input("How long does it take to brush teeth in whole minutes?:"))
    eatBreakfast = "y" #input("Do you eat breakfast, y/n?: ")
    if eatBreakfast == "y":
        mondayBf = "y"#input("Do you eat breakfast Monday, y/n?: ")
        tuesdayBf = "y"#input("Do you eat breakfast Tuesday, y/n?: ")
        wednesdayBf = "y"#input("Do you eat breakfast Wednesday, y/n?: ")
        thursdayBf = "y"#input("Do you eat breakfast Thursday, y/n?: ")
        fridayBf = "y"#input("Do you eat breakfast Friday, y/n?: ")
        saturdayBf = "y"#input("Do you eat breakfast Saturday, y/n?: ")
        sundayBf = "y"#input("Do you eat breakfast Sunday, y/n?: ")
        bfList = [mondayBf,tuesdayBf,wednesdayBf,thursdayBf,fridayBf,saturdayBf,sundayBf]
        timeBf = 20 #int(input("How long does it take to eat breakfast in whole minutes?: "))
    howManyWeeks = 52 #int(input("How many weeks do you want to set up for?: "))

    goToWork = "09:00:00"#input("When do meet for work/school?: please follow the format XX:XX:XX:\n")
    timeWork = 15#int(input("How long does it usually take to go to work/school in minutes?: "))
    localUser.setTime(datetime.time.fromisoformat(goToWork))

    # make every week
    for weeks in range(howManyWeeks):
        localUser.getCalendar().append(Week("Week " + str(weeks+1),[]))
        # make every day
        for day in range(len(weekdays)):
            localUser.getCalendar()[weeks].getDays().append(Day(weekdays[day],[]))
            # make every event
            if brushTeeth == "y":
                localUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event("Brush Teeth",timeBt))
            if eatBreakfast == "y":
                if bfList[day] == "y":
                    localUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event("Breakfast",timeBf))
            localUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event("Go to work/school",timeWork,True))
    
    addAnother = input("Would you like to add extra events? y/n\n")
    while addAnother != "n":
        addEvent()
        addAnother = input("Would you like to add extra events? y/n\n")
    main()

questionnaire()

