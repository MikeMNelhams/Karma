from typing import Any, Callable, Iterable, Tuple, TypeVar, Type

from random import randint

from src.cards import Card, Cards, CardValue, SUITS
from src.hand import Hand
from src.poop import PoopFaceDown, PoopFaceUp
from src.card_pile import CardPile
from src.player import Player
from src.board_interface import IBoard


type BoardConstructor = Callable[[Tuple[Any]], IBoard]
type BoardConstructorStartState[B] = Callable[[Iterable[Player], CardPile, int], B]
B = TypeVar('B')


class BoardFactory:
    def __init__(self, board_constructor: BoardConstructorStartState[B]):
        self.__board_constructor = board_constructor

    def random_start(self, number_of_players: int, number_of_jokers: int = 1, who_starts: int=0) -> IBoard:
        jokers = Cards(Card(SUITS[i % len(SUITS)], CardValue.JOKER) for i in range(number_of_jokers))
        deck = Cards(Card(SUITS[i], CardValue(j)) for j in range(2, 15) for i in range(len(SUITS)))
        deck.shuffle()

        face_down_poops = [PoopFaceDown(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                           for i in range(number_of_players)]
        deck.add_cards(jokers)
        del jokers
        deck.shuffle()
        face_up_poops = [PoopFaceUp(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                         for i in range(number_of_players)]
        hands = [Hand(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2])) for i in range(number_of_players)]

        players = [Player(h, fdp, fup) for h, fdp, fup in zip(hands, face_down_poops, face_up_poops)]
        draw_pile = CardPile(deck)

        return self.__board_constructor(players, draw_pile, who_starts)
