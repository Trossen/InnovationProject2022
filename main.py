# Self written datastructures.
from DataStructures import *

# For time.
import datetime
from datetime import date

# For API requests.
import requests

# For calculating coordinates.
import math

# List with weekdays.
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# Shows the settings menu, where the user wipe all events or retake the questionnaire.
def settings(curUser):
    userInput = 1
    while int(userInput) > 0 and int(userInput) < 6:
        print("This is the settings. here you can:\n")
        print(" 1 - Retake the Questionnaire\n")
        print(" 2 - Delete all events\n")
        print(" 3 - Set an alarm clock\n")
        print(" 4 - Read the Terms of Service\n")
        print(" 5 - Change language\n")
        print(" 6 - Go to main menu\n")
        userInput = input()
        if userInput.isnumeric():
            if int(userInput) == 1:
                areYouSure = input("This will wipe all events from your calendar, are you sure? y/n")
                if areYouSure == "y":
                    questionnaire(curUser)
            elif int(userInput) == 2:
                for weeks in range(len(curUser.getCalendar())):
                        for day in range(len(weekdays)):
                            curUser.getCalendar()[weeks].getDays()[day].setEvents([])
                dummy = input("All events deleted successfully! Press enter to return to settings.")
            elif int(userInput) == 3:
                dummy = input("Setting an alarm is not supported yet. Press enter to return to settings.")
            elif int(userInput) == 4:
                dummy = input("No terms yet. Press enter to return to settings.")
            elif int(userInput) == 5:
                dumy = input("Changing languages is not supported yet. Press enter to return to settings.")

# Given a user, a week number and a day, gives the user the option to choose a priority for a newly created event.
# Returns the number the user chooses.
def choosePriority(curUser,weekNum,weekDay):
    print("\nChoose when the event should happen on " + weekDay + " in week " + str(weekNum) + ":\n")
    counter = 0
    print(" " + str(counter))

    for event in curUser.getCalendar()[weekNum-1].getDays()[weekdays.index(weekDay)].getEvents():
        # There should not be a possibility to add an event after the go to work event.
        if event.getTitle() != "Go to work/school":
            print(" - " + event.getTitle())
            counter = counter + 1
            print(" " + str(counter))
        
    chosenIndex = int(input("Please enter the number where the new event should be: "))
    while chosenIndex < 0 or chosenIndex > counter:
        chosenIndex = int(input("Please choose a valid number: "))
    
    return chosenIndex

# Function for adding an event/events for a given user.
# Prompts the user for various questions to find out where to place the event(s).
def addEvent(curUser):

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
            # Adding an event in one weekday.
            curUser.getCalendar()[weekNum-1].getDays()[weekdays.index(weekDay)].insertEvent(choosePriority(curUser,weekNum,weekDay),Event(newEventTitle,newEventTime))
            print("There should now be an event in week " + str(weekNum) + " on " + weekDay +"\n")
        else:
            # Adding an event in multiple weekdays.
            counter = 0
            for char in weekDays:
                if char == "y":
                    curUser.getCalendar()[weekNum-1].getDays()[counter].insertEvent(choosePriority(curUser,weekNum,weekdays[counter]),Event(newEventTitle,newEventTime))
                counter = counter + 1
            print("There should now be events in week "+str(weekNum)+"!\n")
        dummy = input(("Non repeating event(s) successfully created! Press enter to return"))
    
    # --- CASE REPEAT ---
    else:
        repeatNum = int(input("How many times should the event be repeated excluding the first one?: ")) + 1
        if multipleWeekdays == "n":
            # Adding an event in one weekday in multiple weeks.
            for number in range(repeatNum):
                if weekNum + number < len(curUser.getCalendar()):
                    curUser.getCalendar()[weekNum + number - 1].getDays()[weekdays.index(weekDay)].insertEvent(choosePriority(curUser,weekNum + number,weekDay),Event(newEventTitle,newEventTime))
        else:
            # Adding an event in multiple weekdays in multiple weeks.
            for number in range(repeatNum):
                counter = 0
                if weekNum + number < len(curUser.getCalendar()):
                    for char in weekDays:
                        if char == "y":
                            curUser.getCalendar()[weekNum + number - 1].getDays()[counter].insertEvent(choosePriority(curUser,weekNum + number,weekdays[counter]),Event(newEventTitle,newEventTime))
                        counter = counter + 1
        dummy = input(("Recurring event successfully created! Press enter to return"))

