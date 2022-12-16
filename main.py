#Self written datastructures
from DataStructures import *
#For retaking the questionnaire
import os 
import sys 
import subprocess
#For time
import datetime
from datetime import date
#for API requests
import requests
#for calculating coordinates
import math
google_api_key = 'AIzaSyDdOaN1K1GMwjxLv_x3EScqzWnJvyS-XTc'
openweathermap_api_key = 'b59487c37a2da0337444936e64b3cac9'
localUser = User([],None,None,None,None)
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]



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

def formatTime(eventTime,offset,curUser):
    offsetTotal = eventTime + offset
    printTime = (curUser.getTime().hour,curUser.getTime().minute)
    if offsetTotal > curUser.getTime().minute:
        # Check if loop around midnight
        if printTime[0] > 0:
            hourOffset = (offsetTotal//60) + 1
            printTime = (printTime[0] - hourOffset, printTime[1] - offsetTotal + (60 * hourOffset))
        else:
            printTime = (23,printTime[1] - offsetTotal + 60)
    else:
        printTime = (printTime[0],printTime[1] - offsetTotal)
    
    #Add zero for single digit minutes.
    if printTime[1] < 10:
        return str(printTime[0]) + ":0" + str(printTime[1])
    else:
        return str(printTime[0]) + ":" + str(printTime[1])

def dayCalendar(weekNum,weekDayNum):
    print("Showing routine for " + weekdays[weekDayNum-1] + " in week " + str(weekNum) + "\n")

    offset = 0
    for event in reversed(localUser.getCalendar()[weekNum-1].getDays()[weekDayNum-1].getEvents()):
        print(formatTime(event.getTime(),offset,localUser) + "   " + event.getTitle())
        offset = offset + event.getTime()
    
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

def calculateWind(workTime,weatherCall,latHome,lngHome,latWork,lngWork):
    # Calculate the angle in radians
    travelAngle = math.atan2(lngWork - lngHome, latWork - latHome)
    # Convert the angle from radians to degrees
    # angle_in_degrees = math.degrees(travelAngle)


    # Extract wind.speed and wind.deg
    weatherSpeed = weatherCall['wind']['speed']
    weatherDeg = weatherCall['wind']['deg']
    if weatherDeg > 180:
        weatherDeg = weatherDeg-360
    
    # Convert the angle to radians
    angle1_rad = weatherDeg * (math.pi / 180)
    # Calculate the difference in radians
    diff_rad = abs(angle1_rad - travelAngle)

    if diff_rad > math.pi:
        diff_rad = 2 * math.pi - diff_rad

    # Convert the difference back to degrees
    distance = diff_rad * (180 / math.pi)

    windScale = ((((distance-90)*-1)*(1/9))/1000)
    boost = (weatherSpeed*windScale)+1
    return int(workTime/boost)+1

def getTimeToWork(weatherCall,latHome,lngHome,latWork,lngWork,curUser):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"
    r = requests.get(url + "origins=" + curUser.getHomeAddress() + "&destinations=" + curUser.getWorkAddress() + "&mode=" + curUser.getTransportType() + "&key=" + google_api_key)
    timeWork = r.json()["rows"][0]["elements"][0]["duration"]["text"]
    return calculateWind(int(timeWork.split()[0]),weatherCall,latHome,lngHome,latWork,lngWork)

def sunIsUp(weatherCall,timeToWork):
    sunrise = datetime.datetime.fromtimestamp(weatherCall['sys']['sunrise'])
    if localUser.getTime().minute > timeToWork:
        goFromHomeMinute = localUser.getTime().minute - timeToWork
        goFromHomeHour = localUser.getTime().hour
    else:
        goFromHomeMinute = localUser.getTime().minute - timeToWork + 60
        goFromHomeHour = localUser.getTime().hour - 1
    if goFromHomeHour < 10:
        goFromHomeHourStr = "0"+str(goFromHomeHour)
    else:
        goFromHomeHourStr = str(goFromHomeHour)
    if goFromHomeMinute < 10:
        goFromHomeMinuteStr = "0"+str(goFromHomeMinute)
    else:
        goFromHomeMinuteStr = str(goFromHomeMinute)
    
    goFromHomeTime = datetime.time.fromisoformat(goFromHomeHourStr +":"+ goFromHomeMinuteStr +":0"+ str(localUser.getTime().second))
    return sunrise.time() >= goFromHomeTime

def isRaining(weatherCall):
    weatherCode = weatherCall["weather"][0]["id"]
    if weatherCode < 700:
        return True

def apiRequests(curUser):
    # API REQUESTS
    geoHome = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + curUser.getHomeAddress() + "&key=" + google_api_key)
    geoWork = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + curUser.getWorkAddress() + "&key=" + google_api_key)
    # Coordinates of users home
    latHome = geoHome.json()["results"][0]["geometry"]["location"]["lat"]
    lngHome = geoHome.json()["results"][0]["geometry"]["location"]["lng"]
    # Coordinates of users workplace/school
    latWork = geoWork.json()["results"][0]["geometry"]["location"]["lat"]
    lngWork = geoWork.json()["results"][0]["geometry"]["location"]["lng"]
    weatherData = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + str(latWork) + "&lon=" + str(lngWork) + "&appid=" + openweathermap_api_key)
    weatherCall = weatherData.json()
    return (weatherCall,latHome,lngHome,latWork,lngWork)

