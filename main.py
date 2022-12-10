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

#DONE
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

#SOMEWHAT DONE
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

#DONE
def addEvent():
    print("To create a new event, please answer the following questions:\n")
    newEventTitle = input("What is the title of the new event?:")
    newEventTime = int(input("How long does the new event take?:"))
    oneTime = input("Is this event a one time event? y/n:")
    if oneTime == "y":
        weekNum = int(input("Which week does the event occur?:"))
        weekDay = input("Which weekday does the event occur?:")
        print(str(weekdays.index(weekDay)))
        localUser.getCalendar()[weekNum-1].getDays()[weekdays.index(weekDay)].getEvents().append(Event(newEventTitle,newEventTime))
        print("There should now be an event in week "+str(weekNum)+" on "+ weekDay +"\n")
        dummy = input(("One time event successfully created! Press enter to return to main menu"))
    else:
        monIncl = input("Does the event occur every monday? y/n:")
        tueIncl = input("Does the event occur every tuesday? y/n:")
        wedIncl = input("Does the event occur every wednesday? y/n:")
        thuIncl = input("Does the event occur every thursday? y/n:")
        friIncl = input("Does the event occur every friday? y/n:")
        satIncl = input("Does the event occur every saturday? y/n:")
        sunIncl = input("Does the event occur every sunday? y/n:")
        for weeks in range(len(localUser.getCalendar())):
            for day in range(len(weekdays)):
                localUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event(newEventTitle,newEventTime))
        dummy = input(("Recurring event successfully created! Press enter to return to main menu"))

#DONE
def dayCalendar(weekNum,weekDayNum):
    print("Showing routine for " + weekdays[weekDayNum-1] + " in week " + str(weekNum) + "\n")
    print("This is your morning routine for today:\n")
    offset = 0
    for event in localUser.getCalendar()[weekNum-1].getDays()[weekDayNum-1].getEvents():
        offset = offset + event.getTime()
    for event in localUser.getCalendar()[weekNum-1].getDays()[weekDayNum-1].getEvents():
        print(event.getTitle() +"      "+ formatTime(offset) +"\n")
        offset = offset - event.getTime()
    dummy = input("To go back to the menu press enter.\n")

#DONE
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

#DONE
def yearCalendar():
    userInput = 1
    while userInput != 0:
        print("\nThis is your week calendar\n")
        for week in localUser.getCalendar():
            print(week.getName() + "\n")
        userInput = int(input("To see the days of a week, enter the number of the week you would like to see, to go back to the menu enter 0\n"))
        for weekNum in range(len(localUser.getCalendar())):
            if userInput == weekNum+1:
                weekCalendar(weekNum)

#DONE
def main():
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

#DONE
def questionnaire():
    numberOfEvents = 0
    print("Welcome to the Morning Butler!\n Please fill out the questionnaire")
    brushTeeth = input("Do you brush teeth, y/n?:")
    if brushTeeth == "y":
        numberOfEvents = numberOfEvents + 1
        timeBt = int(input("How long does it take to brush teeth in whole minutes?:"))
    eatBreakfast = input("Do you eat breakfast, y/n?: ")
    if eatBreakfast == "y":
        numberOfEvents = numberOfEvents + 1
        mondayBf = input("Do you eat breakfast Monday, y/n?: ")
        tuesdayBf = input("Do you eat breakfast Tuesday, y/n?: ")
        wednesdayBf = input("Do you eat breakfast Wednesday, y/n?: ")
        thursdayBf = input("Do you eat breakfast Thursday, y/n?: ")
        fridayBf = input("Do you eat breakfast Friday, y/n?: ")
        saturdayBf = input("Do you eat breakfast Saturday, y/n?: ")
        sundayBf = input("Do you eat breakfast Sunday, y/n?: ")
        bfList = [mondayBf,tuesdayBf,wednesdayBf,thursdayBf,fridayBf,saturdayBf,sundayBf]
        timeBf = int(input("How long does it take to eat breakfast in whole minutes?: "))
    howManyWeeks = int(input("How many weeks do you want to set up for?: "))

    goToWork = input("When do meet for work/school?: please follow the format XX:XX:XX:\n")
    timeWork = int(input("How long does it usually take to go to work/school in minutes?: "))
    localUser.setTime(datetime.time.fromisoformat(goToWork))

    print("\n   ------------ Creating Calendar ------------   \n")
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
            localUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event("Go to work/school",timeWork))

                

    print("\nCalendar created Succesfully!\n")
    main()

questionnaire()



