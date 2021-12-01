import os

import requests
import ujson as json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dhooks import Embed, File, Webhook
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.global_utils import crimson, flatten, news_exists, nww_exists

load_dotenv()
nww_webhook = os.getenv("discord_updates")


def getNWWUpdates():
    url = "https://newworldapi.herokuapp.com/news/updates"
    response = requests.get(url)
    return response.json()


def getNWWUpdatesV2():
    url = "https://newworldapi.herokuapp.com/forums/notice"
    response = requests.get(url)
    return response.json()


def getNWWUpdatesV3():
    url = "https://newworldapi.herokuapp.com/forums/updates"
    response = requests.get(url)
    return response.json()


class NWW_Patch(commands.Cog, name="New World Patch Notes"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 200})

    async def nww_patch_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_patch_notes.json"

        # call API
        response_json = getNWWUpdates()

        title = response_json["data"][0]["title"]
        description = response_json["data"][0]["description"]
        thumbnail = response_json["data"][0]["thumbnail"]
        url = response_json["data"][0]["url"]

        # check if file exists
        news_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            return
        elif check_file_json != title:

            hook = Webhook(nww_webhook)

            embed = Embed(
                title="New World",
                description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="NWW Bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            with open(saved_json, "w") as updated:
                json.dump(response_json, updated, ensure_ascii=False)
            updated.close()

    async def nww_patch_monitorv2(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_forum_updates.json"

        # call API
        response_json = getNWWUpdatesV2()

        title = response_json["data"][0]["title"]
        # description = response_json["data"][0]["description"]
        thumbnail = (
            "https://images.ctfassets.net/j95d1p8hsuun/12Tl0sQL6vNRfXPkIrfuaz"
            "/2374cc44fec67de6b53bcc080a57345d/keyart2.jpg "
        )
        url = response_json["data"][0]["url"]

        # check if file exists
        nww_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            return
        elif check_file_json != title:

            hook = Webhook(nww_webhook)

            embed = Embed(
                title="New World Forums",
                description=f"[{title}]({url})\n\n",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="NWW Bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            with open(saved_json, "w") as updated:
                json.dump(response_json, updated, ensure_ascii=False)
            updated.close()

    async def nww_patch_monitorv3(self):

        saved_json = "nww_forum_updates_2.json"

        # call API
        response_json = getNWWUpdatesV3()

        title = response_json["data"][0]["title"]
        thumbnail = (
            "https://images.ctfassets.net/j95d1p8hsuun/12Tl0sQL6vNRfXPkIrfuaz"
            "/2374cc44fec67de6b53bcc080a57345d/keyart2.jpg "
        )
        url = response_json["data"][0]["url"]

        # check if file exists
        nww_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            return
        elif check_file_json != title:

            hook = Webhook(nww_webhook)

            embed = Embed(
                title="New World Forums",
                description=f"[{title}]({url})\n\n\n",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            with open(saved_json, "w") as updated:
                json.dump(response_json, updated, ensure_ascii=False)
            updated.close()

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.nww_patch_monitor, "interval", minutes=30)
        scheduler.add_job(self.nww_patch_monitorv2, "interval", minutes=31)
        scheduler.add_job(self.nww_patch_monitorv3, "interval", minutes=32)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(NWW_Patch(bot))
