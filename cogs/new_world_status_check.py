from datetime import datetime

import nextcord
import requests
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.global_utils import crimson, sec_to_hours

load_dotenv()


def getserver():
    url = "https://nwdb.info/server-status/servers.json"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/94.0.4606.61 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    return response.json()


class NWW_Status(commands.Cog, name="New World Server Status"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="NW Server Status",
        aliases=["nwstatus"],
        help="Displays Status of a specific server",
    )
    async def nwstatus(self, ctx, world_name):
        responsejson = getserver()

        status = responsejson["success"]

        if status is None:
            print("error parsing stream")
        elif status:
            base = responsejson["data"]["servers"]
            # print(base)
            for each in base:
                world = each[4]
                current_players = each[1]
                maximum_players = each[0]
                current_queue = each[2]
                current_queue_time = each[3]
                current_status = each[8]

                if world == world_name:
                    # Capitalize first letter
                    world_name = world_name.capitalize()

                    # Get current time
                    now = datetime.now()

                    embed = nextcord.Embed(
                        title=f"{world_name}\n\n",
                        description=f"**__Current Players__**\n{current_players}/{maximum_players}\n\n**__Players in "
                                    f"Queue__**\n{current_queue}\n\n**__Queue Time__**\n{sec_to_hours(current_queue_time)}\n\n"
                                    f"**__Status__**\n{current_status}",
                        colour=crimson,
                        timestamp=now,
                    )
                    embed.set_footer(text="New World bot")
                    file = nextcord.File(
                        "./assets/images/nw_logo.png", filename="nw_logo.png"
                    )
                    embed.set_thumbnail(url="attachment://nw_logo.png")

                    await ctx.send(file=file, embed=embed)
        else:
            print("result fail")


def setup(bot):
    bot.add_cog(NWW_Status(bot))
