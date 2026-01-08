import sys

if __name__ == "__main__":
    print("=== Player Score Analytics ===")

    value: int = 1
    i: int = 0
    total_players: int = len(sys.argv) - 1
    total_scor: int = 0

    try:
        for value in sys.argv[1:]:
            total_scor += int(value)
        res = total_scor / total_players
    except Exception:
        print("No scores provided. Usage: python3 ft_score_analytics.py "
              "<score1> <score2> ...")
    else:
        my_list: list[int] = []
        print("Scores processed: [", end="")

        for value in sys.argv[1:]:
            print(value, end="")
            if i != total_players - 1:
                print(', ', end="")
            my_list.append(int(value))
            i += 1

        print("]")
        print(f"Total players: {total_players}")
        print(f"Total score: {total_scor}")
        print(f"Average score: {res}")
        print(f"High score: {max(my_list)}")
        print(f"Low score: {min(my_list)}")
        print(f"Score range: {max(my_list) - min(my_list)}")
