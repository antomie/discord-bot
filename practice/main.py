import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import youtube_dl

intents=discord.Intents.default()
intents.members=True

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

load_dotenv()
TOKEN = os.getenv("TOKEN")

#this is a prefex 
#it is used to activate a command in the server
# EX: "!hello" -> returns hello there
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


#this tell us that the bot is ready
#an event is something that is on standby, and if it detects something, it will trigger an action
@client.event  
async def on_ready():
    print("bot is ready")
    print("--------------------")


@client.command()
async def joke(ctx):

    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": "2299bfcb53mshd3c8f377907aa67p1bb99ejsnb03cc539c21b",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    jokes = data['body']
    for joke in jokes:
        setup = joke['setup']
        punchline = joke['punchline']
    await ctx.send(setup + "\n" + punchline)

@client.command()
async def hello(ctx):
    await ctx.send("sup")

#this is detect when a user joins the server
@client.event
async def on_member_join(member):
    channel = client.get_channel(791793540770299938) #this is how you get a specific channel
    await channel.send("yo wassup")

@client.event
async def on_member_remove(memeber):
    channel = client.get_channel(791793540770299938)
    await channel.send("bye bro")

@client.command()
async def play(ctx, url):
    ydl_opts = {
        'format': 'bestaudio',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice_channel.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS))

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice): #if user is in voice channel
        channel = ctx.message.author.voice.channel #this grabs the channel id
        await channel.connect() #this connects the bot to the voice channel
    else:
        await ctx.send("u need to be in a voice channel")

@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client): #if the bot is in the voice channel
        await ctx.guild.voice_client.disconnect() #go to the guild (server) and go into the voice channel to remove the bot
        await ctx.send("i left the channel")
    else:
        await ctx.send("not in a channel bro")

client.run(TOKEN)
