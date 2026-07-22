import random, time, datetime, math
shuffle_time = 15
deal_time = 26
play_time = 1
war_time = 3
gather_time = 2
points_time = 60
war_num = 0
p1_wins = 0
p2_wins = 0
ties = 0
ninety_six = 0
shortest = 600
ace_war = int()
ace_war_count = 0
two_war = int()
two_war_count = 0
four_aces = 0
four_aces_win = 0
ended_early = 0
war_number_players = 0
card = 0
player_data = {}
deck = []
war_first_occurence = []
wars = []
compare = []
war_players = []
leftover_cards = []
players = []
force_war = False
hierarchy = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
war_names = ["Single", "Double", "Triple", "Quadruple", "Quintuple", "Sextuple", "Septuple"]
def assemble_deck():
    global deck
    if force_war == False:
        for i in range(4):
            for i in range(2, 11):
                deck.append(str(i) + "_")
            deck.append("Jack_")
            deck.append("Queen_")
            deck.append("King_")
            deck.append("Ace_")
        for i in range(13):
            deck[i] = deck[i] + "Spades"
        for i in range(13, 26):
            deck[i] = deck[i] + "Hearts"
        for i in range(26, 40):
            deck[i] = deck[i] + "Diamonds"
        for i in range(40, 52):
            deck[i] = deck[i] + "Clubs"
    else:
        deck = ['Ace_Spades', '2_Spades', '3_Spades', '4_Spades', '5_Spades', '6_Spades', '7_Spades', '8_Spades', '9_Spades', '10_Spades', 'Ace_Hearts', 'Jack_Spades', 'Queen_Spades', 'King_Spades', '2_Hearts', '3_Hearts', '4_Hearts', '5_Hearts', '6_Hearts', '7_Hearts', '8_Hearts', '9_Hearts', '10_Hearts', 'Jack_Hearts', 'Queen_Hearts', 'King_Hearts', '2_Diamonds', '3_Diamonds', '4_Diamonds', '5_Diamonds', '6_Diamonds', '7_Diamonds', '8_Diamonds', '9_Diamonds', '10_Diamonds', 'Jack_Diamonds', 'Queen_Diamonds', 'King_Diamonds', 'Ace_Diamonds', '2_Diamonds', '3_Clubs', '4_Clubs', '5_Clubs', '6_Clubs', '7_Clubs', '8_Clubs', '9_Clubs', '10_Clubs', 'Jack_Clubs', 'Queen_Clubs', 'King_Clubs', 'Ace_Clubs']
def deal():
    global leftover_cards
    for i in player_data["draw"].values():
        i.extend(deck[0:math.floor(52/num_players)])
        del deck[0:math.floor(52/num_players)]
    leftover_cards = deck
    print("Leftover cards:")
    print(leftover_cards)
    #for i in range(26):
        #p1_draw.append(deck[i])
    #for i in range(26, 52):
        #p2_draw.append(deck[i])
    global timer
    timer -= deal_time
def check_reshuffle_draw():
    if len(p1_draw) == 0:
        if printing_on == True:
            print("Player 1's draw pile being reshuffled...")
        random.shuffle(p1_collect)
        p1_draw.extend(p1_collect)
        p1_collect.clear()
    if len(p2_draw) == 0:
        if printing_on == True:
            print("Player 2's draw pile being reshuffled...")
        random.shuffle(p2_collect)
        p2_draw.extend(p2_collect)
        p2_collect.clear()
