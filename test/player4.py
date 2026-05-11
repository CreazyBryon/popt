import rps


STARTING_CARDS = {
	"rock": 200,
	"paper": 200,
	"scissors": 200,
}


OUTCOME_SCORE = {
	"lose": 0,
	"draw": 1,
	"win": 2,
}


def choose_card_to_play(round_number, announced_options, player_cards):
	if round_number >= 6 and player_cards["rock"] > 0:
		return "rock"

	best_choice = None
	best_profile = None

	for choice in rps.CHOICES:
		if player_cards[choice] <= 0:
			continue

		results = [rps.decide_result(choice, bot_option) for bot_option in announced_options]
		profile = (
			min(OUTCOME_SCORE[result] for result in results),
			sum(OUTCOME_SCORE[result] for result in results),
			player_cards[choice],
		)

		if best_profile is None or profile > best_profile:
			best_choice = choice
			best_profile = profile

	return best_choice


def play_one_game(player_cards, game_number):
	coins = 0
	round_results = []

	print(f"Game {game_number}")
	print(f"Cards before game: {rps.format_card_counts(player_cards)}")

	for round_number in range(1, 8):
		while True:
			if rps.total_cards_left(player_cards) == 0:
				print("Player 4 cannot throw because all cards are 0.")
				print("Result: run ended with 0 gold coin(s).")
				return 0

			announced_options = rps.generate_announced_options(round_number)
			player_choice = choose_card_to_play(round_number, announced_options, player_cards)

			if player_choice is None:
				print("Player 4 cannot throw because all cards are 0.")
				print("Result: run ended with 0 gold coin(s).")
				return 0

			bot_choice = rps.choose_bot_throw(round_number, announced_options)
			player_cards[player_choice] -= 1
			result = rps.decide_result(player_choice, bot_choice)

			print(f"Round {round_number}")
			print(f"Bot announced: {', '.join(announced_options)}")
			print(f"Bot threw: {bot_choice}")
			print(f"Player 4 threw: {player_choice}")
			print(f"Round result: {result}")

			if result == "draw":
				print("Player 4 retries the same round.\n")
				continue

			if result == "lose":
				print("Player 4 failed the run and gets 0 gold coin(s).")
				print(f"Cards left: {rps.format_card_counts(player_cards)}")
				print()
				return 0

			round_results.append(result)
			if round_number > 1:
				coins += 1
			print()
			break

	print("Player 4 cleared round 7 and stops.")
	print(f"Coins taken: {coins}")
	print(f"Cards left: {rps.format_card_counts(player_cards)}")
	print(f"Result summary: {round_results}")
	print()
	return coins


def play_until_all_cards_consumed():
	player_cards = STARTING_CARDS.copy()
	total_coins = 0
	game_number = 1

	if rps.total_cards_left(player_cards) == 0:
		print("Player 4 cannot start because total cards are 0.")
		return

	while rps.total_cards_left(player_cards) > 0:
		total_coins += play_one_game(player_cards, game_number)
		game_number += 1

	print("All cards have been consumed.")
	print(f"Games played: {game_number - 1}")
	print(f"Total coins earned: {total_coins}")
	print(f"Final cards: {rps.format_card_counts(player_cards)}")


if __name__ == "__main__":
	play_until_all_cards_consumed()
