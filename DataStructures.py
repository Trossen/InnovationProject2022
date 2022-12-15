from dataclasses import dataclass
from typing import List
from datetime import time
@dataclass
class Event:
    title: str
    time: int

    # GETTERS
    def getTitle(self):
        return self.title

    def getTime(self):
        return self.time

    # SETTERS
    def setTitle(self,title):
        self.title = title

    def setTime (self,time):
        self.time = time
    
@dataclass
class Day:
    name: str
    events: List[Event]

    def insertEvent(self,index,newEvent):
        self.events.insert(index,newEvent)

    def getEvents(self):
        return self.events
    
    def getName(self):
        return self.name

    def setEvents(self,events):
        self.events = events


@dataclass
class Week:
    name: str
    days: List[Day]

    def getDays(self):
        return self.days
    
    def getName(self):
        return self.name

@dataclass
class User:
    userCalendar: List[Week]
    goToWorkTime: time
    transportType: str
    homeAddress: str
    workAddress: str

    #GETTERS
    def getCalendar(self):
        return self.userCalendar
    
    def getTime(self):
        return self.goToWorkTime
    
    def getTransportType(self):
        return self.transportType
    
    def getHomeAddress(self):
        return self.homeAddress
    
    def getWorkAddress(self):
        return self.workAddress

    #SETTERS
    def setCalendar(self,userCalendar):
        self.userCalendar = userCalendar
    
    def setTime(self, goToWorkTime):
        self.goToWorkTime = goToWorkTime
    
    def setTransportType(self, transportType):
        self.transportType = transportType
    
    def setHomeAddress(self, homeAddress):
        self.homeAddress = homeAddress

    def setWorkAddress(self, workAddress):
        self.workAddress = workAddress
