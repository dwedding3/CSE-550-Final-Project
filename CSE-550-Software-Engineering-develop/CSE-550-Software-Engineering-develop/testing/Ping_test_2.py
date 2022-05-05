import asyncio
import sys
from distest import TestCollector
from distest import run_dtest_bot
from discord import Embed, Member, Status
from distest import TestInterface

# The tests themselves
test_collector = TestCollector()
created_channel = None

ping = ""
ping_succsuss = False

@test_collector()
async def test_ping(interface):
    await interface.assert_reply_contains("Pong!")
    ping = "Pong!"
    if ping == "Pong!":
        ping_succsuss = True
    else:
        ping_succsuss = False

def output_test(test, result, succsess):
    with open('TestResults.txt', 'a') as f:
        f.write('**********************')
        if succsess:
            f.write('Test passed:',test)
            f.write('Output was:', result)
        else:
            f.write('Test failed:',test)
            f.write('Output was:', result) 
        f.write('**********************')
    return 0

# Actually run the bot
if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector) 

output_test(test_ping, ping, ping_succsuss)
