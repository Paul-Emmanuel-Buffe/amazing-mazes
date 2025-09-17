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
        self.metrics_logger = MetricsLogger(csv_file=r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\constructors_metrics.csv")

    def cell_to_index(self, row, col):
        return row * self.n + col

    def kruskal_maze_canonical(self, seed=None):
        """
        Version académique de Kruskal :
        - On génère toutes les arêtes
        - On les mélange
        - On applique Kruskal strict
        """
        # démarrage de la prise des métriques
        self.metrics_logger.start(self.n, "kruskal", seed)

        if seed is not None:
            random.seed(seed)

        uf = UnionFind(self.V, self.metrics_logger)
        selected_walls = []  
        edges_added = 0

        # 1) Génération de toutes les arêtes possibles (droite et bas seulement pour éviter doublons)
        edges = []
        for row in range(self.n):
            for col in range(self.n):
                u = self.cell_to_index(row, col)
                if col < self.n - 1:  # mur à droite
                    v = self.cell_to_index(row, col + 1)
                    edges.append((u, v))
                    self.metrics_logger.increment_edge()
                if row < self.n - 1:  # mur en bas
                    v = self.cell_to_index(row + 1, col)
                    edges.append((u, v))
                    self.metrics_logger.increment_edge()


        # 2) Mélange aléatoire de toutes les arêtes
        random.shuffle(edges)

        # 3) Algorithme de Kruskal classique
        for u, v in edges:
            if uf.union(u, v):  # ajoute si pas de cycle
                selected_walls.append([u, v])
                edges_added += 1
                if edges_added == self.V - 1:
                    break

        # 4) Construction de la grille
        self.create_maze_grid(selected_walls)
        return selected_walls

    def create_maze_grid(self, selected_edges):
        self.maze_grid = [['#' for _ in range(2*self.n+1)] for _ in range(2*self.n+1)]

        for row in range(1, 2*self.n, 2):
            for col in range(1, 2*self.n, 2):
                self.maze_grid[row][col] = '.'

        # entrée et sortie
        self.maze_grid[0][1] = '.'
        self.maze_grid[2*self.n][2*self.n-1] = '.'

        for u, v in selected_edges:
            u_row, u_col = u // self.n, u % self.n
            v_row, v_col = v // self.n, v % self.n

            u_display_row, u_display_col = 2*u_row + 1, 2*u_col + 1
            v_display_row, v_display_col = 2*v_row + 1, 2*v_col + 1

            wall_row = (u_display_row + v_display_row) // 2
            wall_col = (u_display_col + v_display_col) // 2

            self.maze_grid[wall_row][wall_col] = '.'

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for row in self.maze_grid:
                f.write(''.join(row) + '\n')
        print(f"Labyrinthe sauvegardé dans {filename}")

        # Arrêt de la prise de métrique pour sauvegarde
        self.metrics_logger.stop(filename)
        
        # impression des métriques enregistrée
        self.metrics_logger.print_metrics()

    def print_maze(self):
        if self.maze_grid is None:
            print("Erreur: Aucun labyrinthe généré!")
            return

        if self.n > 20:
            print(f"Labyrinthe généré (taille {self.n}) – affichage désactivé car trop grand.")
            return
        print("\n" + "="*50)
        print("LABYRINTHE GÉNÉRÉ")
        print("="*50)
        for row in self.maze_grid:
            print(''.join(row))
        print("="*50 + "\n")


if __name__ == "__main__":
    n = int(input("Quelle taille de labyrinthe ?: "))
    seed_input = input("Seed ? : ").strip() # nettoyage de l'entrée

    generator = MazeGenerator(n)

    if seed_input.strip():
        generator.kruskal_maze_canonical(seed=int(seed_input))
    else:
        generator.kruskal_maze_canonical()

    generator.print_maze()

    save_dir = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\kuskal_grids"
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"kruskal_strict_{n}_{seed_input}.txt")