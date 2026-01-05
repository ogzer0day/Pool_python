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


if __name__ == "__main__":
    print("=== Player Inventory System ===")
    print()
    print("=== Alice's Inventory ===")
    player = game_data["players"]['alice']['items']
    catalog = game_data["catalog"]
    i = 0
    Inventory_value = 0
    Item_count = 0
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
                Item_count += item_value
                Inventory_value += total_price
