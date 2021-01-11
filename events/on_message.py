from discord.ext import commands
from settings import host, user, passwd, database
import mysql.connector


class EventsReactOnTag(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == f"<@!{self.client.user.id}> prefix":
            db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            cursor = db.cursor()

            cursor.execute("SELECT prefix FROM settings WHERE guild_id = %s", (message.guild.id,))
            prefix_tuple = cursor.fetchone()

            db.close()

            if prefix_tuple is None:
                prefix = "-"
            else:
                prefix = prefix_tuple[0]

            await message.channel.send(f"The prefix of this bot is `{prefix}`\n"
                                       f"If you want to see all commands, please use `{prefix}help`!")


def setup(client):
    client.add_cog(EventsReactOnTag(client))
