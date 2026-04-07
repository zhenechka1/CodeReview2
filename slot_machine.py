import random
import time
import sys

# Символи и множители при 3 еднакви
symbols = {
    "🍒": 2,
    "🍋": 3,
    "🍉": 4,
    "🍇": 5,
    "💎": 10,
    "🔔": 7,
    "🍀": 8
}

# Игрови променливи
balance = 0
total_lost = 0
bet = 1  # минимален залог
game_history = []

# Скрит/случаен бонус настройки
hidden_bonus_trigger = 1000  # праговата загуба при която може да се активира бонус
hidden_bonus_percentage = 0.10  # 10% от загубите
hidden_bonus_chance = 1  # 100% шанс да се активира (може да се промени)


def print_welcome():
    print("=" * 50)
    print("🎰 ДОБРЕ ДОШЪЛ В КАЗИНО РОТАТИВКА 🎰")
    print("=" * 50)
    print("Правила (важни неща):")
    print(" - Минимален залог: 1 лв.")
    print(" - 3 еднакви символа = голяма печалба 🎉")
    print(" - 2 еднакви символа отляво = двойна печалба ✨")
    print("=" * 50)


def deposit_money():
    global balance
    while True:
        try:
            amount = int(input("Въведи начален баланс (лв): "))
            if amount <= 0:
                print("❌ Моля, въведи положително число.")
                continue
            balance = amount
            print(f"✅ Балансът е зададен на {balance} лв.\n")
            break
        except ValueError:
            print("❌ Невалидно число, опитай отново.")


def show_menu():
    print("\n--- ГЛАВНО МЕНЮ ---")
    print("1. Завърти ротативката 🎰")
    print("2. Промени залога (мин. 1 лв) 💵")
    print("3. Покажи баланса 💰")
    print("4. История на играта 📝")
    print("5. Изход 🚪")


def apply_hidden_bonus():
    """
    Опитва да приложи скрит бонус.
    Връща (triggered: bool, bonus_amount: int)
    Ако total_lost >= hidden_bonus_trigger и случайността премине,
    връща True и сумата на бонуса (100% от total_lost като цяло число).
    След това нулира total_lost.
    """
    global total_lost, balance

    if total_lost > hidden_bonus_trigger:
        # шанс за активиране (напр. 100%)
        if random.random() < hidden_bonus_chance:
            bonus = int(total_lost * hidden_bonus_percentage)
            if bonus > 0:
                balance += bonus
                total_lost = 0  # нулираме натрупаните загуби след даване на бонус
                return True, bonus
    return False, 0


def spin_slot():
    global balance, total_lost, bet

    if balance < bet:
        print("⚠️ Нямаш достатъчно пари за завъртане.")
        return

    # Таксуваме залога
    balance -= bet
    total_lost += bet

    # Анимация на завъртане
    print("\nЗавъртане...")
    time.sleep(0.8)

    reels = [random.choice(list(symbols.keys())) for _ in range(3)]
    print(" | ".join(reels))

    win_amount = 0

    # Проверка за 3 еднакви (джакпот)
    if reels[0] == reels[1] == reels[2]:
        multiplier = symbols[reels[0]]
        win_amount = bet * multiplier
        print(f"🎉 ДЖАКПОТ! Спечели {win_amount} лв с {reels[0]} {reels[1]} {reels[2]}!")
        total_lost = 0  # нулираме загубите при голяма печалба
        game_history.append(f"ПЕЧАЛБА: +{win_amount} лв със {reels}")

    # Проверка за 2 еднакви отляво (позиции 0 и 1)
    elif reels[0] == reels[1]:
        win_amount = bet * 2
        print(f"✨ ПЕЧАЛБА! Два еднакви символа отляво → {win_amount} лв!")
        game_history.append(f"ПЕЧАЛБА (2 символа): +{win_amount} лв със {reels}")

    else:
        print("😢 Няма печалба този път.")
        game_history.append(f"ЗАГУБА: -{bet} лв със {reels}")

    # Добавяне на печалбата към баланса
    balance += win_amount

    # Опит за прилагане на скрития бонус
    triggered, bonus_amount = apply_hidden_bonus()
    if triggered:
        # Показваме на играча, че е „случайно спечелил“ и колко е бонусът.
        # Това съобщение е предвидено да изглежда като неочаквана печалба/късмет.
        print()
        print("🎉 Изглежда късметът ти се усмихна! 🎉")
        print(f"Бонус игра: +{bonus_amount} лв.")
        print("Продължавай да играеш — късмета е с теб! 😉")
        game_history.append(f"БОНУС (случаен): +{bonus_amount} лв")

    print(f"\n💰 Текущ баланс: {balance} лв")


def change_bet():
    global bet
    while True:
        try:
            new_bet = int(input("Въведи нов залог (мин. 1 лв): "))
            if new_bet < 1:
                print("⚠️ Минималният залог е 1 лв.")
                continue
            bet = new_bet
            print(f"✅ Новият залог е {bet} лв.")
            break
        except ValueError:
            print("❌ Невалидно число, опитай отново.")


def show_balance():
    print(f"💰 Текущ баланс: {balance} лв")


def show_history():
    if not game_history:
        print("📭 Все още няма изиграни игри.")
    else:
        print("\n--- ИСТОРИЯ НА ИГРАТА ---")
        for entry in game_history:
            print(entry)
        print("-------------------------")


def exit_game():
    print("\n🎲 Благодарим ти, че игра нашата ротативка!")
    print(f"🏁 Финален баланс: {balance} лв")
    sys.exit()


# --- ГЛАВНА ПРОГРАМА ---
print_welcome()
deposit_money()

while True:
    if balance < 1:
        print("\n💀 Нямаш достатъчно пари, за да продължиш.")
        print("Играта приключи!")
        break

    show_menu()
    choice = input("Избери опция (1-5): ")

    if choice == "1":
        spin_slot()
    elif choice == "2":
        change_bet()
    elif choice == "3":
        show_balance()
    elif choice == "4":
        show_history()
    elif choice == "5":
        exit_game()
    else:
        print("❌ Невалиден избор. Моля, избери между 1 и 5.")
