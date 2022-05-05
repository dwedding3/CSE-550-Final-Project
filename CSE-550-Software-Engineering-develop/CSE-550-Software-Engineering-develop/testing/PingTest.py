import discord
import pytest
import asyncio
import discord.ext.test as dpytest 
from discord.ext import commands
import time
 
ping = "Pong!"
ping_success = False
poll = "Reactions[...]"
poll_success = False

#this is a start to attempting to use pytest in test
@pytest.fixture
def bot(event_loop):
    bot = commands.Bot(command_prefix='>') # However you create your bot, make sure to use loop=event_loop
    dpytest.configure(bot)
    return bot

@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message(">ping")
    assert dpytest.verify().message().contains().content("Pong!")

@pytest.mark.asyncio
async def test_poll(bot):
    await dpytest.message(">poll")
    assert dpytest.verify().message().contains().content("Reactions['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟', '✅', '❌']")

def PingResult(ping):   
    if ping == "Pong!":
        ping_success = True
    else:
        ping_success = False
    return ping_success

def PollResult(poll):   
    if poll == "Reactions[...]":
        poll_success = True
    else:
        poll_success = False
    return poll_success

def output_test(test, result, succsess):
    with open('TestResults.txt', 'a') as f:
        f.write('\n**********************\n')
        if succsess:
            f.write('Test passed:')
            f.write(test)
            f.write('Output was:')
            f.write(result)
        else:
            f.write('\n Test failed:')
            f.write(test)
            f.write('\n Output was:')
            f.write(result) 
        f.write('\n**********************')
    return 0 


ping_state = PingResult(ping)
poll_state = PollResult(poll)
time.sleep(30)
output_test('test_ping\n', ping, ping_state)
output_test('test_poll\n', poll, poll_state)
