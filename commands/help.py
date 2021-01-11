import discord
from discord.ext import commands
import datetime
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class HelpMsg(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    @commands.has_permissions(manage_guild=True)
    async def helpcmd(self, ctx):
        db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        cursor = db.cursor()

        cursor.execute("SELECT prefix FROM settings WHERE guild_id = %s", (ctx.guild.id,))
        prefix_tuple = cursor.fetchone()

        db.close()

        if prefix_tuple is None:
            prefix = "-"
        else:
            prefix = prefix_tuple[0]

        if ctx.author == ctx.guild.owner:
            embed = discord.Embed(
                description=f"**__Owner Commands__**\n"
                            f"\n• **{prefix}reset <all | blacklist | whitelist>**\n*Remove data from the bot in the guild.*"
                            f"\n\n**__Admin Commands__** *- Requires ADMINISTRATOR*\n"
                            f"\n• **{prefix}set-mode <mode_number>**\n*Control what the bot does if a blacklisted person joins the server.*"
                            f"\n\n• **{prefix}prefix <prefix>**\n*Setup the prefix for the bot.*"
                            f"\n\n• **{prefix}logchannel <#channel>**\n*Setup the log channel.*"
                            f"\n\n• **{prefix}language <en | nl>**\n*Set your language to english or dutch.*"
                            f"\n\n**__Moderator Commands__** *- Requires MANAGE_SERVER*\n"
                            f"\n• **{prefix}blacklist <add | remove> <name> <reason>**\n*Add/remove someone to/from your blacklist (server only).*"
                            f"\n\n• **{prefix}whitelist <add | remove> <name> <reason>**\n*Add/remove someone to/from your whitelist (server only).*"
                            f"\n\n• **{prefix}blacklist list**\n*See all users on your blacklist.*"
                            f"\n\n• **{prefix}whitelist list**\n*See all users on your whitelist.*"
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help**\n*Displays this Embed.*"
                            f"\n\n• **{prefix}ping**\n*Get the ping in milliseconds of the bot.*"
                            f"\n\n• **{prefix}info**\n*Get all the information about the bot.*"
                            f"\n\n• **{prefix}invite**\n*Get an invite to add the bot.*",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                description=f"\n\n**__Admin Commands__** *- Requires ADMINISTRATOR*\n"
                            f"\n• **{prefix}set-mode <mode_number>**\n*Control what the bot does if a blacklisted person joins the server.*"
                            f"\n\n• **{prefix}set-prefix <prefix>**\n*Setup the prefix for the bot.*"
                            f"\n\n• **{prefix}set-logchannel <#channel>**\n*Setup the log channel.*"
                            f"\n\n• **{prefix}set-language <en | nl>**\n*Set your language to english or dutch.*"
                            f"\n\n**__Moderator Commands__** *- Requires MANAGE_SERVER*\n"
                            f"\n• **{prefix}blacklist <add | remove> <name> <reason>**\n*Add/remove someone to/from your blacklist (server only).*"
                            f"\n\n• **{prefix}whitelist <add | remove> <name> <reason>**\n*Add/remove someone to/from your whitelist (server only).*"
                            f"\n\n• **{prefix}blacklist list**\n*See all users on your blacklist.*"
                            f"\n\n• **{prefix}whitelist list**\n*See all users on your whitelist.*"
                            f"\n\n**__Member Commands__**\n"
                            f"\n• **{prefix}help**\n*Displays this Embed.*"
                            f"\n\n• **{prefix}ping**\n*Get the ping in milliseconds of the bot.*"
                            f"\n\n• **{prefix}info**\n*Get all the information about the bot.*"
                            f"\n\n• **{prefix}invite**\n*Get an invite to add the bot.*",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @helpcmd.error
    async def helpcmd_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            cursor = db.cursor()

            cursor.execute("SELECT prefix FROM settings WHERE guild_id = %s", (ctx.guild.id,))
            prefix_tuple = cursor.fetchone()

            db.close()

            if prefix_tuple is None:
                prefix = "-"
            else:
                prefix = prefix_tuple[0]

            embed = discord.Embed(
                description=f"\n• **{prefix}help**\n*Displays this Embed.*"
                            f"\n\n• **{prefix}ping**\n*Get the ping in milliseconds of the bot.*"
                            f"\n\n• **{prefix}info**\n*Get all the information about the bot.*"
                            f"\n\n• **{prefix}invite**\n*Get an invite to add the bot.*",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HelpMsg(client))
