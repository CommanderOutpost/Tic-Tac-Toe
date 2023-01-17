import random
import time

def create_board():
    """
    This function creates the game board for Tic-Tac-Toe.
    It initializes the board with empty spaces represented by '-'
    """
    board = [["-" for _ in range(3)] for _ in range(3)]
    return board


def display_board(board):
    """
    This function takes in the current game board and displays it to the players
    """
    print("-------------")
    for row in board:
        print("|", end="")
        for element in row:
            print(f" {element} |", end="")
        print("\n-------------")


current_letter = 'X'

def user_input(board):
    """
    This function takes in the current game board and prompts the user to input their desired row and column to place their symbol
    """
    global current_letter
    while True:
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1
            
            if board[row][col] == "-":
                board[row][col] = current_letter
                current_letter = 'X' if current_letter == 'O' else 'O'
                return board
            else:
                print("This cell is already filled. Please choose another cell.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
        except IndexError:
            print("Invalid input. Please enter a number between 1 and 3.")


def computer_input(board):
    global current_letter
    print("Computer is thinking...")
    x = random.randint(1,2)
    time.sleep(x)

    # Check if computer can win in the next move
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = current_letter
                if check_win(board) == current_letter:
                    current_letter = 'X' if current_letter == 'O' else 'O'
                    return board
                board[i][j] = "-"

    # Check if the user can win in the next move
    user_letter = 'O' if current_letter == 'X' else 'X'
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = user_letter
                if check_win(board) == user_letter:
                    board[i][j] = current_letter
                    current_letter = 'X' if current_letter == 'O' else 'O'
                    return board
                board[i][j] = "-"

    # Check if there is a fork opportunity for the computer
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = current_letter
                if check_fork(board, current_letter) == current_letter:
                    current_letter = 'X' if current_letter == 'O' else 'O'
                    return board
                board[i][j] = "-"

    # Check if there is a fork opportunity for the user
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = user_letter
                if check_fork(board, current_letter) == user_letter:
                    board[i][j] = current_letter
                    current_letter = 'X' if current_letter == 'O' else 'O'
                    return board
                board[i][j] = "-"

    # Check if there is an opportunity to play in the center
    if board[1][1] == "-":
        board[1][1] = current_letter
        current_letter = 'X' if current_letter == 'O' else 'O'
        return board

    # Check if there is an opportunity to play in a corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if board[corner[0]][corner[1]] == "-":
            board[corner[0]][corner[1]] = current_letter
            current_letter = 'X' if current_letter == 'O' else 'O'
            return board

    # If no strategic move can be made, play randomly
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == "-":
            board[row][col] = current_letter
            current_letter = 'X' if current_letter == 'O' else 'O'
            return board





def check_win(board):
    """
    This function checks if there is a winning combination of symbols on the board
    """
    # check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "-":
            return board[i][0]
    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "-":
            return board[0][i]
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
        return board[0][2]
    return None

def check_full(board):
    """
    This function checks if the board is full and no more moves can be made
    """
    return all(all(cell != '-' for cell in row) for row in board)
                
def check_tie(board):
    """
    This function checks if the game is a tie
    """
    return check_full(board) and check_win(board) is None             

def check_fork(board, letter):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = letter
                if check_win(board) == letter:
                    # check if playing this move doesn't block the opponent fork
                    opponent_letter = 'X' if letter == 'O' else 'O'
                    board[i][j] = opponent_letter
                    if check_win(board) != opponent_letter:
                        board[i][j] = '-'
                        return letter
                board[i][j] = "-"
    return "-"
 
play_against = input("Would you like to play against the computer or another player? (C/P): ").upper()

def take_turns(board):
    """
    This function alternates turns between the players and prompts them to input
    """
    while True:
        board = user_input(board)
        display_board(board)
        winner = check_win(board)
        if winner:
            print(f"{winner} wins!")
            break
        if check_tie(board):
            print("It's a tie!")
            break
        if play_against == "C":
            board = computer_input(board)
        else:
            board = user_input(board)
        display_board(board)
        winner = check_win(board)
        if winner:
            print(f"{winner} wins!")
            break
        if check_tie(board):
            print("It's a tie!")
            break

            
#Create the board
board = create_board()

#Game Loop
while True:
    
    display_board(board)
    try:
        take_turns(board)
    except Exception as e:
        print(e)
        print("Invalid input, please try again.")
        continue
    winner = check_win(board)
    if winner:
        play_again = input(f"{winner} wins! Do you want to play again? (Y/N): ").upper()
        if play_again == "N":
            print("Thanks for playing!")
            exit()
        else:
            board = create_board()

    if check_tie(board):
        play_again = input("It's a tie! Do you want to play again? (Y/N)").upper()
        if play_again == "N":
            print("Thanks for playing!")
            exit()
        else:
            board = create_board()
