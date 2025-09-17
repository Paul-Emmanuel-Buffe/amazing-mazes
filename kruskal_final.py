import random
import os
from metrics_record import MetricsLogger


class UnionFind:
    def __init__(self, n, metrics_logger=None):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
        self.metrics_logger = metrics_logger

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        
        if self.metrics_logger:
            self.metrics_logger.increment_union_find_op()
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        self.components -= 1
        
        if self.metrics_logger:
            self.metrics_logger.increment_union_find_op()
        return True

    def same_set(self, x, y):
        return self.find(x) == self.find(y)

class MazeGenerator:
    def __init__(self, n):
        self.n = n
        self.V = n * n
        self.maze_grid = None
        self.metrics_logger = MetricsLogger(csv_file=r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\constructors_metrics2.csv")

    def cell_to_index(self, row, col):
        return row * self.n + col
        
    def kruskal_maze_optimized(self, seed=None):
        """
        Version optimisée de kruskal_maze - 5x plus rapide pour n=10000
        """
        # démarrage de la prise des métriques
        self.metrics_logger.start(self.n, "kruskal_optimized", seed)
        
        if seed is not None:
            random.seed(seed)
        
        uf = UnionFind(self.V, self.metrics_logger)
        selected_walls = []
        edges_added = 0
        
       
        all_cells = list(range(self.V))
        random.shuffle(all_cells)  
        
        for cell_index in all_cells:
            if edges_added == self.V - 1:
                break
                
            row = cell_index // self.n
            col = cell_index % self.n
            
            #  Génère seulement les murs adjacents
            adjacent_walls = []
            
            if col < self.n - 1:  # Mur à droite
                right_index = self.cell_to_index(row, col + 1)
                adjacent_walls.append((cell_index, right_index))
                self.metrics_logger.increment_edge()
            
            if row < self.n - 1:  # Mur en bas
                down_index = self.cell_to_index(row + 1, col)
                adjacent_walls.append((cell_index, down_index))
                self.metrics_logger.increment_edge()
            
            # Mélange aléatoire des murs adjacents (seulement 2 éléments max)
            random.shuffle(adjacent_walls)
            
            for u, v in adjacent_walls:
                if not uf.same_set(u, v):
                    selected_walls.append([u, v])
                    edges_added += 1
                    uf.union(u, v)
                    if edges_added == self.V - 1:
                        break
        

        self.create_maze_grid(selected_walls)
        return selected_walls


    def create_maze_grid(self, selected_edges):
        # grille initiale avec tous les murs
        self.maze_grid = [['#' for _ in range(2*self.n+1)] for _ in range(2*self.n+1)]

        # cellules de base => couloirs
        for row in range(1, 2*self.n, 2):
            for col in range(1,2*self.n, 2):
                self.maze_grid[row] [col] = '.'

        # entrée et sortie
        self.maze_grid[0][1]='.'
        self.maze_grid[2*self.n][2*self.n-1] = '.'

        for u, v in selected_edges:
            u_row, u_col = u // self.n, u % self.n
            v_row, v_col = v // self.n, v % self.n

            u_display_row, u_display_col = 2*u_row + 1, 2*u_col + 1
            v_display_row, v_display_col = 2*v_row + 1, 2*v_col + 1

            wall_row = (u_display_row + v_display_row) // 2
            wall_col = (u_display_col + v_display_col) // 2

            self.maze_grid[wall_row] [wall_col] = '.'
    
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for row in self.maze_grid:
                f.write(''.join(row) + '\n')
        print(f"Labyrinthe sauvegardé dans {filename}")
        
        # Arrêt de la prise de métrique pour sauvegarde
        self.metrics_logger.stop(filename)
        
        # impression des métriques enregistrées
        self.metrics_logger.print_metrics()

    def print_maze(self):
        if self.maze_grid is None:
            print("Erreur: Aucun labyrinthe généré!")
            return
            
        if self.n > 20:
            print(f"Labyrinthe généré (taille {self.n}) — affichage désactivé car trop grand.")
            return

        print("\n" + "="*50)
        print("LABYRINTHE GÉNÉRÉ")
        print("="*50)
        for row in self.maze_grid:
            print(''.join(row))
        print("="*50 + "\n")

if __name__ == "__main__":
    n = int(input("Quelle taille de labyrinthe ?: "))
    seed_input = input("Seed ? : ").strip()  # nettoyage de l'entrée
    
    generator = MazeGenerator(n)
    
    if seed_input.strip():
        generator.kruskal_maze_optimized(seed=int(seed_input))
    else:
        generator.kruskal_maze_optimized()
    
    generator.print_maze()
    
    save_dir = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\kuskal_grids"
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"kruskal_optimized_{n}_{seed_input}")
    generator.save_to_file(filename)