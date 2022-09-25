# sqwordle.py
import re
import json
from time import sleep
import asyncpraw
import discord
from discord.ext import commands
from dotenv import dotenv_values

temp = dotenv_values(".env") 
TOKEN = temp['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.members=True
bot=commands.Bot(command_prefix='!', intents=intents)

credentials = json.load(open('credentials.json'))

##### Start Reddit API #####
reddit = asyncpraw.Reddit(client_id = credentials['client_id'],
					 client_secret = credentials['client_secret'],
					 user_agent = credentials['user_agent'])


##### Look for Seattle #####
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if re.search('Seattle', message.content) or re.search('seattle', message.content):
        await message.channel.send('F**k the toots!')
    
    # on_message by default disables bot commands. This forces bot to look for commands
    await bot.process_commands(message)

##### Post the latest Jimmmy G drawing #####
@bot.command(name='rita', help='Starts looking for Rita to post the Jimmy G drawing from Reddit')
async def rita(ctx):

    await ctx.send('Waiting for Rita to post...')
    niners = await reddit.subreddit('49ers')
    rita = await reddit.redditor('RitaOak')
    postText = 'drawing jimmy g every day'
    jimmyG_old = None

    while True:
        async for submission in niners.new(limit=5):
            if submission.author == rita and postText in submission.title.lower():
                jimmyG = submission.url
                if jimmyG_old == jimmyG:
                    break
                else:
                    jimmyG_old = jimmyG
                    await ctx.send(jimmyG)
        sleep(60)

bot.run(TOKEN)