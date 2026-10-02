from abstract_classes import AbstractDungeon
from map_entities import Hero, Goblin, Beholder
from copy import deepcopy
import random
import pickle
from collections import deque

class Dungeon(AbstractDungeon):
    """
    A class representing a dungeon where the hero navigates and fights monsters.
    """
    def __init__(self, size, tunnel_number, hero_name):
        """
        Initializes the dungeon with given size, number of tunnels and the hero's name.
        The dungeon will be created and entities placed.
        """
        super().__init__(size)    # Call parent constructor
        self.hero = Hero("@", hero_name, [1, 1], 5, 5, 1)    # Intialize the hero at position (1, 1)
        self.tunnel_number = tunnel_number
        self.current_map = []
        self.starting_entities = ["goblin", "goblin", "goblin", "goblin", "beholder"]    # Predefined entities
        self.entities = []
        self.empty_space = []
        self.message = ""
        self.create_dungeon()    # Generate the dungeon
        self.place_entities(self.starting_entities)    # Place entities in the dungeon
        self.update_map()    # Update map to reflect the hero's and entities' positions

    def __str__(self):
        """
        Returns a string representation of the current dungeon map and the hero's stats.
        """
        printable_map = ""
        for row in self.current_map:
            for column in row:
                printable_map += column    # Append each column of the map
            printable_map += "\n"    # Newline after each row

        hero_stats = f"Hero: {self.hero.name}  HP: {self.hero.hp}/{self.hero.max_hp}  " \
                     f"Gold: {self.hero.gold}  Stamina: {self.hero.stamina}  " \
                     f"XP: {self.hero.xp}  Level: {self.hero.level}\n"
                     
              
        return hero_stats + printable_map    # Combine the hero's stats and dungeon map

    def create_dungeon(self):
        """
        Initializes the dungeon map with walls and carves paths starting from the hero's position.
        """
        self.dungeon_map = [["▓" for _ in range(self.size[1])] for _ in range(self.size[0])]    # Initialize map with walls
        self.dungeon_map[1][1] = "."    # Set the hero's starting position to empty space
        
        self.carve_paths(1, 1)    # Start carving tunnels from the hero's starting position

        self.current_map = deepcopy(self.dungeon_map)    # Copy the dungeon map for use
        self.empty_space = [(x, y) for x in range(1, self.size[0] - 1) for y in range(1, self.size[1] - 1) if self.dungeon_map[x][y] == "."]

        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier    # Mark the hero's position on the map

    def is_valid(self, x, y):
        """
        Checks if given position is within the bounds of the dungeon.
        """
        return 0 < x < self.size[0] - 1 and 0 < y < self.size[1] - 1

    def carve_paths(self, x=1, y=1):
        """
        Carves random tunnels in the dungeon using depth-first search to create paths.
        """
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]    # Directions for carving tunnels
        random.shuffle(directions)    # Shuffle directions for randomness

        for dy, dx in directions:
            nx, ny = x + dx, y + dy    # Calculate the new coordinates
            if self.is_valid(nx, ny) and self.dungeon_map[ny][nx] == "▓":    # Check if the new position is valid
                self.dungeon_map[y + dy // 2][x + dx // 2] = "."    # Create tunnel between current and new position
                self.dungeon_map[ny][nx] = "."    # Mark the new position as empty space
                self.carve_paths(nx, ny)    # Recursively carve paths

    def place_entities(self, entities):
        """
        Places the specified entities (goblins and beholder) in random empty spaces in the dungeon.
        """
        position = random.sample(self.empty_space, len(self.starting_entities))    # Randomly sample positions
        for idx, entity in enumerate(self.starting_entities):
            if entity == "goblin":
                self.entities.append(Goblin(identifier="g", position=position[idx], base_attack=-1, base_ac=0, damage=1))    # Place goblins
            elif entity == "beholder":
                self.entities.append(Beholder(identifier="B", position=position[idx], base_attack=5, base_ac=2, damage=2))    # Place beholder

        # Update the dungeon map with the entities' positions
        for entity in self.entities:
            self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

    def hero_action(self, action):
        """
        Processes the hero's actions (movement and attack).
        """
        # Handle the hero's movement
        if action == "R" and self.dungeon_map[self.hero.position[0]][self.hero.position[1] + 1] != "▓":
            self.hero.position[1] += 1
        elif action == "L" and self.dungeon_map[self.hero.position[0]][self.hero.position[1] - 1] != "▓":
            self.hero.position[1] -= 1
        elif action == "D" and self.dungeon_map[self.hero.position[0] + 1][self.hero.position[1]] != "▓":
            self.hero.position[0] += 1
        elif action == "U" and self.dungeon_map[self.hero.position[0] - 1][self.hero.position[1]] != "▓":
            self.hero.position[0] -= 1

        self.update_map()    # Update map after the hero's movement

        # Move monsters (beholder)
        for entity in self.entities:
            if isinstance(entity, Beholder):
                entity.move(self, self.empty_space, self.hero.position)

        # Handle the hero's attack
        if action == "A":
            fighting = False
            for entity in self.entities:
                if tuple(self.hero.position) == entity.position:
                    fighting = True
                    if hasattr(entity, "attack"):
                        self.fight(entity)    # Initiate combat
            if not fighting:
                self.message = "Your big sword is hitting air really hard!"
            self.update_map()    # Update map after attack

    def fight(self, monster):
        """
        Simulates combat between the hero and monster.
        """
        hero_roll = self.hero.attack()    # Hero's attack roll
        monster_roll = monster.attack()    # Monster's attack roll

        # Hero attack hits monster
        if hero_roll["attack_roll"] > monster.base_ac:    
            monster.hp -= hero_roll["inflicted_damage"]
            if monster.hp > 0:
                self.message = f"Hero inflicted {hero_roll['inflicted_damage']}"    # Display inflicted damage
            else:
                self.message = f"Hero slain {monster} "    # Display monster slain message
                self.hero.gold += monster.gold    # Add monster's gold to hero
                self.hero.xp += 1    # Add experience
                self.dungeon_map[monster.position[0]][monster.position[1]] = "."    # Remove monster from map
                self.entities.remove(monster)    # Remove monster from entities list

        # Monster attack hits hero
        if monster_roll["attack_roll"] > self.hero.base_ac:
            self.hero.hp -= monster_roll["inflicted_damage"]
            if self.hero.hp < 1:
                self.message += f"{self.hero.name} has been slain by {monster}"    # Display hero slain message
            self.message += f"\nHero HP: {self.hero.hp} Monster HP: {monster.hp}"    # Display hero's remaining HP

    def update_map(self):
        """
        Updates the dungeon map to reflect the current positions of the hero and entitites.
        """
        self.current_map = deepcopy(self.dungeon_map)    # Copy the dungeon map
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier    # Update the hero's position

    def save(self, file):
        """
        Saves the current state of the game to a file using pickle.
        """
        pickle.dump(self, file)

    @staticmethod
    def load(file):
        """
        Loads a saved game from a file using pickle.
        """
        return pickle.load(file)
