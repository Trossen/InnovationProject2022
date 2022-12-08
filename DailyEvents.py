from dataclasses import dataclass
from typing import List
from RoutineEvent import RoutineEvent
@dataclass
class DailyEvents:
    events: List[RoutineEvent]

    def insertEvent(self,index,newEvent):
        self.events.insert(index,newEvent)
