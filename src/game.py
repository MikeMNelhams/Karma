from src.player import Player
from src.cards import Card, Cards, CardValue, SUITS, CARD_VALUE_NAMES
from src.hand import Hand
from src.poop import PoopFaceDown, PoopFaceUp
from src.card_pile import CardPile
from src.board import Board
from src.boardPrinter import BoardPrinter


class Game:
    def __init__(self, number_of_players: int, number_of_jokers: int=1, who_starts: int=0):
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
        board = Board(players, draw_pile, who_starts)

        boardPrinter = BoardPrinter(board)
        boardPrinter.print()


def main():
    game = Game(4)


if __name__ == "__main__":
    main()
