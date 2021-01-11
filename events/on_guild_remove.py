from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database


class OnGuildRemove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"[DEL] Guild: {guild} heeft de bot verwijderd.")

        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM settings WHERE guild_id = %s", (guild.id,))
        cursor.execute(f"DELETE FROM server_blacklist WHERE guild_id = %s", (guild.id,))
        cursor.execute(f"DELETE FROM server_whitelist WHERE guild_id = %s", (guild.id,))
        db.commit()
        db.close()


def setup(client):
    client.add_cog(OnGuildRemove(client))
