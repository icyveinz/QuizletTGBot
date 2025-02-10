def trim_content_to_cards(text: str) -> list[tuple[str, str]]:
    cards = []
    lines = text.strip().split("\n")
    for line in lines:
        parts = line.split("-.-")
        if len(parts) == 2:
            front = parts[0].strip()
            back = parts[1].strip()
            cards.append((front, back))
    return cards