import asyncio
import os
import discord
from discord.ext import commands
from settings import host, user, passwd, database, token, bot_name, folder_list
import mysql.connector

intents = discord.Intents.default()
intents.members = True


def get_prefix(client, message):
    db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = db.cursor()
    cursor.execute("SELECT prefix FROM settings WHERE guild_id = %s", (message.guild.id,))
    prefix_tuple = cursor.fetchone()
    db.close()

    if prefix_tuple is None:
        prefix = "-"
    else:
        prefix = prefix_tuple[0]

    return prefix


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
client.remove_command("help")


def blacklist():
    db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM blacklist")
    blacklist_rows = cursor.fetchall()
    db.close()

    return len(blacklist_rows)


async def change_status():
    await client.wait_until_ready()
    while client.is_ready():
        users = blacklist()
        status = discord.Activity(name=f"{users} Users Blacklisted", type=discord.ActivityType.watching)
        await client.change_presence(activity=status)

        await asyncio.sleep(60)

        status = discord.Activity(name=f"{len(client.guilds)} Servers", type=discord.ActivityType.watching)
        await client.change_presence(activity=status)

        await asyncio.sleep(60)

for folder in folder_list:
    print(f"[{bot_name}] ----------------------[ {folder.title()} ]--------------------")
    for filename in os.listdir(f'./{folder}'):
        if filename.endswith('.py'):
            print(f"[{bot_name}] {folder.title()} > {filename[:-3]} > Loaded!")
            client.load_extension(f'{folder}.{filename[:-3]}')
print(f"[{bot_name}] ------------------------------------------------------")

client.loop.create_task(change_status())
client.run(token)
