import rps

STARTING_CARDS = {
	"rock": 258,
	"paper": 262,
	"scissors": 294,
}

OUTCOME_SCORE = {
	"lose": 0,
	"draw": 1,
	"win": 2,
}


def choose_card_to_play(announced_options, player_cards):
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

def any_card_empty(player_cards):
	return any(player_cards[choice] == 0 for choice in rps.CHOICES)

def rock_excess(player_cards):
	"""Returns how much rock exceeds the minimum of other cards."""
	min_other = min(player_cards["paper"], player_cards["scissors"])
	return player_cards["rock"] - min_other

def choose_card_for_round_6_7(player_cards):
	"""For rounds 6-7, bot always throws scissors, so rock wins."""
	if player_cards["rock"] > 0:
		return "rock"
	return None

def play_one_game(player_cards, game_number):
	coins = 0
	round_results = []

	# If rock exceeds others by more than 10, go to round 7 to burn excess rock
	max_round = 7 if rock_excess(player_cards) > 10 else 5

	print(f"Game {game_number}")
	print(f"Cards before game: {rps.format_card_counts(player_cards)}")
	print(f"Strategy: {'Full 7 rounds (rock excess)' if max_round == 7 else 'Rounds 1-5'}")

	for round_number in range(1, max_round + 1):
		while True:
			announced_options = rps.generate_announced_options(round_number)
			
			# Use special logic for rounds 6-7
			if round_number >= 6:
				player_choice = choose_card_for_round_6_7(player_cards)
			else:
				player_choice = choose_card_to_play(announced_options, player_cards)

			if player_choice is None:
				print("Player 5 cannot throw because all cards are 0.")
				print("Result: run ended with 0 gold coin(s).")
				return 0, False

			bot_choice = rps.choose_bot_throw(round_number, announced_options)
			player_cards[player_choice] -= 1
			result = rps.decide_result(player_choice, bot_choice)

			print(f"Round {round_number}")
			print(f"Bot announced: {', '.join(announced_options)}")
			print(f"Bot threw: {bot_choice}")
			print(f"Player 5 threw: {player_choice}")
			print(f"Round result: {result}")

			if any_card_empty(player_cards):
				print("Player 5 stops because one card type reached 0.")
				print(f"Coins taken: {coins}")
				print(f"Cards left: {rps.format_card_counts(player_cards)}")
				print(f"Result summary: {round_results}")
				print()
				return coins, True

			if result == "draw":
				print("Player 5 retries the same round.\n")
				continue

			if result == "lose":
				print("Player 5 failed the run and gets 0 gold coin(s).")
				print(f"Cards left: {rps.format_card_counts(player_cards)}")
				print()
				return 0, False

			round_results.append(result)
			if round_number > 1:
				coins += 1
			print()
			break

	print(f"Player 5 stops after round {max_round}.")
	print(f"Coins taken: {coins}")
	print(f"Cards left: {rps.format_card_counts(player_cards)}")
	print(f"Result summary: {round_results}")
	print()
	return coins, False

def play_until_all_cards_consumed():
	player_cards = STARTING_CARDS.copy()
	total_coins = 0
	game_number = 1

	if rps.total_cards_left(player_cards) == 0:
		print("Player 5 cannot start because total cards are 0.")
		return

	while rps.total_cards_left(player_cards) > 0 and not any_card_empty(player_cards):
		game_coins, should_stop = play_one_game(player_cards, game_number)
		total_coins += game_coins
		game_number += 1
		if should_stop:
			break

	if any_card_empty(player_cards):
		print("Player 5 ended because at least one card type reached 0.")
	else:
		print("All cards have been consumed.")
	print(f"Games played: {game_number - 1}")
	print(f"Total coins earned: {total_coins}")
	print(f"Final cards: {rps.format_card_counts(player_cards)}")

if __name__ == "__main__":
	play_until_all_cards_consumed()
