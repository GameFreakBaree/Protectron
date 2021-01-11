from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database


class OnGuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"[ADD] Guild: {guild} heeft de bot toegevoegd.")

        insert_guilddata = "INSERT INTO settings (guild_id, modus, logchannel, prefix, language) VALUES (%s, %s, %s, %s, %s)"
        record = (guild.id, 0, 0, "-", "en")

        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()
        cursor.execute(insert_guilddata, record)
        db.commit()
        db.close()


def setup(client):
    client.add_cog(OnGuildJoin(client))
