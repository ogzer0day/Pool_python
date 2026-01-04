data = {
    'alice': ['first_blood', 'pixel_perfect', 'speed_runner',
              'first_blood', 'first_blood'],

    'bob': ['first_blood', 'level_master', 'boss_hunter', 'treasure_seeker',
            'level_master', 'level_master'],

    'charlie': ['treasure_seeker', 'boss_hunter', 'combo_king', 'first_blood',
                'boss_hunter', 'first_blood', 'boss_hunter', 'first_blood'],

    'diana': ['first_blood', 'combo_king', 'level_master', 'treasure_seeker',
              'speed_runner', 'combo_king', 'combo_king', 'level_master'],

    'eve': ['level_master', 'treasure_seeker', 'first_blood',
            'treasure_seeker', 'first_blood', 'treasure_seeker'],

    'frank': ['explorer', 'boss_hunter', 'first_blood',
              'explorer', 'first_blood', 'boss_hunter']
}

if __name__ == "__main__":
    print("=== Achievement Tracker System ===")
    print()

    unique_achievements = set()
    common_to_all_players = set(data['alice'])

    achievement_counts = {}

    for player_name, achievements in data.items():
        player_set = set(achievements)
        print(f"Player {player_name} achievements: {player_set}")

        unique_achievements = unique_achievements.union(player_set)
        common_to_all_players = common_to_all_players.intersection(player_set)

        for achievement in player_set:
            if achievement in achievement_counts:
                achievement_counts[achievement] += 1
            else:
                achievement_counts[achievement] = 1

    print()
    print("=== Achievement Analytics ===")
    print(f"All unique achievements: {unique_achievements}")
    print(f"Total unique achievements: {len(unique_achievements)}\n")
    print(f"Common to all players: {common_to_all_players}")

    rare_achievements = {a for a, count in achievement_counts.items()
                         if count == 1}
    print(f"Rare achievements (1 player): {rare_achievements}")

    print()
    alice = set(data['alice'])
    bob = set(data['bob'])
    print(f"Alice vs Bob common: {set(alice.intersection(bob))}")
    print(f"Alice unique: {set(alice.difference(bob))}")
    print(f"Alice unique: {set(bob.difference(alice))}")
