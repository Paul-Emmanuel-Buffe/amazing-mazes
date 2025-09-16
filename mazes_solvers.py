import heapq

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

    # 🔹 DFS (backtracking récursif)
    def solve_dfs(self):
        visited = set()
        chemin = []
        found = False

        def backtrack(x, y):
            nonlocal found
            if found:
                return
            visited.add((x, y))
            chemin.append((x, y))

            if (x, y) == self.sortie:
                found = True
                return

            for nx, ny in self._voisins(x, y):
                if (nx, ny) not in visited:
                    backtrack(nx, ny)
                    if found:
                        return

            chemin.pop()

        backtrack(*self.depart)
        if not found:
            return None, None
        return self._mark_solution(chemin, visited), chemin

    # 🔹 A* (plus court chemin)
    def solve_astar(self):
        def heuristique(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])  # Manhattan

        open_set = []
        heapq.heappush(open_set, (0, self.depart))
        came_from = {}
        g_score = {self.depart: 0}
        f_score = {self.depart: heuristique(self.depart, self.sortie)}
        explored = set()

        # ✅ Correction : initialiser avec le vrai f_score
        heapq.heappush(open_set, (f_score[self.depart], self.depart))

        while open_set:
            _, current = heapq.heappop(open_set)
            explored.add(current)

            if current == self.sortie:
                # Reconstruction du chemin
                chemin = []
                while current in came_from:
                    chemin.append(current)
                    current = came_from[current]
                chemin.append(self.depart)
                chemin = chemin[::-1]
                return self._mark_solution(chemin, explored), chemin

            for voisin in self._voisins(*current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(voisin, float('inf')):
                    came_from[voisin] = current
                    g_score[voisin] = tentative_g
                    f_score[voisin] = tentative_g + heuristique(voisin, self.sortie)
                    heapq.heappush(open_set, (f_score[voisin], voisin))

        return None, None


#  Exemple d’utilisation
if __name__ == "__main__":
    # Lecture d’un labyrinthe depuis un fichier
    input_file = input("Nom du fichier contenant le labyrinthe : ")
    with open(input_file, "r") as f:
        labyrinthe = [line.strip() for line in f.readlines()]
        n = (len(labyrinthe) - 1) // 2   # retrouver n
        depart = (0, 1)
        sortie = (2*n, 2*n - 1)
        

    solver = Solver(labyrinthe , depart, sortie)

    choix = input("Choisir un solveur (dfs / astar) : ").strip().lower()
    if choix == "dfs":
        solution, chemin = solver.solve_dfs()
        output_file = "solution_dfs.txt"
    else:
        solution, chemin = solver.solve_astar()
        output_file = "solution_astar.txt"

    # Correction : écrire la grille ASCII solution, pas la liste de coordonnées
    if solution:
        with open(output_file, "w") as f:
            for ligne in solution:
                f.write(ligne + "\n")
        print(f" Solution écrite dans {output_file}")
    else:
        print(" Aucun chemin trouvé !")
