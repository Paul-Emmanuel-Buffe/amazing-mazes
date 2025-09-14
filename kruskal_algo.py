import random
import os

class UnionFind:
    # structure pour gérer les ensembles disjoints
    # utile pour vérifier si deux cellules sont déjà reliées
    def __init__(self, n):
        # chaque élément commence dans son propre ensemble
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        # trouve le représentant de l ensemble de x avec compression de chemin
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # fusionne les ensembles de x et y
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # on attache l arbre le moins profond sous l autre
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
        # retourne vrai si x et y appartiennent déjà au même ensemble
        return self.find(x) == self.find(y)

    def get_components(self):
        # retourne le nombre de composantes encore séparées
        return self.components


class MazeGenerator:
    def __init__(self, n):
        # prépare un graphe carré de n par n cellules
        self.n = n
        self.V = n * n
        self.maze_grid = None

    def cell_to_index(self, row, col):
        # convertit une cellule ligne colonne en index unique
        return row * self.n + col
        
    def generate_all_walls(self):
        # génère la liste de tous les murs possibles du labyrinthe
        walls = []
        for row in range(self.n):
            for col in range(self.n):
                cell_index = self.cell_to_index(row, col)
                if col < self.n - 1:
                    right_index = self.cell_to_index(row, col + 1)
                    walls.append([cell_index, right_index])
                if row < self.n - 1:
                    down_index = self.cell_to_index(row + 1, col)
                    walls.append([cell_index, down_index])
        return walls

    def create_maze_grid(self, selected_edges):
        # construit la grille ascii du labyrinthe à partir des arêtes retenues
        self.maze_grid = [['#' for _ in range(2*self.n+1)] for _ in range(2*self.n+1)]
        
        # on place les cellules accessibles
        for row in range(1, 2*self.n, 2):
            for col in range(1, 2*self.n, 2):
                self.maze_grid[row][col] = '.'
        
        # entrée en haut et sortie en bas
        self.maze_grid[0][1] = '.'
        self.maze_grid[2*self.n][2*self.n-1] = '.'
        
        # suppression des murs entre cellules connectées
        for u, v in selected_edges:
            u_row, u_col = u // self.n, u % self.n
            v_row, v_col = v // self.n, v % self.n
            u_display_row, u_display_col = 2*u_row + 1, 2*u_col + 1
            v_display_row, v_display_col = 2*v_row + 1, 2*v_col + 1
            wall_row = (u_display_row + v_display_row) // 2
            wall_col = (u_display_col + v_display_col) // 2
            self.maze_grid[wall_row][wall_col] = '.'
    
    def kruskal_maze(self, seed=None):
        # applique l algorithme de kruskal pour générer un arbre couvrant
        walls = self.generate_all_walls()
        
        # mélange aléatoire des murs
        if seed is not None:
            random.seed(seed)
        random.shuffle(walls)
        
        uf = UnionFind(self.V)
        selected_walls = []
        edges_added = 0
        
        # on parcourt les murs et on ne garde que ceux qui relient deux ensembles séparés
        for u, v in walls:
            if not uf.same_set(u, v):
                selected_walls.append([u, v])
                edges_added += 1
                uf.union(u, v)
                if edges_added == self.V - 1:
                    break
        
        self.create_maze_grid(selected_walls)
        return selected_walls
    
    def save_to_file(self, filename):
        # écrit la grille ascii du labyrinthe dans un fichier texte
        if self.maze_grid is None:
            print("erreur aucun labyrinthe généré")
            return
        with open(filename, 'w') as f:
            for row in self.maze_grid:
                f.write(''.join(row) + '\n')
        print(f"labyrinthe sauvegardé dans {filename}")
    
    def print_maze(self):
        # affiche le labyrinthe seulement si la taille est raisonnable
        if self.maze_grid is None:
            print("erreur aucun labyrinthe généré")
            return
        if self.n > 20:
            print(f"labyrinthe généré taille {self.n} affichage désactivé")
            return
        print("\n" + "="*50)
        print("labyrinthe généré")
        print("="*50)
        for row in self.maze_grid:
            print(''.join(row))
        print("="*50 + "\n")


if __name__ == "__main__":
    # récupération des paramètres utilisateur
    n = int(input("quelle taille de labyrinthe : "))
    seed = input("seed optionnel appuyez entrée pour aléatoire : ")
    
    generator = MazeGenerator(n)
    
    # génération avec ou sans graine
    if seed.strip():
        generator.kruskal_maze(seed=int(seed))
    else:
        generator.kruskal_maze()
    
    # affichage console
    generator.print_maze()
    
    # sauvegarde automatique dans le dossier défini
    save_dir = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\kuskal_grids"
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f"kruskal_grid_{n}.txt")
    generator.save_to_file(filename)
