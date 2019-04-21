def canRecord(response_body: str) -> bool:
    r = response_body
    if not_in_active_game(r) or not_registered(r) or already_recording(r):
        return False
    return True


def not_in_active_game(response_body: str) -> bool:
    text = "is not in an active game"
    return check_page(response_body, text)


def not_registered(response_body: str) -> bool:
    text = "is not registered at OP.GG"
    return check_page(response_body, text)


def already_recording(response_body: str) -> bool:
    text = "NowRecording"
    to_print = "Already recording..."
    return check_page(response_body, text, to_print)


def check_page(response_body: str, text: str, to_print: str = "") -> bool:
    if to_print != "":
        text = to_print

    if text in response_body:
        msg = f"{text}..."
        print(msg)
        return True

    return False
