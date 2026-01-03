class Plant:
    """A simple program that manage and make plant growth over time."""
    def __init__(self, name, height, age):
        """
        Initialize a Plant object with a name, height, and age.
        """
        self.name = name
        self.height = height
        self.age = age

    def age_up(self):
        """This is the function that make age grow."""
        self.age += 1

    def grow(self):
        """This is the function that make height grow."""
        self.height += 1

    def get_info(self):
        """This is the function that print info about plant."""
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    plant = Plant("Rose", 25, 30)
    print("=== Day 1 ===")
    plant.get_info()
    old_height = plant.height
    i = 0
    while i < 6:
        plant.age_up()
        plant.grow()
        i += 1
    print("=== Day 7 ===")
    plant.get_info()
    print(f"Growth this week: +{plant.height - old_height}cm")