def war():
    global timer, war_num, ace_war, ace_war_count, two_war, two_war_count, war_players, card, first_round
    card = 0
    compare.clear()
    for x in war_players:
        for y in range(4):
            if len(player_data["draw"][x]) == 0:
                continue
            player_data["war"][x].append(player_data["draw"][x].pop(0))
    print("Player data after war cards distributed")
    print(player_data)
    for i in war_players:
        if len(player_data["draw"][i]) == 0:
            continue
        compare.append(player_data["draw"][i][0] + "_" + i)
    compare.sort(reverse=True, key=sort)
    print("Cards being compared (within war)")
    print(compare)
    if hierarchy.index((compare[card]).split("_")[0]) == hierarchy.index((compare[card + 1]).split("_")[0]):
        card += 1
        same_top_card()
        war_players = list(set(war_players))
        print("war")
        war()
    else:
        print("no war")
        player_data["collect"][compare[0].split("_")[2]].extend(player_data["draw"][i][0] for i in war_players)
        if first_round == True:
            player_data["collect"][compare[0].split("_")[2]].extend(leftover_cards)
            first_round == False
        for i in war_players:
            player_data["collect"][compare[0].split("_")[2]].extend(player_data["war"][i])
        for i in players:
            player_data["draw"][i].pop(0)
        compare.clear()
        war_players.clear()
        for i in player_data["war"].values():
            i.clear()
        print("Player data after war ends")
        print(player_data)
    """
    try:
        for i in range(4):
            p1_war.append(p1_draw[0])
            p2_war.append(p2_draw[0])
            p1_draw.pop(0)
            p2_draw.pop(0)
            check_reshuffle_draw()
        timer -= war_time
        if "Ace" in p1_war[0] and "Ace" in p1_draw[0] and "Ace" in p2_war[0] and "Ace" in p2_draw[0]:
            if not ace_war:
                ace_war = game_number
            ace_war_count += 1
        elif "2" in p1_war[0] and "2" in p1_draw[0] and "2" in p2_war[0] and "2" in p2_draw[0]:
            if not two_war:
                two_war = game_number
            two_war_count += 1
        if hierarchy.index((p1_draw[0]).split("_")[0]) > hierarchy.index((p2_draw[0]).split("_")[0]):
            if printing_on == True:
                print(f"Player 1's {(p1_draw[0]).split("_")[0]} of {(p1_draw[0]).split("_")[1]} beats Player 2's {(p2_draw[0]).split("_")[0]} of {(p2_draw[0]).split("_")[1]}")
            timer -= play_time
            p1_collect.extend([p1_draw[0], p2_draw[0]])
            p1_collect.extend(p1_war)
            p1_collect.extend(p2_war)
            p1_draw.pop(0)
            p2_draw.pop(0)
            timer -= gather_time
            p1_war.clear()
            p2_war.clear()
            war_num = 0
        elif hierarchy.index((p1_draw[0]).split("_")[0]) < hierarchy.index((p2_draw[0]).split("_")[0]):
            if printing_on == True:
                print(f"Player 2's {(p2_draw[0]).split("_")[0]} of {(p2_draw[0]).split("_")[1]} beats Player 1's {(p1_draw[0]).split("_")[0]} of {(p1_draw[0]).split("_")[1]}")
            timer -= play_time
            p2_collect.extend([p1_draw[0], p2_draw[0]])
            p2_collect.extend(p1_war)
            p2_collect.extend(p2_war)
            p1_draw.pop(0)
            p2_draw.pop(0)
            timer -= gather_time
            p1_war.clear()
            p2_war.clear()
            war_num = 0
        else:
            war_num += 1
            if war_num == len(wars):
                wars.append(0)
            wars[war_num] += 1
            if war_num - 1 == len(war_first_occurence):
                war_first_occurence.append(game_number)
            if printing_on == True:
                print(war_names[war_num] + " War!!")
            war()
    except IndexError:
        if printing_on == True:
            print("Game ends due to insufficient cards for War")
        return "insufficient_cards_for_war"
    """
def scoring():
    p1_score = 0
    p2_score = 0
    p1_aces = 0
    p2_aces = 0
    p1_total = p1_draw + p1_collect + p1_war
    p2_total = p2_draw + p2_collect + p2_war
    p1_score = len(p1_total)
    p2_score = len(p2_total)
    global p1_wins, p2_wins, ties, four_aces, four_aces_win
    for i in p1_total:
        if "Jack" in i:
            p1_score += 1
        elif "Queen" in i:
            p1_score += 2
        elif "King" in i:
            p1_score += 3
        elif "Ace" in i:
            p1_score += 5
            p1_aces += 1
    if p1_aces == 4:
        four_aces += 1
    for i in p2_total:
        if "Jack" in i:
            p2_score += 1
        elif "Queen" in i:
            p2_score += 2
        elif "King" in i:
            p2_score += 3
        elif "Ace" in i:
            p2_score += 5
            p2_aces += 1
    if p2_aces == 4:
        four_aces += 1
    if p1_score == 96 or p2_score == 96:
        ninety_six += 1
    if p1_score > p2_score:
        if printing_on == True:
            print(f"Player 1 wins, {p1_score} to {p2_score}")
        p1_wins += 1
        if p1_aces == 4:
            four_aces_win += 1
    elif p1_score < p2_score:
        if printing_on == True:
            print(f"Player 2 wins, {p2_score} to {p1_score}")
        p2_wins += 1
        if p2_aces == 4:
            four_aces_win += 1
    elif p1_score == p2_score:
        if printing_on == True:
            print("It's a tie - 48 to 48 :O")
        ties += 1