# Given a user, a time and an offset, formats the time to XX:XX or X:XX depending on hours.
# Formatted time is relative to the current users meeting time for work.
def formatTime(curUser,eventTime,offset):
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

# Given a user, a week number and a weekday, shows the events of the weekday with time that
# respects the users meeting time for work.
def dayCalendar(curUser,weekNum,weekDayNum):
    print("Showing routine for " + weekdays[weekDayNum - 1] + " in week " + str(weekNum) + "\n")

    offset = 0
    # For loop reverse to accumulate offset.
    # Shows earliest event at the bottom
    for event in reversed(curUser.getCalendar()[weekNum - 1].getDays()[weekDayNum - 1].getEvents()):
        print(formatTime(curUser,event.getTime(),offset) + "   " + event.getTitle())
        offset = offset + event.getTime()
    
    dummy = input("\nTo go back to the menu press enter.\n")

# Given a user and a week number, shows the days in the week in the users calendar 
# and provides navigation to those days.
def weekCalendar(curUser,weekNum):
    userInput = ""
    while userInput != "back":
        print("\nThis is your calendar for week " + str(weekNum + 1) + "\n")

        for day in curUser.getCalendar()[weekNum].getDays():
            print(day.getName() + "\n")
        
        userInput = input("To see the events of a day, enter the day you would like to see, to go back to the menu enter back\n")
        if userInput in weekdays:
            dayCalendar(curUser,weekNum + 1,weekdays.index(userInput) + 1)

# Given a user, shows the weeks in the users calendar and provides navigation to these weeks.
def yearCalendar(curUser):
    userInput = 1
    while userInput != "back":
        print("\nThis is your week calendar\n")

        for week in curUser.getCalendar():
            print(week.getName() + "\n")
        
        userInput = input("To see the days of a week, enter the number of the week you would like to see, to go back to the menu enter back\n")
        if userInput.isnumeric():
            for week in range(len(curUser.getCalendar())):
                if (int(userInput) - 1) == week:
                    weekCalendar(curUser,week)

# Given various different data provided by method apiRequests, changes the time it takes to go to
# work based on the wind data and difference in directions.
def calculateWind(windSpeed,windAngle,latHome,lngHome,latWork,lngWork,workTime):

    # Calculate the travelling angle in radians
    travelAngle = math.atan2(lngWork - lngHome, latWork - latHome)

    # Convert the angle to radians
    if windAngle > 180:
        windAngle = windAngle-360
    windAngleRad = windAngle * (math.pi / 180)

    # Calculate the difference in radians
    diffRad = abs(windAngleRad - travelAngle)

    # If the difference is greater than pi, we need to take the "short way" around the circle
    if diffRad > math.pi:
        # which is the same as subtracting the difference from 2 * pi
        diffRad = 2 * math.pi - diffRad

    # Convert the difference to degrees
    diffDeg = diffRad * (180 / math.pi)

    # Change the difference in degrees to be a percentage to apply to the work time
    windScale = ((((diffDeg-90)*-1)*(1/9))/1000)
    boost = (windSpeed*windScale)+1
    return int(workTime/boost)+1

