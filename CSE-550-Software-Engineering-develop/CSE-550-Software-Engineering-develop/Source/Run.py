from ImportCSVFile import ImportCSVFile
from Scheduler import background_scheduler
from InitializeConfig import startInit

test = ImportCSVFile('./')
    
background_scheduler(test.Schedule_List)
