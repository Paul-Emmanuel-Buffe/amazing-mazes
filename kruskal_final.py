import random
import os

class UnionFind:
    """
    Structure de données Union-Find (Disjoints Sets)
    
    Cette structure nous permet de :
    1. Grouper les sommets en composantes connexes
    2. Vérifier rapidement si deux sommets sont dans la même composante
    3. Fusionner deux composantes efficacement
    """

    def __init__(self, n):
        """
        Initialise n éléments, chacun dans son propre ensemble
        
        Args:
            n: nombre d'éléments (sommets)
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        """
        Trouve le représentant (racine) de l'ensemble contenant x
        
        Utilise la compression de chemin pour optimiser les recherches futures.
        
        Args:
            x: élément dont on cherche le représentant
            
        Returns:
            Le représentant de l'ensemble contenant x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        Unit les ensembles contenant x et y
        
        Utilise l'union par rang pour maintenir les arbres équilibrés.
        
        Args:
            x, y: éléments dont on veut unir les ensembles
            
        Returns:
            True si les ensembles ont été unis, False s'ils étaient déjà dans le même ensemble
        """
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
        return True

    def same_set(self, x, y):
        return self.find(x) == self.find(y)

    def get_components(self):
        return self.components


class MazeGenerator:
    def __init__(self, n):
        """
        Initialise un graphe avec le nombre spécifié de sommets
        
        Args:
            vertices: nombre de sommets dans le graphe
        """
        self.n = n  # taille => n couloirs
        self.V = n * n # Total des cellules à connecter
        self.maze_grid = None # Grille (à compléter)

    def cell_to_index(self, row, col):
        """
        Convertit les coordonnées d'une cellule (row, col) en index unique
        
        Pour une grille de n×n cellules, chaque cellule a des coordonnées:
        - row: de 0 à n-1
        - col: de 0 à n-1
        
        Args:
            row: ligne de la cellule (0 à n-1)
            col: colonne de la cellule (0 à n-1)
            
        Returns:
            Index unique de 0 à n²-1
        """
        return row * self.n + col
    def generate_all_walls(self):

        walls = [] # liste de toutes les connexion possibles
        for row in range(self.n):
            for col in range(self.n):
                cell_index = self.cell_to_index(row, col)

                # pour les connexions à droite
                if col < self.n - 1:
                    right_index = self.cell_to_index(row, col + 1)
                    walls.append([cell_index, right_index])

                # pour les connexions bas
                if row < self.n - 1:
                    down_index = self.cell_to_index(row + 1, col)
                    walls.append([cell_index, down_index])

        return walls


    def create_maze_grid(self, selected_edges):
        # grille initiale avec tous les murs
        self.maze_grid = [['#' for _ in range(2*self.n+1)] for _ in range(2*self.n+1)]

        # cellules de base => couloirs
        for row in range(1, 2*self.n, 2):
            for col in range(1,2*self.n, 2):
                self.maze_grid[row] [col] = '.'

        # céation de de l'entrée et de la sortie
        self.maze_grid[0][1]='.'
        self.maze_grid[2*self.n][2*self.n-1] = '.'

        for u, v in selected_edges:
            
            # conversion des index u, v en coordonnées cellules
            u_row, u_col = u // self.n, u % self.n
            v_row, v_col = v // self.n, v % self.n

            # Calculer la position du mur à supprimer dans la grille d'affichage
            # Position des cellules dans la grille d'affichage

            u_display_row, u_display_col = 2*u_row + 1, 2*u_col + 1
            v_display_row, v_display_col = 2*v_row + 1, 2*v_col + 1

            # position du mur entre 2 cellules
            wall_row = (u_display_row + v_display_row) // 2
            wall_col = (u_display_col + v_display_col) // 2

            # suppression du mur
            self.maze_grid[wall_row] [wall_col] = '.'
    
    def kruskal_maze(self, seed=None):
        """
        Applique l'algorithme de Kruskal pour trouver l'Arbre Couvrant Minimal
        
        Returns:
            Liste des arêtes de l'ACM et le poids total
        """
        walls = self.generate_all_walls()

        if seed is not None: # avec seed
            random.seed(seed)

        random.shuffle(walls) # sans seed
        
        uf = UnionFind(self.V)

        selected_walls = []
        edges_added = 0

        for u, v  in walls:
            if not uf.same_set(u, v):
                selected_walls.append([u, v])
                edges_added += 1
                uf.union(u, v)

                if edges_added == self.V - 1:
                    break
        # créer la grille d'affichage avec les murs selectionnés
        self.create_maze_grid(selected_walls)

        return selected_walls
    
    def save_to_file(self, filename):
        # sauvegarde des grilles

        with open(filename, 'w') as f:
            for row in self.maze_grid:
                    f.write(''.join(row) + '\n')

        print(f"Labyrinthe sauvegardé dans {filename}")

    def print_maze(self):
    
        if self.maze_grid is None:
            print("Erreur: Aucun labyrinthe généré!")
            return
            
        print("\n" + "="*50)
        print("LABYRINTHE GÉNÉRÉ")
        print("="*50)
        for row in self.maze_grid:
            print(''.join(row))
        print("="*50 + "\n")


import random

class UnionFind:
    """
    Structure de données Union-Find (Disjoints Sets)
    
    Cette structure nous permet de :
    1. Grouper les sommets en composantes connexes
    2. Vérifier rapidement si deux sommets sont dans la même composante
    3. Fusionner deux composantes efficacement
    """

    def __init__(self, n):
        """
        Initialise n éléments, chacun dans son propre ensemble
        
        Args:
            n: nombre d'éléments (sommets)
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        """
        Trouve le représentant (racine) de l'ensemble contenant x
        
        Utilise la compression de chemin pour optimiser les recherches futures.
        
        Args:
            x: élément dont on cherche le représentant
            
        Returns:
            Le représentant de l'ensemble contenant x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        Unit les ensembles contenant x et y
        
        Utilise l'union par rang pour maintenir les arbres équilibrés.
        
        Args:
            x, y: éléments dont on veut unir les ensembles
            
        Returns:
            True si les ensembles ont été unis, False s'ils étaient déjà dans le même ensemble
        """
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
        return True

    def same_set(self, x, y):
        return self.find(x) == self.find(y)

    def get_components(self):
        return self.components


