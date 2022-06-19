import discord
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from discord.ext import commands
import asyncio
import random
import os

# Load the token from ./token.txt
# If ./token.txt does not exist, gives a nice error message!
try:
    token = ""
    with open("token.txt") as f:
        token = f.readline().rstrip()
except FileNotFoundError:
    print("Error: ./token.txt was not found. The bot cannot be started.")
    exit()

YDL_OPTIONS    = {'format': 'bestaudio', 'noplaylist':'True' , 'default-search':'ytsearch'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1', 'options': '-vn'}        

grubs    = ["Pizza", "Burger", "Fries", "Hotdogs", "Icecream", "Donuts", "Ass", "Brisket", "Sushi", "Pho", "Chicken", "Shwarma", "Taco", "Spaghetti", "Kielbasa"]
adjs     = ["Gourmet", "Stinky", "Nasty", "Scrumptious", "Tasty", "Bloody", "Burnt", "Well-Prepared", "Uncooked", "RAW", "Yummy", "Doubley-Good", "Spicy", "Sweet", "Tangy", "Sour", "FLAMIN HOT","Bland"] 
rarities = ["Common","Uncommon","Rare","Epic","Legendary","Mystic"]
weights  = [49,25,15,6,4,1]
sheaders = ["Enjoy your grub!","Grub: eat it.","CONSUME GRUB.","Grub is the basic building block of all life.","One day, we will all be one with Grub."]

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
        asyncio.create_task(  self.sendEmbed(ctx,video_title,"Queued to: "+ctx.author.voice.channel.name,16741788)  )

        async def afterFunc():
            await self.voice.disconnect()
        
        self.voice.play(source=FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=afterFunc)

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
    
class Funnies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def grubplease(self, ctx):
        channel = ctx.channel
        rarity = random.choices(rarities,weights)[0]
        generated = rarity + " " + adjs[random.randint(0, len(adjs)-1)] + " " + grubs[random.randint(0, len(grubs)-1)]
        subheader = sheaders[random.randint(0, len(sheaders)-1)] + "\n\n" + rarity + "\n" + str(weights[rarities.index(rarity)]) + "% chance."

        if rarity == "Common":
            color = 13553358
        elif rarity == "Uncommon":
            color = 52736
        elif rarity == "Rare":
            color = 206
        elif rarity == "Epic":
            color = 13500622
        elif rarity == "Legendary":
            color = 16764416
        elif rarity == "Mystic":
            color = 8355839


        embed = discord.Embed(
            title = generated,
            description = subheader,
            colour = color
        )


        await channel.send(embed=embed)
    
    @commands.command()
    async def troll(self, ctx):
        channel = ctx.channel
        await channel.send("https://upload.wikimedia.org/wikipedia/en/9/9a/Trollface_non-free.png")


bot = commands.Bot(command_prefix=("$"))

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))

bot.add_cog(Music(bot))
bot.add_cog(Funnies(bot))
bot.run(token)
