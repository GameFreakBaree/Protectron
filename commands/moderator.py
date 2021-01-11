import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector


class CommandsBlacklist(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mod(self, ctx, option: str, member: int, *, reason="Unspecified"):
        moderator_list = [643072638075273248, 747018426576535562, 282229113262178306, 513020026488619012]
        # GameFreakBaree, Jefke, ~Joonthom, Tibo
        if ctx.author.id in moderator_list:
            await ctx.message.delete()
            db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
            cursor = db.cursor()

            if option.lower() == "add":
                if member is not None:
                    cursor.execute(f"SELECT * FROM blacklist WHERE user_id = %s", (member,))
                    blacklist_user = cursor.fetchone()

                    if blacklist_user is None:
                        insert_data = "INSERT INTO blacklist (user_id, moderator, reason) VALUES (%s, %s, %s)"
                        record = (member, ctx.author.id, f"{reason}")
                        cursor.execute(insert_data, record)
                        db.commit()

                        embed = discord.Embed(
                            description=f"User {member} is added to the blacklist.",
                            color=embedcolor
                        )
                        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        embed.set_footer(text=footer)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("This user is already blacklisted.")
            elif option.lower() == "remove":
                if member is not None:
                    cursor.execute(f"SELECT * FROM blacklist WHERE user_id = %s", (member,))
                    blacklist_user = cursor.fetchone()

                    if blacklist_user is not None:
                        cursor.execute("DELETE FROM blacklist WHERE user_id = %s", (member,))
                        db.commit()

                        embed = discord.Embed(
                            description=f"User {member} has been removed from the blacklist.",
                            color=embedcolor
                        )
                        embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                        embed.set_footer(text=footer)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("This user was not blacklisted.")
            db.close()


def setup(client):
    client.add_cog(CommandsBlacklist(client))
