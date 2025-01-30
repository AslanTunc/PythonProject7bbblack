import pygame
import os
from blackjack import BlackjackGame


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack - Pygame")


def draw_button(text, x, y, width, height, color, text_color, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    return pygame.Rect(x, y, width, height), action



CARD_WIDTH, CARD_HEIGHT = 80, 120


TABLE_IMAGE = pygame.image.load(os.path.join("cards", "table.png"))
TABLE_IMAGE = pygame.transform.scale(TABLE_IMAGE, (WIDTH, HEIGHT))

CARD_BACK = pygame.image.load(os.path.join("cards", "back.png"))
CARD_BACK = pygame.transform.scale(CARD_BACK, (CARD_WIDTH, CARD_HEIGHT))


def load_card_images():
    card_images = {}
    suits = {'♥': 'H', '♦': 'D', '♣': 'C', '♠': 'S'}
    values = {'A': 'A', 'K': 'K', 'Q': 'Q', 'J': 'J',
              '10': '10', '9': '9', '8': '8', '7': '7',
              '6': '6', '5': '5', '4': '4', '3': '3', '2': '2'}

    for value, v in values.items():
        for suit, s in suits.items():
            file_name = os.path.join("cards", f"{v}{s}.png")
            if os.path.exists(file_name):
                image = pygame.image.load(file_name)
                image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
                card_images[(value, suit)] = image

    return card_images

card_images = load_card_images()


class BlackjackPygame:

    def update_display(self):

        screen.blit(TABLE_IMAGE, (0, 0))

        self.draw_text(f"balance: {self.game.balance}", 600, 50)
        self.draw_text(f"player: {self.game.calculate_score(self.game.player_hand)}", 50, 350)

        if not self.dealer_hidden:
            self.draw_text(f"dealer: {self.game.calculate_score(self.game.dealer_hand)}", 50, 50)

        self.draw_buttons()
        self.draw_cards()

        pygame.display.flip()

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.game = None
        self.dealer_hidden = True
        self.menu()




    def show_rules(self):
        screen.fill((1, 7, 4))
        self.draw_text("Blackjack Rules:", 250, 100, (255, 255, 255))


        self.draw_text("1. Number cards (2-10) are worth their face value, face cards", 50, 200, (255, 255, 255))
        self.draw_text("(K, Q, J) are worth 10, and Ace can be 1 or 11.", 50, 240, (255, 255, 255))

        self.draw_text("2. You can 'Hit' (draw a card) or 'Stand' (keep your hand).", 50, 280, (255, 255, 255))

        self.draw_text("3. If your total exceeds 21, you 'Bust' and lose the round.", 50, 320, (255, 255, 255))

        self.draw_text("4. A 'Blackjack' (Ace + 10-value card) wins the round.", 50, 360, (255, 255, 255))

        self.draw_text("5. Goal: Get as close to 21 as possible.", 50, 400, (255, 255, 255))

        self.draw_text("6. A tie happens if you and the dealer have the same score.", 50, 440, (255, 255, 255))

        self.draw_text("7. You can start a new game after each round.", 50, 480, (255, 255, 255))

        self.draw_text("Press ENTER to return to the main menu.", 150, 520, (255, 255, 255))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

    def enter_nickname(self):
        """Nickname giriş ekranı"""
        screen.fill((0, 0, 0))
        self.draw_text("Nickname girin ve ENTER'a basın:", 200, 250, (255, 255, 255))
        pygame.display.flip()

        nickname = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return nickname
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        nickname += event.unicode
            screen.fill((0, 0, 0))
            self.draw_text(f"Nickname: {nickname}", 200, 300, (255, 255, 255))
            pygame.display.flip()

    def menu(self):
        menu_running = True

        while menu_running:
            screen.fill((0, 100, 0))

            self.draw_text("Welcome to Blackjack!", 220, 100, (255, 255, 255))

            # Butonları ekrana çiz
            buttons = []
            buttons.append(draw_button("Quick Start", 300, 200, 200, 50, (255, 255, 255), (0, 0, 0), "quick_start"))
            buttons.append(draw_button("Game Rules", 300, 270, 200, 50, (255, 255, 255), (0, 0, 0), "rules"))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for button, action in buttons:
                        if button.collidepoint(x, y):
                            if action == "quick_start":
                                self.start_game("")
                            elif action == "rules":
                                self.show_rules()

    def start_game(self, nickname):
        self.game = BlackjackGame(self)
        self.dealer_hidden = True
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()


        self.game.player_hand.append(self.game.draw_card())
        self.game.player_hand.append(self.game.draw_card())

        self.game.dealer_hand.append(self.game.draw_card())
        self.game.dealer_hand.append(self.game.draw_card())

        self.run()

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_cards(self):
        for i, card in enumerate(self.game.player_hand):
            screen.blit(card_images[(card["value"], card["suit"])], (50 + i * 90, 400))


        for i, card in enumerate(self.game.dealer_hand):
            if i == 1 and self.dealer_hidden:
                screen.blit(CARD_BACK, (50 + i * 90, 100))
            else:
                screen.blit(card_images[(card["value"], card["suit"])], (50 + i * 90, 100))

        pygame.display.flip()

    def draw_buttons(self):
        pygame.draw.rect(screen, (255, 255, 255), (600, 400, 150, 50))  # Hit
        pygame.draw.rect(screen, (255, 255, 255), (600, 470, 150, 50))  # Stand

        self.draw_text("Hit", 655, 415, (0, 0, 0))
        self.draw_text("Stand", 640, 485, (0, 0, 0))

    def run(self):
        while self.running:
            screen.blit(TABLE_IMAGE, (0, 0))

            self.draw_text(f"Balance: {self.game.balance}", 600, 50)
            self.draw_text(f"Player: {self.game.calculate_score(self.game.player_hand)}", 50, 350)
            if not self.dealer_hidden:
                self.draw_text(f"dealer: {self.game.calculate_score(self.game.dealer_hand)}", 50, 50)

            self.draw_cards()
            self.draw_buttons()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 600 <= x <= 750 and 400 <= y <= 450:
                        self.hit()
                    if 600 <= x <= 750 and 470 <= y <= 520:
                        self.stand()

            self.clock.tick(30)

    def hit(self):
        self.game.hit()
        if self.game.calculate_score(self.game.player_hand) > 21:
            print("BUST! You lost.")
            self.reset_game()

    def stand(self):
        self.dealer_hidden = False
        self.update_display()


        while self.game.calculate_score(self.game.dealer_hand) < 17:
            pygame.time.delay(500)
            self.game.dealer_hand.append(self.game.draw_card())
            self.update_display()


        player_score = self.game.calculate_score(self.game.player_hand)
        dealer_score = self.game.calculate_score(self.game.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            winner_text = "You WON!"
        elif player_score < dealer_score:
            winner_text = "The Croupier WON!"
        else:
            winner_text = "It's a Tie!"

        self.draw_text(winner_text, 300, 300, (255, 255, 0))


        self.new_game_button = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(screen, (255, 255, 255), self.new_game_button)
        self.draw_text("New Game", 350, 415, (0, 0, 0))

        pygame.display.flip()


        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.new_game_button.collidepoint(x, y):
                        waiting_for_restart = False
                        self.reset_game()

    def reset_game(self):
        """Yeni oyunu başlatır"""
        self.dealer_hidden = True
        self.game = BlackjackGame(self)

        self.game.player_hand.clear()
        self.game.dealer_hand.clear()

        # 📌 Oyuncuya ve krupiyeye yeni kartlar dağıt
        self.game.player_hand.append(self.game.draw_card())
        self.game.player_hand.append(self.game.draw_card())

        self.game.dealer_hand.append(self.game.draw_card())
        self.game.dealer_hand.append(self.game.draw_card())

        self.update_display()



if __name__ == "__main__":
    game = BlackjackPygame()
    game.run()
    pygame.quit()