def main():
    apiInfo = apiRequests()
    # Pull todays date
    todayWeek = date.today().isocalendar().week
    todayWeekday = date.today().isocalendar().weekday
    timeToWork = getTimeToWork(apiInfo[0],apiInfo[1],apiInfo[2],apiInfo[3],apiInfo[4])

    # If raining, insert an event with get rainjacket to todays routine.
    if isRaining(apiInfo[0]):
        print("Its Raining today!")
        localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Get raincoat.",2))
    # If dark, insert an event with get bikelights to todays routine.
    if sunIsUp(apiInfo[0],timeToWork) and localUser.getTransportType() == "bicycling":
        print("Sun is not up yet!")
        localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Grab bikelights and put on your bike.",2))

    # Add the "go to work/school" event to todays calendar
    localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Go to work/school",timeToWork))

    userInput = 1
    while userInput > 0 and userInput < 5:
        # if case for changing date if date changes while using program.
        if date.today().isocalendar().weekday != todayWeekday or date.today().isocalendar().week != todayWeek:
            todayWeek = date.today().isocalendar().week
            todayWeekday = date.today().isocalendar().weekday
            localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Go to work/school",getTimeToWork(),True))
        print("This is the main menu, you can by pressing the corresponding number:\n")
        print(" 1 - View your morning routine today\n")
        print(" 2 - View your week calendar\n")
        print(" 3 - View settings\n")
        print(" 4 - Add an event\n")
        print(" 5 - Close Morning Butler\n")
        userInput = int(input())
        if userInput == 1:
            dayCalendar(todayWeek,todayWeekday)
        if userInput == 2:
            yearCalendar()
        if userInput == 3:
            settings()
        if userInput == 4:
            addEvent()   
    print("Goodbye!\n")

def questionnaire():
    print("\nPlease fill out the questionnaire.\n")

    home = "Stationsvænget 2, 5260 Odense"#input("Enter your home address, eg. Exampleroad 1, 9999 Exampletown:\n")
    work = "Campusvej 55, 5230 Odense"#input("Enter a work/school address, eg. Exampleroad 1, 9999 Exampletown:\n")
    localUser.setHomeAddress(home)
    localUser.setWorkAddress(work)
    transportType = input("How do you go to work/school?\n Please enter a transport number.\n1: Car\n2: Public Transport\n3: Walking\n4: Bike\n")
    if transportType == "1":
        localUser.setTransportType("driving")
    if transportType == "2":
        localUser.setTransportType("transit")
    if transportType == "3":
        localUser.setTransportType("walking")
    if transportType == "4":
        localUser.setTransportType("bicycling")


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
    
    addAnother = input("Would you like to add extra events? y/n\n")
    while addAnother != "n":
        addEvent()
        addAnother = input("Would you like to add extra events? y/n\n")
    main()

#questionnaire()
