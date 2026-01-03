class Plant:
    """
    A simple program that stores and displays information about garden plants.
    """
    def __init__(self, name, height, age):
        """
        Initialize a Plant object with a name, height, and age.
        """
        self.name = name
        self.height = height
        self.age = age

    def ft_garden_data_fun(self):
        """
        Print the plant's details in a formatted string.
        """
        print(f"{self.name}: {self.height}cm, {self.age} days old")


print("=== Garden Plant Registry ===")
plant1 = Plant("Rose", 25, 30)
plant2 = Plant("Sunflower", 80, 45)
plant3 = Plant("Cactus", 15, 120)

plant1.ft_garden_data_fun()
plant2.ft_garden_data_fun()
plant3.ft_garden_data_fun()
