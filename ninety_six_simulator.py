import random
import time
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
deck = []
war_first_occurence = []
wars = []
hierarchy = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
war_names = ["Single", "Double", "Triple", "Quadruple", "Quintuple", "Sextuple", "Septuple"]
def assemble_deck():
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
def deal():
    for i in range(26):
        p1_draw.append(deck[i])
    for i in range(26, 52):
        p2_draw.append(deck[i])
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
    global timer
    global war_num
    try:
        for i in range(4):
            p1_war.append(p1_draw[0])
            p2_war.append(p2_draw[0])
            p1_draw.pop(0)
            p2_draw.pop(0)
            check_reshuffle_draw()
        timer -= war_time
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
def scoring():
    p1_score = 0
    p2_score = 0
    p1_total = p1_draw + p1_collect + p1_war
    p2_total = p2_draw + p2_collect + p2_war
    p1_score = len(p1_total)
    p2_score = len(p2_total)
    global p1_wins
    global p2_wins
    global ties
    for i in p1_total:
        if i.split("_")[0] == "Jack":
            p1_score += 1
        elif i.split("_")[0] == "Queen":
            p1_score += 2
        elif i.split("_")[0] == "King":
            p1_score += 3
        elif i.split("_")[0] == "Ace":
            p1_score += 5
    for i in p2_total:
        if i.split("_")[0] == "Jack":
            p2_score += 1
        elif i.split("_")[0] == "Queen":
            p2_score += 2
        elif i.split("_")[0] == "King":
            p2_score += 3
        elif i.split("_")[0] == "Ace":
            p2_score += 5
    if p1_score == 96 or p2_score == 96:
        ninety_six += 1
    if p1_score > p2_score:
        if printing_on == True:
            print(f"Player 1 wins, {p1_score} to {p2_score}")
        p1_wins += 1
    elif p1_score < p2_score:
        if printing_on == True:
            print(f"Player 2 wins, {p2_score} to {p1_score}")
        p2_wins += 1
    elif p1_score == p2_score:
        if printing_on == True:
            print("It's a tie - 48 to 48 :O")
        ties += 1
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
    random.shuffle(deck)
    timer -= shuffle_time
    if printing_on == True:
        print("Dealing cards...")
    deal()
    if printing_on == True:
        print(f"Starting game number {game_number}")
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
    if timer <= 0:
       if printing_on == True: 
           print("Time is up!")
    else:
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
            print(f"Simulated {i + 1} of {desired_games} games")
            print("\033[1A", end = "\x1b[2K")
        else:
            print(f"Simulated {i + 1} of {desired_games} games", end = "\n")
print("-----------------------")
print(f"Simulation took {time.time() - start_time} seconds")
print(f"Player 1 won {round((p1_wins/desired_games) * 100, 5)}% of the time ({'{:,}'.format(p1_wins)} times), while Player 2 won {round((p2_wins/desired_games) * 100, 5)}% of the time ({'{:,}'.format(p2_wins)} time(s))")    
print(f"Ties happened {round((ties/desired_games) * 100, 5)}% of the time ({'{:,}'.format(ties)} time(s))")
print(f"There were {'{:,}'.format(ninety_six)} 96 to 0 game(s) (Happened {round((ninety_six/desired_games) * 100)}% of the time)")
print(f"The shortest game took {round(shortest / 60)} minute(s) and {shortest % 60} second(s)")
print("Wars:")
if wars[0] != 0:
    print(f"{'{:,}'.format(wars[0])} single wars")
for i in wars[1:]:
    print(f"{'{:,}'.format(wars[wars.index(i)])} {war_names[wars.index(i)].lower()} wars - took {'{:,}'.format(war_first_occurence[wars.index(i) - 1])} games to occur")
