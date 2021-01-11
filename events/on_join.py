from discord.ext import commands
import discord
import mysql.connector
from settings import host, user, passwd, database, embedcolor, footer


class OnGuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            ban_member = False
            on_list = "global blacklist"

            db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
            cursor = db.cursor()

            cursor.execute(f"SELECT * FROM server_whitelist WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
            whitelist = cursor.fetchone()

            if whitelist is None:
                cursor.execute(f"SELECT * FROM server_blacklist WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
                server_blacklist = cursor.fetchone()

                if server_blacklist is None:
                    cursor.execute(f"SELECT * FROM blacklist WHERE user_id = {member.id}")
                    blacklist = cursor.fetchone()

                    if blacklist is not None:
                        ban_member = True
                else:
                    ban_member = True
            else:
                ban_member = True

            if ban_member:
                cursor.execute(f"SELECT * FROM settings WHERE guild_id = {member.guild.id}")
                settings = cursor.fetchone()

                if settings is None:
                    print(f"Error correcting in on_join.py for {member.guild.id}")
                    insert_guilddata = "INSERT INTO settings (guild_id, modus, logchannel, prefix, language) VALUES (%s, %s, %s, %s, %s)"
                    record = (member.guild.id, 0, 0, "-", "en")
                    cursor.execute(insert_guilddata, record)
                    db.commit()

                    modus = 0
                    logchannel = 0
                    language = "en"
                else:
                    modus = settings[1]
                    logchannel = settings[2]
                    language = settings[4]

                if modus == 1:
                    bot_name = self.client.user.display_name
                    if language == "nl":
                        modus_title = f"{member} probeerde te joinen."
                        modus_desc = f"{member.mention} probeerde te joinen, maar is nu verbannen.\nGebruiker staat op de {on_list}."
                        reason = f"{bot_name}: Automatische gebruiker ban. (Gebruiker staat op de {on_list})"
                    else:
                        modus_title = f"{member} tried to join."
                        modus_desc = f"{member.mention} tried to join, but is now banned.\nUser is on the {on_list}."
                        reason = f"{bot_name}: Automatic user ban. (User is on {on_list})"
                    await member.ban(reason=reason)
                else:
                    if language == "nl":
                        modus_title = f"{member} is gejoined."
                        modus_desc = f"{member.mention} is gejoined, maar staat op de {on_list}."
                    else:
                        modus_title = f"{member} joined."
                        modus_desc = f"{member.mention} joined, but is on the {on_list}."

                try:
                    if logchannel != 0:
                        log_channel = self.client.get_channel(logchannel)

                        embed = discord.Embed(
                            title=f"{modus_title}",
                            description=f"{modus_desc}",
                            color=embedcolor
                        )
                        embed.set_footer(text=f"{footer}")
                        embed.set_author(name=member, icon_url=member.avatar_url)
                        await log_channel.send(embed=embed)
                except AttributeError:
                    pass
            db.close()


def setup(client):
    client.add_cog(OnGuildJoin(client))
