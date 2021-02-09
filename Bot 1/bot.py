import discord
import json
import datetime
import asyncio
import random
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle

def get_prefix(client , message):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
status = cycle(['Woke Up!' , 'Checking Server!' , 'Helping Altersplatz!' , 'Moderating Star Explorers!!!' , 'Going for Play!' , 'Doing HomeWork' , 'Moderating Star Explorers' , 'Doing something else'])

# General Commands

@client.event
async def on_ready():
    change_status.start()
    print('I am Online!')

@tasks.loop(minutes=10)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))

@client.event
async def on_guild_join(guild):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '>'

@client.event
async def on_guild_remove(guild):
    with open('prefix.json' , 'r') as f:
        prefix = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefix.json' , 'w') as f:
        json.dump(prefixes , f , indent = 4)

# Help Commands

@client.command()
async def Help(ctx):
    await ctx.send('Join my Support Server: https://discord.gg/4DkNnk8p2m')
    await ctx.send('Avaliable Commands are `>ping` , `>purge` , `>kick` , `>ban` and `>unban`.')
    await ctx.send('To know more about these commands , do >help_{command_name}!')


@client.command()
async def help_ping(ctx):
    await ctx.send('It is used to check my status and ping/latency level!')
    await ctx.send('**Usage:** >ping')

@client.command()
async def help_purge(ctx):
    await ctx.send('I will delete the amount oof message **YOU** say to!')
    await ctx.send('**Usage:** >purge {amount}')

@client.command()
async def help_kick(ctx):
    await ctx.send('I will kick the member **YOU**  mention.')
    await ctx.send('**Usage:** >kick {user}')

@client.command()
async def help_ban(ctx):
    await ctx.send('I will ban the member **YOU** mention.')
    await ctx.send('**Usage:** >ban {user}')

@client.command()
async def help_unban(ctx):
    await ctx.send('I will unban a previously banned user.')
    await ctx.send('**Usage:** >unban {User_Name####}')

# Events

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

# Commands

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}')

@client.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx , amount = int):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'I have deleted {limit} messages')
    # @purge.error

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx , member : discord.Member  , * , reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'Kicked {member.mention}')
    # @kick.error

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx , member : discord.Member , * , reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'Banned {member.mention}')
    # @ban.error

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx , * , member):
    banned_users = await ctx.guild.bans()
    member_name , member_discriminator = member.split('#')
    # @unban.error

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name , user.discriminator) == (member_name , member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
@commands.has_permissions(administrator = True)
async def change_prefix(ctx , prefix):
    with open('prefixes.json' , 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json' , 'w') as f:
        json.dump(prefixes , f , indent = 4)

    await ctx.send(f'Prefix changed to: {prefix}')

# Lockdown

@client.command()
async def staff_day_lockdown(ctx):
    await ctx.send('The server is locked due to staff day!')
    await ctx.send('**You are not muted , please DO NOT DM ANY STAFF MEMBER ABOUT THIS.**')
    await ctx.send('The server will be locked for **24 hours**.')

@client.command()
async def raid_lockdown(ctx):
    await ctx.send('The server has been locked due to a raid.')

@client.command()
async def lockdown_end(ctx):
    await ctx.send('The lockdown has ended :)')

# Error Commands

@client.event
async def on_command_error(ctx , error):
    if isinstance(error , commands.CommandNotFound):
        await ctx.send('Invalid Command Used')

@purge.error
async def purge_error(ctx , error):
    if isinstance(error , commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete!')

@kick.error
async def kick_error(ctx , error):
    if isinstance(error , commands.MissingRequiredArgument):
        await ctx.send('Please mention a user!')

@ban.error
async def ban_error(ctx , error):
    if isinstance(error , commands.MissingRequiredArgument):
        await ctx.send('Please mention a user!')

@unban.error
async def unban_error(ctx , error):
    if isinstance(error , commands.MissingRequiredArgument):
        await ctx.send('Please mention User_Name#### of a banned user!')

client.run('ADD BOT TOKEN')