def sort(e):
    return hierarchy.index(e.split("_")[0])
def same_top_card():
    global card
    if hierarchy.index((compare[card]).split("_")[0]) == hierarchy.index((compare[card + 1]).split("_")[0]):
        war_players.append(compare[card].split("_")[2])
        war_players.append(compare[card + 1].split("_")[2])
        card += 1
        same_top_card()
print("Welcome to the 96 Simulator!")
desired_games = input("Please enter the number of games you'd like to simulate - up to 100,000 ")
while True:
    try:
        desired_games = int(desired_games)
    except ValueError:
        desired_games = input("Please enter a valid input ")
        continue
    else:
        if desired_games > 100000 or desired_games <= 0:
            desired_games = input("Please enter a valid input ")
            continue
        else:
            break

num_players = input("Please enter how many players you'd like to be playing - up to 10 ")
while True:
    try:
        num_players = int(num_players)
    except ValueError:
        num_players = input("Please enter a valid input ")
        continue
    else:
        if num_players > 10 or num_players <= 1:
            num_players = input("Please enter a valid input ")
            continue
        else:
            break
player_data["collect"] = {}
player_data["draw"] = {}
player_data["war"] = {}
for i in range(num_players):
    player_data["collect"]["p" + str(i + 1)] = []
    player_data["draw"]["p" + str(i + 1)] = []
    player_data["war"]["p" + str(i + 1)] = []
    players.append("p" + str(i + 1))               
desired_time = input("Please enter how many minutes per game you'd like - between 5 and 10 minutes inclusive (enter 'random' to pick randomly each game) ")
while not (desired_time == "5" or desired_time == "6" or desired_time == "7" or desired_time == "8" or desired_time == "9" or desired_time == "10" or desired_time.lower() == "random"):
    desired_time = input("Please enter a valid input ")
if desired_time.lower() != "random":
    desired_time = int(desired_time) * 60
printing_on = input("Would you like to turn on print statements? (They will cause significant slowdown with large numbers of games) (Y/N) ")
while not (printing_on.lower() == "y" or printing_on.lower() == "n"):
    printing_on = input("Please enter a valid input ")
if printing_on.lower() == "y":
    printing_on = True
else:
    printing_on = False