class MazeGenerator:
    def __init__(self, n):
        """
        Initialise un graphe avec le nombre spécifié de sommets
        
        Args:
            vertices: nombre de sommets dans le graphe
        """
        self.n = n  # taille => n couloirs
        self.V = n * n # Total des cellules à connecter
        self.maze_grid = None # Grille (à compléter)

    def cell_to_index(self, row, col):
        """
        Convertit les coordonnées d'une cellule (row, col) en index unique
        
        Pour une grille de n×n cellules, chaque cellule a des coordonnées:
        - row: de 0 à n-1
        - col: de 0 à n-1
        
        Args:
            row: ligne de la cellule (0 à n-1)
            col: colonne de la cellule (0 à n-1)
            
        Returns:
            Index unique de 0 à n²-1
        """
        return row * self.n + col
        
    def generate_all_walls(self):
        walls = [] # liste de toutes les connexion possibles
        for row in range(self.n):
            for col in range(self.n):
                cell_index = self.cell_to_index(row, col)

                # pour les connexions à droite
                if col < self.n - 1:
                    right_index = self.cell_to_index(row, col + 1)
                    walls.append([cell_index, right_index])

                # pour les connexions bas
                if row < self.n - 1:
                    down_index = self.cell_to_index(row + 1, col)
                    walls.append([cell_index, down_index])

        return walls

    def create_maze_grid(self, selected_edges):
        # grille initiale avec tous les murs
        self.maze_grid = [['#' for _ in range(2*self.n+1)] for _ in range(2*self.n+1)]

        # cellules de base => couloirs
        for row in range(1, 2*self.n, 2):
            for col in range(1,2*self.n, 2):
                self.maze_grid[row] [col] = '.'

        # céation de de l'entrée et de la sortie
        self.maze_grid[0][1]='.'
        self.maze_grid[2*self.n][2*self.n-1] = '.'

        for u, v in selected_edges:
            
            # conversion des index u, v en coordonnées cellules
            u_row, u_col = u // self.n, u % self.n
            v_row, v_col = v // self.n, v % self.n

            # Calculer la position du mur à supprimer dans la grille d'affichage
            # Position des cellules dans la grille d'affichage

            u_display_row, u_display_col = 2*u_row + 1, 2*u_col + 1
            v_display_row, v_display_col = 2*v_row + 1, 2*v_col + 1

            # position du mur entre 2 cellules
            wall_row = (u_display_row + v_display_row) // 2
            wall_col = (u_display_col + v_display_col) // 2

            # suppression du mur
            self.maze_grid[wall_row] [wall_col] = '.'
    
    def kruskal_maze(self, seed=None):
        """
        Applique l'algorithme de Kruskal pour trouver l'Arbre Couvrant Minimal
        
        Returns:
            Liste des arêtes de l'ACM et le poids total
        """
        walls = self.generate_all_walls()

        if seed is not None: # avec seed
            random.seed(seed)

        random.shuffle(walls) # sans seed
        
        uf = UnionFind(self.V)

        selected_walls = []
        edges_added = 0

        for u, v  in walls:
            if not uf.same_set(u, v):
                selected_walls.append([u, v])
                edges_added += 1
                uf.union(u, v)

                if edges_added == self.V - 1:
                    break
        # créer la grille d'affichage avec les murs selectionnés
        self.create_maze_grid(selected_walls)

        return selected_walls
    
    def save_to_file(self, filename):
        """
        Sauvegarde le labyrinthe dans un fichier
        """
        if self.maze_grid is None:
            print("Erreur: Aucun labyrinthe généré!")
            return
            
        with open(filename, 'w') as f:
            for row in self.maze_grid:
                f.write(''.join(row) + '\n')
        print(f"Labyrinthe sauvegardé dans {filename}")
    
    def print_maze(self):
        """
        Affiche le labyrinthe dans la console
        """
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
    n = int(input("Quelle taille de labyrinthe : "))
    seed = input("Seed (optionnel, appuyez sur Entrée pour aléatoire) : ")
    
    generator = MazeGenerator(n)
    
    if seed.strip():  # Si une seed est saisie
        generator.kruskal_maze(seed=int(seed))
    else:
        generator.kruskal_maze()
    
    # Affichage du labyrinthe dans la console
    generator.print_maze()
    
    # Génération automatique du nom du fichier
    save_dir = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\kuskal_grids"
    os.makedirs(save_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas
    
    filename = os.path.join(save_dir, f"kruskal_grid_{n}.txt")
    
    # Sauvegarde dans un fichier
    generator.save_to_file(filename)
