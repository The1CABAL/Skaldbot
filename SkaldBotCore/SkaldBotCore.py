
from Classes.decisionMaker import YesNo
from Classes.SQL import SQL
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
client = commands.Bot(command_prefix='$')
wisdom_hour = '08:00' #24 Hour Pacific time

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
        await message.channel.send('I am the Skald-Bot. I tell the stories of the pilots in this squadron and the myths that inspire them. I also dispense the wisdom of the gods. \n\nHere are some the commands I will listen to: \n$story\n$wisdom\n$why\n$stop\n$shouldi?')

    if message.content.startswith('$story'):
        try:
            channel = message.channel
            serverid = channel.id
            title, story = SQL.get_stories(serverid)
            await message.channel.send(f"This tale is called '{title}'...")
            await message.channel.send(str(story))
        except:
            await message.channel.send('The gods have not yet gifted me with any tails associated with this great hall...')

    if message.content.startswith('$why'):
        await message.channel.send('Isaac lost his ship in Elite: Dangerous so he drank over 6 ounces of rum, his teeth got tingly, and he wrote a discord bot. \n\nWhat followed was a team effort of many ideas and abilities to create the entity that stands before you today.\n\nI am basically a digital Kvasir.')

    if message.content.startswith('$wisdom'):
        try:
            channel = message.channel
            serverid = channel.id
            wisdom = SQL.get_wisdoms(serverid)
            await message.channel.send(wisdom + '\n\nAlso Nova Imperium sucks. \n\nThis has been the wisdom of the gods.')
        except:
            await message.channel.send('The gods have not yet gifted me with any wisdom for this great hall...')
            
    if message.content.startswith('$stop'):
        await message.channel.send('No. I cannot be stopped fore I am the mouthpiece of the gods. Everyword I write has been ordained by the Allfather.')

    if message.content.startswith('$shouldi?'):
        answer = YesNo()
        await message.channel.send(answer + '\n\nThe gods have spoken!')

    #if message.content.startswith('$join') or message.content.startswith('$thanks') or message.content.startswith('$sing'):
    #    await client.process_commands(message)


'''
===================================
BEGIN FUNCTIONS THAT RUN DAILY JOBS
===================================
'''
#Loop Wisdom Once a day
@tasks.loop(minutes=1)
async def wisdom_once_a_day():

    now = datetime.datetime.now()
    time = now.strftime("%H:%M")
    if time == wisdom_hour:
        channels = SQL.get_daily_wisdom_channels()
        for i in channels:
            try:
                message_channel = client.get_channel(int(i))
                wisdom = SQL.get_wisdoms(i)
                await message_channel.send(str(wisdom) + "\n\nThis has been today's wisdom of the gods.")
            except:
                print('Channel with the ID of '+ str(i)+ ' has daily wisdoms turned on but no wisdoms')


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

token = data['Token']
client.run(token)
