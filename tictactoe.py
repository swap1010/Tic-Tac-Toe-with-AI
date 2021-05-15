import random

cells = ["_"] * 9


def print_game(elem):
    print("---------")
    res = ["|"]
    for n, cell in enumerate(elem, 1):
        if cell == "_":
            res.append(" ")
        else:
            res.append(cell)
        if n % 3 == 0:
            res.append("|")
            print(" ".join(res))
            res = ["|"]
    print("---------")


def computer_move_easy():
    global cells
    print('Making move level "easy"')
    select = random.randint(0, 8)
    while cells[select] != "_":
        select = random.randint(0, 8)
    if cells.count("X") > cells.count("O"):
        cells[select] = "O"
    else:
        cells[select] = "X"
    print_game(cells)


def result(chance):
    x_o = "".join(chance)
    win = [x_o[:3], x_o[3:6], x_o[6:], x_o[2:8:2], x_o[::4], x_o[::3], x_o[1::3], x_o[2::3]]
    if "XXX" in win:
        return "X wins"
    elif "OOO" in win:
        return "O wins"
    elif "_" not in x_o:
        return "Draw"
    else:
        return "Game not finished"


def computer_move_medium():
    print('Making move level "medium"')
    my = "O" if cells.count("X") > cells.count("O") else "X"
    op = "O" if my == "X" else "X"
    for n, win in enumerate(cells):
        if win == "_":
            cells[n] = my
            if my in result(cells):
                break
            cells[n] = op
            if op in result(cells):
                break
            cells[n] = "_"
    else:
        select = random.randint(0, 8)
        while cells[select] != "_":
            select = random.randint(0, 8)
        if cells.count("X") > cells.count("O"):
            cells[select] = "O"
        else:
            cells[select] = "X"

    print_game(cells)


scores = {'X': -1, 'O': 1}


def minimax(start_player, current, ismaximizing):
    state = result(cells)[0]
    if "_" not in cells:
        return 0
    if state in scores:
        return 10 if start_player in state else -10
    bot = "O" if current == "X" else "X"
    bestscore = float('-inf') if ismaximizing else float('inf')
    for n, cell in enumerate(cells):
        if cell == "_":
            cells[n] = current
            score = minimax(start_player, bot, not ismaximizing)
            cells[n] = "_"
            bestscore = max(score, bestscore) if ismaximizing else min(score, bestscore)
    return bestscore


def computer_move_hard():
    global cells
    print('Making move level "hard"')
    bot = "O" if cells.count("X") > cells.count("O") else "X"
    human = "O" if bot == "X" else "X"
    bestscore = float('-inf')
    move = 0
    for n, cell in enumerate(cells):
        if cell == "_":
            cells[n] = bot
            score = minimax(bot, human, False)
            cells[n] = "_"
            if score > bestscore:
                bestscore = score
                move = n
    cells[move] = bot
    print_game(cells)


def user_move():
    while True:
        try:
            row, col = map(int, input("Enter the coordinates: ").split())
            if not 1 <= row <= 3 or not 1 <= col <= 3:
                print("Coordinates should be from 1 to 3!")
            else:
                cell_num = ((row - 1) * 3) + (col - 1)
                if cells[cell_num] != "_":
                    print("This cell is occupied! Choose another one!")
                else:
                    if cells.count("X") > cells.count("O"):
                        cells[cell_num] = "O"
                    else:
                        cells[cell_num] = "X"
                    print_game(cells)
                    break
        except ValueError:
            print("You should enter numbers!")


player = {"user": user_move, "easy": computer_move_easy, "medium": computer_move_medium, "hard": computer_move_hard}


def play(move1, move2):
    while "_" in cells:
        move1()
        if result(cells) != "Game not finished":
            print(result(cells))
            exit()

        move2()
        if result(cells) != "Game not finished":
            print(result(cells))
            exit()


while True:
    user_choice = input("Input command: ").strip()
    if user_choice == "exit":
        break
    else:
        try:
            start, mode1, mode2 = user_choice.split()
            if mode1 not in player or mode2 not in player:
                raise ValueError
            print_game(cells)
            play(player[mode1], player[mode2])
        except ValueError:
            print("Bad parameters!")
