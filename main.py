from discord.ext import commands
from dotenv import load_dotenv
import os

from handlers.correct_number_handler import determine_next_number

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="!", self_bot=True)

game_master_id = 422800248935546880
game_location_id = 1379091983053750412
target_bot_id = 996129161825484911

@bot.event
async def on_ready():
    print(f"bot is running. logged in as {bot.user}")


number_to_await = 1
@bot.event
async def on_message(message):
    global number_to_await
    try:
        guild = message.guild.id
    except AttributeError:  return  # channel is a dm
    if guild != game_location_id: return
    if message.author == bot.user: return

    empty_rule_dict = {"div": [], "digsum": [], "root": []}

    if message.content.endswith('money.') and message.author.id == target_bot_id:
        number_to_await = 1
        await message.channel.send("streak failed. send 1 to start again")
        return

    try: number_received = int(message.content)
    except ValueError: return

    print(number_to_await, number_received)
    if number_received == number_to_await:
        number_to_send = determine_next_number(number_to_await, empty_rule_dict, base=10)
        number_to_await = determine_next_number(number_to_send, empty_rule_dict, base=10)
        await message.channel.send(number_to_send)
    return

bot.run(TOKEN)
