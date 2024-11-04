import random

def set_up_players(num_of_players):
    players = []
    for i in range(1, num_of_players + 1):
        players.append(f"Player {i}")
    return players

def set_up_chips(players):
    poker_chips = []
    for player in players:
        poker_chips.append(5)
    return poker_chips

def determine_start_player(people_playing):
    rolls = {}
    for player in people_playing:
        rolls[player] = random.randint(1, 6)
    highest_roll = max(rolls.values())

    # Check if more than one player rolled the highest and reroll
    highest_rolling_players = []
    while len(highest_rolling_players) != 1:
        highest_rolling_players = []
        for player in rolls:
                if rolls[player] == highest_roll:
                    rolls[player] = random.randint(1, 6)
                    highest_rolling_players.append(player)
                else:
                    rolls[player] = 0
        highest_roll = max(rolls.values()) 
    return "".join(highest_rolling_players)

def order_of_turns(players_list, chips_list, starting_player):
    index = players_list.index(starting_player)

    # Change the players order
    beginning_players = players_list[index:]
    ending_players = players_list[0:index]
    new_turn_order = beginning_players + ending_players

    # Change chips to be parallel to the correct corresponding player
    begin_player_chips = chips_list[index:]
    end_player_chips = chips_list[0:index]
    new_chip_order = begin_player_chips + end_player_chips

    return new_turn_order, new_chip_order

def roll_dice():
    # Roll two dice
    dice_rolls = []
    for i in range(2):
        roll = random.randint(1, 6)
        dice_rolls.append(str(roll))
    
    # Figure out their dice score
    dice_rolls.sort()
    dice_rolls.reverse()
    roll_score = "".join(dice_rolls)
    return int(roll_score)
    
def determine_num_tries(player_starting):
    score = roll_dice()
    num_tries = 1
    keep_or_roll = input(f"{player_starting} rolled a {score}. Would you like to roll again? (yes or no): ")

    while (num_tries < 3) and (keep_or_roll == "yes"):
        if num_tries == 2:
            keep_or_roll = input("Warning: This is your last roll and you will keep whatever you roll next. Do you want to continue? ")
        
        if keep_or_roll == "yes":
            score = roll_dice()
            if num_tries < 2:
                keep_or_roll = input(f"{player_starting} rolled a {score}. Would you like to roll again? (yes or no): ")
        else:
            break
        num_tries += 1
    return num_tries, score

def roll_score(player, num_tries):
    score = roll_dice()
    if num_tries > 1:
        keep_or_roll = input(f"{player} rolled a {score}. Would you like to roll again? (yes or no): ")
    num_tries -= 1

    while num_tries != 0:
        if keep_or_roll == "yes":
            score = roll_dice()
            if num_tries != 1:
                keep_or_roll = input(f"{player} rolled a {score}. Would you like to roll again? (yes or no): ")
        num_tries -= 1
            
    return score

def determine_loser(player_list, rolls_list):
    # The rank of possible rolls from lowest to highest
    rank_of_rolls = [31, 32, 41, 42, 43, 51, 52, 53, 54, 61, 62, 63, 64, 65, 11, 22, 33, 44, 55, 66, 21]
    player_roll_rank = []
    
    # Find the rank of each player by getting their rank_of_roll index
    for i in range(len(rolls_list)):
        for j in range(len(rank_of_rolls)):
            if rolls_list[i] == rank_of_rolls[j]:
                player_roll_rank.append(j)

    # Determine the lowest rolling player
    # Lower the index, lower the roll so lowest index is the loser of the round
    lowest_roll = min(player_roll_rank)
    lowest_player = []

    for i in range(len(player_roll_rank)):
        if player_roll_rank[i] == lowest_roll:
            lowest_player.append(player_list[i])
    
    # If 2 or more players tie for lowest roll, make the tied players reroll
    if len(lowest_player) > 1:
        tied_breaking_roll = []
        print(lowest_player, "tied. Rerolling...")

        for player in lowest_player:
            score = roll_score(player, 1)
            print(f"{player} rolled a {score}.")
            tied_breaking_roll.append(score)
            
        tied_breaking_rank = [rank_of_rolls.index(tied_breaking_roll[0]), rank_of_rolls.index(tied_breaking_roll[1])]
        if tied_breaking_rank[0] < tied_breaking_rank[1]:
            lowest_player = lowest_player[0]
        else:
            lowest_player = lowest_player[1]

    return "".join(lowest_player)

        
def main():
    # Tell the user how to play Mexico and how scoring works
    print(f"\n\nGame: Mexico is a dice game in which players roll 2 dice. In the begining, each player rolls one dice and the highest rolling player goes first. \nThe first player will have a maxium of 3 rolls to get a number they're pleased with. The number of times they roll is the number of times the \nrest of the players gets to roll. For example, if the first player rolled 2 times, everyone else has up to 2 rolls. The numbers you roll will be \ncombined into a two-digit number which is considered as your score. There are certain score rules for Mexico: Double digit number (ex: 33) is \nhigher than any mixed number (ex: 63) and the highest number you can get is 21 which is known as a Mexico. Every player starts out \nwith 5 chips and every round the lowest rolling player will lose a chip. Once you run out of chips you are out. \nLast player standing wins.\n")

    # Set up the game
    num_players = int(input("How many players are playing (at least 2): "))
    while num_players < 2:
        num_players = int(input("You need at least 2 players to play. How many players are playing: "))
    players = set_up_players(num_players)
    poker_chips_left = set_up_chips(players)

    # Determine the starting player
    start_player = determine_start_player(players)
    print(f"{start_player} rolled the highest.")

    # Game play
    while len(players) > 1:

        # Determine the order of the rest of the players
        order = order_of_turns(players, poker_chips_left, start_player)
        players = order[0]
        poker_chips_left = order[1]

        # Display the information to user
        print(f"{start_player} goes first this round.")
        print("The player turn order:", players)
        print(f"Number of chips left:  {poker_chips_left}\n")

        # First player determines how many rolls for round by rolling for themself
        player_rolls = []
        starting_info = determine_num_tries(start_player)
        num_tries = starting_info[0]
        score = starting_info[1]
        player_rolls.append(score)
        print(f"{start_player} rolled a {score} and each player gets {num_tries} rolls.\n")

        # Rest of the players roll
        for player in players[1:]:
            score = roll_score(player, num_tries)
            print(f"{player} rolled a {score}.\n")
            player_rolls.append(score)

        # The player with smallest roll loses a chip
        loser = determine_loser(players, player_rolls)
        print(f"{loser} rolled the lowest so they lose a chip.\n")
        for i in range(len(players)):
            if players[i] == loser:
                loser_index = i
        poker_chips_left[loser_index] -= 1

        # Check if player has 0 chips left
        if poker_chips_left[loser_index] == 0:
            print(f"Game: {players[loser_index]} has no chips left and is eliminated.\n")
            poker_chips_left.remove(poker_chips_left[loser_index])
            players.remove(players[loser_index])
        
        # Make the next starting player the loser of the round
        if len(players) > 1:
            if loser_index > (len(players) - 1):
                start_player = players[loser_index - 1]
            else:
                start_player = players[loser_index]
        else:
            start_player = players

    print(f"The winner is {''.join(players)}")

main()