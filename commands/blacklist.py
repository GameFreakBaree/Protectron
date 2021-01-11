import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class CommandsBlacklist(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='blacklist')
    @commands.has_permissions(manage_guild=True)
    async def blacklist(self, ctx, option: str, member: discord.Member = None, *, reason="Unspecified"):
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
            invalid_arguments = "Ongeldige argumenten."
            user_already_blacklisted = "Deze gebruiker staat al op de zwarte lijst."
            add_embed_desc = "is toegevoegd op de zwarte lijst."
            user_not_blacklisted = "Deze gebruiker staat nog niet op de zwarte lijst."
            remove_embed_desc = "is van de zwarte lijst afgehaald."
            user_is_bot = "Deze gebruiker is een bot, ja kan geen bots op de zwarte lijst zetten."
        else:
            invalid_arguments = "Invalid Arguments."
            user_already_blacklisted = "This user is already blacklisted."
            add_embed_desc = "is added to the blacklist."
            user_not_blacklisted = "This user was not blacklisted."
            remove_embed_desc = "has been removed from the blacklist."
            user_is_bot = "This user is a bot, you cannot blacklist bots."

        if option.lower() == "add":
            if member is not None:
                if not member.bot:
                    cursor.execute(f"SELECT * FROM server_blacklist WHERE guild_id = %s AND user_id = %s", (ctx.guild.id, member.id))
                    blacklist_user = cursor.fetchone()

                    if blacklist_user is None:
                        insert_data = "INSERT INTO server_blacklist (guild_id, user_id, reason) VALUES (%s, %s, %s)"
                        record = (ctx.guild.id, member.id, f"{reason}")
                        cursor.execute(insert_data, record)
                        db.commit()

                        embed = discord.Embed(
                            description=f"{member.mention} {add_embed_desc}",
                            color=embedcolor
                        )
                        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        embed.set_footer(text=footer)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"{user_already_blacklisted}")
                else:
                    await ctx.send(f"{user_is_bot}")
            else:
                await ctx.send(f"{invalid_arguments}")
        elif option.lower() == "remove":
            if member is not None:
                if not member.bot:
                    cursor.execute(f"SELECT * FROM server_blacklist WHERE guild_id = %s AND user_id = %s", (ctx.guild.id, member.id))
                    blacklist_user = cursor.fetchone()

                    if blacklist_user is not None:
                        cursor.execute("DELETE FROM server_blacklist WHERE guild_id = %s AND user_id = %s", (ctx.guild.id, member.id))
                        db.commit()

                        embed = discord.Embed(
                            description=f"{member.mention} {remove_embed_desc}",
                            color=embedcolor
                        )
                        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        embed.set_footer(text=footer)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"{user_not_blacklisted}")
                else:
                    await ctx.send(f"{user_is_bot}")
            else:
                await ctx.send(f"{invalid_arguments}")
        elif option.lower() == "list":
            await ctx.send("Coming soon!")
        else:
            await ctx.send(f"{invalid_arguments}")
        db.close()


def setup(client):
    client.add_cog(CommandsBlacklist(client))
