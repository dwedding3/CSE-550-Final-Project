from datetime import datetime,timedelta
from typing import List
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from Schedule_list import Schedule_list
from DiscordWebhook import DiscordWebHook
from Source.InitializeConfig import startInit

def background_scheduler(scheduler_list:List[Schedule_list]):

    config = startInit();
    def tick(schedule:Schedule_list):
        if len(schedule.people)>0:
            schedule.Message=f'<@{schedule.people}>{schedule.Message}'

        DiscordWebHook(URL=config['webhookURL'],userName="Bot",content=schedule.Message)

        print(f'{datetime.now()} A message send out to server' )

    scheduler = BackgroundScheduler()
    for item in scheduler_list:
            #Set the time by now for demo
            item.DateTimeStamp = datetime.now()+ timedelta(milliseconds=3000)
            scheduler.add_job(lambda:tick(item),'date',run_date= item.DateTimeStamp)

    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 


