import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class CommandsSetLogchannel(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='set-logchannel', aliases=['set-log-channel', 'set-logs'])
    @commands.has_permissions(administrator=True)
    async def set_logchannel(self, ctx, *, channel: discord.TextChannel):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM settings WHERE guild_id = {ctx.guild.id}")
        settings = cursor.fetchone()

        if settings is None:
            insert_guilddata = "INSERT INTO settings (guild_id, modus, logchannel, prefix, language) VALUES (%s, %s, %s, %s, %s)"
            record = (ctx.guild.id, 0, 0, "-", "en")
            cursor.execute(insert_guilddata, record)
            db.commit()

        if settings is None:
            language = "en"
        else:
            language = settings[4]

        if language == "nl":
            embed_desc = "Je hebt het log kanaal geupdate naar"
        else:
            embed_desc = "You've updated the logchannel to"

        cursor.execute(f"UPDATE settings SET logchannel = %s WHERE guild_id = %s", (channel.id, ctx.guild.id))
        db.commit()
        db.close()

        embed = discord.Embed(
            description=f"{embed_desc} {channel.mention}",
            color=embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @set_logchannel.error
    async def set_logchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel was not found.")
        else:
            raise error


def setup(client):
    client.add_cog(CommandsSetLogchannel(client))
