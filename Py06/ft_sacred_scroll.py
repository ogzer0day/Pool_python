import alchemy

print("=== Sacred Scroll Mastery ===\n")

print("Testing direct module access:")
print(f"alchemy.elements.create_fire(): "
      f"{alchemy.elements.create_fire()}")
print("alchemy.elements.create_water(): "
      f"{alchemy.elements.create_water()}")
print(f"alchemy.elements.create_earth(): "
      f"{alchemy.elements.create_earth()}")
print(f"alchemy.elements.create_air(): "
      f"{alchemy.elements.create_air()}\n")

print("Testing package-level access "
      "(controlled by __init__.py):")
try:
    print(f"alchemy.create_fire(): {alchemy.create_fire()}")
except AttributeError:
    print("alchemy.create_fire(): AttributeError - not exposed")
try:
    print(f"alchemy.create_water(): {alchemy.create_water()}")
except AttributeError:
    print("alchemy.create_wate: AttributeError - not exposed")
try:
    print(f"alchemy.create_earth(): {alchemy.reate_earth()}")
except AttributeError:
    print("alchemy.create_earth(): AttributeError - not exposed")

try:
    print(f"alchemy.create_earth(): {alchemy.create_air()}")
except AttributeError:
    print("alchemy.create_air(): AttributeError - not exposed")

print()
print("Package metadata:")
print(f"Version: {alchemy.__version__}")
print(f"Author: {alchemy.__author__}")
