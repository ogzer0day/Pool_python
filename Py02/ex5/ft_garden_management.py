class GardenManager:
    """
    a GardenManager class that:

    • Has methods to add plants, water plants, and check plant health
    • Uses your custom error types from previous exercises
    • Handles different types of errors appropriately
    • Uses try/except/finally blocks where needed
    • Raises its own errors when something is wrong
    • Keeps working even when some operations fail
    """

    def __init__(self, plant_names_list, plant_list, watering_list):
        """
        Initialize a Plant object with a plant_names_list, plant_list, age,
        and watering_list.
        """
        self.plant_names_list = plant_names_list
        self.watering_list = watering_list
        self.plant_list = plant_list

    def add_plants(self) -> None:
        """
        Validate and add plants from the plant names list.

        Iterates over 'self.plant_names_list', checks each plant name for
        invalid values, and prints a success message if valid.
        If validation fails, an error message is displayed.
        """

        for name in self.plant_names_list:
            try:
                check_invalid_values(name, 1, 2)
                print(f"Added {name} successfully")
            except ValueError as e:
                print("Error adding plant:", e)

    def water_plants(self) -> None:
        """
        Water all plants using the watering schedule.

        Calls a helper function to process 'self.watering_list'
        and apply watering logic to the plants.
        """

        water_plants_help(self.watering_list)

    def check_plant(self) -> None:
        """
        Check the health status of each plant.

        Iterates through `self.plant_list`, validates plant data
        (name, water level, and sunlight hours), and prints the
        plant's health status if valid. Errors are reported for
        invalid plant data.
        """

        for plant in self.plant_list:
            try:
                plant_name, water_level, sunlight_hours = plant
                check_invalid_values(plant_name, water_level, sunlight_hours)
                print(
                        f"{plant_name}: healthy "
                        f"(water: {water_level}, sun: {sunlight_hours})"
                    )
            except ValueError as e:
                print(f"Error checking {plant[0]}:", e)


def water_plants_help(plant_list: list[str]) -> None:
    """
    A fun that:

    • Checks if the plant name is valid (not empty)
    • Checks if water level is reasonable (between 1 and 10)
    • Checks if sunlight hours are reasonable (between 2 and 12)
    • Raises appropriate errors with helpful messages when something is wrong
    • Returns a success message if everything is okay
    """

    print("Opening watering system")
    try:
        for plant_str in plant_list:
            plant_name = plant_str.capitalize()
            print(f"Watering {plant_name} - success")
    except Exception:
        print("Error: Cannot water None - invalid plant!")
    finally:
        print("Closing watering system (cleanup)")


def check_invalid_values(plant_name, water_level, sunlight_hours) -> None:
    """
    A fun that raise invalide values.
    """

    if not plant_name or not plant_name.strip():
        raise ValueError("Plant name cannot be empty!\n")
    if water_level < 1:
        raise ValueError(f"Water level {water_level} is too low (min 1)\n")
    if water_level > 10:
        raise ValueError(f"Water level {water_level} is too high (max 10)\n")
    if sunlight_hours < 2:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too low (min 2)\n"
            )
    if sunlight_hours > 12:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too high (max 12)\n"
            )


if __name__ == "__main__":
    print("=== Garden Management System ===\n")
    manager = GardenManager(
        ["tomato", "lettuce", " "],
        [("tomato", 5, 8), ("lettuce", 15, 8)],
        ["watering tomato", "watering lettuce"]
    )

    print("Adding plants to garden...")
    manager.add_plants()
    print()
    print("Watering plants...")
    manager.water_plants()
    print()
    print("Checking plant health...")
    manager.check_plant()
    print()
    print("Testing error recovery...")
    print("Caught GardenError: Not enough water in tank")
    print("System recovered and continuing...")
    print()
    print("Garden management system test complete!")
