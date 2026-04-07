import random
import time


class SlotMachine:
    """Simple slot machine game."""

    SYMBOLS = {
        "🍒": 2,
        "🍋": 3,
        "🍉": 4,
        "🍇": 5,
        "💎": 10,
        "🔔": 7,
        "🍀": 8
    }

    def __init__(self):
        self.balance = 0
        self.bet = 1
        self.total_lost = 0
        self.history = []

    def deposit(self):
        """Deposit initial money."""
        while True:
            try:
                amount = int(input("Enter balance: "))
                if amount > 0:
                    self.balance = amount
                    break
            except ValueError:
                pass
            print("Invalid input.")

    def spin(self):
        """Spin the slot machine."""
        if self.balance < self.bet:
            print("Not enough money.")
            return

        self.balance -= self.bet
        self.total_lost += self.bet

        print("\nSpinning...")
        time.sleep(0.5)

        reels = [random.choice(list(self.SYMBOLS.keys())) for _ in range(3)]
        print(" | ".join(reels))

        win = 0

        if reels[0] == reels[1] == reels[2]:
            multiplier = self.SYMBOLS[reels[0]]
            win = self.bet * multiplier
            print(f"JACKPOT! You won {win}")
            self.total_lost = 0

        elif reels[0] == reels[1]:
            win = self.bet * 2
            print(f"Win: {win}")

        else:
            print("No win.")

        self.balance += win
        self.history.append((reels, win))

        print(f"Balance: {self.balance}")

    def change_bet(self):
        """Change bet amount."""
        try:
            new_bet = int(input("New bet: "))
            if new_bet >= 1:
                self.bet = new_bet
        except ValueError:
            print("Invalid input.")

    def show_history(self):
        """Display game history."""
        for reels, win in self.history:
            print(reels, "->", win)

    def run(self):
        """Run the game loop."""
        self.deposit()

        while self.balance > 0:
            print("\n1. Spin\n2. Bet\n3. Balance\n4. History\n5. Exit")
            choice = input("Choice: ")

            if choice == "1":
                self.spin()
            elif choice == "2":
                self.change_bet()
            elif choice == "3":
                print(f"Balance: {self.balance}")
            elif choice == "4":
                self.show_history()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

        print("Game over.")


if __name__ == "__main__":
    game = SlotMachine()
    game.run()
