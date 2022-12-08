from dataclasses import dataclass
from typing import List
@dataclass
class RoutineEvent:
    title: str
    time: int
    priority: int #index of list in DailyEvents instead?
    weekday: List[int]

    # GETTERS
    def getTitle(self):
        return self.title

    def getTime(self):
        return self.time

    def getPriority(self):
        return self.priority

    def getWeekday(self):
        return self.weekday

    # SETTERS
    def setTitle(self,title):
        self.title = title

    def setTime (self,time):
        self.time = time

    def setPriority(self,priority):
        self.priority = priority

    def setWeekday (self,weekday):
        self.weekday = weekday

    # Change priority
    
