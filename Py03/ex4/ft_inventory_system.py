"""
Player Inventory System

This script manages and analyzes the inventory of players in a game.

Data Structure:
- game_data:
    - players: dictionary of players with their items, total value, and item count
    - catalog: dictionary of item definitions with type, value, and rarity

Functions:
1. alice_inventory(player, catalog, inventory_value, item_count)
    - Prints a detailed inventory summary for Alice.
    - Shows each item with type, rarity, quantity, value per unit, and total value.
    - Prints total inventory value and item count.
    - Prints a static example of categories (hardcoded for Alice).

2. inventory_analytics()
    - Finds and prints:
        * Most valuable player based on total inventory value
        * Player with the most items in their inventory

Main Execution:
- Prints Alice's inventory
- Demonstrates a transaction: Alice giving Bob 2 quantum_rings
- Prints updated quantities if the transaction succeeds
- Runs inventory analytics to find top players
- Finds the last iterated item as the "rarest item" (from last loop)
"""

game_data = {
    "players": {
        "alice": {
            "items": {
                "pixel_sword": 1,
                "code_bow": 1,
                "health_byte": 1,
                "quantum_ring": 3,
            },
            "item_count": 6,
            "total_value": 1875,
        },
        "bob": {
            "items": {
                "pixel_sword": 2,
                "code_bow": 3,
            },
            "item_count": 5,
            "total_value": 900,
        },
        "charlie": {
            "items": {
                "pixel_sword": 1,
                "code_bow": 1,
            },
            "item_count": 2,
            "total_value": 350,
        },
        "diana": { 
            "items": {
                "pixel_sword": 3,
                "code_bow": 3,
                "health_byte": 3,
                "data_crystal": 3,
            },
            "item_count": 12,
            "total_value": 4125,
        },
    },

    "catalog": {
        "pixel_sword": {
            "type": "weapon",
            "value": 150,
            "rarity": "common",
        },
        "code_bow": {
            "type": "weapon",
            "value": 200,
            "rarity": "uncommon",
        },
        "health_byte": {
            "type": "consumable",
            "value": 25,
            "rarity": "common",
        },
        "quantum_ring": {
            "type": "accessory",
            "value": 500,
            "rarity": "rare",
        },
        "data_crystal": {
            "type": "material",
            "value": 1000,
            "rarity": "legendary",
        },
    },
}


def alice_inventory(player, catalog, inventory_value, item_count):
    """
    Prints a detailed inventory report for a given player (Alice).
    """
    for value in player.keys():
        for val in catalog.keys():
            if value == val:
                quantity = player[value]
                item_value = catalog[val].get("value")
                total_price = quantity * item_value

                print(f"{val} ({catalog[val].get('type')},"
                      f"{catalog[val].get('rarity')}): ", end="")
                print(
                    f"{quantity}x @ {item_value} gold each = "
                    f"{total_price} gold"
                    )
    print()
    print(f"Inventory value: {inventory_value} gold")
    print(f"Item count: {item_count} items")
    print("Categories: pixel_sword(1), code_bow(1), health_byte(1), "
          "quantum_ring(3)\n")


def inventory_analytics():
    """
    Analyzes all players' inventories to find top performers.'
    """
    print("=== Inventory Analytics ===")

    max_item = 0
    max_value = 0
    player_max_item = ""
    player_max_value = ""

    for name, values in game_data["players"].items():
        if values['item_count'] > max_item:
            max_item = values['item_count']
            player_max_item = name
        if values['total_value'] > max_value:
            max_value = values['total_value']
            player_max_value = name

    print(f"Most valuable player: {player_max_value} ({max_value} gold)")
    print(f"Most items: {player_max_item} ({max_item} items)")


if __name__ == "__main__":
    print("=== Player Inventory System ===\n")

    print("=== Alice's Inventory ===")
    player = game_data["players"]['alice']['items']
    catalog = game_data["catalog"]
    inventory_value = game_data["players"]['alice']['total_value']
    item_count = game_data["players"]['alice']['item_count']

    alice_inventory(player, catalog, inventory_value, item_count)

    print("=== Transaction: Alice gives Bob 2 quantum_ring ===")
    if (player['quantum_ring'] - 2) > 0:
        print("Transaction successful!\n")
        print("=== Updated Inventories ===")
        print(f"Alice potions: {player['quantum_ring'] - 2}")
        print("Bob potions: 2\n")
    else:
        print("Transaction failed: not enough items\n")

    inventory_analytics()
    rerest = ()
    for key, val in game_data["players"].items():
        for x in val['items']:
            rerest = x

    print(f"Rarest items: {rerest}")
