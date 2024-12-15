import math
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="bank.", self_bot=True)

@bot.event
async def on_ready():
    print(f"bot is running. logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot or message.channel.id != 1317905858687930369:
        return
    print(message.content)

    def regerplatz(geld2, rate2):
        return math.ceil(geld2 ** 0.5 / 10) / (4 * rate2)

    if message.content.startswith("bank.offer"):
        try:
            _, geld, rate = message.content.split(" ")
        except ValueError:
            await message.channel.send("hast mit den arguments gekackt")
            return

        try:
            geld = int(geld)
            rate = int(rate)
        except ValueError:
            await message.channel.send("integer bitte")
            return

        reingeschissen = 0
        if geld < 1000:
            await message.channel.send("1000 ist untergrenze für geld bratan")
            reingeschissen += 1
        if geld > 1000000:
            await message.channel.send("du kannst dir nicht mehr als 1e6 geld leihen")
            reingeschissen += 1
        if rate < 1 or rate > 100:
            await message.channel.send("rate von 1% bis 100%")
            reingeschissen += 1

        if reingeschissen:
            await message.channel.send(f"hast{' doppelt' if reingeschissen == 2 else ''} reingeschissen{', wie kann man nur so ein blöder spast sein' if reingeschissen == 2 else ''}.")
            return

        user_id = message.author.id
        result = geld, rate, int(regerplatz(geld, rate) * 100), int(geld * (1 + regerplatz(geld, rate)))
        for i in result:
            print(i)
        await message.channel.send(f"~tradeoffer <@{user_id}> you_get: money: {geld} I_get: contract: perc: {rate}%; limit: {int(geld * (1 + regerplatz(geld, rate)))}")

    if message.content.startswith("bank.help"):
        await message.channel.send("`bank.offer <geld> <rückzahlrate in %>`\nExample: `bank.offer 100000 30`")

bot.run(TOKEN)
