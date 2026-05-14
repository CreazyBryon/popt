import rps

STARTING_CARDS = {
	"rock": 256,
	"paper": 263,
	"scissors": 244,
}

OUTCOME_SCORE = {
	"lose": 0,
	"draw": 1,
	"win": 2,
}


def choose_card_to_play(announced_options, player_cards):
    """
    Final, simplified, and correct strategy:
    1. Find the moves that give the most possible wins.
    2. If there's a tie between "rock" and another card, be smart:
       - If "scissors" is NOT a possible throw from the bot, our rock has no special value, so save it.
       - Otherwise (if scissors is a threat or rock is the only winner), it's okay to use rock.
    3. If the tie doesn't involve rock, pick the card you have more of.
    """
    best_moves = []
    max_wins = -1

    # Step 1: Find all moves that result in the maximum number of wins.
    for choice in rps.CHOICES:
        if player_cards[choice] <= 0:
            continue
        
        wins = sum(1 for bot_option in announced_options if rps.decide_result(choice, bot_option) == "win")
        
        if wins > max_wins:
            max_wins = wins
            best_moves = [choice]
        elif wins == max_wins:
            best_moves.append(choice)

    # If there are no moves that can win, fall back to a move that is least likely to lose.
    if max_wins == 0:
        best_choice = None
        # Profile: (draws, card_count)
        best_profile = (-1, -1)
        for choice in rps.CHOICES:
            if player_cards[choice] <= 0:
                continue
            draws = sum(1 for bot_option in announced_options if rps.decide_result(choice, bot_option) == "draw")
            profile = (draws, player_cards[choice])
            if profile > best_profile:
                best_profile = profile
                best_choice = choice
        return best_choice

    # Step 2: Analyze the best moves to break ties.
    if len(best_moves) == 1:
        # No tie, the choice is clear.
        return best_moves[0]
    
    # There is a tie. Apply smart "rock-saving" logic.
    is_rock_an_option = "rock" in best_moves
    non_rock_options = [move for move in best_moves if move != "rock"]

    if is_rock_an_option and non_rock_options:
        # Tie-break between rock and at least one other card.
        bot_can_throw_scissors = "scissors" in announced_options
        
        if not bot_can_throw_scissors:
            # The bot CANNOT throw scissors. Our rock has no special value here.
            # Therefore, save the rock and use the best non-rock option.
            return max(non_rock_options, key=lambda c: player_cards[c])

    # In all other tie cases (e.g., bot can throw scissors, or tie is between paper/scissors),
    # just use the card we have the most of from the best options.
    return max(best_moves, key=lambda c: player_cards[c])

def any_card_empty(player_cards):
	return any(player_cards[choice] == 0 for choice in rps.CHOICES)

def choose_card_for_round_6_7(player_cards):
	"""For rounds 6-7, bot always throws scissors, so rock wins."""
	if player_cards["rock"] > 0:
		return "rock"
	# If no rock, we can't win, so we can't continue.
	return None

def play_one_game(player_cards, game_number):
	coins = 0
	round_results = []
	max_round = 7  # Always aim for 7 rounds for maximum coins

	print(f"Game {game_number}")
	print(f"Cards before game: {rps.format_card_counts(player_cards)}")
	print("Strategy: Optimal (Aim for 7 rounds)")

	for round_number in range(1, max_round + 1):
		while True:
			announced_options = rps.generate_announced_options(round_number)
			
			# Use special logic for rounds 6-7
			if round_number >= 6:
				player_choice = choose_card_for_round_6_7(player_cards)
			else:
				player_choice = choose_card_to_play(announced_options, player_cards)

			if player_choice is None:
				# This can happen if we need a card we don't have (e.g., no rock for round 6)
				print(f"Player 5 cannot make a winning move and stops.")
				print(f"Coins taken: {coins}")
				print(f"Cards left: {rps.format_card_counts(player_cards)}")
				print(f"Result summary: {round_results}")
				print()
				return coins, True # Stop playing games

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
				# A draw consumes a card but doesn't end the game. We continue the inner while loop.
				continue

			if result == "lose":
				print("Player 5 failed the run and gets 0 gold coin(s).")
				print(f"Cards left: {rps.format_card_counts(player_cards)}")
				print()
				return 0, False # Game lost, but we can start a new one

			# If we win the round:
			round_results.append(result)
			if round_number > 1:
				coins += 1
			print()
			break # Break the inner while loop to proceed to the next round

	print(f"Player 5 won all {max_round} rounds.")
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
