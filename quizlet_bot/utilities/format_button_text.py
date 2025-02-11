def format_button_text(text: str, length: int = 15) -> str:
    if not len(text) > length:
        padding = (length - len(text)) // 2
        return " " * padding + text + " " * (length - len(text) - padding)
    else:
        return text
