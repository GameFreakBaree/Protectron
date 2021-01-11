import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class CommandsLanguage(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lang'])
    @commands.has_permissions(administrator=True)
    async def language(self, ctx, option=None):
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
            invalid_language = "Dat is geen geldige taal.\nGeldige talen zijn:\n`en`, `nl`"
            invalid_arguments = "Ongeldige argumenten."
            embed_desc = "Je hebt de taal veranderd naar"
        else:
            invalid_language = "That's not a valid language.\nValid languages are:\n`en`, `nl`"
            invalid_arguments = "Invalid Arguments."
            embed_desc = "You've updated the language to"

        languages = ['en', 'nl']

        if option is not None:
            if option.lower() in languages:
                cursor.execute(f"UPDATE settings SET language = %s WHERE guild_id = %s", (option.lower(), ctx.guild.id))
                db.commit()

                embed = discord.Embed(
                    description=f"{embed_desc} `{option.upper()}`",
                    color=embedcolor
                )
                embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{invalid_language}")
        else:
            await ctx.send(f"{invalid_arguments}")
        db.close()

    @language.error
    async def language_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(CommandsLanguage(client))
