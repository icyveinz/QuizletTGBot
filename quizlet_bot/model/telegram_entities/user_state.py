from model.enums import StateEnum


class UserState:
    def __init__(self, state : StateEnum, front : str):
        self.state = state
        self.front = front