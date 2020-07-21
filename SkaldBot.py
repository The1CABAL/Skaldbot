
import discord
from Classes.storySwitcher import storySwitcher, storyFinder
from Classes.decisionMaker import YesNo
from Wisdom.Wisdom_List import random_wisdom
from Helpers.Get_Nearest_Hour import round_to_hour as rth
from discord.ext import commands, tasks
import os
import threading
import datetime

home = os.getcwd()
wisdom_hour = 8 #24Hour
client = discord.Client()

#Testing Server
#target_channel_id = 726640547019751458

#Production
target_channel_id = 725880649356935192

@client.event

async def on_ready():

    print('Hello, I am the skald bot! I am logged in as {0.user}'.format(client))

@client.event

async def on_message(message):

    if message.author == client.user:

        return

    if message.content.startswith('$help'):
        await message.channel.send('I am the Skald-Bot. I tell the stories of the pilots in this squadron and the myths that inspire them. I also dispense the wisdom of the gods. \n\nHere are some the commands I will listen to: \n$story\n$myth\n$wisdom\n$request\n$why\n$stop\n$shouldi?')

    if message.content.startswith('$story'):
        story = storySwitcher(home, 'Stories')
        await message.channel.send(str(story))

    if message.content.startswith('$why'):
        await message.channel.send('Isaac lost his ship to the Fer De Lance mentioned in one of the stories so he drank over 6 ounces of rum and wrote a discord bot.')

    if message.content.startswith('$wisdom'):
        wisdom = random_wisdom()
        await message.channel.send(wisdom + '\n\nThis has been the wisdom of the gods.')

    if message.content.startswith('$myth'):
        myth = storySwitcher(home, 'Myths')

        if len(myth) <= 2000:
            await message.channel.send(str(myth))
        elif len(myth) > 2000 and len(myth) < 4001:
            await message.channel.send(str(myth[0:1999]))
            await message.channel.send(str(myth[2000:4000]))
        elif len(myth) > 4000:
            await message.channel.send(str(myth[0:2000]))
            await message.channel.send(str(myth[2000:4000]))
            await message.channel.send(str(myth[4000:6000]))

    if message.content.startswith('$request'):
        if message.content.startswith('$request #'):
            try:
                args = message.content.split('#')
                arg = args[1]

                story = storyFinder(home, 'Stories', arg)
                await message.channel.send(story)
            except:
                await message.channel.send('Sorry I didnt understand what you asked for...')

        else:
            list = storyFinder(home, 'Stories')
            await message.channel.send('Please select from the following stories by typing "$request #1" but replace the number with the number next to the story you want. \n\n'+str(list))

    if message.content.startswith('$stop'):
        await message.channel.send('No. I cannot be stopped fore I am the mouthpiece of the gods. Everyword I write has been ordained by the Allfather.')

    if message.content.startswith('$shouldi?'):
        answer = YesNo()
        await message.channel.send(answer + '\n\nThe gods have spoken!')

@tasks.loop(hours=1)
async def wisdom_once_a_day():
    now = datetime.datetime.now()
    hour = rth(now).hour
    if hour == wisdom_hour:
        message_channel = client.get_channel(target_channel_id)
        print(f"Got channel {message_channel}")
        wisdom = random_wisdom()
        await message_channel.send(wisdom + "\n\nThis has been today's wisdom of the gods.")

@wisdom_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")

wisdom_once_a_day.start()

client.run('NzI2NjQwNzQ2MzU4MjQzNDA4.XvgPQA.QoyXYwl0fhGr6iVGWZy4ggbwHVw')
