import json

# Full gam reset
# Used when:
# - Player dies in Level 2
# - Player chooses New Game
# - Player quits to Main Menu
def reset_game():
    # Reset inventory
    with open('save_inventory.json', 'w') as f:
        json.dump({"items": [], "uses": {}, "collected":{}}, f, indent = 4)

    # Reset level 1
    with open('save_level1.json', 'w') as f:
        json.dump(
            {
                "security_room_unlocked": False,
                "room116_unlocked": False,
                "room117_unlocked": False,
                "connecting_door_unlocked": False,
                "exit_door_unlocked": False,
                "receptionist_defeated": False,
                "ghost_defeated": False
            },
            f, 
            indent = 4
        )

    # Reset level 2
    with open('save_level2.json', 'w') as f:
        json.dump(
            {
                "room206_unlocked": False,
                "room210_unlocked": False,
                "janitor_room_unlocked": False,
                "janitor_defeated": False,
                "stairs_unlocked": False,

                "room210_key_collected": False,
                "janitor_key_collected": False,
                "security_badge_collected": False,

                "locker_unlocked": False,
                
                "toolbox_collected": False,
                "stool_collected": False,
                "box_collected": False,
                "locker_collected": False,

                "treadmill_completed": False
            }, 
            f, 
            indent = 4
        )

    print("Game reset successfully.")

# Reset level 1 only
# Used when: Player dies in Level 1 and presses Retry
# Keeps:
# - Level 2 progress
# - Level 2 inventory
# Resets:
# - Level 1 progress
# - Level 1 inventory
def reset_level1():
    # Load current inventory
    try:
        with open('save_inventory.json', 'r') as f:
            inventory_data = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        inventory_data = {"items": [], "uses": {}, "collected":{}}

    # Remove ONLY Level 1 items
    level1_items = [
        "ROOM116_KEY",
        "ROOM117_KEY",
        "ROOM116_117_CODE",
        "EXIT_DOOR_KEY"
    ]

    inventory_data["items"] = [
        item 
        for item in inventory_data.get("items", [])
        if item not in level1_items
    ]

    # Remove collected state
    for item in level1_items:
        inventory_data.get("collected", {}).pop(item, None)  # Safely remove the item if it exists
        inventory_data.get("uses", {}).pop(item, None)  # Safely remove the item if it exists

    # Save inventory back
    with open('save_inventory.json', 'w') as f:
        json.dump(inventory_data, f, indent=4)

    # Reset level 1 progress
    with open('save_level1.json', 'w') as f:
        json.dump(
            {
                "security_room_unlocked": False,
                "room116_unlocked": False,
                "room117_unlocked": False,
                "connecting_door_unlocked": False,
                "exit_door_unlocked": False,
                "receptionist_defeated": False,
                "ghost_defeated": False
            },
            f, 
            indent = 4
        )

    print("Level 1 reset successfully.")