class Plant:
    """
    A simple program that make creat many plants with defferent starting
    values.
    """
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


def ft_plan_factory(list_plants):
    """A simple function that set up plants with  their starting values."""
    i = 0
    while i < len(list_plants):
        print(
            f"Created: {list_plants[i].name} "
            f"({list_plants[i].height}cm, {list_plants[i].age} days)"
        )
        i += 1
    print()
    print(f"Total plants created: {i}")


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    plant1 = Plant("Rose", 25, 30)
    plant2 = Plant("Oak", 200, 365)
    plant3 = Plant("Cactus", 5, 90)
    plant4 = Plant("Sunflower", 80, 45)
    plant5 = Plant("Fern", 15, 120)

    list_plants = [plant1, plant2, plant3, plant4, plant5]
    ft_plan_factory(list_plants)
