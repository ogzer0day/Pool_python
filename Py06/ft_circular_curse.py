from alchemy.grimoire.validator import validate_ingredients
from alchemy.grimoire.spellbook import record_spell

print("=== Circular Curse Breaking ===\n")

print("Testing ingredient validation:")
print("validate_ingredients(\"fire air\"): "
      f"{validate_ingredients('fire air')}")
print("validate_ingredients(\"dragon scales\"): "
      f"{validate_ingredients('firdragone scales')}\n")

print("Testing spell recording with validation:")
print("record_spell(\"Fireball\", \"fire air\"): "
      f"{record_spell('Fireball', 'fire air')}")
print("record_spell(\"Dark Magic\", \"shadow\"): "
      f"Spell rejected: {record_spell('Dark Magic', 'shadow')}\n")

print("Testing late import technique:")
print("record_spell(\"Lightning\", \"air\"): "
      f"{record_spell('Lightning', 'air')}\n")

print("Circular dependency curse avoided using late imports!\n"
      "All spells processed safely!")
