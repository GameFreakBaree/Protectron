import discord
from discord.ext import commands
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer


class CommandsSetMuteRole(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="set-muterole")
    @commands.has_permissions(manage_guild=True)
    async def set_mute_role(self, ctx, *, role: discord.Role):
        db_bumblebee = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        bumblebee_cursor = db_bumblebee.cursor()

        bumblebee_cursor.execute("SELECT * FROM bumblebee_guildsettings WHERE guild_id = %s", (ctx.guild.id,))
        guildsettings = bumblebee_cursor.fetchone()

        if guildsettings is None:
            insert_guilddata = "INSERT INTO bumblebee_guildsettings (guild_id, logchannel_id, mute_role, prefix) VALUES (%s, %s, %s, %s)"
            record = (ctx.guild.id, 0, 0, "b!")
            bumblebee_cursor.execute(insert_guilddata, record)
            db_bumblebee.commit()

        bumblebee_cursor.execute(f"UPDATE bumblebee_guildsettings SET mute_role = %s WHERE guild_id = %s", (role.id, ctx.guild.id))
        db_bumblebee.commit()
        db_bumblebee.close()

        embed = discord.Embed(
            description=f"You've updated the mute role to {role.mention}",
            color=embedcolor
        )
        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @set_mute_role.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send(f"Role was not found.")
        else:
            raise error


def setup(client):
    client.add_cog(CommandsSetMuteRole(client))
