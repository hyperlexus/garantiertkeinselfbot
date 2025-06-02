from handlers.base_to_decimal_handler import convert_number_in_base_to_decimal

def parse_rule_message(message_content: str, base) -> tuple[str, int] | int:
    if "divisible" in message_content:
        rule_string, rule_number = "div", message_content.partition(": ")[2]
    elif "digsum" in message_content:
        rule_string, rule_number = "digsum", message_content.partition("with the digsum ")[2].rpartition(" has to be skipped")[0]
    elif "root" in message_content:
        rule_string, rule_number = "root", message_content.partition("with an integer ")[2].rpartition(" root must be skipped")[0][:-2]
    else:
        return -1
    # this doesn't check if the base is valid since it is assumed that the counting bot already checked that
    decimal_rule_number = convert_number_in_base_to_decimal(rule_number, base=base)

    return rule_string, decimal_rule_number