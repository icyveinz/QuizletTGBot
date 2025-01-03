def int_to_str(num: int) -> str:
    try:
        return str(num)
    except TypeError as e:
        raise e
