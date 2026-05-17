from inventory import Inventory, JANITOR_KEY
from door import Door

# Create inventory and door
inventory = Inventory()
janitor_room = Door("Janitor Room", JANITOR_KEY)

# Show initial door status
janitor_room.show_status()

# Try unlocking without key
inventory.use_item(JANITOR_KEY, janitor_room)

print()

# Add janitor key
inventory.add_item(JANITOR_KEY)

print()

# Try unlocking again
inventory.use_item(JANITOR_KEY, janitor_room)

# Show updated door status
janitor_room.show_status()
