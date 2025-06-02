from handlers.correct_number_handler import base_characters_dict
base_characters_dict_inv = {k: v for v, k in base_characters_dict.items()}

# is this message valid in base n? if yes, it has to be processed, if not, it is likely a normal text message
def all_characters_in_message_valid_in_base(base: int, message_content: str) -> bool:
    if not message_content: return False
    all_dict_values = list(base_characters_dict.values())
    characters_in_base = all_dict_values[:base]
    for char in list(message_content):
        if char in characters_in_base: continue
        else: return False
    return True

# for received number
def convert_number_in_base_to_decimal(number_received: str, base: int):
    digit_list = reversed(list(number_received))
    decimal_number = 0
    for idx, digit in enumerate(digit_list):
        decimal_number += base_characters_dict_inv[digit] * (base**idx)
    return decimal_number