start_time = time.time()
assemble_deck()
for i in range(desired_games):
    first_round = True
    if str(desired_time).lower() == "random":
        desired_time = random.randrange(5, 10) * 60
    timer = desired_time
    game_number = i + 1
    p1_collect = []
    p2_collect = []
    p1_draw = []
    p2_draw = []
    p1_war = []
    p2_war = []
    if printing_on == True:
        print("Shuffling deck...")
    if force_war == False:
        random.shuffle(deck)
    timer -= shuffle_time
    if printing_on == True:
        print("Dealing cards...")
    deal()
    if printing_on == True:
        print(f"Starting game number {game_number}")
    print("Original player data")
    print(player_data)
    for i in players:
        compare.append(player_data["draw"][i][0] + "_" + i)
    compare.sort(reverse=True, key=sort)
    print("Cards being compared")
    print(compare)
    if hierarchy.index((compare[card]).split("_")[0]) == hierarchy.index((compare[card + 1]).split("_")[0]):
        war_players.append(compare[card].split("_")[2])
        war_players.append(compare[card + 1].split("_")[2])
        card += 1
        same_top_card()
        war_players = list(set(war_players))
        print("war")
        print("war players")
        print(war_players)
        war()
    else:
        print("no war")
        player_data["collect"][compare[0].split("_")[2]].extend(i.rpartition("_")[0] for i in compare)
        if first_round == True:
            player_data["collect"][compare[0].split("_")[2]].extend(leftover_cards)
            first_round == False
        for i in players:
            player_data["draw"][i].pop(0)
        compare.clear()
        print("Player data")
        print(player_data)
    """
    while not ((len(p1_draw) == 0 and len(p1_collect) == 0) or (len(p2_draw) == 0 and len(p2_collect) == 0) or
    timer <= 0 or war == "insufficient_cards_for_war"):
        check_reshuffle_draw()        
        if hierarchy.index((p1_draw[0]).split("_")[0]) > hierarchy.index((p2_draw[0]).split("_")[0]):
            if printing_on == True:
                print(f"Player 1's {(p1_draw[0]).split("_")[0]} of {(p1_draw[0]).split("_")[1]} beats Player 2's {(p2_draw[0]).split("_")[0]} of {(p2_draw[0]).split("_")[1]}")
            timer -= play_time
            p1_collect.extend([p1_draw[0], p2_draw[0]])
            p2_draw.pop(0)
            p1_draw.pop(0)
            timer -= gather_time
        elif hierarchy.index((p1_draw[0]).split("_")[0]) < hierarchy.index((p2_draw[0]).split("_")[0]):
            if printing_on == True:
                print(f"Player 2's {(p2_draw[0]).split("_")[0]} of {(p2_draw[0]).split("_")[1]} beats Player 1's {(p1_draw[0]).split("_")[0]} of {(p1_draw[0]).split("_")[1]}")
            timer -= play_time
            p2_collect.extend([p1_draw[0], p2_draw[0]])
            p1_draw.pop(0)
            p2_draw.pop(0)
            timer -= gather_time
        else:
            timer -= play_time
            if printing_on == True:
                print(f"Player 1 plays {(p1_draw[0]).split("_")[0]} of {(p1_draw[0]).split("_")[1]} and Player 2 plays {(p2_draw[0]).split("_")[0]} of {(p2_draw[0]).split("_")[1]}")
                print("War!!")
            if not wars:
                wars.append(0)
            wars[0] += 1
            war()
    if timer < 0:
        timer = 0
    if timer == 0:
       if printing_on == True: 
           print("Time is up!")
    else:
        ended_early += 1
    if desired_time - timer < shortest:
        shortest = desired_time - timer 
    if len(p1_draw) == 0 and len(p1_collect) == 0:
        if printing_on == True:
            print("Player 1 ran out of cards!")
            print("Player 2 wins, 96 to 0")
        p2_wins += 1
        ninety_six += 1
    elif len(p2_draw) == 0 and len(p2_collect) == 0:
        if printing_on == True:    
            print("Player 2 ran out of cards!")
            print("Player 1 wins, 96 to 0")
        p1_wins += 1
        ninety_six += 1
    else:
        if printing_on == True:
            print("Calculating scores...")
        scoring()
    if printing_on == False:
        if i != desired_games - 1:
            print(f"{i + 1} of {desired_games} games simulated")
            print("\033[1A", end = "\x1b[2K")
        else:
            print(f"{i + 1} of {desired_games} games simulated", end = "\n")
print("-----------------------")
print(f"Simulation runtime: {str(datetime.timedelta(seconds = time.time() - start_time))}")
print(f"Shortest game: {str(datetime.timedelta(seconds = shortest))}")
print(f"Player 1 wins: {'{:,}'.format(p1_wins)} ({round((p1_wins/desired_games) * 100, 5)}%)") 
print(f"Player 2 wins: {'{:,}'.format(p2_wins)} ({round((p2_wins/desired_games) * 100, 5)}%)") 
print(f"Ties: {'{:,}'.format(ties)} ({round((ties/desired_games) * 100, 5)}%)")
print(f"96 to 0 games: {'{:,}'.format(ninety_six)} ({round((ninety_six/desired_games) * 100, 5)}%)")
print(f"Games that ended early: {'{:,}'.format(ended_early)} ({round((ended_early/desired_games) * 100, 5)}%)")
if four_aces != 0:
    print(f"Games where someone has 4 aces: {'{:,}'.format(four_aces)} ({round((four_aces/desired_games) * 100, 5)}%) (wins in this situation: {'{:,}'.format(four_aces_win)} [{round((four_aces_win/four_aces)* 100, 5)}%])")
else:
    print("Games where someone has 4 aces: 0")
if wars[0] != 0:
    print(f"Single wars: {'{:,}'.format(wars[0])}")
for i in wars[1:]:
    print(f"{war_names[wars.index(i)]} wars: {'{:,}'.format(wars[wars.index(i)])} - games to occur: {'{:,}'.format(war_first_occurence[wars.index(i) - 1])}")
print(f"Double wars with 4 aces: {'{:,}'.format(ace_war_count)} - games to occur: {'{:,}'.format(ace_war)}")
print(f"Double wars with 4 twos: {'{:,}'.format(two_war_count)} - games to occur: {'{:,}'.format(two_war)}")
"""