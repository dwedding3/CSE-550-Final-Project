import discord
from discord.ext import commands,tasks
import csv
from datetime import datetime,date

schedule_name = 'schedule_list.csv'
channel_name = 'channel_id_list.csv'

#functions
def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
        if item != tup[-1]:
            str = str + ' '
    return str

def clear_Schedule():
    with open(schedule_name, 'w', newline='') as csvfile:
        spamreader = csv.writer(csvfile, delimiter=',')
        spamreader.writerow(["Date","Time", "Event Name"])
    csvfile.close()

def order_Schedule():
    schedule = []
    time_list = []
    with open(schedule_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            schedule.append(row)
        schedule.pop(0)
    csvfile.close()
    for i in schedule:
        time_list.append(datetime_int(i[0],i[1]))
    new_schedule = [x for _,x in sorted(zip(time_list,schedule))]
    clear_Schedule()
    for i in new_schedule:
        add_to_Schedule(i[0],i[1],i[2])   

def datetime_int(x_date,x_time):#MM/DD/YYYY and HH:mm into int YYYYMMDDHHmm
    year = x_date[6:10]
    month = x_date[0:2]
    day = x_date[3:5]
    hour = x_time[0:2]
    minute = x_time[3:5]
    return (year + month + day + hour + minute)

def add_to_Schedule(date,time,event_name):
    with open(schedule_name, 'a', newline='') as csvfile:
        spamreader = csv.writer(csvfile, delimiter=',')
        spamreader.writerow([date, time, event_name])
        datetime_int(date,time)
    csvfile.close()

def add_channel_id(channel_id):
    f = open(channel_name, "a")
    f.write(channel_id + '\n')
    f.close()

def remove_from_Schedule(total_event):
    with open(schedule_name, "r") as f:
        lines = f.readlines()
    with open(schedule_name, "w") as f:
        for line in lines:
            if line.strip("\n") != total_event:
                f.write(line)

def remove_channel_id(channel_id):
    with open(channel_name, "r") as f:
        lines = f.readlines()
    with open(channel_name, "w") as f:
        for line in lines:
            if line.strip("\n") != channel_id:
                f.write(line)

class Events(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        y = date.today()
        self.today = y.strftime("%m/%d/%Y")
        x = datetime.now()
        self.clock = x.strftime("%H:%M")
        self.seconds.start()
##        self.message_channel = bot.get_channel(channel id)

    def cog_unload(self):
        self.minutes.cancel()
        self.daily.cancel()
        self.seconds.cancel()

    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Event Cog Online')

    #tasks
    @tasks.loop(hours=24.0)
    async def daily(self):
        x = date.today()
        self.today = x.strftime("%m/%d/%Y")
        print("Today is", self.today)

    @tasks.loop(seconds=1.0)
    async def seconds(self, count = 61): #start minute timer at 0 seconds to sync it close to actual time
        x = datetime.now()
        print("mark", self.seconds.current_loop)
        if x.strftime("%S") == "00":
            self.minutes.start()
            print("sync")

    @seconds.after_loop
    async def after_seconds(self):
        print("syncronized!")
        self.today = x.strftime("%m/%d/%Y")
     
    @tasks.loop(seconds=60.0)
    async def minutes(self):
        self.seconds.cancel()
        x = datetime.now()
        self.clock = x.strftime("%H:%M")
        if self.clock == "00:00": #start daily timer at midnight to resync it
            self.daily.start()
        schedule = []
        with open(schedule_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                schedule.append(row)
            schedule.pop(0)
        csvfile.close()
        for i in schedule:
            if i[0] == self.today and i[1] == self.clock:
                remove_from_Schedule(','.join(i))
                to_alert = []
                with open(channel_name, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    for row in spamreader:
                        to_alert.append(row)
                csvfile.close()
                for j in to_alert:
                    id_chan = int(j[0])
                    channel = self.bot.get_channel(id_chan)
                    await channel.send("@everyone")
                    await channel.send(i[2])
    #commands                    
    @commands.command(aliases = ["l"])
    async def list_events(self,ctx):
        order_Schedule()
        with open(schedule_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                print(','.join(row))
                await ctx.send(', '.join(row))
        csvfile.close()

    @commands.command(aliases = ["o"])
    async def order_events(self,ctx):
        order_Schedule()

    @commands.command(aliases = ["a"])
    async def add_event(self,ctx,*args):
        if len(args) == 0: # no arguments
            await ctx.send("please add date, hour, and event name")
        elif len(args) == 1: # only date
            await ctx.send("please add time and event name")
        elif len(args) == 2: # only date and time
            await ctx.send("please add event name")
        else: #all good
            x_date = args[0]
            x_time = args[1]
            name_list = args[2:]
            event_name = convertTuple(name_list)
            dateFlag = True
            while (dateFlag):
                # i basically just want it to go thru all these tests
                # and stop checking if anything fails
                if len(x_date) != 10:
                    dateFlag = False
                    break
                if x_date[2] != "/" or x_date[5] != "/":
                    dateFlag = False
                    break
                if int(x_date[0:2]) > 12 or int(x_date[0:2]) < 1:
                    dateFlag = False
                    break
                if int(x_date[3:5]) > 31 or int(x_date[3:5]) < 1:
                    dateFlag = False
                    break
                break
            if not dateFlag:
                await ctx.send("Please have date be in MM/DD/YYYY, using 0s to fill blank spots")
            timeFlag = True
            while (timeFlag):
                if len(x_time) != 5:
                    timeFlag = False
                    break
                if x_time[2] != ":":
                    timeFlag = False
                    break
                if int(x_time[0:2]) > 23 or int(x_time[0:2]) < 0:
                    timeFlag = False
                    break
                if int(x_time[3:5]) > 59 or int(x_time[3:5]) < 0:
                    timeFlag = False
                    break
                break
            if not timeFlag:
                await ctx.send("please have time be in HH:MM format in 24 hour time (00:00 - 23:59)")
            futureFlag = True
            now_time = datetime_int(self.today,self.clock)
            add_time = datetime_int(x_date,x_time)
            if now_time >= add_time:
                futureFlag = False
                await ctx.send("you can't schedule events in the past!")
            if timeFlag and dateFlag and futureFlag:
                add_to_Schedule(x_date,x_time,event_name)
                await ctx.send("Event added to schedule")

    #admin commands
    @commands.command(aliases = ["cs"])
    @commands.has_permissions(administrator = True)
    async def clear_schedule(self,ctx):
        clear_Schedule()
        await ctx.send("Schedule Cleared")

    @commands.command(aliases = ["sub"])
    @commands.has_permissions(administrator = True)
    async def subscribe_to_alerts(self,ctx):
        x = str(int(ctx.message.channel.id))
        print(x)
        add_channel_id(x)
        await ctx.send("Channel subscribed to event alerts!")

    @commands.command(aliases = ["unsub"])
    @commands.has_permissions(administrator = True)
    async def unsubscribe_to_alerts(self,ctx):
        x = str(int(ctx.message.channel.id))
        print(x)
        remove_channel_id(x)
        await ctx.send("Channel unsubscribed to event alerts!")
    
    @commands.command(aliases = ["sac"])
    @commands.has_permissions(administrator = True)
    async def see_alerted_channels(self,ctx):
        await ctx.send("Channels alerted by this bot:")
        with open(channel_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                print(''.join(row))
                await ctx.send(''.join(row))
        csvfile.close()
        
    @commands.command(aliases = ["ps"])
    @commands.has_permissions(administrator = True)
    async def ping_subs(self,ctx):
        to_alert = []
        with open(channel_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                to_alert.append(row)
            csvfile.close()
        for j in to_alert:
            id_chan = int(j[0])
            print(id_chan)
            channel = self.bot.get_channel(id_chan)
            await channel.send("PONG")
        

def setup(bot):
    bot.add_cog(Events(bot))
