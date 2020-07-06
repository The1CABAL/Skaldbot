
import discord, os
import threading
from Classes.storySwitcher import storySwitcher, storyFinder
from Classes.decisionMaker import YesNo
from Classes.SQLITE import SQLITE as SQL
from Wisdom.Wisdom_List import random_wisdom

home = os.getcwd()

SUM_IsSent = False

client = discord.Client()

@client.event

async def on_ready():

    SQL.create_dbo()

    ##Establish a 24 hour cycling job in a different thread
    populate_jsons = threading.Thread(target = SQL.populate_jsons, args=())
    populate_jsons.start()

    print('Logged in as {0.user}'.format(client))

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
        await message.channel.send('Isaac lost his ship to the Fer De Lance mentioned in one of the stories so he drank over 6 ounces of rum and wrote a discord bot. \n\nI am a bot if you would like me to say something new please type "$newStory" but without the quotes.')

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

    if message.content.startswith('$modules'):
        if message.channel.type != discord.ChannelType.private:
            await message.channel.send('Go ahead and DM me and I will help you find what youre looking for.')
        elif message.content.startswith('$module, '):
            args = message.content.split(', ')
            arg = args[1]

            ##Check for exactly matching module name
            try:
                SQL.find_station_by_module(arg)
            except:
                possibleModules = SQL.get_modules_names(arg)
                #send out these possibilities with a message stating to retry $module with the right module name
                #consider just requesting that the user submit an exact module name

    if message.content.startswith('$getAllSystems'):
        if message.author.id == 270864751947546625:
            await message.channel.send('This little maneuver is going to cost us 51 years...')
            SQL.get_all_systems()
        else:
            await message.channel.send('I am sorry, but in order to make sure I can continuously be a conduit to the gods, I can not do that for you.')


client.run('NzI2NjQwNzQ2MzU4MjQzNDA4.XvgPQA.QoyXYwl0fhGr6iVGWZy4ggbwHVw')