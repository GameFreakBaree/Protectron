import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database, embedcolor


class InviteCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT language FROM settings WHERE guild_id = {ctx.guild.id}")
        language = cursor.fetchone()
        db.close()

        if language is None:
            language = ("en",)

        if language[0] == "nl":
            embed = discord.Embed(
                description=f":link: Invite me hier: [Klik hier](https://discord.com/api/oauth2/authorize?client_id=785976677829705740&permissions=268520516&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot)",
                color=embedcolor
            )
        else:
            embed = discord.Embed(
                description=f":link: Invite me here: [Click Here](https://discord.com/api/oauth2/authorize?client_id=785976677829705740&permissions=268520516&redirect_uri=https%3A%2F%2Fdiscord.gg%2F5gvn5pn&scope=bot)",
                color=embedcolor
            )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(InviteCmd(client))
