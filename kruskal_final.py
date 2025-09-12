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
        self.V = n * n
        self.maze_grid = None

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

    def kruskal_maze(self):
        """
        Applique l'algorithme de Kruskal pour trouver l'Arbre Couvrant Minimal
        
        Returns:
            Liste des arêtes de l'ACM et le poids total
        """
        walls = self.generate_all_walls()
        random.shuffle(walls)
        
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
if __name__ == "__nain__" :   
    def main():
        n = int(input("Quelle taille de labyrinthe : "))
        filename = input("Nom du fichier : ")

        generator = MazeGenerator(n)
        generator.kruskal_maze()
        generator.save_to_file(filename)


