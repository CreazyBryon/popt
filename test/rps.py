import random


CHOICES = ["rock", "paper", "scissors"]
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


def decide_result(player_choice, bot_choice):
	if player_choice == bot_choice:
		return "draw"
	if (player_choice, bot_choice) in WINNING_MATCHUPS:
		return "win"
	return "lose"


def prompt_player_choice(options):
	allowed_text = ", ".join(options)

	while True:
		player_choice = input(
			f"Choose your throw ({allowed_text}). You may pick any of: rock, paper, scissors: "
		).strip().lower()
		if player_choice in CHOICES:
			return player_choice

		print("Invalid choice. Pick rock, paper, or scissors.")


def play_round(round_number):
	while True:
		announced_options = generate_announced_options(round_number)
		print(f"\nRound {round_number}/7")
		print(f"Bot announces: {', '.join(announced_options)}")

		player_choice = prompt_player_choice(announced_options)
		bot_choice = random.choice(announced_options)
		result = decide_result(player_choice, bot_choice)

		print(f"You threw: {player_choice}")
		print(f"Bot threw: {bot_choice}")

		if result == "draw":
			print("Draw. Retry this round.")
			continue

		if result == "win":
			print("You win this round.")
		else:
			print("You lose this round.")

		return result


def main():
	print("Rock Paper Scissors")
	print("Win 7 rounds to clear the game.")
	print("If you draw, the same round restarts with a new bot announcement.")
	print("The announced options only limit what the bot can throw.")
	print("If you lose once, the game ends.")

	for round_number in range(1, 8):
		result = play_round(round_number)
		if result == "lose":
			print(f"\nGame over. You failed on round {round_number}.")
			return

	print("\nYou cleared all 7 rounds.")


if __name__ == "__main__":
	main()
