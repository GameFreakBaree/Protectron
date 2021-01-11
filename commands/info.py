import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer


class InfoCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT language FROM settings WHERE guild_id = {ctx.guild.id}")
        language = cursor.fetchone()
        db.close()

        if language is None:
            language = ("en",)

        if language[0] == "nl":
            embed = discord.Embed(
                description=f"__Gemaakt door:__ Siebe#9999"
                            f"\n__Shard:__ 1/1"
                            f"\n\n**Handige URLs**"
                            f"\n[Invite de Bot](https://discord.com/api/oauth2/authorize?client_id=785976677829705740&permissions=268520516&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot)"
                            f" - [Wiki](https://github.com/GameFreakBaree/Protectron/wiki)"
                            f" - [Support Server](https://discord.gg/5gvn5pn)",
                color=embedcolor
            )
        else:
            embed = discord.Embed(
                description=f"__Created by:__ Siebe#9999"
                            f"\n__Shard:__ 1/1"
                            f"\n\n**Useful URLs**"
                            f"\n[Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=785976677829705740&permissions=268520516&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot)"
                            f" - [Wiki](https://github.com/GameFreakBaree/Protectron/wiki)"
                            f" - [Support Server](https://discord.gg/5gvn5pn)",
                color=embedcolor
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(InfoCmd(client))
