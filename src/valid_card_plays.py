from enum import Enum

from src.cards import Card, CardValue
from src.card_pile import CardPile


class BoardPlayOrder(Enum):
    UP = 0
    DOWN = 1


def is_legal_move(play_card: Card, board_play_order: BoardPlayOrder, is_blind: bool, play_pile: CardPile) -> bool:
    if is_blind:
        return True

    if not play_pile and play_card.value != CardValue.JOKER:
        return True

    if play_card.value == CardValue.JOKER:
        return play_pile.pop_card(-1).value == CardValue.ACE

    first_non_four = None
    for card in reversed(play_pile):
        if card.value != CardValue.FOUR:
            first_non_four = card
            break
    if first_non_four is None:
        return True

    if board_play_order == BoardPlayOrder.UP:
        return play_card.value >= first_non_four.value
    return play_card.value <= first_non_four.value

