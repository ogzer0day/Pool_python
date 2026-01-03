class Plan:
    """A program that make you handle handle different types of plants:
    flowers, trees, and vegetables, and Each specialized type should
    inherit the basic plant features"""
    def __init__(self, name, height, age):
        """
        Initialize a Plant object with a name, height, and age.
        """
        self.name = name
        self.height = height
        self.age = age


class Flower(Plan):
    """
    Represents a Flower, which is a type of plant.
    """
    def __init__(self, name, height, age, color):
        """
        Initialize a Plant object with a name, height, age, and color.
        """
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        """
         A simple fun that print info about plant and ability to bloom.
        """
        print(
            f"{self.name} (Flower): "
            f"{self.height}cm, {self.age} days, {self.color} color"
        )
        print(f"{self.name} is blooming beautifully!")


class Tree(Plan):
    """
    Represents a tree, which is a type of plant with a trunk diameter.
    """
    def __init__(self, name, height, age, trunk_diameter):
        """
        Initialize a Plant object with a name, height, age, and trunk_diameter.
        """
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self):
        """
         A simple fun that print info about plant and ability to produce_shade.
        """
        print(
            f"{self.name} (Tree): "
            f"{self.height}cm, {self.age} days, {self.trunk_diameter} diameter"
        )
        Shade_area = self.trunk_diameter / 7
        print(f"{self.name} provides {int(Shade_area)} square meters of shade")


class Vegetable(Plan):
    """
    Represents a Vegetable, which is a type of plant with a nutritional_value.
    """
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        """
        Initialize a Plant object with a name, height, age,
        and nutritional_value.
        """
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def summery_veg(self):
        """
        A simple fun that print info about plant and ability to produce_shade.
        """
        print(
            f"{self.name} (Vegetable): "
            f"{self.height}cm, {self.age} days, {self.harvest_season} harvest"
        )
        print(f"{self.name}  is rich in {self.nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    my_flower = Flower("Rose", 25, 30, "red")
    my_flower.bloom()
    print()
    my_tree = Tree("Oak", 500, 1825, 50)
    my_tree. produce_shade()
    print()
    my_vegetable = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    my_vegetable.summery_veg()
