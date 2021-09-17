import discord
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext import commands
import asyncio
import keep_alive


# Load the token from ./token.txt
# If ./token.txt does not exist, gives a nice error message.
try:
    token = ""
    with open("token.txt") as f:
        token = f.readline().rstrip()
except FileNotFoundError:
    print("Error: ./token.txt was not found. The bot cannot be started.")
    exit()

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True' , 'default-search':'ytsearch'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1', 'options': '-vn'}        

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.paused = False

    async def msg(self,ctx,input):
        channel = ctx.channel
        await channel.send(input)

    async def sendEmbed(self,ctx,title,desc,color):
        embed = discord.Embed(
            title = title,
            description = desc,
            colour = color
        )

        await ctx.send(embed = embed)
        
    
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *,input):
        asyncio.create_task(self.join(ctx))

        await asyncio.sleep(1)
        self.voice = ctx.voice_client
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info("ytsearch:"+input, download=False)
        URL = info['entries'][0]['formats'][0]['url']

        title = video_title = info['entries'][0]['title']
        asyncio.create_task(  self.sendEmbed(ctx,video_title,"Now playing in: "+ctx.author.voice.channel.name,16741788)  )

        self.voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

    @commands.command()
    async def leave(self, ctx):
        self.voice.pause()
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def tpause(self, ctx):
        if self.paused == True:
            asyncio.create_task(  self.sendEmbed(ctx,'Resumed',"Music in "+ctx.author.voice.channel.name+" was resumed.",16741788)  )
            self.voice.resume()
            self.paused = False
        else:
            asyncio.create_task(  self.sendEmbed(ctx,'Paused',"Music in "+ctx.author.voice.channel.name+" was paused.",16741788)  )
            self.voice.pause()
            self.paused = True

bot = commands.Bot(command_prefix=("$"))

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))

bot.add_cog(Music(bot))
bot.run(token)
