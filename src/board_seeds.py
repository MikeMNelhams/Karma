from typing import Any, Callable, Iterable, Tuple, TypeVar, Type

from random import randint

from src.cards import Card, Cards, CardValue, SUITS
from src.hand import Hand
from src.karma import KarmaFaceDown, KarmaFaceUp
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

        face_down_poops = [KarmaFaceDown(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                           for i in range(number_of_players)]
        deck.add_cards(jokers)
        del jokers
        deck.shuffle()
        face_up_poops = [KarmaFaceUp(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                         for i in range(number_of_players)]
        hands = [Hand(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2])) for i in range(number_of_players)]

        players = [Player(h, fdp, fup) for h, fdp, fup in zip(hands, face_down_poops, face_up_poops)]
        draw_pile = CardPile(deck)

        return self.__board_constructor(players, draw_pile, who_starts)

    def random_fdpfup_only(self, number_of_players: int, number_of_jokers: int = 0, who_starts: int=0) -> IBoard:
        deck = Cards(Card(SUITS[0], CardValue(j)) for j in range(2, 15))
        deck.shuffle()

        face_down_poops = [KarmaFaceDown(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                           for i in range(number_of_players)]
        face_up_poops = [KarmaFaceUp(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                         for i in range(number_of_players)]
        hands = [Hand(Cards([])) for _ in range(number_of_players)]

        players = [Player(h, fdp, fup) for h, fdp, fup in zip(hands, face_down_poops, face_up_poops)]
        draw_pile = CardPile(deck)

        return self.__board_constructor(players, draw_pile, who_starts)

    def random_fdpfup_only_with_jokers(self, number_of_players: int, number_of_jokers: int = 1, who_starts: int=0) -> IBoard:
        jokers = Cards(Card(SUITS[i % len(SUITS)], CardValue.JOKER) for i in range(number_of_jokers))
        deck = Cards(Card(SUITS[0], CardValue(j)) for j in range(2, 15))
        deck.add_cards(jokers)
        deck.shuffle()
        print(deck)
        face_down_poops = [KarmaFaceDown(deck.pop_multiple([i * 3, i * 3 + 1, i * 3 + 2]))
                           for i in range(number_of_players)]
        face_up_poops = [KarmaFaceUp([]) for _ in range(number_of_players)]
        hands = [Hand(Cards([])) for _ in range(number_of_players)]
        print(deck)
        players = [Player(h, fdp, fup) for h, fdp, fup in zip(hands, face_down_poops, face_up_poops)]
        draw_pile = CardPile(deck)

        return self.__board_constructor(players, draw_pile, who_starts)