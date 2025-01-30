import random

class BlackjackGame:
    def __init__(self, gui):
        self.gui = gui
        self.deck = self.create_deck()
        self.balance = 1000
        self.current_bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.show_full_dealer_hand = False

    def create_deck(self):

        suits = ['♥', '♦', '♣', '♠']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [{'value': v, 'suit': s} for v in values for s in suits]

    def draw_card(self):

        return self.deck.pop(random.randint(0, len(self.deck) - 1))

    def calculate_score(self, hand):

        total = 0
        ace_count = 0
        for card in hand:
            if card["value"] in ["J", "Q", "K"]:
                total += 10
            elif card["value"] == "A":
                ace_count += 1
                total += 11
            else:
                total += int(card["value"])


        while total > 21 and ace_count:
            total -= 10
            ace_count -= 1

        return total

    def place_bet(self, amount):

        if amount > self.balance:
            print("Mistake: Insufficient funds!")
            return False
        self.current_bet = amount
        self.balance -= amount
        return True

    def resolve_bet(self, result):

        if result == "win":
            self.balance += self.current_bet * 2
        elif result == "tie":
            self.balance += self.current_bet
        self.current_bet = 0
        self.show_full_dealer_hand = True

    def hit(self):

        self.player_hand.append(self.draw_card())
        if self.calculate_score(self.player_hand) > 21:
            print("BUST! lost.")
            self.resolve_bet("loss")
            self.gui.reset_game()

    def stand(self):

        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())

        player_value = self.calculate_score(self.player_hand)
        dealer_value = self.calculate_score(self.dealer_hand)

        if dealer_value > 21 or player_value > dealer_value:
            result = "win"
            print("You Won!")
        elif player_value < dealer_value:
            result = "loss"
            print("You Lost.")
        else:
            result = "tie"
            print("Tie!")

        self.show_full_dealer_hand = True
        self.resolve_bet(result)
        self.gui.reset_game()
