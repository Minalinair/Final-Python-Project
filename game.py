# beginning the game by laying out the board display format
def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")
#taking user input allowing the current player to choose the postion
def get_valid_move(board, current_player):

    while True:
        try:
            move_input = input(f"Player {current_player}, enter a cell number (1-9): ").strip()
            
            if not move_input:
                print("Input cannot be empty. Please try again.")
                continue
                
            move = int(move_input)
            
        
            if move < 1 or move > 9:
                print("Invalid range! Please pick a number between 1 and 9.")
                continue
            
            if board[move - 1] in ['X', 'O']:
                print("That cell is already taken! Choose an empty one.")
                continue
                
            return move - 1
         # Return 0-indexed position for the list
            
        except ValueError:
            print("Invalid input! Please enter a valid whole number.")

#checking if any of the player has won- by checking the rows, columns and diagonals
def check_win(board):
    """Checks all 3 rows, 3 columns, and 2 diagonals for a winning match."""
    win_conditions = [[0,1,2], [3, 4, 5], [6, 7, 8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]] 
    
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]]:
            return True
    return False

#checks for any draw i.e in cases where the cells are full but no same full row, column or diagonal
def check_draw(board):
    for cell in board:
        if cell != 'X' and cell != 'O':
            return False
    return True


def play_game():
    # Main game loop controlling turns, win/draw detection, and restarts.
    print("=== WELCOME TO TIC-TAC-TOE ===")
    
    while True:
        board = [str(i) for i in range(1, 10)]
        current_player = 'X'
        game_over = False
        
        while not game_over:
            display_board(board)
            
            # Get valid player move
            position = get_valid_move(board, current_player)
            board[position] = current_player
            
            # Check for a win
            if check_win(board):
                display_board(board)
                print(f"🎉 Congratulations! Player {current_player} wins! 🎉")
                game_over = True
            # Check for a draw
            elif check_draw(board):
                display_board(board)
                print("🤝 It's a draw! The board is full. 🤝")
                game_over = True
            # Switch players
            else:
                current_player = 'O' if current_player == 'X' else 'X'
        
        # Ask to play again
        play_again = input("Do you want to play another round? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\nThank you for playing! Goodbye.")
            break


# Trigger the game execution
if __name__ == "__main__":
    play_game()