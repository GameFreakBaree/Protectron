import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector
import re


class CommandsPrefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix=None):
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

        valid_chars = "`A-Z`, `a-z`, `!`, `<`, `>`, `~`, `.`, `,`, `^`, `-`, `$`, `/`"

        if language == "nl":
            invalid_prefix = f"De prefix bevat ongeldige karakters.\nGeldige karaters zijn:\n{valid_chars}"
            max_length_prefix = "De prefix is gelimiteerd tot een maximum van 5 karakters."
            invalid_arguments = "Ongeldige argumenten."
            embed_desc = "Je hebt de prefix geupdate naar"
        else:
            invalid_prefix = f"Prefix contains invalid characters.\nValid characters are:\n{valid_chars}"
            max_length_prefix = "The prefix is limited to a maximum of 5 characters."
            invalid_arguments = "Invalid Arguments."
            embed_desc = "You've updated the prefix to"

        if prefix is not None:
            lengte_prefix = len(prefix)

            if lengte_prefix <= 5:
                regex = re.sub(r'[^A-Za-z!~,.<>^/$-]', '', prefix)

                if prefix == regex:
                    cursor.execute(f"UPDATE settings SET prefix = %s WHERE guild_id = %s", (prefix, ctx.guild.id))
                    db.commit()

                    embed = discord.Embed(
                        description=f"{embed_desc} `{regex}`",
                        color=embedcolor
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"{invalid_prefix}")
            else:
                await ctx.send(f"{max_length_prefix}")
        else:
            await ctx.send(f"{invalid_arguments}")
        db.close()

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(CommandsPrefix(client))
