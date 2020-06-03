def check_position(main_list):
    valid_position = []
    for i in range(3):
        for j in range(3):
            if main_list[i][j] == " ":
                valid_position.append((i,j))
    return valid_position

def draw(main_list):
    for i in range(3):
        print("-------")
        for j in range(3):
            print(main_list[i][j], end="|")
        print()
    print("-------")

def check_win(main_list, player):
    print(player)
    for i in range(3):
        if main_list[i][0] == main_list[i][1] == main_list[i][2] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"
    for j in range(3):
        if  main_list[0][j] == main_list[1][j] == main_list[2][j] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"
    if main_list[0][0] == main_list[1][1] == main_list[2][2] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"
    elif main_list[2][0] == main_list[1][1] == main_list[0][2] == player:
            return True, "Player1 wins!" if player == "X" else "Player2 wins!"
    return False, ""


player1 = "X"
player2 = "O"

main_list = [[" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]]

player = player1
while True:
    draw(main_list)

    print("-------------------------------")
    print("Player1" if player == "X" else "Player2")
    valid_position = check_position(main_list)
    print("Check please your move: ", valid_position, "\n")
    x, y = map(int, input().split())
    while (x, y) not in valid_position:
        print("Check please your move: ", valid_position, "\n")
        x, y = input().split()
    main_list[x][y] = player 
    
    flag, result = check_win(main_list, player)
    if flag:
        print(result)
        break

    if player == player1:
        player = player2
    else:
        player = player1