from abstract_classes import Creature
import random
from collections import deque

class Goblin(Creature):
    object_type = "monster"
    
    def __init__(self, identifier, position, base_attack, base_ac, damage):
        """
        Initializes the Goblin with given identifier, position, attack stats and damage.
        The Golbin's health and gold is randomized within given range.
        """
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.hp = random.randint(1, 5)    # Random health between 1 and 5
        self.xp = 10    # Experience points given when defeated
        self.gold = random.randint(1, 6)    # Random gold drop between 1 and 6

    def __str__(self):
        """
        Returns string representation of the Goblin.
        """
        return "goblin"

class Hero(Creature):
    object_type = "hero"
    
    def __init__(self, identifier, name, position, base_attack, base_ac, damage):
        """
        Initializes the Hero with given identifier, name, position, attack stats and damage.
        The Hero starts with full health and stamina and level 1.
        """
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.name = name    # Hero's name
        self.max_hp = 50    # Maximum health
        self.hp = 50    # Current health
        self.max_stamina = 20    # Maximum stamina
        self.stamina = 20    # Current stamina
        self.xp = 0    # Experience points
        self.level = 1    # Starting level
        self.gold = 0    # Starting gold
        
    def rest(self):
        """
        Restores Hero's health and stamina to their maximum.
        """
        self.hp = self.max_hp
        self.stamina = self.max_stamina
        
    def level_up(self):
        """
        Increases Hero's level and maximum health.
        """
        self.level += 1
        self.max_hp += 5

class Beholder(Creature):
    object_type = "monster"

    def __init__(self, identifier, position, base_attack, base_ac, damage):
        """
        Initializes the Beholder with given identifier, position, attack stats and damage.
        The Beholder's health and gold are randomized within given range.
        """
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.hp = random.randint(10, 20)    # Random health between 10 and 20
        self.xp = 30    # Experience points given when defeated
        self.gold = random.randint(5, 15)    # Random gold drop between 5 and 15
        
    def __str__(self):
        """
        Returns string representation of the Beholder.
        """
        return "beholder"
    
    def move(self, dungeon, empty_space, hero_position):
        """
        Moves the Beholder towards Hero if within certain distance or randomly if farther away.
        It updates the dungeon map afterwards.
        """
        distance_to_hero = abs(hero_position[0] - self.position[0]) + abs(hero_position[1] - self.position[1])
        
        if distance_to_hero <= 10:    # If the Hero is close enough
            path = self.find_shortest_path(dungeon, hero_position)

            if path:
                next_step = path[0]    # Get the next step to take
                old_position = self.position
                goblins_to_restore = []    # List to track goblins displaced by the Beholder

                # Restore any goblins that were displaced by the Beholder's movement
                for entity in dungeon.entities:
                    if isinstance(entity, Goblin) and entity.position == old_position:
                        goblins_to_restore.append(entity)
                        
                dungeon.dungeon_map[old_position[0]][old_position[1]] = "."
                self.position = next_step
                dungeon.dungeon_map[self.position[0]][self.position[1]] = self.map_identifier

                # Restore the goblins' positions
                for goblin in goblins_to_restore:
                    dungeon.dungeon_map[goblin.position[0]][goblin.position[1]] = "g"
        else:
            self.move_randomly(dungeon)

    def find_shortest_path(self, dungeon, target):
        """
        Uses BFS to find the shortest path to Hero on the dungeon map.
        Returns the path as a list of positions if found or None if no path exists.
        """
        start = tuple(self.position)
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            if current == tuple(target):
                return path    # Return the found path

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_position = (current[0] + dy, current[1] + dx)
                if 0 <= next_position[0] < len(dungeon.dungeon_map) and 0 <= next_position[1] < len(dungeon.dungeon_map[0]):
                    tile = dungeon.dungeon_map[next_position[0]][next_position[1]]

                    if tile == "." and next_position not in visited:
                        queue.append((next_position, path + [next_position]))
                    elif tile.lower() == "g" and next_position not in visited:
                        queue.append((next_position, path + [next_position]))
        return None

    def move_towards_hero(self, dungeon, hero_position):
        """
        Moves the Beholder one step towards the Hero's position considering the shortest path
        along the x and y axes.
        """
        hy, hx = hero_position
        by, bx = self.position

        dy = hy - by
        dx = hx - bx

        if abs(dy) > abs(dx):
            new_y = by + (1 if dy > 0 else -1)
            new_x = bx
        else:
            new_x = bx + (1 if dx > 0 else -1)
            new_y = by

        if dungeon.dungeon_map[new_y][new_x] == "." and (new_y, new_x) not in [e.position for e in dungeon.entities]:
            dungeon.dungeon_map[by][bx] = "."
            self.position = [new_y, new_x]
            dungeon.dungeon_map[new_y][new_x] = self.map_identifier

    def move_randomly(self, dungeon):
        """
        Moves the Beholder randomly within dungeon ensuring new position is valid.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        old_y, old_x = self.position
        dungeon.dungeon_map[old_y][old_x] = "."    # Clear old position

        for dy, dx in directions:
            new_x = self.position[1] + dx
            new_y = self.position[0] + dy

            # Check if the new positon is within bounds and valid
            if (0 < new_x < len(dungeon.dungeon_map[0]) - 1 and
                0 < new_y < len(dungeon.dungeon_map) -1 and
                dungeon.dungeon_map[new_y][new_x] == "." and
                (new_y, new_x) not in [e.position for e in dungeon.entities]):
                self.position = [new_y, new_x]
                break
        new_y, new_x = self.position
        dungeon.dungeon_map[new_y][new_x] = self.map_identifier    # Update dungeon map
        
    def update_position(self, dungeon):
        """
        Updates the Beholder's position on the dungeon map.
        """
        dungeon.dungeon_map[self.position[0]][self.position[1]] = self.map_identifier
