# Inventory System
class Inventory:
    def __init__(self):
        self.items = []

    # Add item to inventory
    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
            print (f"Picked up: {item}")
        else:
            print (f"You already have {item} in your inventory.")

    # Check if item is in inventory
    def has_item(self, item):
        return item in self.items
    
    # Remove item from inventory
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print (f"Removed: {item} from inventory.")
        else:
            print (f"{item} is not in your inventory.")

    # Display inventory items
    def show_inventory(self):
        if self.items:
            print("Inventory:", self.items)
        else:
            print("Your inventory is empty.")

# Keys
JANITOR_KEY = "janitor_key"
ROOM_210_KEY = "room_210_key"
SECURITY_BADGE = "security_badge"
EXIT_KEY = "exit_key"

# Tools
LOCK_CUTTER = "lock_cutter"
SCREWDRIVER = "screwdriver"

# Weapon Pieces
WEAPON_1 = "weapon_piece_1"
WEAPON_2 = "weapon_piece_2"
WEAPON_3 = "weapon_piece_3"


# --------------------
# TEST / DEMO
# --------------------

if __name__ == "__main__":
    inventory = Inventory()

    # Show empty inventory
    inventory.show_inventory()

    # Pick up items
    inventory.add_item(JANITOR_KEY)
    inventory.add_item(LOCK_CUTTER)
    inventory.add_item(SCREWDRIVER)

    # Try duplicate
    inventory.add_item(JANITOR_KEY)

    # Show inventory
    inventory.show_inventory()

    # Check items
    print("Has janitor key?", inventory.has_item(JANITOR_KEY))
    print("Has room 210 key?", inventory.has_item(ROOM_210_KEY))

    # Remove item
    inventory.remove_item(LOCK_CUTTER)

    # Final inventory
    inventory.show_inventory()