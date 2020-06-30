
import discord
from Classes.SQLITE import SQLITE as SQL
from SkaldBot import client

@client.event
async def on_message(message):
    if message.content.startswith('$module, '):
        args = message.content.split(', ')
        arg = args[1]

        ##Check for matching name
        try:
            SQL.find_station_by_module()
        except:
            possibleModules = SQL.get_modules_names(arg)
            #send out these possibilities with a message stating to retry $module with the right module name

