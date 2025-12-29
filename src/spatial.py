import math

class SpatialGrid:
    def __init__(self, map_width, map_height, cell_size):
        self.cell_size = cell_size
        self.cols = math.ceil(map_width / cell_size)
        self.rows = math.ceil(map_height / cell_size)
        self.grid = {} # Dictionary mapping (col, row) -> list of objects
                       # Object structure: (snake_instance, body_part_rect)

    def clear(self):
        self.grid = {}

    def _get_cell_coords(self, x, y):
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        return col, row

    def insert(self, snake):
        """
        Insert a snake's body parts into the grid.
        Optimization: Instead of every pixel, we insert every body part rect.
        Ideally, since body parts are close, we could check which cells the rect overlaps.
        For simplicity, we just add the center point of each body part to its cell.
        """
        # Set to track which cells we've already added this snake to (to avoid duplicates per cell if multiple parts in same cell)
        # Actually, we need to store individual body parts for collision checks, 
        # so we might want to store (snake, body_part) tuples.
        
        for part in snake.body:
            col, row = self._get_cell_coords(part.centerx, part.centery)
            
            # Boundary check
            if 0 <= col < self.cols and 0 <= row < self.rows:
                key = (col, row)
                if key not in self.grid:
                    self.grid[key] = []
                self.grid[key].append((snake, part))

    def get_potential_colliders(self, rect, search_radius_cells=1):
        """
        Return a list of (snake, body_part_rect) that are in cells neighboring the rect.
        """
        candidates = []
        
        # Calculate range of cells to check
        start_col, start_row = self._get_cell_coords(rect.left, rect.top)
        end_col, end_row = self._get_cell_coords(rect.right, rect.bottom)
        
        # Expand search by radius (to catch bodies just across the border)
        start_col -= search_radius_cells
        start_row -= search_radius_cells
        end_col += search_radius_cells
        end_row += search_radius_cells
        
        for c in range(start_col, end_col + 1):
            for r in range(start_row, end_row + 1):
                key = (c, r)
                if key in self.grid:
                    candidates.extend(self.grid[key])
                    
        return candidates
