import rps


STARTING_CARDS = {
	"rock": 256,
	"paper": 263,
	"scissors": 244,
}


def choose_card_to_play(announced_options, player_cards):
	# For rounds 1-2: bot announces 1 option and always throws it
	bot_will_throw = announced_options[0]

	for choice in rps.CHOICES:
		if player_cards[choice] > 0 and rps.decide_result(choice, bot_will_throw) == "win":
			return choice

	for choice in rps.CHOICES:
		if player_cards[choice] > 0 and rps.decide_result(choice, bot_will_throw) == "draw":
			return choice

	for choice in rps.CHOICES:
		if player_cards[choice] > 0:
			return choice

	return None


def play_one_game(player_cards, game_number):
	coins = 0
	round_results = []

	print(f"Game {game_number}")
	print(f"Cards before game: {rps.format_card_counts(player_cards)}")

	for round_number in range(1, 3):
		while True:
			announced_options = rps.generate_announced_options(round_number)
			player_choice = choose_card_to_play(announced_options, player_cards)
			bot_choice = rps.choose_bot_throw(round_number, announced_options)

			if player_choice is None:
				print("Player 1 cannot throw because all cards are 0.")
				print("Result: run ended with 0 gold coin(s).")
				return 0

			player_cards[player_choice] -= 1
			result = rps.decide_result(player_choice, bot_choice)

			print(f"Round {round_number}")
			print(f"Bot announced: {', '.join(announced_options)}")
			print(f"Bot threw: {bot_choice}")
			print(f"Player 1 threw: {player_choice}")
			print(f"Round result: {result}")

			if result == "draw":
				print("Player 1 retries the same round.\n")
				continue

			if result == "lose":
				print("Player 1 failed the run and gets 0 gold coin(s).")
				print(f"Cards left: {rps.format_card_counts(player_cards)}")
				return 0

			round_results.append(result)
			if round_number > 1:
				coins += 1
			print()
			break

	print("Player 1 stops after round 2.")
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
		print("Player 1 cannot start because total cards are 0.")
		return

	while rps.total_cards_left(player_cards) > 0:
		total_coins += play_one_game(player_cards, game_number)
		game_number += 1

	print("All cards have been consumed.")
	print(f"Games played: {game_number - 1}")
	print(f"Total coins earned: {total_coins}")
	print(f"Final cards: {rps.format_card_counts(player_cards)}")

def any_card_is_zero(player_cards):
    return any(count == 0 for count in player_cards.values())


def play_until_any_card_zero():
    player_cards = STARTING_CARDS.copy()
    total_coins = 0
    game_number = 1

    if any_card_is_zero(player_cards):
        print("Player 1 cannot start because one card type is 0.")
        return

    while not any_card_is_zero(player_cards):
        total_coins += play_one_game(player_cards, game_number)
        game_number += 1

    print("One card type reached 0. Stopping.")
    print(f"Games played: {game_number - 1}")
    print(f"Total coins earned: {total_coins}")
    print(f"Final cards: {rps.format_card_counts(player_cards)}")



if __name__ == "__main__":
	play_until_any_card_zero()
