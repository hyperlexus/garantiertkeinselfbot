from handlers.correct_number_handler import determine_next_number
from handlers.rule_added_handler import parse_rule_message
from handlers.base_to_decimal_handler import all_characters_in_message_valid_in_base

TARGET_BOT_ID = 996129161825484911

class ChannelCounter:
    def __init__(self, channel_id: int, initial_rules: dict = None, initial_base: int = 10, initial_expected_number: int = 1, initial_last_number: int = 0):
        self.channel_id = channel_id
        self.rules = initial_rules if initial_rules is not None else {"div": [], "digsum": [], "root": []}
        self.base = initial_base
        self.last_number = initial_last_number
        self.expected_next_number = initial_expected_number
        self.is_streak_active = True

    def process_message(self, message_content: str, author_id: int, is_bot: bool) -> int | str | None:
        if message_content.endswith('money.') and author_id == TARGET_BOT_ID:
            self.reset_streak()
            return -1

        if not is_bot and all_characters_in_message_valid_in_base(self.base, message_content):
            number_received = int(message_content)
        else: return None

        print(f"[channel: {self.channel_id} base:{self.base} rules:{self.rules}] awaited: {self.expected_next_number}, received: {number_received}")

        if number_received == self.expected_next_number:
            print(self.expected_next_number, self.rules, self.last_number)
            number_bot_should_send = determine_next_number(self.expected_next_number, self.rules, self.base)
            self.last_number = number_bot_should_send
            self.expected_next_number = determine_next_number(number_bot_should_send, self.rules, self.base)
            self.is_streak_active = True
            return number_bot_should_send
        else:
            return None

    def reset_streak(self):
        self.expected_next_number = 1
        self.is_streak_active = False
        self.rules = {"div": [], "digsum": [], "root": []}  # reset rules on streak fail
        print(f"[channel {self.channel_id}]'s streak was reset. next 1 will continue it")

    def refresh_next_number(self):
        self.expected_next_number = determine_next_number(self.last_number, self.rules, self.base)
        print(self.expected_next_number, self.rules, self.last_number)

    def parse_rule_update(self, rule_message_content: str):
        rule_mode, rule_number = parse_rule_message(rule_message_content, self.base)
        self.rules[rule_mode].append(rule_number)
        self.refresh_next_number()

    def parse_base_message(self, base_message_content: str):
        # todo
        pass

    def get_state(self) -> dict:
        return {
            "channel_id": self.channel_id,
            "rules": self.rules,
            "base": self.base,
            "expected_next_number": self.expected_next_number,
            "last_number": self.last_number,
            "is_streak_active": self.is_streak_active
        }

    @classmethod
    def from_state(cls, state_data: dict):
        counter = cls(
            channel_id=state_data["channel_id"],
            initial_rules=state_data.get("rules", {"div": [], "digsum": [], "root": []}),
            initial_base=state_data.get("base", 10),
            initial_expected_number=state_data.get("expected_next_number", 1)
        )
        counter.is_streak_active = state_data.get("is_streak_active", True)
        return counter