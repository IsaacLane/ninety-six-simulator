import random, time, datetime, math
shuffle_time = 15
deal_time = 26
play_time = 1
war_time = 3
gather_time = 2
points_time = 60
war_num = 1
ties = ninety_six = four_aces = four_aces_win = ended_early = war_number_players = card = 0
war_first_occurence = []
wars = []
two_way_wars = []
three_way_wars = []
four_way_wars = []
two_way_wars_time = []
three_way_wars_time = []
four_way_wars_time = []
compare = []
war_players = []
extra_cards = []
players = []
og_players = []
scores = []
scores_players = []
player_data = {}
score_data = {}
shortest = 600
force_war = False
hierarchy = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
war_names = ["single", "double", "triple", "quadruple", "quintuple", "sextuple", "septuple"]
def deal():
    global extra_cards
    for i in player_data["draw"].values():
        i.extend(deck[0:math.floor(52/num_players)])
        del deck[0:math.floor(52/num_players)]
    check_for_dups()
    extra_cards = deck
    global timer
    timer -= deal_time
def check_empty_piles():
    global out_of_game
    out_of_game = False
    for i in players[:]:
        if len(player_data["draw"][i]) == 0:
            if len(player_data["collect"][i]) == 0:
                if printing_on == True:
                    print(f"Player {i[1:]} ran out of cards!")
                players.remove(i)
                if i in war_players:
                    war_players.remove(i)
                out_of_game = True
                continue
            if printing_on == True:
                print(f"Player {i[1:]}'s draw pile being reshuffled...")
            random.shuffle(player_data["collect"][i])
            player_data["draw"][i].extend(player_data["collect"][i])
            player_data["collect"][i].clear()
def war():
    global timer, war_num, ace_war, ace_war_count, two_war, two_war_count, war_players, card, extras, extra_cards
    card = 0
    compare.clear()
    for x in war_players[:]:
        for y in range(4):
            check_empty_piles()
            if x in war_players:
                player_data["war"][x].append(player_data["draw"][x].pop(0))
            else:
                break
    timer -= war_time       
    for i in war_players[:]:
        check_empty_piles()
        if i in war_players:
            compare.append(player_data["draw"][i][0] + "_" + i)
    if len(war_players) == 0:
        if printing_on == True:
            print("All players in war ran out of cards!")
        for i in player_data["war"].values():
            extra_cards.extend(i)
            i.clear()
        extras = True
        return
    compare.sort(reverse=True, key=sort)
    timer -= play_time
    if len(compare) != 1:
        if hierarchy.index((compare[card]).split("_")[0]) == hierarchy.index((compare[card + 1]).split("_")[0]):
            card += 1
            same_top_card()
            war_players = list(set(war_players))
            war_num += 1
            if printing_on == True:
                print(f"{war_names[war_num - 1].upper()} WAR")
            war()
        else:
            no_war()
    else:
        if printing_on == True:
            print("Only one remaining player in war")
        no_war()
def no_war():
    global war_num, extras, timer
    if len(war_players) == 2:
        while war_num > len(two_way_wars): 
            two_way_wars.append(0)
        two_way_wars[war_num - 1] += 1
        while war_num > len(two_way_wars_time):
            two_way_wars_time.append(game_number)
    elif len(war_players) == 3:
        while war_num > len(three_way_wars):
            three_way_wars.append(0)
        three_way_wars[war_num - 1] += 1
        while war_num > len(three_way_wars_time):
            three_way_wars_time.append(game_number)
    elif len(war_players) == 4:
        while war_num > len(four_way_wars):
            four_way_wars.append(0)
        four_way_wars[war_num - 1] += 1
        while war_num > len(four_way_wars_time):
            four_way_wars_time.append(game_number)
    war_num = 1
    if printing_on == True:
        print(f"Player {compare[0].rpartition("_")[2][1:]}'s {compare[0].split("_")[0]} of {compare[0].split("_")[1]} is victorious")
    player_data["collect"][compare[0].split("_")[2]].extend(player_data["draw"][i][0] for i in war_players)
    if extras == True:
        player_data["collect"][compare[0].split("_")[2]].extend(extra_cards)
        extras = False
        extra_cards.clear()
    for i in og_players:
        player_data["collect"][compare[0].split("_")[2]].extend(player_data["war"][i])
    for i in war_players:
        player_data["draw"][i].pop(0)
    timer -= gather_time
    compare.clear()
    war_players.clear()
    for i in player_data["war"].values():
        i.clear()
