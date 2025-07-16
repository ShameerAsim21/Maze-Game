import pygame
import random
import time
import os 


pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Maze Game")

# Colors
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Made by shameer


MAZE_WIDTH = 25  # Number of cells horizontally
MAZE_HEIGHT = 20 # Number of cells vertically
CELL_SIZE = 25   # Size of each cell in pixels

MAZE_OFFSET_X = (SCREEN_WIDTH - MAZE_WIDTH * CELL_SIZE) // 2
MAZE_OFFSET_Y = (SCREEN_HEIGHT - MAZE_HEIGHT * CELL_SIZE) // 2

# Player settings
PLAYER_SIZE = CELL_SIZE // 2
PLAYER_COLOR = RED

# Goal settings
GOAL_COLOR = GREEN

# Font for text display
font = pygame.font.Font(None, 36)

# File to save game results
RESULTS_FILE = "maze_game_results.txt"

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Initialize all walls as True (exists)
        self.maze = [[[True, True, True, True] for _ in range(height)] for _ in range(width)]
        # maze[x][y] = [top, right, bottom, left] wall
        self.visited = [[False for _ in range(height)] for _ in range(width)]
        self.player_x, self.player_y = 0, 0
        self.goal_x, self.goal_y = width - 1, height - 1
        self.moves = 0
        self.start_time = 0
        self.game_over = False
        self.won = False
        self.generate_maze()

    def generate_maze(self):
        """Generates the maze using Recursive Backtracking algorithm."""

        self.maze = [[[True, True, True, True] for _ in range(self.height)] for _ in range(self.width)]
        self.visited = [[False for _ in range(self.height)] for _ in range(self.width)]
        
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        stack = [(start_x, start_y)]
        self.visited[start_x][start_y] = True

        while stack:
            current_x, current_y = stack[-1]
            
            neighbors = []

            if current_y > 0 and not self.visited[current_x][current_y - 1]:
                neighbors.append((current_x, current_y - 1, 0, 2))
            # right
            if current_x < self.width - 1 and not self.visited[current_x + 1][current_y]:
                neighbors.append((current_x + 1, current_y, 1, 3))
            # bottom
            if current_y < self.height - 1 and not self.visited[current_x][current_y + 1]:
                neighbors.append((current_x, current_y + 1, 2, 0))
            # left
            if current_x > 0 and not self.visited[current_x - 1][current_y]:
                neighbors.append((current_x - 1, current_y, 3, 1))

            if neighbors:

                next_x, next_y, wall_current, wall_neighbor = random.choice(neighbors)

                self.maze[current_x][current_y][wall_current] = False
                self.maze[next_x][next_y][wall_neighbor] = False

                self.visited[next_x][next_y] = True
                stack.append((next_x, next_y))
            else:
                stack.pop() # Backtrack

        # Ensure start and end points are clear
        self.player_x, self.player_y = 0, 0
        self.goal_x, self.goal_y = self.width - 1, self.height - 1
        
        
        if self.player_x == 0: self.maze[self.player_x][self.player_y][3] = False 
        if self.player_y == 0: self.maze[self.player_x][self.player_y][0] = False 
        if self.goal_x == self.width - 1: self.maze[self.goal_x][self.goal_y][1] = False 
        if self.goal_y == self.height - 1: self.maze[self.goal_x][self.goal_y][2] = False 
        
        self.moves = 0
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.won = False

    def move_player(self, dx, dy):
        """
        Moves the player if the new position is valid (within bounds and no wall).
        dx, dy are change in x and y coordinates.
        """
        if self.game_over:
            return

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return 

        if dx == 1: # Moving right
            if self.maze[self.player_x][self.player_y][1]: 
                return
        elif dx == -1: # Moving left
            if self.maze[self.player_x][self.player_y][3]: 
                return
        elif dy == 1: # Moving down
            if self.maze[self.player_x][self.player_y][2]: 
                return
        elif dy == -1: # Moving up
            if self.maze[self.player_x][self.player_y][0]: 
                return
        
        self.player_x = new_x
        self.player_y = new_y
        self.moves += 1

        if self.player_x == self.goal_x and self.player_y == self.goal_y:
            self.won = True
            self.game_over = True
            self.save_game_results() 

    def save_game_results(self):
        """Saves the game results (moves and time) to a text file."""
        if not self.won: 
            return

        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000 
        
        current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

        result_line = f"Date/Time: {current_datetime}, Moves: {self.moves}, Time: {elapsed_time}s\n"

        try:
            with open(RESULTS_FILE, "a") as f:
                f.write(result_line)
            print(f"Game results saved to {RESULTS_FILE}")
        except IOError as e:
            print(f"Error saving game results to {RESULTS_FILE}: {e}")


    def draw(self, screen):
        """Draws the maze, player, and goal on the screen."""
        screen.fill(BLACK) # Background

        for x in range(self.width):
            for y in range(self.height):
                cell_left = MAZE_OFFSET_X + x * CELL_SIZE
                cell_top = MAZE_OFFSET_Y + y * CELL_SIZE

               
                if self.maze[x][y][0]:
                    pygame.draw.line(screen, WHITE, (cell_left, cell_top), (cell_left + CELL_SIZE, cell_top), 2)

                if self.maze[x][y][1]:
                    pygame.draw.line(screen, WHITE, (cell_left + CELL_SIZE, cell_top), (cell_left + CELL_SIZE, cell_top + CELL_SIZE), 2)

                if self.maze[x][y][2]:
                    pygame.draw.line(screen, WHITE, (cell_left, cell_top + CELL_SIZE), (cell_left + CELL_SIZE, cell_top + CELL_SIZE), 2)

                if self.maze[x][y][3]:
                    pygame.draw.line(screen, WHITE, (cell_left, cell_top), (cell_left, cell_top + CELL_SIZE), 2)

        # player
        player_center_x = MAZE_OFFSET_X + self.player_x * CELL_SIZE + CELL_SIZE // 2
        player_center_y = MAZE_OFFSET_Y + self.player_y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, PLAYER_COLOR, (player_center_x, player_center_y), PLAYER_SIZE)

        # goal
        goal_rect = pygame.Rect(MAZE_OFFSET_X + self.goal_x * CELL_SIZE, MAZE_OFFSET_Y + self.goal_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GOAL_COLOR, goal_rect)

        if not self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000 # in seconds
        else:

            if self.won:
                elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            else:
                elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000 


        moves_text = font.render(f"Moves: {self.moves}", True, YELLOW)
        time_text = font.render(f"Time: {elapsed_time}s", True, YELLOW)
        
        screen.blit(moves_text, (10, 10))
        screen.blit(time_text, (10, 50))

        if self.game_over:
            if self.won:
                message = "Congratilations, you Won!"
                message_color = GREEN
            else:
                message = "Game Over (Better Luck next time)" 
                message_color = RED
            
            game_over_text = font.render(message, True, message_color)
            restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)

            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

            screen.blit(game_over_text, text_rect)
            screen.blit(restart_text, restart_rect)


def main():
    """Main function to run the maze game."""
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if maze.game_over:
                    if event.key == pygame.K_r: 
                        maze.generate_maze() 
                    elif event.key == pygame.K_q: 
                        running = False
                else:
                    if event.key == pygame.K_UP:
                        maze.move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        maze.move_player(0, 1)
                    elif event.key == pygame.K_LEFT:
                        maze.move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        maze.move_player(1, 0)

        maze.draw(screen)
        pygame.display.flip() 

    pygame.quit()

if __name__ == "__main__":
    main()