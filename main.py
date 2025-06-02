import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

from channel_counter import ChannelCounter

load_dotenv()
TOKEN = os.getenv('TOKEN')
TARGET_GUILD_ID = 1379091983053750412
TARGET_BOT_ID = 996129161825484911

DEFAULT_RULES = {"div": [], "digsum": [], "root": []}
DEFAULT_BASE = 10

bot = commands.Bot(command_prefix="whateveritdoesntmatteritsaselfbotleel", self_bot=True)

DATA_DIR = "counter_data"
MASTER_STATE_FILE = os.path.join(DATA_DIR, "all_channel_states.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

active_counters: dict[int, ChannelCounter] = {}


def save_all_active_counters():
    """Saves the state of all active counters to the json."""
    states_to_save = {}
    for channel_id, counter_instance in active_counters.items():
        states_to_save[str(channel_id)] = counter_instance.get_state()

    try:
        with open(MASTER_STATE_FILE, 'w') as f:
            json.dump(states_to_save, f, indent=4)
    except IOError as e:
        print(f"error saving all counter states: {e}")


def load_all_active_counters() -> dict[int, ChannelCounter]:
    """Loads all counter states from the json."""
    loaded_counters_map: dict[int, ChannelCounter] = {}
    if os.path.exists(MASTER_STATE_FILE):
        try:
            with open(MASTER_STATE_FILE, 'r') as f:
                all_states_data = json.load(f)
                for channel_id_str, state_data in all_states_data.items():
                    try:
                        channel_id_int = int(channel_id_str)
                        loaded_counters_map[channel_id_int] = ChannelCounter.from_state(state_data)
                    except ValueError:
                        print(f"{channel_id_str} has invalid format, don't mess with the json please")
                    except Exception as e_item:
                        print(f"{channel_id_str} couldn't load {e_item} item")
            print(f"loaded {len(loaded_counters_map)} channels")
        except (IOError, json.JSONDecodeError) as e:
            print(f"state file couldn't be loaded. if it was empty, it will now be created.")
    else:
        print(f"state file '{MASTER_STATE_FILE}' not found.")
    return loaded_counters_map


@bot.event
async def on_ready():
    print(f"Bot is running. Logged in as {bot.user}")

    # Load all existing states
    global active_counters
    active_counters = load_all_active_counters()

    guild = bot.get_guild(TARGET_GUILD_ID)
    if not guild:
        print(f"error: server not found")
        return

    print(f"initialising")
    initial_save_needed = False
    for channel in guild.text_channels:
        if channel.id not in active_counters:
            print(f"channel {channel.name} ({channel.id}) not in file. adding it...")
            new_counter = ChannelCounter(
                channel_id=channel.id,
                initial_rules=DEFAULT_RULES.copy(),
                initial_base=DEFAULT_BASE
            )
            active_counters[channel.id] = new_counter
            initial_save_needed = True  # mark that new counters were added
            print(f"channel loaded: {channel.name} ({channel.id}). next number awaited: {new_counter.expected_next_number}")

        current_counter = active_counters[channel.id]
        print(f"channel {channel.name} loaded with id {channel.id}. next number awaited: {current_counter.expected_next_number}.")

    if initial_save_needed:
        save_all_active_counters()

    print(f"initialised. number of monitored channels: {len(active_counters)}")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user: return
    if not message.guild or message.guild.id != TARGET_GUILD_ID:
        return

    counter = active_counters.get(message.channel.id)
    if not counter:  # happens if a channel is created after bot has already been started
        print(f"warning: message received in channel not in the json: {message.channel.id} consider restarting")
        return

    if message.author.id == TARGET_BOT_ID:
        parsed_action = False
        if message.content.startswith("You paid "):
            rule_message = message.content.partition("to add: ")[2]
            counter.parse_rule_update(rule_message)
            save_all_active_counters()
            parsed_action = True

        if parsed_action:
            try:
                await message.add_reaction('👌')
            except Exception as e:
                print(e)
            return

    if "base" in message.content and message.author != bot.user and not message.author.bot:
        # todo
        pass

    number_to_send = counter.process_message(message.content, message.author.id, message.author.bot)

    if number_to_send == -1:
        await message.channel.send(f"skill issue.")
        save_all_active_counters()
        return

    if number_to_send is not None:
        try:
            await message.channel.send(str(number_to_send))
            save_all_active_counters()
        except discord.Forbidden:
            print(f"ERROR: No permission to send messages in {message.channel.name} ({message.channel.id})")
        except discord.HTTPException as e:
            print(f"ERROR: Failed to send message in {message.channel.name} ({message.channel.id}): {e}")


if TOKEN:
    bot.run(TOKEN)
else:
    print("you didn't add a token. it goes in .env in the format: TOKEN=\"<token>\"")