import random 

def draw(main_list):
    for i in range(3):
        print("---------")
        for j in range(3):
            print(main_list[i][j], end="|")
        print()
    print("---------")

def check_position(main_list):
    valid_position = []
    for i in range(3):
        for j in range(3):
            if main_list[i][j] == " ":
                valid_position.append((i, j))
    return valid_position

def check_win(main_list, player):
    for i in range(3):
        if main_list[i][0] == main_list[i][1] == main_list[i][2] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"
    for j in range(3):
        if main_list[0][j] == main_list[1][j] == main_list[2][j] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"

    if main_list[0][0] == main_list[1][1] == main_list[2][2] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"
    elif main_list[2][0] == main_list[1][1] == main_list[0][2] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"

    return False, ""

def diff_normal(valid_position):
    for i in range(3):
        if main_list[i].count(human) == 2 and main_list[i].count(" ") >= 1:
            pos = main_list[i].index(" ")
            return (i,pos)
    for j in range(3):
        column_list = [main_list[0][j], main_list[1][j], main_list[2][j]]
        if column_list.count(human) == 2 and column_list.count(" ") >= 1:
            pos = column_list.index(" ")
            return (pos, j)
    diag_list1 = [main_list[0][0], main_list[1][1], main_list[2][2]]
    if diag_list1.count(human) == 2 and diag_list1.count(" ") >= 1:
        pos = diag_list1.index(" ")
        return (pos, pos) 
    diag_list2 = [main_list[2][0], main_list[1][1], main_list[0][2]]
    if diag_list2.count(human) == 2 and diag_list2.count(" ") >= 1:
        pos = diag_list2.index(" ")
        return (pos, pos)
    return random.choice(valid_position)

def diff_hard(valid_position):
    if computer == "O":
        pos = diff_normal(valid_position)
        return pos
    else:
        for i in range(3):
            if main_list[i].count(computer) == 2 and main_list[i].count(" ") >= 1:
                pos = main_list[i].index(" ")
                return (i,pos)
    for j in range(3):
        column_list = [main_list[0][j], main_list[1][j], main_list[2][j]]
        if column_list.count(computer) == 2 and column_list.count(" ") >= 1:
            pos = column_list.index(" ")
            return (pos, j)
    diag_list1 = [main_list[0][0], main_list[1][1], main_list[2][2]]
    if diag_list1.count(computer) == 2 and diag_list1.count(" ") >= 1:
        pos = diag_list1.index(" ")
        return (pos, pos) 
    diag_list2 = [main_list[2][0], main_list[1][1], main_list[0][2]]
    if diag_list2.count(computer) == 2 and diag_list2.count(" ") >= 1:
        pos = diag_list2.index(" ")
        return (pos, pos)
    return random.choice(valid_position)

def comp_move(valid_position):
    if difficult == "1":
        pos = random.choice(valid_position)
        return pos[0], pos[1]
    if difficult == "2":
        pos = diff_normal(valid_position)
        return pos[0], pos[1]
    if difficult == "3":
        pos = diff_hard(valid_position)
        return pos[0], pos[1]

player1 = "X"
player2 = "O"

main_list = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "] ]

while True:
    first_move = input("Do you want to keep the first move? (y / n): ").lower().strip()
    if first_move in ("y", "n"):
        if first_move == "y":
            human = "X"
            computer = "O"
        else:
            human = "O"
            computer = "X"
        break

text_diff = """
What type of difficult you will be choice? 
1 - easy;
2 - normal;
3 - hard
 """
difficult = input(text_diff)

player = player1

while True:
    draw(main_list)

    print("----------------------------------")
    print("Player1" if player == "X" else "Player2")
    valid_position = check_position(main_list)
    if len(valid_position) == 0:
        print("No winners!")
        break
    print("Please choose your move: ", valid_position)

    if player == computer:
        x, y = comp_move(valid_position)

    else:
        x, y = map(int, input().split())
        while (x, y) not in valid_position:
            print("Please choose your move: ", valid_position)
            x, y = map(int, input().split())

    main_list[x][y] = player

    flag, result = check_win(main_list, player)
    if flag:
        print(result)
        draw(main_list)
        break

    if player == player1:
        player = player2
    else:
        player = player1
    
    