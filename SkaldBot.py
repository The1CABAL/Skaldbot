
from Classes.storySwitcher import storySwitcher, storyFinder
from Classes.decisionMaker import YesNo
from Wisdom.Wisdom_List import random_wisdom
from Helpers.Get_Nearest_Hour import round_to_hour as rth

import discord
import os
import threading
import datetime
import json
import youtube_dl
import random
import shutil

from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio

'''
==================================
BEGIN VARIABLES NEEDED PRE STARTUP
==================================
'''
home = os.getcwd()
wisdom_hour = 3 #24Hour UTC Time. I cannot stress this enough. UTC TIME
client = commands.Bot(command_prefix='$')

#Testing Server
#target_channel_id = 726640547019751458
#Production
target_channel_id = 725880649356935192

'''
================================
END VARIABLES NEEDED PRE STARTUP
================================
'''

@client.event
async def on_ready():
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
        await message.channel.send('Isaac lost his ship in Elite: Dangerous so he drank over 6 ounces of rum and wrote a discord bot. \n\nWhat followed was a team effort of many ideas and abilities to create the entity that stands before you today.\n\nI am basically a digital Kvasir.')

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

    if message.content.startswith('$join') or message.content.startswith('$thanks') or message.content.startswith('$sing'):
        await client.process_commands(message)


'''
===================================
BEGIN FUNCTIONS THAT RUN DAILY JOBS
===================================
'''
#Loop Wisdom Once a day
@tasks.loop(hours=1)
async def wisdom_once_a_day():
    now = datetime.datetime.now()
    hour = rth(now).hour
    if hour == wisdom_hour:
        message_channel = client.get_channel(target_channel_id)
        print(f"Got channel {message_channel}")
        wisdom = random_wisdom()
        await message_channel.send(wisdom + "\n\nThis has been today's wisdom of the gods.")

#Wait until bot is started to start loop
@wisdom_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")

wisdom_once_a_day.start()

'''
=================================
END FUNCTIONS THAT RUN DAILY JOBS
=================================
'''


'''
=============================================
BEGIN FUNCTIONS THAT ALLOW FOR MUSIC PLAYBACK
=============================================
'''
#Join channel requesting author is in
@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    try:
        global voice
        channel  = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"Connected to channel {channel}")

        await ctx.send(f"I have arrived in channel {channel} and I am awaiting requests! Presently, I only accept single song requests from YouTube...")
    except:
        await ctx.send("I cannot possibly know what channel to join unless you are already in that channel...")

#leave channel
@client.command(pass_context=True, aliases=['t', 'tha'])
async def thanks(ctx):
    channel  = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot has left channel {channel}")
        await ctx.send(f"A pleasure to serve in channel {channel}, as always.")
    else:
        print("Bot failed to leave voice channel")
        await ctx.send("I can't tell if I am in a voice channel...")

#play music from youtube
@client.command(pass_context=True, aliases=['s', 'sin'])
async def sing(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Excuse you, I am in the middle of a piece!")
        return

    coinflip = random.randint(1,2)
    if coinflip == 1:
        await ctx.send("*AHEM*")
    else:
        await ctx.send("May I have everyone's attention please? I am about to begin...")

    voice = get(client.voice_clients, guild=ctx.guild)
    if 'youtube' in url:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"I call this piece {nname[0]}")
    elif 'spotify' in url:
        await ctx.send('... Or not... Becuase, unfortunately, I cannot sing requests from Spotify at this time...')
    else:
        await ctx.send('I dont think you are asking me to sing a song...')

    #Stop
#    @client.command(pass_context=True, aliases=['s', 'sto'])
#    async def stop(ctx):
#        voice = get(client.voice_clients, guild=ctx.guild)

#        queues.clear()

#        if voice and voice.is_playing():
#            print("music stopped")
#        else:
#            print('no music to stop')
#            await ctx.send()
'''
======================
END PLAYBACK FUNCTIONS
======================
'''

token_file = open('SkaldBotToken.json')
data = json.load(token_file)

token = data['token']
client.run(token)