def scoring():
    global ties, four_aces, four_aces_win
    four_aces_player = str()
    for i in og_players:
        score_data["total"][i] = player_data["collect"][i] + player_data["draw"][i] + player_data["war"][i]
        score_data["score"][i] = len(score_data["total"][i])
        score_data["aces"][i] = 0
    for key, values in score_data["total"].items():
        for i in values:
            if "Jack" in i:
                score_data["score"][key] += 1
            elif "Queen" in i:
                score_data["score"][key] += 2
            elif "King" in i:
                score_data["score"][key] += 3
            elif "Ace" in i:
                score_data["score"][key] += 5
                score_data["aces"][key] += 1
        if score_data["aces"][key] == 4:
            four_aces += 1
            four_aces_player = key 
    score_data["score"] = dict(sorted(score_data["score"].items(), key=lambda x: x[1], reverse=True))
    scores = list(score_data["score"].values())
    scores_players = list(score_data["score"].keys())
    if scores[0] == scores[1]:
        if printing_on == True:
            print("One or more players tied!")
        ties += 1
    else:
        if printing_on == True:
            print(f"Player {scores_players[0][1:]} wins with {scores[0]} points")
        if scores_players[0] == four_aces_player:
            four_aces_win += 1
        score_data["wins"][scores_players[0]] += 1
def sort(e):
    return hierarchy.index(e.split("_")[0])
def same_top_card():
    global card
    if not card + 2 > len(compare):
        if hierarchy.index((compare[card]).split("_")[0]) == hierarchy.index((compare[card + 1]).split("_")[0]):
            war_players.append(compare[card].split("_")[2])
            war_players.append(compare[card + 1].split("_")[2])
            card += 1
            same_top_card()
def check_for_dups():
    seen = set()
    dups = set()
    for x, d in player_data.items():
        for y, l in d.items():
            for i in l:
                if i in seen:
                    dups.add(i)
                else:
                    seen.add(i)
    if len(dups) != 0:
        raise Exception(f"{dups} is duplicated ({len(dups)} cards)")
def check_for_removed():
    cards_found = ['Ace_Spades', '2_Spades', '3_Spades', '4_Spades', '5_Spades', '6_Spades', '7_Spades', '8_Spades', '9_Spades', '10_Spades', 'Ace_Hearts', 'Jack_Spades', 'Queen_Spades', 'King_Spades', '2_Hearts', '3_Hearts', '4_Hearts', '5_Hearts', '6_Hearts', '7_Hearts', '8_Hearts', '9_Hearts', '10_Hearts', 'Jack_Hearts', 'Queen_Hearts', 'King_Hearts', '2_Diamonds', '3_Diamonds', '4_Diamonds', '5_Diamonds', '6_Diamonds', '7_Diamonds', '8_Diamonds', '9_Diamonds', '10_Diamonds', 'Jack_Diamonds', 'Queen_Diamonds', 'King_Diamonds', 'Ace_Diamonds', '2_Clubs', '3_Clubs', '4_Clubs', '5_Clubs', '6_Clubs', '7_Clubs', '8_Clubs', '9_Clubs', '10_Clubs', 'Jack_Clubs', 'Queen_Clubs', 'King_Clubs', 'Ace_Clubs']
    for x, d in player_data.items():
        for y, l in d.items():
            for i in l:
                if i in cards_found:
                    cards_found.remove(i)
    if len(cards_found) != 0:
        if extras == False:
            print(player_data)
            raise Exception(f"{cards_found} was deleted (or this thing is broken :P)")
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
score_data["total"] = {}
score_data["score"] = {}
score_data["wins"] = {}
score_data["aces"] = {}
for i in range(num_players):
    player_data["collect"]["p" + str(i + 1)] = []
    player_data["draw"]["p" + str(i + 1)] = []
    player_data["war"]["p" + str(i + 1)] = []
    score_data["total"]["p" + str(i + 1)] = []
    score_data["score"]["p" + str(i + 1)] = 0
    score_data["wins"]["p" + str(i + 1)] = 0
    score_data["aces"]["p" + str(i + 1)] = 0
    og_players.append("p" + str(i + 1))              
desired_time = input("Please enter how many minutes per game you'd like (enter 'r' to pick randomly each game) ")
while not (desired_time == "5" or desired_time == "6" or desired_time == "7" or desired_time == "8" or desired_time == "9" or desired_time == "10" or desired_time.lower() == "r"):
    desired_time = input("Please enter a valid input ")
if desired_time.lower() != "r":
    desired_time = int(desired_time) * 60
printing_on = input("Would you like to turn on print statements? (They will cause significant slowdown with large numbers of games) (Y/N) ")
while not (printing_on.lower() == "y" or printing_on.lower() == "n"):
    printing_on = input("Please enter a valid input ")
if printing_on.lower() == "y":
    printing_on = True
else:
    printing_on = False
