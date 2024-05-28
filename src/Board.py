from typing import Iterable

from collections import deque

from src.cards import Cards
from src.player import Player
from src.card_pile import CardPile
from src.valid_card_plays import BoardPlayOrder


class Board:
    INVALID_ACTIONS = {"draw_card", "receive_card", "rotate_hand"}

    def __init__(self, players: Iterable[Player], draw_pile: CardPile, who_starts: int):
        self.players = deque(players)
        self.draw_pile = draw_pile

        self.burn_pile = CardPile([])
        self.play_pile = CardPile([])

        self.play_order = BoardPlayOrder.UP
        self.cards_are_flipped = False
        self.effect_multiplier = 1
        self.player_index = who_starts

    def play_turn(self) -> None:
        current_player = self.players[self.player_index]

        self.executePlayerAction(current_player)

        self.player_index += 1
        self.player_index %= len(self.players)

    def executePlayerAction(self, player: Player):
        # TRIPLE DISPATCH
        # 1. Choosing player method based on user input
        # - Doing a dictionary lookup based on user input
        # 2. Choosing the input selecting method which asks the user for inputs about the action they want to execute
        # - Doing a dictionary lookup based on action_name
        # 3. Execute the method which asks for user input
        # 4. Execute the player action with given input

        action_name = ""
        while not hasattr(player, action_name) or action_name in Board.INVALID_ACTIONS:
            if action_name == "exit":
                raise InterruptedError("Quiting game!")
            action_name = input("What would you like to do? ").lower()

        if action_name == "pickup":
            player.pickup(self.play_pile)
            return None
        if action_name == "pop_from_hand":
            chosen_index = input("What card INDEX would you like to play?")

        return None



