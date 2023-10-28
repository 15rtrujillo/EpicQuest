class Game:
    """A class that has methods for running the game"""

    def __init__(self):
        pass


def parse_int_input(text_to_parse: str, number_of_choices: int = 0) -> int:
    """Parses int input. Returns -1 if the input is invalid in some way
    text_to_parse: The text to parse
    number_of_choices: If this is not 0, the parsed int will be range checked form one to this value (inclusive)"""
    try:
        int_input = int(text_to_parse)
        if number_of_choices == -1:
            return int_input
        if int_input in range(1, number_of_choices + 1):
            return int_input
        else:
            return -1
    except ValueError:
        return -1


def validate_text_input(text_to_validate: str, allowed_responses: list[str],
                        case_sensitive: bool = False, partial_match: bool = False) -> bool:
    """Validates text input
    text_to_validate: The text to validate
    allowed_responses: If this is not None, the user's input will be checked against a list of
    allowed responses. If the user enters an invalid response, they will be prompted to try again
    case_sensitive: All string comparisons will be case-sensitive if this is set
    partial_match: Checks if the text is a substring of one of the allowed responses"""
    # If we don't care about validating the response
    # But then what is the point of calling this function?
    if allowed_responses is None:
        return True

    for allowed_response in allowed_responses:
        if case_sensitive:
            if partial_match and text_to_validate in allowed_response:
                return True

            elif text_to_validate == allowed_response:
                return True

        else:
            if partial_match and text_to_validate.lower() in allowed_response.lower():
                return True

            elif text_to_validate.lower() == allowed_response.lower():
                return True

    return False