start_time = time.time()
for z in range(desired_games):
    extras = True
    if str(desired_time).lower() == "r":
        desired_time = random.randrange(5, 10) * 60
    timer = desired_time
    game_number = z + 1
    players.clear()
    for i in range(num_players):
        players.append("p" + str(i + 1))
    p1_collect = []
    p2_collect = []
    p1_draw = []
    p2_draw = []
    p1_war = []
    p2_war = []
    deck = ['Ace_Spades', '2_Spades', '3_Spades', '4_Spades', '5_Spades', '6_Spades', '7_Spades', '8_Spades', '9_Spades', '10_Spades', 'Ace_Hearts', 'Jack_Spades', 'Queen_Spades', 'King_Spades', '2_Hearts', '3_Hearts', '4_Hearts', '5_Hearts', '6_Hearts', '7_Hearts', '8_Hearts', '9_Hearts', '10_Hearts', 'Jack_Hearts', 'Queen_Hearts', 'King_Hearts', '2_Diamonds', '3_Diamonds', '4_Diamonds', '5_Diamonds', '6_Diamonds', '7_Diamonds', '8_Diamonds', '9_Diamonds', '10_Diamonds', 'Jack_Diamonds', 'Queen_Diamonds', 'King_Diamonds', 'Ace_Diamonds', '2_Clubs', '3_Clubs', '4_Clubs', '5_Clubs', '6_Clubs', '7_Clubs', '8_Clubs', '9_Clubs', '10_Clubs', 'Jack_Clubs', 'Queen_Clubs', 'King_Clubs', 'Ace_Clubs']
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
    while not (len(players) == 1 or timer <= 0):
        check_for_dups()
        check_for_removed()
        for i in players:
            compare.append(player_data["draw"][i][0] + "_" + i)
        compare.sort(reverse=True, key=sort)
        timer -= play_time
        if hierarchy.index((compare[card]).split("_")[0]) == hierarchy.index((compare[card + 1]).split("_")[0]):
            war_players.append(compare[card].split("_")[2])
            war_players.append(compare[card + 1].split("_")[2])
            card += 1
            same_top_card()
            war_players = list(set(war_players))
            if printing_on == True:
                print("WAR")
            war()
        else:
            if printing_on == True:
                print(f"Player {compare[0].rpartition("_")[2][1:]}'s {compare[0].split("_")[0]} of {compare[0].split("_")[1]} is victorious")
            player_data["collect"][compare[0].split("_")[2]].extend(i.rpartition("_")[0] for i in compare)
            if extras == True:
                player_data["collect"][compare[0].split("_")[2]].extend(extra_cards)
                extras = False
                extra_cards.clear()
            for i in players:
                player_data["draw"][i].pop(0)
            timer -= gather_time
            compare.clear()
        check_empty_piles()
    if timer < 0:
        timer = 0
    if timer == 0:
        if printing_on == True:
            print("Time's up!")
            print("Calculating scores...")
        scoring()
    else:
        ended_early += 1
    if desired_time - timer < shortest:
        shortest = desired_time - timer
    if len(players) == 1:
        if printing_on == True:
            print(f"Player {players[0][1:]} wins with 96 points")
        score_data["wins"][players[0]] += 1
        ninety_six += 1
    if printing_on == False:
        if z != desired_games - 1:
            print(f"{z + 1} of {desired_games} games simulated")
            print("\033[1A", end = "\x1b[2K")
        else:
            print(f"{z + 1} of {desired_games} games simulated", end = "\n")
    for x, d in player_data.items():
            for i in d.values():
                i.clear()
print("-----------------------")
print(f"Simulation runtime: {str(datetime.timedelta(seconds = time.time() - start_time))}")
print(f"Shortest game: {str(datetime.timedelta(seconds = shortest))}")
for i in og_players:
    print(f"Player {i[1:]} wins: {'{:,}'.format(score_data["wins"][i])} ({round((score_data["wins"][i]/desired_games) * 100, 5)}%)")
print(f"Ties: {'{:,}'.format(ties)} ({round((ties/desired_games) * 100, 5)}%)")
print(f"96 to 0 games: {'{:,}'.format(ninety_six)} ({round((ninety_six/desired_games) * 100, 5)}%)")
print(f"Games that ended early: {'{:,}'.format(ended_early)} ({round((ended_early/desired_games) * 100, 5)}%)")
if four_aces != 0:
    print(f"Games where someone has 4 aces: {'{:,}'.format(four_aces)} ({round((four_aces/desired_games) * 100, 5)}%) (wins in this situation: {'{:,}'.format(four_aces_win)} [{round((four_aces_win/four_aces)* 100, 5)}%])")
else:
    print("Games where someone has 4 aces: 0")
if len(two_way_wars) != 0:
    print(f"Two-way single wars: {'{:,}'.format(two_way_wars[0])}")
for i in two_way_wars[1:]:
    print(f"Two-way {war_names[two_way_wars.index(i)]} wars: {'{:,}'.format(i)} - games to occur: {'{:,}'.format(two_way_wars_time[two_way_wars.index(i)])}")
for i in three_way_wars:
    print(f"Three-way {war_names[three_way_wars.index(i)]} wars: {'{:,}'.format(i)} - games to occur: {'{:,}'.format(three_way_wars_time[three_way_wars.index(i)])}")
for i in four_way_wars:
    print(f"Four-way {war_names[four_way_wars.index(i)]} wars: {'{:,}'.format(i)} - games to occur: {'{:,}'.format(four_way_wars_time[four_way_wars.index(i)])}")