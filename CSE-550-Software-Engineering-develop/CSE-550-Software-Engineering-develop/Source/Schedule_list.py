from dataclasses import dataclass
from datetime import datetime
import string


@dataclass
class Schedule_list:
    DateTimeStamp:datetime
    Message:string
    people:string
    
    