# Returns true or false given a sunrise time, a work time and a user.
# True if the sun is up when the user has to leave for work, False otherwise.
def sunIsUp(curUser,sunrise,timeToWork):

    # Subtract an hour if necessary
    if curUser.getTime().minute > timeToWork:
        goFromHomeMinute = curUser.getTime().minute - timeToWork
        goFromHomeHour = curUser.getTime().hour
    else:
        goFromHomeMinute = curUser.getTime().minute - timeToWork + 60
        goFromHomeHour = curUser.getTime().hour - 1
    
    # Prepare and format the times as strings
    if goFromHomeHour < 10:
        goFromHomeHourStr = "0" + str(goFromHomeHour)
    else:
        goFromHomeHourStr = str(goFromHomeHour)
    if goFromHomeMinute < 10:
        goFromHomeMinuteStr = "0" + str(goFromHomeMinute)
    else:
        goFromHomeMinuteStr = str(goFromHomeMinute)
    
    # Make a time from the string
    goFromHomeTime = datetime.time.fromisoformat(goFromHomeHourStr +":"+ goFromHomeMinuteStr +":0"+ str(curUser.getTime().second))

    # Compare times and return
    return sunrise.time() >= goFromHomeTime

# Returns true or false given a weathercode.
# True if it is raining, snowing or something similar, False otherwise.
def isRaining(weatherCode):
    if weatherCode < 700:
        return True

# Returns geolocation(Google), weather(OpenWeather) and distancematrix(Google) data for a given user.
# Assumes non-garbage input in the user's address fields.
def apiRequests(curUser):
    # API KEYS
    google_api_key = 'AIzaSyDdOaN1K1GMwjxLv_x3EScqzWnJvyS-XTc'
    openweathermap_api_key = 'b59487c37a2da0337444936e64b3cac9'

    # Request geolocation from Google API
    geoHomeData = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + curUser.getHomeAddress() + "&key=" + google_api_key)
    geoWorkData = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + curUser.getWorkAddress() + "&key=" + google_api_key)

    # Extract latitude and longitude coordinates of users home
    geoHome = geoHomeData.json()
    latHome = geoHome["results"][0]["geometry"]["location"]["lat"]
    lngHome = geoHome["results"][0]["geometry"]["location"]["lng"]

    # Extract latitude and longitude coordinates of users workplace/school
    geoWork = geoWorkData.json()
    latWork = geoWork["results"][0]["geometry"]["location"]["lat"]
    lngWork = geoWork["results"][0]["geometry"]["location"]["lng"]

    # Request weatherdata from OpenWeather API
    weatherData = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + str(latWork) + "&lon=" + str(lngWork) + "&appid=" + openweathermap_api_key)
    weatherCall = weatherData.json()

    # Extract the weather code
    weatherCode = weatherCall["weather"][0]["id"]

    # Extract the sunrise time
    sunrise = datetime.datetime.fromtimestamp(weatherCall['sys']['sunrise'])


    # Extract wind speed and wind angle
    windSpeed = weatherCall['wind']['speed']
    windAngle = weatherCall['wind']['deg']

    #Request distancematrix from Google API
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"
    timeToWorkData = requests.get(url + "origins=" + curUser.getHomeAddress() + "&destinations=" + curUser.getWorkAddress() + "&mode=" + curUser.getTransportType() + "&key=" + google_api_key)

    # Extract the time as an integer
    timeToWork = int(timeToWorkData.json()["rows"][0]["elements"][0]["duration"]["text"].split()[0])

    return (windSpeed,windAngle,latHome,lngHome,latWork,lngWork,timeToWork,weatherCode,sunrise)

