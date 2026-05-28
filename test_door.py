from inventory import Inventory, JANITOR_KEY, ROOM_210_KEY
from door import Door

# Create inventory
inventory = Inventory()

# Create doors
janitor_room = Door("Janitor Room", JANITOR_KEY)
room_210 = Door("Room 210", ROOM_210_KEY)

# Test Janitor Room
print("=== JANITOR ROOM TEST ===")

janitor_room.show_status()

# Try unlocking without key
inventory.use_item(JANITOR_KEY, janitor_room)

print()

# Add key
inventory.add_item(JANITOR_KEY)

print()

# Unlock door
inventory.use_item(JANITOR_KEY, janitor_room)

# Show status
janitor_room.show_status()

print("\n")

# Test Room 210
print("=== ROOM 210 TEST ===")

room_210.show_status()

# Try unlocking without key
inventory.use_item(ROOM_210_KEY, room_210)

print()

# Add key
inventory.add_item(ROOM_210_KEY)

print()

# Unlock door
inventory.use_item(ROOM_210_KEY, room_210)

# Show status
room_210.show_status()