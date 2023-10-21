import random

def print_piles(piles):
    for i, pile in enumerate(piles):
        print(f"Row {i + 1}: {'*' * pile}")

def is_winner(piles):
    return all(pile == 0 for pile in piles)

def minimax(piles, depth, is_maximizing):
    if is_winner(piles):
        return (-1, 0) if is_maximizing else (1, 0)
    if depth == 0:
        return (0, 0)

    best_move = (-1, 0)
    best_value = -float("inf") if is_maximizing else float("inf")
    for i, pile in enumerate(piles):
        if pile > 0:
            for objects in range(1, pile + 1):
                new_piles = piles[:]
                new_piles[i] -= objects
                result = minimax(new_piles, depth - 1, not is_maximizing)
                if is_maximizing:
                    if result[0] > best_value:
                        best_value = result[0]
                        best_move = (i, objects)
                else:
                    if result[0] < best_value:
                        best_value = result[0]
                        best_move = (i, objects)
    return best_move

def alpha_beta(piles, depth, alpha, beta, is_maximizing):
    if is_winner(piles):
        return (-1, 0) if is_maximizing else (1, 0)
    if depth == 0:
        return (0, 0)

    if is_maximizing:
        best_move = (-1, 0)
        value = -float("inf")
        for i, pile in enumerate(piles):
            if pile > 0:
                for objects in range(1, pile + 1):
                    new_piles = piles[:]
                    new_piles[i] -= objects
                    result = alpha_beta(new_piles, depth - 1, alpha, beta, False)
                    if result[0] > value:
                        value = result[0]
                        best_move = (i, objects)
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
        return best_move
    else:
        best_move = (-1, 0)
        value = float("inf")
        for i, pile in enumerate(piles):
            if pile > 0:
                for objects in range(1, pile + 1):
                    new_piles = piles[:]
                    new_piles[i] -= objects
                    result = alpha_beta(new_piles, depth - 1, alpha, beta, True)
                    if result[0] < value:
                        value = result[0]
                        best_move = (i, objects)
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
        return best_move


def dfs(piles, depth, is_maximizing):
    if is_winner(piles):
        return 1 if is_maximizing else -1
    if depth == 0:
        return 0

    if is_maximizing:
        max_value = -float("inf")
        for i, pile in enumerate(piles):
            if pile > 0:
                for objects in range(1, pile + 1):
                    new_piles = piles[:]
                    new_piles[i] -= objects
                    value = dfs(new_piles, depth - 1, False)
                    max_value = max(max_value, value)
        return max_value
    else:
        min_value = float("inf")
        for i, pile in enumerate(piles):
            if pile > 0:
                for objects in range(1, pile + 1):
                    new_piles = piles[:]
                    new_piles[i] -= objects
                    value = dfs(new_piles, depth - 1, True)
                    min_value = min(min_value, value)
        return min_value

def ai_move(piles, ai_type):
    if ai_type == 1:  # Alpha-Beta Pruning
        best_move = alpha_beta(piles, 3, -float("inf"), float("inf"), True)
        return best_move
    elif ai_type == 2:  # Minimax
        best_move = minimax(piles, 3, True)
        return best_move
    elif ai_type == 3:  # Depth-First Search
        best_value = -float("inf")
        best_move = (0, 1)

        for i, pile in enumerate(piles):
            if pile > 0:
                for objects in range(1, pile + 1):
                    new_piles = piles[:]
                    new_piles[i] -= objects
                    value = dfs(new_piles, 3, False)

                    if value > best_value:
                        best_value = value
                        best_move = (i, objects)
        return best_move

def main():
    piles = [4, 5, 6, 7]
    game_over = False
    player_turn = True

    print("Nim Game")
    print_piles(piles)

    ai_type = int(input("Choose your AI opponent (1 for Alpha-Beta, 2 for Minimax, 3 for DFS): "))

    while not game_over:
        if player_turn:
            try:
                player_row, player_objects = map(int, input("Enter your move (row objects): ").split())
                if player_row < 1 or player_row > len(piles) or player_objects < 1 or player_objects > piles[player_row - 1]:
                    print("Invalid move. Try again.")
                    continue
                piles[player_row - 1] -= player_objects
            except (ValueError, IndexError):
                print("Invalid input. Please enter your move in the format 'row objects'.")
                continue
        else:
            ai_row, ai_objects = ai_move(piles, ai_type)
            if ai_row is not None:
                piles[ai_row] -= ai_objects
                print(f"AI removes {ai_objects} objects from row {ai_row + 1}")

        player_turn = not player_turn
        print_piles(piles)

        if all(pile == 0 for pile in piles):
            if player_turn:
                print("AI wins!")
            else:
                print("You win!")
            game_over = True

if __name__ == "__main__":
    main()
