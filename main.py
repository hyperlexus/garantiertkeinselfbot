import math
from datetime import date
from time import sleep

from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="bank.", self_bot=True)

is_christmas_complete = False

allowed_users = (422800248935546880, 649457215564152852, 290148556776407050, 468786219258740756)

@bot.event
async def on_ready():
    print(f"bot is running. logged in as {bot.user}")

@bot.event
async def on_message(message):
    global is_christmas_complete
    if message.author == bot.user or message.author.bot or message.channel.id != 1317905858687930369:
        return
    user_id = message.author.id

    if not is_christmas_complete and date.today().month == 12 and date.today().day == 24 and message.guild.id == 995966314877300737:
        await message.channel.send("ES IST WEIHNACHTEN HURRUH")
        for spast in (422800248935546880, 649457215564152852, 468786219258740756, 290148556776407050):
            await message.channel.send(f"~tradeoffer <@{spast}> you_get: money: 1000")
        is_christmas_complete = True

    def regerplatz(geld2, rate2):
        return math.ceil(geld2 ** 0.5 / 10) / (4 * rate2)

    if message.content.startswith("bank.offer"):
        if user_id not in allowed_users:
            await message.channel.send("you do not have an account at the bank!")
            return
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

        result = geld, rate, int(regerplatz(geld, rate) * 100), int(geld * (1 + regerplatz(geld, rate)))
        for i in result:
            print(i)
        await message.channel.send(f"~tradeoffer <@{user_id}> you_get: money: {geld} I_get: contract: perc: {rate}%; limit: {int(geld * (1 + regerplatz(geld, rate)))}")

    elif message.content.startswith("bank.help"):
        await message.channel.send("die bank ist eine separate entity die geld hat und es für ihren eigenen zweck verleiht.\n"
                                   "sie hat folgende commands:\n\n"
                                   "bank.offer: leih dir geld von der bank, und spezifiziere die rate (% von income)\n"
                                   "`bank.offer <geld> <rückzahlrate in %>`\nExample: `bank.offer 100000 30`\n\n"
                                   "bank.donate: schenk der bank geld\n`bank.donate <geld>`\nExample: `bank.donate 10000`\n\n"
                                   "bank.take: nimm geld aus der bank raus. dürfen nur alex und daan, da sie die grünen gründer der bank sind.\n"
                                   "`bank.take <geld>`\nExample: `bank.take 10000`")

    elif message.content.startswith("bank.donate"):
        try:
            _, geld = message.content.split(" ")
        except ValueError:
            await message.channel.send("hast mit den arguments gekackt")
            return
        try:
            geld = int(geld)
        except ValueError:
            await message.channel.send("integer bitte")
            return

        await message.channel.send(f"~tradeoffer <@{user_id}> I_get: money: {geld}")

    elif message.content.startswith("bank.take"):
        if user_id not in (422800248935546880, 649457215564152852):
            await message.channel.send("blud versucht erstmal die bank auszurauben; bomboclaat")
            return
        try:
            _, geld = message.content.split(" ")
        except ValueError:
            await message.channel.send("hast mit den arguments gekackt")
            return
        try:
            geld = int(geld)
        except ValueError:
            await message.channel.send("integer bitte")
            return

        await message.channel.send(f"~tradeoffer <@{user_id}> you_get: money: {geld}")

    elif message.content.startswith("bank.eval"):
        if user_id != 422800248935546880:
            await message.channel.send("das passiert mir nicht nochmal; es passiert nicht was passieren muss und es wird folglich auch nicht gefickt")
            return

        split_message = message.content.split(" ")
        message_to_send = " ".join(split_message[1:])
        await message.channel.send(message_to_send)

    elif message.content.startswith("bank.streak"):
        await message.channel.send("~num")
        await message.channel.send("~last")
        await message.channel.send("~rules")
        await message.channel.send("~base")
        return

bot.run(TOKEN)
