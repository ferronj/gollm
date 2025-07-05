import pygame
import numpy as np
import random
import sys

class GameOfLife:
    def __init__(self, width=800, height=600, cell_size=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # Initialize grid
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.running = True
        self.paused = False
        self.generation = 0
        
    def randomize_grid(self, density=0.3):
        """Fill grid with random alive cells based on density"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 1 if random.random() < density else 0
        self.generation = 0
    
    def clear_grid(self):
        """Clear all cells"""
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.generation = 0
    
    def count_neighbors(self, row, col):
        """Count living neighbors for a given cell"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                
                # Handle boundary conditions (wrap around)
                neighbor_row = (row + i) % self.rows
                neighbor_col = (col + j) % self.cols
                count += self.grid[neighbor_row][neighbor_col]
        
        return count
    
    def update_grid(self):
        """Apply Conway's Game of Life rules"""
        new_grid = np.zeros((self.rows, self.cols), dtype=int)
        
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(i, j)
                
                # Conway's rules:
                # 1. Any live cell with 2-3 neighbors survives
                # 2. Any dead cell with exactly 3 neighbors becomes alive
                # 3. All other cells die or stay dead
                
                if self.grid[i][j] == 1:  # Currently alive
                    if neighbors == 2 or neighbors == 3:
                        new_grid[i][j] = 1
                else:  # Currently dead
                    if neighbors == 3:
                        new_grid[i][j] = 1
        
        self.grid = new_grid
        self.generation += 1
    
    def draw_grid(self):
        """Draw the current state of the grid"""
        self.screen.fill(self.BLACK)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.cell_size
                y = i * self.cell_size
                
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, self.GREEN, 
                                   (x, y, self.cell_size, self.cell_size))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, self.GRAY, 
                               (x, y, self.cell_size, self.cell_size), 1)
    
    def handle_mouse_click(self, pos):
        """Toggle cell state when clicked"""
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        
        # Make sure we're within bounds
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 - self.grid[row][col]
            print(f"Toggled cell at ({row}, {col}) to {self.grid[row][col]}")
    
    def draw_info(self):
        """Draw generation counter and controls"""
        font = pygame.font.Font(None, 36)
        
        # Generation counter
        gen_text = font.render(f"Generation: {self.generation}", True, self.WHITE)
        self.screen.blit(gen_text, (10, 10))
        
        # Status
        status = "PAUSED" if self.paused else "RUNNING"
        status_text = font.render(status, True, self.WHITE)
        self.screen.blit(status_text, (10, 50))
        
        # Controls
        controls = [
            "SPACE: Pause/Resume",
            "R: Randomize",
            "C: Clear",
            "Click: Toggle cell"
        ]
        
        small_font = pygame.font.Font(None, 24)
        for i, control in enumerate(controls):
            text = small_font.render(control, True, self.WHITE)
            self.screen.blit(text, (10, self.height - 100 + i * 20))
    
    def run(self):
        """Main game loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.randomize_grid()
                    elif event.key == pygame.K_c:
                        self.clear_grid()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_mouse_click(event.pos)
            
            # Update simulation
            if not self.paused:
                self.update_grid()
            
            # Draw everything
            self.draw_grid()
            self.draw_info()
            pygame.display.flip()
            
            # Control frame rate
            self.clock.tick(10)  # 10 FPS
        
        pygame.quit()
        sys.exit()

# Example patterns you can create manually
def create_glider(game, start_row=10, start_col=10):
    """Create a glider pattern"""
    glider = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ]
    
    for i, row in enumerate(glider):
        for j, cell in enumerate(row):
            if start_row + i < game.rows and start_col + j < game.cols:
                game.grid[start_row + i][start_col + j] = cell

def create_blinker(game, start_row=5, start_col=5):
    """Create a blinker pattern"""
    blinker = [
        [1, 1, 1]
    ]
    
    for i, row in enumerate(blinker):
        for j, cell in enumerate(row):
            if start_row + i < game.rows and start_col + j < game.cols:
                game.grid[start_row + i][start_col + j] = cell

if __name__ == "__main__":
    # Create and run the game
    game = GameOfLife(width=1000, height=800, cell_size=8)
    
    # Optional: Start with some interesting patterns
    create_glider(game, 10, 10)
    create_blinker(game, 5, 5)
    
    game.run()