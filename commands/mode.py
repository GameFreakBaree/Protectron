import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class CommandsMode(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mode(self, ctx, option=None):
        db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM settings WHERE guild_id = {ctx.guild.id}")
        settings = cursor.fetchone()

        if settings is None:
            insert_guilddata = "INSERT INTO settings (guild_id, modus, logchannel, prefix, language) VALUES (%s, %s, %s, %s, %s)"
            record = (ctx.guild.id, 0, 0, "-", "en")
            cursor.execute(insert_guilddata, record)
            db.commit()

            cursor.execute(f"SELECT * FROM settings WHERE guild_id = {ctx.guild.id}")
            settings = cursor.fetchone()

        if settings is None:
            language = "en"
            oude_modus = 0
        else:
            language = settings[4]
            oude_modus = settings[1]

        if language == "nl":
            no_integer = f"Je hebt geen geldig getal ingegeven.\n\n**Gebruik command:**\n`{settings[3]}set-mode <nummer>`\n\n**Modus Lijst:**\n__0__ - Waarschuwingsbericht in logs kanaal als een gebruiker van de zwarte lijst joined.\n__1__ - Automatisch bannen als een gebruiker van de zwarte lijst joined.\n__2__ - Automatisch mute role geven als een gebruiker van de zwarte lijst joined.\n__More coming soon!__"
            modus0 = "Modus 0 is geactiveerd. Je krijgt nu een waarschuwing als een blacklisted gebruiker joined."
            modus1 = "Modus 1 is geactiveerd. De gebruiker wordt nu verbannen als hij op de blacklist staat."
            modus2 = "Modus 2 is geactiveerd. De gebruiker zal nu gemute worden als hij op de blacklist staat."
            already_activated = "Deze modus is al geactiveerd."
        else:
            no_integer = f"No valid number was given.\n\n**Usage:**\n`{settings[3]}set-mode <number>`\n\n**Mode List:**\n__0__ - Warnings message in log channel when blacklisted user joins.\n__1__ - Auto banning when blacklisted user joins.\n__2__ - Auto muting when blacklisted user joins.\n__More coming soon!__"
            modus0 = "Mode 0 activated. You will now receive warnings if a blacklisted user joins."
            modus1 = "Mode 1 activated. The user will be banned if he tries to join while on a blacklist."
            modus2 = "Mode 2 activated. The user will be muted if he tries to join while on a blacklist."
            already_activated = "This mode has already been activated."

        doorgaan = False
        mode = "null"

        try:
            option = int(option)

            if oude_modus == option:
                await ctx.send(f"{already_activated}")
            else:
                if option == 0:
                    doorgaan = True
                    mode = modus0
                elif option == 1:
                    doorgaan = True
                    mode = modus1
                elif option == 3:
                    doorgaan = True
                    mode = modus2
                else:
                    option = "ERROR"
                    int(option)
        except ValueError:
            embed = discord.Embed(
                description=f"{no_integer}",
                color=embedcolor
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)

        if doorgaan:
            cursor.execute("UPDATE settings SET modus = %s WHERE guild_id = %s", (option, ctx.guild.id))
            db.commit()

            embed = discord.Embed(
                description=f"{mode}",
                color=embedcolor
            )
            embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)

        db.close()

    @mode.error
    async def mode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(CommandsMode(client))
