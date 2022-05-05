from typing import List
import csv
import string

from Schedule_list import Schedule_list
import os

class ImportCSVFile:
    path:string
    Schedule_List:List[Schedule_list] = []

    def __init__(self,path):
        self.path=path
        self.startImport()

    def startImport(self):
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                if(filename.lower().endswith(".csv")):
                    with open(f'{root}/{filename}', mode='r', newline='') as schedules:
                        reader = csv.reader(schedules)
                        next(reader)
                        for record in reader:  
                            if(len(record)>0):
                                DateTimeStamp, Message, People = record
                                self.Schedule_List.append(Schedule_list(DateTimeStamp=DateTimeStamp,Message=Message,people=People))
                        break
        
        