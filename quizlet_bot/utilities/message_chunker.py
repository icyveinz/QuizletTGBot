MAX_MESSAGE_LENGTH = 4000  # Telegram's safe message size limit


def chunk_message(text: str, max_length=MAX_MESSAGE_LENGTH):
    chunks = []
    while len(text) > max_length:
        split_index = text.rfind("\n", 0, max_length)
        if split_index == -1:
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:].strip()
    chunks.append(text)
    return chunks
