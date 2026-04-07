class CreditCard:
    """Class for validating and analyzing credit card numbers."""

    def __init__(self, card_number: str):
        self.card_number = card_number.strip()

    @property
    def company(self) -> str:
        """Return the card company based on number prefix."""
        if self.card_number.startswith("4"):
            company = "Visa"
        elif self.card_number.startswith("5"):
            company = "MasterCard"
        elif self.card_number.startswith("37"):
            company = "American Express"
        else:
            company = "Unknown"

        return f"Company card name: {company}"

    def is_valid_length(self) -> bool:
        """Check if card number length is valid."""
        return 13 <= len(self.card_number) <= 19

    @property
    def checksum(self) -> str:
        """Return the last digit of the card (checksum)."""
        return f"CHECKSUM: {self.card_number[-1]}"

    def validate(self) -> bool:
        """Validate card using Luhn algorithm."""
        digits = [int(d) for d in self.card_number[::-1]]
        total = 0

        for i, digit in enumerate(digits):
            if i % 2 == 1:
                doubled = digit * 2
                total += doubled if doubled < 10 else sum(int(d) for d in str(doubled))
            else:
                total += digit

        return total % 10 == 0

    @classmethod
    def from_input(cls):
        """Create card from user input."""
        number = input("Enter a card number: ")
        return cls(number)


def main():
    card = CreditCard.from_input()

    print(card.company)
    print(f"Card: {card.card_number}")

    if card.is_valid_length():
        print("Length check: VALID")
    else:
        print("Length check: INVALID")

    print(card.checksum)

    print("Validation:", "Valid Card" if card.validate() else "Invalid Card")


if __name__ == "__main__":
    main()
