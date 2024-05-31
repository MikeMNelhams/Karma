from typing import Any, Callable

from src.cards import Card, Cards, CardValue, SUITS
from src.hand import Hand
from src.karma import KarmaFaceDown, KarmaFaceUp
from src.card_pile import CardPile
from src.player import Player
from src.board_interface import IBoard

type BoardConstructor = Callable[[Any], IBoard]


class BoardFactory:
    def __init__(self, board_constructor: BoardConstructor):
        self.__board_constructor = board_constructor

    def random_start(self, number_of_players: int, number_of_jokers: int = 1, who_starts: int=0) -> IBoard:
        jokers = Cards(Card(SUITS[i % len(SUITS)], CardValue.JOKER) for i in range(number_of_jokers))
        deck = Cards(Card(SUITS[i], CardValue(j)) for j in range(2, 15) for i in range(len(SUITS)))
        deck.shuffle()

        face_down_poops = [KarmaFaceDown(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                           for i in range(number_of_players)]
        deck.add_cards(jokers)
        del jokers
        deck.shuffle()
        face_up_poops = [KarmaFaceUp(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                         for i in range(number_of_players)]
        hands = [Hand(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2])) for i in range(number_of_players)]
        players = [Player(h, fdp, fup) for h, fdp, fup in zip(hands, face_down_poops, face_up_poops)]
        return self.__board_constructor(draw_pile=CardPile(deck), players=players, who_starts=who_starts)
