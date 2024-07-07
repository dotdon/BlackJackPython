import random
import tkinter as tk
from tkinter import font, messagebox

# Card values and suits
values = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
suits = ['♥', '♦', '♣', '♠']

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value}{self.suit}"

    def color(self):
        return "red" if self.suit in ['♥', '♦'] else "black"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in suits for value in values.keys()]
        random.shuffle(self.cards)

    def deal(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        if card:
            self.cards.append(card)
            self.value += values[card.value]
            if card.value == 'Ace':
                self.aces += 1
            self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.master.geometry("1200x900")
        self.master.configure(bg="#2c3e50")
        self.master.resizable(False, False)

        self.player_money = 1000
        self.current_bet = 0
        self.insurance_bet = 0
        self.split_hands = []

        self.setup_gui()
        self.show_start_screen()

    def setup_gui(self):
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.card_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.info_font = font.Font(family="Helvetica", size=16)

        self.title_label = tk.Label(self.master, text="Blackjack", font=self.title_font, bg="#2c3e50", fg="white")
        self.title_label.pack(pady=20)

        self.dealer_frame = tk.Frame(self.master, bg="#34495e", padx=20, pady=10)
        self.dealer_frame.pack(pady=10)

        self.player_frame = tk.Frame(self.master, bg="#34495e", padx=20, pady=10)
        self.player_frame.pack(pady=10)

        self.info_frame = tk.Frame(self.master, bg="#2c3e50")
        self.info_frame.pack(pady=10)

        self.money_label = tk.Label(self.info_frame, text=f"Money: ${self.player_money}", font=self.info_font, bg="#2c3e50", fg="white")
        self.money_label.pack(side=tk.LEFT, padx=10)

        self.bet_label = tk.Label(self.info_frame, text=f"Current Bet: ${self.current_bet}", font=self.info_font, bg="#2c3e50", fg="white")
        self.bet_label.pack(side=tk.LEFT, padx=10)

        self.result_label = tk.Label(self.master, text="", font=self.info_font, bg="#2c3e50", fg="white")
        self.result_label.pack(pady=10)

        self.bet_frame = tk.Frame(self.master, bg="#2c3e50")
        self.bet_frame.pack(pady=10)

        self.bet_entry = tk.Entry(self.bet_frame, font=self.button_font, width=12)
        self.bet_entry.pack(side=tk.LEFT, padx=10)

        self.place_bet_button = tk.Button(self.bet_frame, text="Place Bet", command=self.place_bet, font=self.button_font, bg="#f39c12", fg="white", width=12)
        self.place_bet_button.pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.master, bg="#2c3e50")
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, font=self.button_font, bg="#27ae60", fg="white", width=12)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, font=self.button_font, bg="#e74c3c", fg="white", width=12)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        self.double_button = tk.Button(self.button_frame, text="Double Down", command=self.double_down, font=self.button_font, bg="#f39c12", fg="white", width=12)
        self.double_button.pack(side=tk.LEFT, padx=10)

        self.split_button = tk.Button(self.button_frame, text="Split", command=self.split_hand, font=self.button_font, bg="#9b59b6", fg="white", width=12)
        self.split_button.pack(side=tk.LEFT, padx=10)

        self.insurance_button = tk.Button(self.button_frame, text="Insurance", command=self.place_insurance, font=self.button_font, bg="#d35400", fg="white", width=12)
        self.insurance_button.pack(side=tk.LEFT, padx=10)

        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.new_game, font=self.button_font, bg="#3498db", fg="white", width=12)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.refill_button = tk.Button(self.button_frame, text="Refill Balance", command=self.refill_balance, font=self.button_font, bg="#9b59b6", fg="white", width=12)
        self.refill_button.pack(side=tk.LEFT, padx=10)

        self.hide_game_buttons()

    def show_start_screen(self):
        self.start_frame = tk.Frame(self.master, bg="#2c3e50")
        self.start_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(self.start_frame, text="Welcome to Blackjack", font=self.title_font, bg="#2c3e50", fg="white")
        title.pack(pady=20)

        start_button = tk.Button(self.start_frame, text="Start Game", command=self.start_game, font=self.button_font, bg="#27ae60", fg="white", width=15)
        start_button.pack(pady=10)

        quit_button = tk.Button(self.start_frame, text="Quit", command=self.master.quit, font=self.button_font, bg="#c0392b", fg="white", width=15)
        quit_button.pack(pady=10)

    def start_game(self):
        self.start_frame.destroy()
        self.show_game_buttons()
        self.new_game()

    def refill_balance(self):
        self.player_money += 1000
        self.update_money_labels()
        messagebox.showinfo("Balance Refilled", f"$1000 has been added to your balance. Your new balance is ${self.player_money}!")

    def new_game(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.split_hands = []
        self.current_bet = 0
        self.insurance_bet = 0
        self.update_money_labels()
        self.result_label.config(text="")
        self.enable_bet()
        self.disable_game_buttons()
        self.update_gui()

    def place_bet(self):
        if not hasattr(self, 'deck'):
            self.result_label.config(text="Please start the game first!")
            return
        try:
            bet = int(self.bet_entry.get())
            if 1 <= bet <= self.player_money:
                self.current_bet = bet
                self.player_money -= bet
                self.update_money_labels()
                self.start_round()
            else:
                self.result_label.config(text="Invalid bet amount!")
        except ValueError:
            self.result_label.config(text="Please enter a valid number!")

    def place_insurance(self):
        if not hasattr(self, 'deck'):
            self.result_label.config(text="Please start the game first!")
            return
        if self.dealer_hand.cards and self.dealer_hand.cards[0].value == 'Ace':
            insurance = self.current_bet // 2
            if self.player_money >= insurance:
                self.insurance_bet = insurance
                self.player_money -= insurance
                self.update_money_labels()
                messagebox.showinfo("Insurance Bet", f"Insurance bet of ${insurance} placed!")
            else:
                self.result_label.config(text="Not enough money for insurance!")
        else:
            self.result_label.config(text="Insurance can only be placed when dealer's up card is an Ace!")

    def start_round(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())
        self.update_gui()
        self.enable_game_buttons()
        self.disable_bet()

    def hit(self):
        if not hasattr(self, 'deck'):
            self.result_label.config(text="Please start the game first!")
            return
        card = self.deck.deal()
        if card:
            self.player_hand.add_card(card)
            self.update_gui()

            if self.player_hand.value > 21:
                self.end_game(player_wins=False)
        else:
            self.result_label.config(text="No more cards in the deck!")

    def stand(self):
        if not hasattr(self, 'deck'):
            self.result_label.config(text="Please start the game first!")
            return
        while self.dealer_hand.value < 17:
            card = self.deck.deal()
            if card:
                self.dealer_hand.add_card(card)
            else:
                self.result_label.config(text="No more cards in the deck!")
                break

        self.update_gui(reveal_dealer=True)
        self.end_game()

    def double_down(self):
        if not hasattr(self, 'deck'):
            self.result_label.config(text="Please start the game first!")
            return
        if self.player_money >= self.current_bet:
            self.player_money -= self.current_bet
            self.current_bet *= 2
            self.hit()
            if self.player_hand.value <= 21:
                self.stand()
            else:
                self.end_game(player_wins=False)
        else:
            self.result_label.config(text="Not enough money to double down!")

    def split_hand(self):
        if not hasattr(self, 'deck'):
            self.result_label.config(text="Please start the game first!")
            return
        if len(self.player_hand.cards) == 2 and values[self.player_hand.cards[0].value] == values[self.player_hand.cards[1].value]:
            if self.player_money >= self.current_bet:
                self.player_money -= self.current_bet
                self.split_hands = [Hand(), Hand()]
                self.split_hands[0].add_card(self.player_hand.cards[0])
                self.split_hands[1].add_card(self.player_hand.cards[1])
                self.player_hand = self.split_hands[0]
                self.update_money_labels()
                self.start_round()
            else:
                self.result_label.config(text="Not enough money to split!")
        else:
            self.result_label.config(text="You can only split when you have two cards of the same value!")

    def update_gui(self, reveal_dealer=False):
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        for widget in self.player_frame.winfo_children():
            widget.destroy()

        tk.Label(self.dealer_frame, text="Dealer's Hand", font=self.card_font, bg="#34495e", fg="white").pack()
        if reveal_dealer:
            for card in self.dealer_hand.cards:
                tk.Label(self.dealer_frame, text=str(card), font=self.card_font, bg="#34495e", fg=card.color()).pack(side=tk.LEFT, padx=5)
            tk.Label(self.dealer_frame, text=f"Total: {self.dealer_hand.value}", font=self.card_font, bg="#34495e", fg="white").pack(side=tk.LEFT, padx=20)
        else:
            if self.dealer_hand.cards:
                tk.Label(self.dealer_frame, text=str(self.dealer_hand.cards[0]), font=self.card_font, bg="#34495e", fg=self.dealer_hand.cards[0].color()).pack(side=tk.LEFT, padx=5)
                tk.Label(self.dealer_frame, text="🂠", font=self.card_font, bg="#34495e", fg="blue").pack(side=tk.LEFT, padx=5)
            else:
                tk.Label(self.dealer_frame, text="No cards yet", font=self.card_font, bg="#34495e", fg="white").pack()

        tk.Label(self.player_frame, text="Player's Hand", font=self.card_font, bg="#34495e", fg="white").pack()
        for card in self.player_hand.cards:
            tk.Label(self.player_frame, text=str(card), font=self.card_font, bg="#34495e", fg=card.color()).pack(side=tk.LEFT, padx=5)
        tk.Label(self.player_frame, text=f"Total: {self.player_hand.value}", font=self.card_font, bg="#34495e", fg="white").pack(side=tk.LEFT, padx=20)

    def end_game(self, player_wins=None):
        self.update_gui(reveal_dealer=True)
        
        if player_wins is None:
            if self.player_hand.value > 21:
                result = "Player busts! Dealer wins!"
                player_wins = False
            elif self.dealer_hand.value > 21:
                result = "Dealer busts! Player wins!"
                player_wins = True
            elif self.dealer_hand.value > self.player_hand.value:
                result = "Dealer wins!"
                player_wins = False
            elif self.dealer_hand.value < self.player_hand.value:
                result = "Player wins!"
                player_wins = True
            else:
                result = "It's a tie! Push."
                player_wins = None
        else:
            result = "Player wins!" if player_wins else "Dealer wins!"

        self.result_label.config(text=result)
        
        if player_wins:
            self.player_money += self.current_bet * 2
        elif player_wins is None:  # Tie
            self.player_money += self.current_bet
        else:
            if self.dealer_hand.cards[1].value == 'Ace' and self.insurance_bet:
                self.player_money += self.insurance_bet * 2

        self.current_bet = 0
        self.update_money_labels()
        self.disable_game_buttons()
        self.enable_bet()

        if self.player_money <= 0:
            self.result_label.config(text="You're out of money! Game over.")
            self.disable_bet()

    def update_money_labels(self):
        self.money_label.config(text=f"Money: ${self.player_money}")
        self.bet_label.config(text=f"Current Bet: ${self.current_bet}")

    def enable_game_buttons(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL)
        self.insurance_button.config(state=tk.NORMAL)

    def disable_game_buttons(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)
        self.insurance_button.config(state=tk.DISABLED)

    def enable_bet(self):
        self.bet_entry.config(state=tk.NORMAL)
        self.place_bet_button.config(state=tk.NORMAL)

    def disable_bet(self):
        self.bet_entry.config(state=tk.DISABLED)
        self.place_bet_button.config(state=tk.DISABLED)

    def hide_game_buttons(self):
        self.hit_button.pack_forget()
        self.stand_button.pack_forget()
        self.double_button.pack_forget()
        self.split_button.pack_forget()
        self.insurance_button.pack_forget()
        self.new_game_button.pack_forget()
        self.refill_button.pack_forget()
        self.bet_entry.pack_forget()
        self.place_bet_button.pack_forget()

    def show_game_buttons(self):
        self.hit_button.pack(side=tk.LEFT, padx=10)
        self.stand_button.pack(side=tk.LEFT, padx=10)
        self.double_button.pack(side=tk.LEFT, padx=10)
        self.split_button.pack(side=tk.LEFT, padx=10)
        self.insurance_button.pack(side=tk.LEFT, padx=10)
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        self.refill_button.pack(side=tk.LEFT, padx=10)
        self.bet_entry.pack(side=tk.LEFT, padx=10)
        self.place_bet_button.pack(side=tk.LEFT, padx=10)

def main():
    root = tk.Tk()
    game = BlackjackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()