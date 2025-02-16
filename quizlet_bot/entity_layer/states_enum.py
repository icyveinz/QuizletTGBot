from enum import Enum


class StatesEnum(Enum):
    ZERO_STATE = "ZERO_STATE"
    AWAITING_BACK = "AWAITING_BACK"
    AWAITING_FRONT = "AWAITING_FRONT"
    TRAINS_CARDS = "TRAINS_CARDS"
    CREATING_CARDS = "CREATING_CARDS"
    UPLOADING_CARDS_SETS = "UPLOADING_CARDS_SETS"
    CHOOSING_TRAINING_MODE = "CHOOSING_TRAINING_MODE"
