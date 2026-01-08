GameData = {
    "players": {
        "alice": {
            "level": 41,
            "total_score": 2824,
            "sessions_played": 13,
            "favorite_mode": "ranked",
            "achievements_count": 5,
        },
        "bob": {
            "level": 16,
            "total_score": 4657,
            "sessions_played": 27,
            "favorite_mode": "ranked",
            "achievements_count": 2,
        },
        "charlie": {
            "level": 44,
            "total_score": 9935,
            "sessions_played": 21,
            "favorite_mode": "ranked",
            "achievements_count": 7,
        },
        "diana": {
            "level": 3,
            "total_score": 1488,
            "sessions_played": 21,
            "favorite_mode": "casual",
            "achievements_count": 4,
        },
        "eve": {
            "level": 33,
            "total_score": 1434,
            "sessions_played": 81,
            "favorite_mode": "casual",
            "achievements_count": 7,
        },
        "frank": {
            "level": 15,
            "total_score": 8359,
            "sessions_played": 85,
            "favorite_mode": "competitive",
            "achievements_count": 1,
        },
    },

    "sessions": [
        {"player": "bob", "duration_minutes": 94, "score": 1831,
         "mode": "competitive", "completed": False},
    ],

    "meta": {
        "game_modes": ["casual", "competitive", "ranked"],
        "achievements": [
            "first_blood",
            "level_master",
            "speed_runner",
            "treasure_seeker",
            "boss_hunter",
            "pixel_perfect",
            "combo_king",
            "explorer",
        ],
    },
}


def list_comprehension():
    """
    Demonstrates list comprehension usage.

    - hights_scores: List of players whose total_score > 2000
    - Scores_doubled: List of those players' scores multiplied by 2
    - Active_players: List of all players in the dataset

    Prints:
    - High scorers (>2000)
    - Scores doubled
    - Active players
    """
    players = GameData["players"]
    hights_scores = [player for player in players
                     if players[player]['total_score'] > 2000]
    Scores_doubled = [players[player]['total_score'] * 2 for player in players
                      if players[player]['total_score'] > 2000]
    Active_players = [player for player in players]

    print(f"High scorers (>2000): {hights_scores}")
    print(f"Scores doubled: {Scores_doubled}")
    print(f"Active players: {Active_players}\n")


def dict_comprehension():
    """
    Demonstrates dictionary comprehension usage.

    - Player_scores: Maps each player to their total_score
    - achievements_count: Maps each player to their achievements_count
    - Score categories:
        * high: total_score >= 5000
        * medium: 2000 <= total_score <= 5000
        * low: total_score < 2000

    Prints:
    - Player scores dictionary
    - Count of players in each score category
    - Player achievement counts
    """
    players = GameData["players"]
    high = sum(1 for player in players
               if players[player]['total_score'] >= 5000)
    medium = sum(1 for player in players
                 if players[player]['total_score'] >= 2000 and
                 players[player]['total_score'] <= 5000)
    low = sum(1 for player in players if players[player]['total_score'] < 2000)

    Player_scores = {player:  players[player]['total_score']
                     for player in players}

    achievements_count = {player: players[player]['achievements_count']
                          for player in players}

    print(f"Unique players: {Player_scores}")
    print(f"Score categories: "
          f"{dict({'high': high, 'medium': medium, 'low': low})}")
    print(f"Achievement counts: {achievements_count}\n")


def set_comprehension():
    """
    Demonstrates set comprehension usage.

    - Unique_players: Set of all players
    - Unique achievements: Set of all achievements defined in meta
    - Active regions: Set of all game modes defined in meta

    Prints:
    - Unique players
    - Unique achievements
    - Active game modes
    """
    players = GameData["players"]
    meta = GameData["meta"]
    Unique_players = {player for player in players}

    print(f"Unique players: {Unique_players}")
    print(f"Unique achievements: {set(meta['achievements'])}")
    print(f"Active regions: {set(meta['game_modes'])}\n")


if __name__ == "__main__":
    print("=== Game Analytics Dashboard ===\n")

    print("=== List Comprehension Examples ===")
    list_comprehension()

    print("=== Dict Comprehension Examples ===")
    dict_comprehension()

    print("=== Set Comprehension Examples ===")
    set_comprehension()

    print("=== Generator Demonstration ===")
    print(f"Total players: {len(GameData['players'])}")
    print(f"Total unique achievements: "
          f"{len(GameData['meta']['achievements'])}")
    players = GameData["players"]
    avrage_scor = sum(players[player]['total_score'] for player in players)
    print(f"Average score: "
          f"{avrage_scor / len(GameData['meta']['achievements'])}")
    print(
        f"Top performer: alice "
        f"({GameData['players']['alice']['total_score']} points, "
        f"{GameData['players']['alice']['achievements_count']} achievements)"
    )
