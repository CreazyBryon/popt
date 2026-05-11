import random


CHOICES = ["rock", "paper", "scissors"]
STARTING_CARDS = {
	"rock": 1,
	"paper": 1,
	"scissors": 1,
}
WINNING_MATCHUPS = {
	("rock", "scissors"),
	("paper", "rock"),
	("scissors", "paper"),
}


def option_count_for_round(round_number):
	if round_number <= 2:
		return 1
	if round_number <= 5:
		return 2
	return 3


def generate_announced_options(round_number):
	return random.sample(CHOICES, option_count_for_round(round_number))


def choose_bot_throw(round_number, announced_options):
	if round_number >= 6:
		return "scissors"
	return random.choice(announced_options)


def decide_result(player_choice, bot_choice):
	if player_choice == bot_choice:
		return "draw"
	if (player_choice, bot_choice) in WINNING_MATCHUPS:
		return "win"
	return "lose"


def format_card_counts(player_cards):
	return ", ".join(f"{choice}: {player_cards[choice]}" for choice in CHOICES)


def total_cards_left(player_cards):
	return sum(player_cards.values())


def prompt_player_choice(options, player_cards):
	allowed_text = ", ".join(options)

	while True:
		print(f"Your cards: {format_card_counts(player_cards)}")
		player_choice = input(
			f"Choose your throw ({allowed_text}). You may pick any of: rock, paper, scissors: "
		).strip().lower()
		if player_choice in CHOICES and player_cards[player_choice] > 0:
			return player_choice
		if player_choice in CHOICES:
			print(f"You have no {player_choice} cards left.")
			continue

		print("Invalid choice. Pick rock, paper, or scissors.")


def prompt_continue_or_stop():
	while True:
		choice = input("Type 'c' to continue or 's' to stop and take your coins: ").strip().lower()
		if choice in {"c", "continue"}:
			return "continue"
		if choice in {"s", "stop"}:
			return "stop"

		print("Invalid choice. Type 'c' to continue or 's' to stop.")


def prompt_play_again():
	while True:
		choice = input("Type 'y' to start another game or 'n' to quit: ").strip().lower()
		if choice in {"y", "yes"}:
			return True
		if choice in {"n", "no"}:
			return False

		print("Invalid choice. Type 'y' or 'n'.")


def play_round(round_number, player_cards):
	while True:
		if total_cards_left(player_cards) == 0:
			print("You have no cards left.")
			return "out_of_cards"

		announced_options = generate_announced_options(round_number)
		print(f"\nRound {round_number}/7")
		print(f"Bot announces: {', '.join(announced_options)}")

		player_choice = prompt_player_choice(announced_options, player_cards)
		player_cards[player_choice] -= 1
		bot_choice = choose_bot_throw(round_number, announced_options)
		result = decide_result(player_choice, bot_choice)

		print(f"You threw: {player_choice}")
		print(f"Bot threw: {bot_choice}")

		if result == "draw":
			print("Draw.")
			choice = prompt_continue_or_stop()
			if choice == "stop":
				return "stop"
			print("Retry this round.")
			continue

		if result == "win":
			print("You win this round.")
		else:
			print("You lose this round.")

		return result



def play_game(player_cards):
	coins = 0

	print("Rock Paper Scissors")
	print("Win 7 rounds to clear the game.")
	print("If you draw, the same round restarts with a new bot announcement.")
	print("The announced options only limit what the bot can throw.")
	print("You start with 100 rock cards, 90 paper cards, and 110 scissors cards.")
	print("Each throw spends one card from your shared card box.")
	print("Round 1 gives no coins. Each later round gives 1 coin if you win it.")
	print("You can stop after any successful round or draw and take your coins.")
	print("If you lose once, the game ends and you get no coins.")

	for round_number in range(1, 8):
		result = play_round(round_number, player_cards)
		if result == "stop":
			print(f"\nYou stopped on round {round_number} and took {coins} gold coin(s).")
			return coins

		if result == "out_of_cards":
			print("This run ends with no coins.")
			return 0

		if result == "lose":
			print(f"\nGame over. You failed on round {round_number}.")
			print("You lost all unclaimed coins.")
			return 0

		if round_number > 1:
			coins += 1

		print(f"Your current coins: {coins}")

		if round_number < 7:
			choice = prompt_continue_or_stop()
			if choice == "stop":
				print(f"\nYou stopped after round {round_number} and took {coins} gold coin(s).")
				return coins

	print(f"\nYou cleared all 7 rounds and earned {coins} gold coin(s).")
	return coins


def main():
	player_cards = STARTING_CARDS.copy()
	banked_coins = 0

	while total_cards_left(player_cards) > 0:
		print(f"\nCards available before game: {format_card_counts(player_cards)}")
		game_coins = play_game(player_cards)
		banked_coins += game_coins
		print(f"Cards left after game: {format_card_counts(player_cards)}")
		print(f"Total banked coins: {banked_coins}")

		if total_cards_left(player_cards) == 0:
			print("\nYou cannot start another game because your total cards are 0.")
			break

		if not prompt_play_again():
			break

	print(f"\nFinal banked coins: {banked_coins}")


if __name__ == "__main__":
	main()