# Prompts the user to answer questions and generates a new calendar for a given user. 
# Erases existing calendar data.
# Assumes the user answers properly.
def questionnaire(curUser):
    print("\nPlease fill out the questionnaire.\n")
    curUser.setHomeAddress("Stationsvænget 1, 5260 Odense")
    curUser.setWorkAddress("Campusvej 55, 5230 Odense")
    #curUser.setHomeAddress(input("Enter your home address, eg. Exampleroad 1, 9999 Exampletown:\n"))
    #curUser.setWorkAddress(input("Enter a work/school address, eg. Exampleroad 1, 9999 Exampletown:\n"))

    transportType = input("How do you go to work/school?\n Please enter a transport number.\n1: Car\n2: Public Transport\n3: Walking\n4: Bike\n")
    if transportType == "1":
        curUser.setTransportType("driving")
    if transportType == "2":
        curUser.setTransportType("transit")
    if transportType == "3":
        curUser.setTransportType("walking")
    if transportType == "4":
        curUser.setTransportType("bicycling")

    brushTeeth = input("Do you brush teeth, y/n?:")
    if brushTeeth == "y":
        btList = []
        for day in weekdays:
            btList.append(input("Do you brush teeth " + day + ", y/n?: "))
        timeBt = int(input("How long does it take to brush teeth in whole minutes?:"))
    
    eatBreakfast = input("Do you eat breakfast, y/n?: ")
    if eatBreakfast == "y":
        bfList = []
        for day in weekdays:
            bfList.append(input("Do you eat breakfast " + day + ", y/n?: "))
        timeBf = int(input("How long does it take to eat breakfast in whole minutes?: "))
    
    howManyWeeks = int(input("How many weeks do you want to set up for?: "))

    goToWork = input("When do meet for work/school?: please follow the format XX:XX:XX:\n")
    curUser.setTime(datetime.time.fromisoformat(goToWork))
    
    # Create the calendar for the user
    # Empty the calendar
    curUser.setCalendar([])
    # for every week
    for weeks in range(howManyWeeks):
        # Add the week
        curUser.getCalendar().append(Week("Week " + str(weeks+1),[]))
        # for every day
        for day in range(len(weekdays)):
            # Add the day
            curUser.getCalendar()[weeks].getDays().append(Day(weekdays[day],[]))
            # Add events if they do it on the day
            if brushTeeth == "y" and btList[day] == "y":
                curUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event("Brush Teeth",timeBt))

            if eatBreakfast == "y" and bfList[day] == "y":
                curUser.getCalendar()[weeks].getDays()[day].getEvents().append(Event("Breakfast",timeBf))
    
    while input("Would you like to add extra events? y/n\n") != "n":
        addEvent(curUser)
                             
# Runs a text based interface of the Morning Butler.
def main():
    # Create a new user for the program
    localUser = User([],None,None,None,None)

    # Run the questionnaire when the program is started
    questionnaire(localUser)

    # Get info tuple from API's
    apiInfo = apiRequests(localUser)
    #  [0]: wind speed
    #  [1]: wind angle
    #  [2]: home latitude coordinate
    #  [3]: home longitude coordinate
    #  [4]: work latitude coordinate
    #  [5]: work longitude coordinate
    #  [6]: transport time from home to work in minutes
    #  [7]: weather code
    #  [8]: sunrise time

    # Pull todays date
    todayWeek = date.today().isocalendar().week
    todayWeekday = date.today().isocalendar().weekday

    # Calculate the time it takes to go to work with the current wind
    timeToWork = calculateWind(apiInfo[0],apiInfo[1],apiInfo[2],apiInfo[3],apiInfo[4],apiInfo[5],apiInfo[6])

    # If raining, insert an event with get rainjacket to todays routine.
    if isRaining(apiInfo[7]):
        localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Get raincoat.",2))

    # If dark, insert an event with get bikelights to todays routine.
    if sunIsUp(localUser,apiInfo[8],timeToWork) and localUser.getTransportType() == "bicycling":
        localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Grab bikelights and put on your bike.",2))

    # Add the "go to work/school" event to todays calendar
    # Added here as it should be the last event
    localUser.getCalendar()[todayWeek-1].getDays()[todayWeekday-1].getEvents().append(Event("Go to work/school",timeToWork))

    # Menu loop
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
            dayCalendar(localUser,todayWeek,todayWeekday)
        if userInput == 2:
            yearCalendar(localUser)
        if userInput == 3:
            settings(localUser)
        if userInput == 4:
            addEvent(localUser)   
    print("Goodbye!\n")