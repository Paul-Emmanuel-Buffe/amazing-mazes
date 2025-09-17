import os
import random
from metrics_record import MetricsLogger

class MazeGeneratorRecursive:
    def __init__(self, n, seed=None):
        self.n = n
        self.size = 2 * n + 1
        self.grid = [["#" for _ in range(self.size)] for _ in range(self.size)]
        self.visited = set()
        self.seed = seed
        
        if seed is not None:
            random.seed(seed)
        
        # Répertoire de sauvegarde
        self.save_dir = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\recursive_grids"
        os.makedirs(self.save_dir, exist_ok=True)
        
        # Chemin absolu pour le fichier CSV
        csv_path = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\constructors_metrics.csv"
        self.logger = MetricsLogger(csv_file=csv_path)

    def _get_neighbors(self, x, y):
        """Retourne les voisins accessibles non visités"""
        moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        neighbors = []
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.size - 1 and 0 < ny < self.size - 1 and (nx, ny) not in self.visited:
                neighbors.append((nx, ny))
                
        return neighbors

    def _recursive_backtracking(self, x, y):
        """Algorithme récursif de génération du labyrinthe"""
        # Marquer la cellule comme visitée
        self.visited.add((x, y))
        self.grid[y][x] = "."
        
        # Obtenir les voisins dans un ordre aléatoire
        neighbors = self._get_neighbors(x, y)
        random.shuffle(neighbors)
        
        for nx, ny in neighbors:
            if (nx, ny) not in self.visited:
                # Casser le mur entre les deux cellules
                wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
                self.grid[wall_y][wall_x] = "."
                self.logger.increment_edge()  # Compter l'arête traitée
                
                # Explorer récursivement
                self._recursive_backtracking(nx, ny)
                
                # Compter le backtracking si nécessaire
                if any(n not in self.visited for n in self._get_neighbors(x, y)):
                    self.logger.increment_backtrack()

    def generate(self):
        """Lance la génération du labyrinthe"""
        self.logger.start(maze_size=self.n, algorithm="recursive_backtracking", seed=self.seed)
        self._recursive_backtracking(1, 1)
        
        # Ajouter l'entrée et la sortie
        self.grid[0][1] = "."
        self.grid[self.size - 1][self.size - 2] = "."

    def save_to_file(self, seed_input="default"):
        """Sauvegarde le labyrinthe et enregistre les métriques"""
        # Créer le nom de fichier avec le chemin complet
        filename = os.path.join(self.save_dir, f"recursive_maze_{self.n}_{seed_input}")
        
        # Écrire le labyrinthe dans le fichier
        with open(filename, "w") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")
        
        # Arrêter le chrono et enregistrer les métriques
        # (c'est ici que les données sont écrites dans le CSV)
        self.logger.stop(filename)
        print(f"Labyrinthe sauvegardé dans : {filename}")
        
        # Afficher le résumé des métriques
        self.logger.print_metrics()

    def print_maze(self):
        """Affiche le labyrinthe dans la console (si petite taille)"""
        if self.size <= 50:
            for row in self.grid:
                print("".join(row))
        else:
            print(f"Labyrinthe trop grand pour l'affichage ({self.size}x{self.size})")

# Programme principal
if __name__ == "__main__":
    # Demander les paramètres à l'utilisateur
    n = int(input("Taille du labyrinthe ?: "))
    seed_input = input("Seed (laisser vide pour aléatoire) ?: ").strip()
    
    # Créer le générateur
    if seed_input:
        generator = MazeGeneratorRecursive(n, seed=int(seed_input))
    else:
        generator = MazeGeneratorRecursive(n)
    
    # Générer le labyrinthe
    print("Génération en cours...")
    generator.generate()
    
    # Afficher le labyrinthe
    generator.print_maze()
    
    # Sauvegarder et afficher les métriques
    generator.save_to_file(seed_input if seed_input else "default")