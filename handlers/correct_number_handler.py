base_characters_dict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B',
                        12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M',
                        23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V', 32: 'W', 33: 'X',
                        34: 'Y', 35: 'Z', 36: '[', 37: '\\', 38: ']', 39: '^', 40: '_', 41: '`', 42: 'a', 43: 'b', 44: 'c',
                        45: 'd', 46: 'e', 47: 'f', 48: 'g', 49: 'h', 50: 'i', 51: 'j', 52: 'k', 53: 'l', 54: 'm', 55: 'n',
                        56: 'o', 57: 'p', 58: 'q', 59: 'r', 60: 's', 61: 't', 62: 'u', 63: 'v', 64: 'w', 65: 'x', 66: 'y',
                        67: 'z', 68: '{', 69: '|', 70: '}', 71: '~'}

def number_to_base(number_to_conv, base) -> list:
    if base > len(base_characters_dict) - 1:
        raise IndexError("base provided was too high. max is 72")
    if number_to_conv == 0:
        return [0]
    elif base == 1:
        return [1] * number_to_conv
    digits = []
    while number_to_conv:
        digits.append(int(number_to_conv % base))
        number_to_conv //= base
    digits = digits[::-1]
    return digits

def convert_base10_list_to_base(base10_list):
    return [base_characters_dict[i] for i in base10_list]

def get_digsum(number_list):
    return sum(number_list)

def has_illegal_divs(number, divisor_list):
    return any(number % divisor == 0 for divisor in divisor_list)

def has_illegal_roots(number, root_list):
    for root in root_list:
        root_value = number ** (1.0 / root)
        if root_value == int(root_value):
            return True
    return False

def is_illegal_number(number, rules, base):
    divs = rules["div"]
    digsums = rules["digsum"]
    roots = rules["root"]
    if (has_illegal_divs(number, divs) or
        has_illegal_roots(number, roots) or
        get_digsum(number_to_base(number, base)) in digsums):
            return True
    return False

def determine_next_number(current_number: int, rules: dict, base: int):
    next_number = current_number + 1
    while is_illegal_number(next_number, rules, base):
        next_number += 1
        continue
    if base == 10:
        return next_number
    else:
        return ''.join(convert_base10_list_to_base(number_to_base(next_number, base)))
