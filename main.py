import json
import random
import aiohttp

import discord
from discord.ext import commands
from dotenv import load_dotenv

with open('setting.json', 'r', encoding='utf8') as file:
    Data = json.load(file)

load_dotenv()

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)} (ms)')


@bot.command()
async def link(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=866384615395688548&permissions=8&scope=bot')


@bot.command()
async def help(ctx):
    embed = discord.Embed(color=0xff0000)
    embed.add_field(name="loveClient Help ", value="**.help** `Help you use bot!` \n**.ping** `Watch bot Ping!` \n**.rps** `play Rock-Paper-Scissors Game` \n**.info** `Information` \n**.link** `Get bot link` \n**.meme** `Get meme`", inline=False)
    embed.set_footer(text="loveClient")
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    await ctx.send('My name is loveClient')


@bot.listen()
async def on_raw_reaction_add(data):
    global user_choose, get_channel
    if str(data.emoji) == '✊' and bot.user != bot.get_user(data.user_id):
        get_channel = bot.get_channel(data.channel_id)
        user_choose = 2
        await game(get_channel, user_choose)
    elif str(data.emoji) == '✌️' and bot.user != bot.get_user(data.user_id):
        get_channel = bot.get_channel(data.channel_id)
        user_choose = 1
        await game(get_channel, user_choose)
    elif str(data.emoji) == '🖐️' and bot.user != bot.get_user(data.user_id):
        get_channel = bot.get_channel(data.channel_id)
        user_choose = 3
        await game(get_channel, user_choose)
    if bot.user != bot.get_user(data.user_id):
        await embed_msg.remove_reaction(str(data.emoji), data.member)


@bot.command()
async def rps(ctx):
    global embed_msg
    if ctx.message.author != bot.user:
        embed = discord.Embed(title='**剪刀石頭布遊戲(Rock-Paper-Scissors Game)**', description='**✌ - 剪刀(Scissors)**\n'  '**✊ - 石頭(Rock)**\n' '**🖐️ - 布(Paper)**',
                              color=0xff0000)
        embed.set_footer(text="loveClient")
        embed_msg = await ctx.message.channel.send(embed=embed)
        Emoji = ["🖐️", "✌️", "✊"]
        await embed_msg.add_reaction(Emoji[1])
        await embed_msg.add_reaction(Emoji[2])
        await embed_msg.add_reaction(Emoji[0])


async def game(channel, select):
    Game = {1: "剪刀", 2: "石頭", 3: "布"}
    Ai_1 = random.randint(1, 3)
    Ai = Game.get(Ai_1)
    User = Game.get(select)
    if User == "剪刀" and Ai == "石頭":
        await channel.send("✊ `You LOSS!`")
    elif User == "剪刀" and Ai == "布":
        await channel.send("🖐️ `You WIN!`")
    elif User == "石頭" and Ai == "剪刀":
        await channel.send("✌️ `You WIN!`")
    elif User == "石頭" and Ai == "布":
        await channel.send("🖐️ `You LOSS!`")
    elif User == "布" and Ai == "石頭":
        await channel.send("✊ `You WIN!`")
    elif User == "布" and Ai == "剪刀":
        await channel.send("✌️ `You LOSS!`")
    else:
        if Ai == "石頭":
            await channel.send("✊ `Tie`")
        elif Ai == "剪刀":
            await channel.send("✌️ `Tie`")
        elif Ai == "布": 
          await channel.send("🖐️ `Tie`")

@bot.event
async def on_ready():
    activity = discord.Game(name=".help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(">>Bot is online<<")

@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession()as cs:
        async with cs.get("https://www.reddit.com/r/meme.json")as r:
            memes = await r.json()
            await ctx.send(memes["data"]["children"][random.randint(0, 25)]["data"]["url"])


if __name__ == "__main__":
    bot.run(Data['TOKEN'])
