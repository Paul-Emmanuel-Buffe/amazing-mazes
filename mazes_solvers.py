import heapq # pour la file de priorité(trie par tas ici min-heap permet de d'acceder rapidemment au noeud avec le cout f(n) minimal)
from PIL import Image
from solver_metric import SolverMetricsLogger
class Solver:
    def __init__(self, labyrinthe, depart, sortie):
        self.labyrinthe = [list(row) for row in labyrinthe]
        self.n = len(labyrinthe)
        self.m = len(labyrinthe[0])
        self.depart = depart
        self.sortie = sortie 

    def _voisins(self, x, y):
        """Retourne les voisins accessibles (cases vides)."""
        deplacements= [(0,1),(1,0),(-1,0),(0,-1)]
        for dx, dy in deplacements:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.n and 0 <= ny < self.m and self.labyrinthe[nx][ny] == '.':
                yield nx, ny    
    
    def _mark_solution(self, chemin, explored):
        """Retourne une version du labyrinthe avec o/*/S/E marqués."""
        lab_mod = [row[:] for row in self.labyrinthe]  
        for (x, y) in explored:
            if (x, y) not in chemin and lab_mod[x][y] == '.':
                lab_mod[x][y] = '*'
        for (x, y) in chemin:
            lab_mod[x][y] = 'o'
        lab_mod[self.depart[0]][self.depart[1]] = 'S'
        lab_mod[self.sortie[0]][self.sortie[1]] = 'E'
        return ["".join(row) for row in lab_mod]

    #  DFS (backtracking récursif)
    def solve_dfs(self):
        visited = set()
        chemin = []
        etat = {"sortie_trouvee": False}

        def backtrack(x, y):
            if etat["sortie_trouvee"]:
                return
            
            visited.add((x, y))
            chemin.append((x, y))

            if logger:
                logger.increment_nodes()  # chaque fois qu’on explore un nœud

            if (x, y) == self.sortie:
                etat["sortie_trouvee"] = True
                return

            for nx, ny in self._voisins(x, y):
                if (nx, ny) not in visited:
                    backtrack(nx, ny)
                    if etat["sortie_trouvee"]:
                        return

            chemin.pop()

        backtrack(*self.depart)
        if not etat["sortie_trouvee"]:
            return None, None
        return self._mark_solution(chemin, visited), chemin

    #  A* (plus court chemin)
    def solve_astar(self):
        def heuristique(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])  # Manhattan

        open_set = []
        heapq.heappush(open_set, (0, self.depart))
        parent = {}
        cout_g = {self.depart: 0} # cout reel du chemin depuis le départ
        cout_f = {self.depart: heuristique(self.depart, self.sortie)} # cout total estimé
        explored = set()

        # Initialisation
        heapq.heappush(open_set, (cout_f[self.depart], self.depart))

        while open_set:
            _, case_courante = heapq.heappop(open_set) # cout_f est ignoré mais represente le cout total estimé et est utilisé pour le tri(min-heap pour prioriser les noeuds)
            explored.add(case_courante)
             #  chaque fois qu’on explore un nœud
            if logger:
                logger.increment_nodes()

            if case_courante == self.sortie:
                # Reconstruction du chemin
                chemin = []
                while case_courante in parent:
                    chemin.append(case_courante)
                    case_courante = parent[case_courante]
                chemin.append(self.depart)
                chemin = chemin[::-1]
                if logger:
                    logger.set_path_length(len(chemin))

                return self._mark_solution(chemin, explored), chemin
                

            for voisin in self._voisins(*case_courante):
                tentative_g = cout_g[case_courante] + 1
                if tentative_g < cout_g.get(voisin, float('inf')):
                    parent[voisin] = case_courante
                    cout_g[voisin] = tentative_g
                    cout_f[voisin] = tentative_g + heuristique(voisin, self.sortie)
                    heapq.heappush(open_set, (cout_f[voisin], voisin))

        return None, None
    
    def to_image(self, labyrinthe_solution, pixel_size=20, output_file="solution.jpg"):
        n = len(labyrinthe_solution)
        m = len(labyrinthe_solution[0])
        img = Image.new("RGB", (m*pixel_size, n*pixel_size), "white")
        pixels = img.load()

        couleurs = {
            "#": (0, 0, 0),
            ".": (255, 255, 255),
            "o": (0, 255, 0),
            "*": (100, 100, 100),
            "S": (0, 0, 255),
            "E": (255, 0, 0)
        }

        for i, row in enumerate(labyrinthe_solution):
            for j, cell in enumerate(row):
                couleur = couleurs.get(cell, (255, 255, 255))
                for dx in range(pixel_size):
                    for dy in range(pixel_size):
                        pixels[j*pixel_size + dx, i*pixel_size + dy] = couleur

        img.save(output_file)
        print(f"Image enregistrée sous {output_file}")


#  Exemple d’utilisation
if __name__ == "__main__":
    input_file = input("Nom du fichier contenant le labyrinthe : ")
    with open(input_file, "r") as f:
        labyrinthe = [line.strip() for line in f.readlines()]
        n = (len(labyrinthe) - 1) // 2
        depart = (0, 1)
        sortie = (2*n, 2*n - 1)

    solver = Solver(labyrinthe, depart, sortie)
    logger = SolverMetricsLogger()

    choix = input("Choisir un solveur (dfs / astar) : ").strip().lower()
    logger.start(maze_name= input_file, maze_size=f"{solver.n}x{solver.m}", algorithm=choix)

    if choix == "dfs":
        solution, chemin = solver.solve_dfs()
    else:
        solution, chemin = solver.solve_astar()

    if solution:
        output_file = f"solution_{choix}_{input_file}"
        with open(output_file, "w") as f:
            for ligne in solution:
                f.write(ligne + "\n")
        solver.to_image(solution, output_file=output_file.replace(".txt", ".jpg"))

        # enregistrement métriques
        logger.increment_nodes()  # à adapter -> tu peux incrémenter dans tes solveurs
        if chemin:
            logger.set_path_length(len(chemin))
        logger.stop(output_file)
        logger.print_metrics()

        print(f" Solution écrite dans {output_file}")
    else:
        print(" Aucun chemin trouvé !")
