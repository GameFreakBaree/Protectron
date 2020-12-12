import discord
from discord.ext import commands
import time

start_time = time.time()


class PingCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["uptime"])
    async def ping(self, ctx):
        ping = round(self.client.latency * 1000)

        if ping > 1000:
            embedcolor = 0xEC0808
        elif 1000 >= ping >= 250:
            embedcolor = 0xFF8A00
        else:
            embedcolor = 0x01D31E

        current_uptime = time.time()
        difference = int(round(current_uptime - start_time))
        if difference >= 86400:
            uptime = time.strftime('%-dd %-Hh %-Mm %-Ss', time.gmtime(difference))
        else:
            uptime = time.strftime('%-Hh %-Mm %-Ss', time.gmtime(difference))

        embed = discord.Embed(
            description=f"**Ping:** {ping}ms\n**Uptime:** {uptime}",
            color=embedcolor
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PingCmd(client))
