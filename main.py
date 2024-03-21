import discord
import asyncio
from discord import app_commands
from discord.ext import commands
import random
from pytube import YouTube
from youtube_search import YoutubeSearch
import webbrowser
import os

#IDEA: GET CHANNEL MESSAGES FROM COPIPASTE CHANNEL TO SEND RANDOM INDEX COPIPASTE: 
#COPIPASTE.FROMCHANNELCOPIPASTE[RANDINT]

description = 'bot'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='!', description = description, intents=intents)

@client.event
async def on_ready():
    await tree.sync()
    print("LET'S ROLL")

#these three methods are a bit weird, did them just to get'em workin
#the command method calls the search method that calls the download method
async def video_search(search: str):
    results = YoutubeSearch(search, max_results = 1).to_dict()
    for v in results:
        name = v['title']+'.mp4'
        link = 'https://youtube.com'+v['url_suffix']
    new_value = await video_downloader(link, name)
    return new_value

async def video_downloader(link: str, name: str):
    yt = YouTube(link)
    ytfile = yt.streams.filter(file_extension="mp4").get_by_resolution("360p").download("./")
    os.rename(ytfile, name)
    return name

@tree.command(name = "video", description = "Search a video and receive a .mp4 file")
async def video(interaction, search: str):
    await interaction.response.defer()
    name = await asyncio.wait_for(video_search(search), timeout=None)
    await interaction.followup.send(file=discord.File(name))
    os.remove(name)

#
#eventos on_message
#

@client.event
async def on_message(message):
    if message.content.startswith("!help"):
        await message.channel.send('```Commands \n ------------------------------ \n !video --> Search a phrase and send a internet video lmaooo (the command may not work for certain vids because of length) \n ------------------------------ \n !download --> gets a url and send a mp4 (may not work for length and certain naming errors) \n ------------------------------ \n```')

    #still passive of errors from file names
    if message.content.startswith("!download"):
        helper = message.content
        helper = helper.split(' ', 1)
        yt = YouTube(helper[1])
        ytfile = yt.streams.filter(file_extension="mp4").get_by_resolution("360p").download("./")
        await message.channel.send(file=discord.File(ytfile))
        os.remove(ytfile)

    #passive of errors with files sizes
    if message.content.startswith("!video"):
        helper = message.content
        helper = helper.split(' ', 1)
        name = await asyncio.wait_for(video_search(helper[1]), timeout = None)
        await message.channel.send(file=discord.File(name))
        os.remove(name)

client.run('TOKEN')
