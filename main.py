import os
import subprocess
from datetime import datetime
from dungeon import Dungeon

def save_game(dungeon, hero_name):
    """
    Saves the current game state to a file with a timestamp filename.
    """
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")    # Current timestamp (date and time)
    filename = f"{hero_name}_{timestamp}.dng"    # Creates a filename in format hero_name_timestamp.dng
    
    with open(filename, "wb") as file:    # Open the file in binary write mode to save the game state
        dungeon.save(file)    # Call the save method from Dungeon class
    print(f"Game saved as {filename}")    # Notify the player that the game has been saved succesfully

def load_game(filename):
    """
    Loads a previously saved game state from a file.
    """
    with open(filename, "rb") as file:   # Open the file in binary read mode
        return Dungeon.load(file)    # Load and return the saved dungeon object

if __name__ == "__main__":
    hero_name = input("What is your name, hero? ")    # Prompt user for their hero name 

    # Ask if the player wants to load an existing game
    load_existing = input("Do you want to load an existing game? (y/n): ").strip().lower()
    
    if load_existing == "y":
        filename = input("Enter the filename of the saved game: ").strip()    # Prompt for the filename
        if os.path.exists(filename):    # Check if the file exists
            dungeon = load_game(filename)    # Load the existing game
        else:
            print("File not found. Starting a new game.")    # If the file doesn't exist start a new game
            dungeon = Dungeon(size=(15, 15), tunnel_number=10, hero_name=hero_name)    # Create a new dungeon
    else:
        dungeon = Dungeon(size=(15, 15), tunnel_number=10, hero_name=hero_name)    # Create a new dungeon if the user doesn't want to load game
    
    while True:
        subprocess.Popen("cls", shell=True).communicate()    # Clear the screen (Windows command)
        print(dungeon)    # Print the dungeon state (current map and hero stats)
        print(dungeon.message)    # Print any message (combat results)

        # Prompt for an action
        action = input(f"Select an action {hero_name}: (L)EFT, (R)IGHT, (D)OWN, (U)P, (A)TTACK, (S)AVE, (Q)UIT: ").strip().upper()
        
        if action == "Q":
            print("You coward!")    # If the player chooses to quit print a message and exit 
            exit(0)
        elif action == "S":
            save_game(dungeon, hero_name)    # Save the game if the player chooses to save
        else:
            dungeon.hero_action(action)    # Execute the chosen hero action
