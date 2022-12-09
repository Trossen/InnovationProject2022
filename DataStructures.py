from dataclasses import dataclass
from typing import List
@dataclass
class Event:
    title: str
    time: int
    #priority: int #index of list in DailyEvents instead?
    #weekday: List[bool]

    # GETTERS
    def getTitle(self):
        return self.title

    def getTime(self):
        return self.time

    #def getPriority(self):
    #    return self.priority

    #def getWeekday(self):
    #    return self.weekday

    # SETTERS
    def setTitle(self,title):
        self.title = title

    def setTime (self,time):
        self.time = time

    #def setPriority(self,priority):
    #    self.priority = priority

    #def setWeekday (self,weekday):
    #    self.weekday = weekday

    # Change priority
    
@dataclass
class Day:
    name: str
    events: List[Event]

    def insertEvent(self,index,newEvent): #which index should be chosen?
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
class Calendar:
    weeks: List[Week]

    def getWeeks (self):
        return self.weeks