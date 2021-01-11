import discord
from discord.ext import commands
import datetime
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer


class CommandsReset(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reset(self, ctx, option=None):
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
            option_is_none = ""
            option_is_incorrect = ""
        else:
            option_is_none = ""
            option_is_incorrect = ""

        reset = False
        if option is not None:
            if option.lower() == "all":
                cursor.execute(f"DELETE FROM settings WHERE guild_id = %s", (ctx.guild.id,))
                cursor.execute(f"DELETE FROM server_blacklist WHERE guild_id = %s", (ctx.guild.id,))
                cursor.execute(f"DELETE FROM server_whitelist WHERE guild_id = %s", (ctx.guild.id,))
                db.commit()

                insert_guilddata = "INSERT INTO settings (guild_id, modus, logchannel, prefix, language) VALUES (%s, %s, %s, %s, %s)"
                record = (ctx.guild.id, 0, 0, "-", "en")
                cursor.execute(insert_guilddata, record)
                db.commit()

                reset = True
            elif option.lower() == "blacklist":
                cursor.execute(f"DELETE FROM server_blacklist WHERE guild_id = %s", (ctx.guild.id,))
                db.commit()

                reset = True
            elif option.lower() == "whitelist":
                cursor.execute(f"DELETE FROM server_whitelist WHERE guild_id = %s", (ctx.guild.id,))
                db.commit()

                reset = True
            else:
                await ctx.send(f"{option_is_incorrect}")
        else:
            await ctx.send(f"{option_is_none}")

        db.close()

        if reset:
            embed = discord.Embed(
                description=f"**Reset {option.title()} Data Complete!**",
                color=embedcolor,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)

    @reset.error
    async def reset_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("You don't have enough permissions. "
                           "You need to be the **OWNER** of this Guild to use this command.")
        else:
            raise error


def setup(client):
    client.add_cog(CommandsReset(client))
