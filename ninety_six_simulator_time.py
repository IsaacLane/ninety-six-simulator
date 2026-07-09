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
shortest = 600
game_number = 0
deck = []
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
        random.shuffle(p1_collect)
        p1_draw.extend(p1_collect)
        p1_collect.clear()
    if len(p2_draw) == 0:
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
            war()
    except IndexError:
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
    global total_timer
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
    if p1_score > p2_score:
        p1_wins += 1
    elif p1_score < p2_score:
        p2_wins += 1
    elif p1_score == p2_score:
        ties += 1
    total_timer -= points_time
    
print("Welcome to the 96 Simulator!")
desired_minutes = input("Please enter how many minutes of gameplay you'd like to simulate ")
while True:
    try:
        desired_minutes = int(desired_minutes)
    except ValueError:
        desired_minutes = input("Please enter a valid input ")
        continue
    else:
        if desired_minutes > 10000000 or desired_minutes <= 0:
            desired_minutes = input("Please enter a valid input ")
            continue
        else:
            break
total_timer = desired_minutes * 60
start_time = time.time()
assemble_deck()
while total_timer > 0:
    beginning_time = random.randrange(5, 10) * 60
    timer = beginning_time
    game_number += 1
    p1_collect = []
    p2_collect = []
    p1_draw = []
    p2_draw = []
    p1_war = []
    p2_war = []
    random.shuffle(deck)
    timer -= shuffle_time
    deal()
    while not ((len(p1_draw) == 0 and len(p1_collect) == 0) or (len(p2_draw) == 0 and len(p2_collect) == 0) or
    timer <= 0 or war == "insufficient_cards_for_war"):
        check_reshuffle_draw()
        if hierarchy.index((p1_draw[0]).split("_")[0]) > hierarchy.index((p2_draw[0]).split("_")[0]):
            timer -= play_time
            p1_collect.extend([p1_draw[0], p2_draw[0]])
            p2_draw.pop(0)
            p1_draw.pop(0)
            timer -= gather_time
        elif hierarchy.index((p1_draw[0]).split("_")[0]) < hierarchy.index((p2_draw[0]).split("_")[0]):
            timer -= play_time
            p2_collect.extend([p1_draw[0], p2_draw[0]])
            p1_draw.pop(0)
            p2_draw.pop(0)
            timer -= gather_time
        else:
            timer -= play_time
            if not wars:
                wars.append(0)
            wars[0] += 1
            war()
    if timer < 0:
        timer = 0
    if beginning_time - timer < shortest:
        shortest = beginning_time - timer
    total_timer -= beginning_time - timer 
    if len(p1_draw) == 0 and len(p1_collect) == 0:
        p2_wins += 1
    elif len(p2_draw) == 0 and len(p2_collect) == 0:
        p1_wins += 1
    else:
        scoring()
    if total_timer > 0:
        print(f"Simulated {round(desired_minutes - total_timer / 60)} of {desired_minutes} minutes")
        print("\033[1A", end = "\x1b[2K")
    else:
        print(f"Simulated {desired_minutes} of {desired_minutes} minutes", end = "\n")
print("-----------------------")
print(f"Simulation took {time.time() - start_time} seconds")
print(f"{game_number} games were played")
print(f"Player 1 won {round((p1_wins/game_number) * 100, 5)}% of the time ({p1_wins} times), while Player 2 won {round((p2_wins/game_number) * 100, 5)}% of the time ({p2_wins} time(s))")    
print(f"Ties happened {round((ties/game_number) * 100, 5)}% of the time ({ties} time(s))")
print(f"The shortest game took {round(shortest / 60)} minute(s) and {shortest % 60} second(s)")
print("Wars:")
if wars[0] != 0:
    print(f"{wars[0]} single war(s)")
for i in wars[1:]:
    print(f"{wars[wars.index(i)]} {war_names[wars.index(i)].lower()} war(s)")
